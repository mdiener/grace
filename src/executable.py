#! /usr/bin/env python

from sys import exit
import argparse
from new import New
from build import Build
from error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError


def build_project(b, restrict):
    try:
        b.build_project(restrict)
    except FileNotFoundError as e:
        print e.msg
        exit()
    except FileNotWritableError as e:
        print e.msg
        exit()
    except CreateFolderError as e:
        print e.msg
        exit()
    except FolderNotFoundError as e:
        print e.msg
        exit()
    except WrongFormatError as e:
        print e.msg
        exit()
    except RemoveFolderError as e:
        print e.msg
        exit()
    except RemoveFileError as e:
        print e.msg
        exit()

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
    try:
        b = Build()
    except MissingKeyError as e:
        print e.msg
        exit()
    except FileNotFoundError as e:
        print e.msg
        exit()
    except WrongFormatError as e:
        print e.msg
        exit()

    try:
        task = args.args[1]
    except:
        build_project(b, None)

    if task == 'project':
        try:
            subtask = args.args[2]
        except:
            build_project(b, None)
            exit()

        build_project(b, subtask)
    elif task == 'clean':
        try:
            b.clean()
        except RemoveFolderError as e:
            print e.msg
            exit()
    else:
        print help
else:
    print help
