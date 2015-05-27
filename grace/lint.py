import os
import sys
import subprocess
from error import NoExectuableError, FolderNotFoundError
from tempfile import NamedTemporaryFile

try:
    from urllib2 import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3

class Lint(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

        self._node_script = r"""
var jslint = require("%s").jslint;
var print = require("sys").print;
var readFileSync = require("fs").readFileSync;
var warnings = null;
var i = 0;
var lint = null;
var src = null;

print("Analyzing file " + process.argv[2] + "\n");
src = readFileSync(process.argv[2], "utf8");
lint = jslint(src, {%s});

for (i = 0; i < lint.warnings.length; i++ ) {
    error = lint.warnings[i];
    if (error !== null) {
        print(' \n')
        print('Lint Warning at ' + error.line + ':' + error.column + ': ' + error.message + '\n');
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
        self._options = {
            'jslint': os.path.join(os.path.expanduser('~'), '.jslint', 'jslint.js'),
            'jsoptions': 'maxerr: 100',
            'force': False,
            'node': 'node'
        }

        if self._check_executable('node'):
            self._options['node'] = 'node'
        elif self._check_executable('nodejs'):
            self._options['node'] = 'nodejs'
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

        application = os.path.join(self._cwd, 'src', 'application.js')

        errors = self._lint_file(application)
        print errors

    def _lint_file(self, jsfile):
        lint = self._get_lint()
        command = [self._options['node'], lint.name, jsfile]

        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = p.communicate()

        lint.close()

        return out

    def _get_lint(self):
        jslint = os.path.join(os.path.expanduser('~'), '.jslint', 'jslint')
        response = urlopen('https://raw.github.com/douglascrockford/JSLint/master/jslint.js')

        if not os.path.exists(os.path.dirname(jslint)):
            os.makedirs(os.path.dirname(jslint))

        with open(jslint, 'w') as f:
            f.write(response.read())
            f.write('\n\nexports.jslint = jslint')
        response.close()

        lint = NamedTemporaryFile('w+')
        lint.write(self._node_script % (jslint[:-3], self._options['jsoptions']))
        lint.file.flush()
        return lint
