#! /usr/bin/env python

from sys import exit
import argparse
from new import New
from build import Build, clean
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

help = ''
helpargs = ' '.join(args.args)
if helpargs != 'help':
    help = '`' + helpargs + '` is not a valid command.\n\n'

help = help + 'Syntax: grace command\n\n\
commands\n\
--------\n\
help\t\t\tDisplay this help.\n\
new [name]\t\tCreate a new project with project name. Default is `MyProject`.\n\
build\t\t\tBuild the project.\n\
build:javascript\tBuild only the JavaScript.\n\
build:html\t\tBuild only the HTML.\n\
build:css\t\tBuild only the CSS.\n\
build:libraries\t\tBuild all the libraries.\n\
build:images\t\tBuild all the images.\n\
clean\t\t\tClean the directory of any build artefacts.'

if len(args.args) < 1:
    print help
    exit()

if args.args[0] == 'new':
    try:
        name = args.args[1]
    except:
        name = 'MyProject'
    New(name)
else:
    tasks = args.args[0].split(':')

    if tasks[0] == 'build':
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
            subtask = tasks[1]
        except IndexError:
            subtask = None

        if len(tasks) < 3:
            build_project(b, subtask)
            exit()
        else:
            print help
            exit()
    elif tasks[0] == 'clean':
        try:
            clean()
        except RemoveFolderError as e:
            print e.msg
            exit()
    else:
        print help
        exit()
