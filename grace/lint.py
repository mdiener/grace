class Lint(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

        self._node_script = r"""
var jslint = require("%s").jslint;
var print = require("sys").print;
var readFileSync = require("fs").readFileSync;
var warnings = null,;
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
            'jslint': '~/.jslint/jslint.js',
            'jsoptions': 'maxerr: 100',
            'force': False,
            'node': 'node'
        }

        if os.path.exists()

    def run(self):
        if not os.path.exists(os.join(self._cwd, 'src')):
            raise FolderNotFoundError('Could not find the source folder for the project.')

        application = os.path.join(self._cwd, 'src', 'application.js')

        self._lint_file(application)

    def _lint_file(self, application):
        lint = self._get_lint()
        command = [self._options.node]

    def _get_lint(self):
        jslint = os.path.join(os.expanduser(), '.jslint', 'jslint')
        response = urlopen('https://raw.github.com/douglascrockford/JSLint/master/jslint.js')

        if not os.path.exists(os.path.dirname(jslint)):
            os.makedirs(os.path.dirname(jslitn))

        with open(jslint, 'w') as f:
            f.write(response.read())
            f.write('\n\nexports.jslint = jslint')
        response.close()

        lint = NamedTemporaryFile('w+')
        lint.write(self._node_script % (jslint[:-3], self._options['jsoptions']))
        lint.write.flush()
        return lint

















#!/usr/bin/env python

import sys
import os

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


args = sys.argv
exists.py



















#!/usr/bin/env python

# Copyright (C) 2011  Alejandro Blanco <ablanco@yaco.es>

"""
wrapper for JSLint
"""
import os
import sys
import subprocess

from optparse import OptionParser
from tempfile import NamedTemporaryFile

try:
    from urllib2 import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3

default_jslint_options = r"""
maxerr: 100
"""
node_script = r"""
var jslint = require("%s").jslint,
    print = require("sys").print,
    readFileSync = require("fs").readFileSync,
    error = null, i = 0, j = 0, src = null;

print("Analyzing file " + process.argv[2] + "\n");
src = readFileSync(process.argv[2], "utf8");
lint = jslint(src, {%s});

for (j = 0; j < lint.warnings.length; j++ ) {
    error = lint.warnings[j];
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
usage = "Usage: %prog [options] jsfile"
parser = OptionParser(usage)
parser.add_option('-u', '--upgrade', dest='force', help='Upgrade JSLint',
                  action='store_true', default=False)
parser.add_option('-j', '--jslint', dest='jslint', help='JSLint location',
                  default=os.path.join('~', '.jslint', 'jslint.js'))
parser.add_option('-o', '--options', dest='jsoptions',
                  help='JSLint options', default=default_jslint_options)
parser.add_option('-n', '--node', dest='node',
                  help='Node location', default='node')


def execute_command(proc):
    p = subprocess.Popen(proc, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out, p.returncode


def get_lint(options):
    jslint = os.path.expanduser(options.jslint)

    if not os.path.exists(jslint) or options.force:
        # download jslint from github
        response = urlopen('https://raw.github.com/douglascrockford/'
                           'JSLint/master/jslint.js')
        if not os.path.exists(os.path.dirname(jslint)):
            os.makedirs(os.path.dirname(jslint))
        f = open(jslint, 'w')
        f.write(response.read())
        response.close()
        f.write('\n\nexports.jslint = jslint')  # add node support
        f.close()

    # write node script
    lint = NamedTemporaryFile("w+")
    lint.write(node_script % (jslint[:-3], options.jsoptions))
    lint.file.flush()
    return lint


def process(jsfile, options):
    print(options)
    lint = get_lint(options)
    command = [options.node, lint.name, jsfile.name]
    output, valid = execute_command(command)
    jsfile.close()
    lint.close()
    output = output.decode("utf-8")
    return [line for line in output.split("\n") if line], valid == 0


# Hooks entry point
def check_JSLint(code_string):
    tmpfile = NamedTemporaryFile("w+")
    tmpfile.write(code_string)
    tmpfile.file.flush()
    output, valid = process(tmpfile, parser.get_default_values())
    if valid:
        return []
    else:
        return output
