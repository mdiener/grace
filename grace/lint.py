import os
import sys
import subprocess
from error import NoExectuableError, FolderNotFoundError
from tempfile import NamedTemporaryFile
import json

try:
    from urllib2 import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3

class Lint(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config
        self.lint_valid = False

        self._jshint_node_script = r"""
var jshint = require("%s").JSHINT;
var print = require("sys").print;
var readFileSync = require("fs").readFileSync;
var warnings = null;
var i = 0;
var lint = null;
var src = null;
var data = null;
var options = null;

print("Analyzing file " + process.argv[2] + "\n");
src = readFileSync(process.argv[2], "utf8");
options = '%s';
options = JSON.parse(options);

jshint(src, options, ['dizmo', 'viewer', 'bundle']);

data = jshint.data();

if (data.errors && data.errors.length > 0) {
    print('\nErrors\n------\n')
    for (index in data.errors) {
        error = data.errors[index];
        print('Error ' + error.code + ' on line ' + error.line + ' character ' + error.character + ': ' + error.reason + '\n');
        print('\t' + error.evidence.trim() + '\n');
    };

    print('\n' + data.errors.length + ' Error(s) found.\n');
    print(' \n');
} else {
    print('No errors found.\n');
    print(' \n');
}

/*
if (data.unused && data.unused.length > 0) {
    print('Unused\n------\n')
    for (index in data.unused) {
        unused = data.unused[index]
        print('Unused \'' + unused.name + '\' on line ' + unused.line + ' character ' + unused.character + '\n');
    };
} else {
    print('No unused found.')
}
*/

if (data.errors) {
    process.exit(1);
} else {
    process.exit(0);
}
"""

        self._jslint_node_script = r"""
var jslint = require("%s").jslint;
var print = require("sys").print;
var readFileSync = require("fs").readFileSync;
var warnings = null;
var i = 0;
var lint = null;
var src = null;
var options = null;

print("Analyzing file " + process.argv[2] + "\n");
src = readFileSync(process.argv[2], "utf8");
options = '%s';
options = JSON.parse(options);

lint = jslint(src, options, ['dizmo', 'viewer', 'bundle', 'window']);

for (i = 0; i < lint.warnings.length; i++ ) {
    error = lint.warnings[i];
    if (error !== null) {
        print(' \n')
        print('Lint Warning at line ' + error.line + ' column ' + error.column + ': ' + error.message + '\n');
        print('\t' + lint.lines[error.line].trim() + '\n');
    }
}

if (lint.warnings.length > 0) {
    print("\n" + lint.warnings.length + " Error(s) found.\n");
    process.exit(1);
} else {
    print("\nNo warnings found.\n");
    process.exit(0);
}
"""

        if self._config['linter'] == 'jslint':
            self._options = {
                'jslint': os.path.join(os.path.expanduser('~'), '.grace-lint', 'jslint.js'),
                'jsoptions': {
                    'maxerr': 100,
                    'browser': True,
                    'fudge': True,
                    'for': True
                },
                'node': 'node'
            }
        else:
            self._options = {
                'jshint': os.path.join(os.path.expanduser('~'), '.grace-lint', 'jshint.js'),
                'jsoptions': {
                    'maxerr': 100,
                    'browser': True
                },
                'node': 'node'
            }

        tmp = self._options['jsoptions'].copy()
        tmp.update(self._config['lintoptions'])

        self._options['jsoptions'] = json.dumps(tmp)

        if self._check_executable('nodejs'):
            self._options['node'] = 'nodejs'
        elif self._check_executable('node'):
            self._options['node'] = 'node'
        else:
            raise NoExectuableError('Could not find a node js executable on the system.')

    def _check_executable(self, program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return True
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return True

        return False

    def run(self):
        if not os.path.exists(os.path.join(self._cwd, 'src')):
            raise FolderNotFoundError('Could not find the source folder for the project.')

        application = os.path.join('src', 'application.js')

        self.lint_valid = True

        valid = self._lint_file(application)
        if not valid:
            self.lint_valid = False

        if os.path.exists(os.path.join(self._cwd, 'src', 'javascript')):
            for dirname, subdirs, files in os.walk(os.path.join('src', 'javascript')):
                for filename in files:
                    valid = self._lint_file(os.path.join(dirname, filename))
                    if not valid:
                        self.lint_valid = False

    def _lint_file(self, jsfile):
        if 'jslint' in self._options:
            lint = self._get_jslint()
        else:
            lint = self._get_jshint()

        command = [self._options['node'], lint.name, jsfile]
        err = subprocess.call(command)

        lint.close()

        if err == 0:
            return True
        else:
            return False

    def _get_jshint(self):
        jshint_path = self._options['jshint']
        response = urlopen('https://raw.githubusercontent.com/jshint/jshint/master/dist/jshint.js')

        if not os.path.exists(os.path.dirname(jshint_path)):
            os.makedirs(os.path.dirname(jshint_path))

        with open(jshint_path, 'w') as f:
            f.write(response.read())
            response.close()

        jshint = NamedTemporaryFile('w+')
        jshint.write(self._jshint_node_script % (jshint_path, self._options['jsoptions']))
        jshint.file.flush()
        return jshint

    def _get_jslint(self):
        jslint_path = self._options['jslint']
        response = urlopen('https://raw.github.com/douglascrockford/JSLint/master/jslint.js')

        if not os.path.exists(os.path.dirname(jslint_path)):
            os.makedirs(os.path.dirname(jslint_path))

        with open(jslint_path, 'w') as f:
            f.write(response.read())
            response.close()
            f.write('\n\nexports.jslint = jslint')

        jslint = NamedTemporaryFile('w+')
        jslint.write(self._jslint_node_script % (jslint_path, self._options['jsoptions']))
        jslint.file.flush()
        return jslint
