#! /usr/bin/env python

from sys import exit
import argparse
from new import New
from build import Build

parser = argparse.ArgumentParser(description='Tasks to execute')
parser.add_argument('args', action='store', nargs='*')

args = parser.parse_args()

if len(args.args) < 1:
    argument = ''
else:
    argument = str(args.args)

help = '\
`' + argument + '` is not a valid argument.\n\
--------------------------\n\n\
Valid arguments:\n\
help\t\t\tDisplay this help.\n\
new\t[name]\t\tCreate a new project with project name. Default is `MyProject`.\n\
build\tproject, test\tBuild the project or the tests. Ommit both and build both.'

if len(args.args) < 1:
    print help
    exit()

if args.args[0] == 'new':
    try:
        name = args.args[1]
    except:
        name = 'MyProject'
    New(name)
elif args.args[0] == 'build':
    b = Build()
    try:
        task = args.args[1]
    except:
        b.build_project()
        b.build_test()
        exit()

    if task == 'project':
        b.build_project()
    elif task == 'test':
        b.build_test()
    else:
        print help
else:
    print help
