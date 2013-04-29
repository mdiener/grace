#! /usr/bin/env python

import argparse
from grace.task import Task
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, UnknownCommandError
from sys import exit

parser = argparse.ArgumentParser(description='Tasks to execute', prog='grace')
parser.add_argument('--new', help='Create a new project in the current directory with a project name or `MyProject` as default.', action='store_true')
parser.add_argument('--name', help='Provide a name for the project. Only used with --new option.', action='store', default='MyProject')
parser.add_argument('--type', help='Decide what type of project you want to create. Only used with --new', action='store', default='default')
parser.add_argument('--build', '-b', help='Build the project.', action='store_true')
parser.add_argument('--deploy', '-d', help='Deploy the project.', action='store_true')
parser.add_argument('--zip', '-z', help='Zip the project.', action='store_true')
parser.add_argument('--test', '-t', help='Build the tests.', action='store_true')
parser.add_argument('--html', help='Only use html for the task.', action='store_true')
parser.add_argument('--js', help='Only use js for the task.', action='store_true')
parser.add_argument('--css', help='Only use css for the task.', action='store_true')
parser.add_argument('--img', help='Only use images for the task.', action='store_true')
parser.add_argument('--lib', help='Only use libraries for the task.', action='store_true')
parser.add_argument('--specific-test', help='Only build the specified test', action='store')
parser.add_argument('--clean', '-c', help='Clean the build environment', action='store_true')
parser.add_argument('--bad', help='Execute all tasks: build, test, deploy, zip and clean.', action='store_true')

try:
    task = Task(parser.parse_args())
except FileNotFoundError as e:
    print e.msg
    exit()
except WrongFormatError as e:
    print e.msg
    exit()
except MissingKeyError as e:
    print e.msg
    exit()
except UnknownCommandError as e:
    parser.print_help()
    exit()

try:
    task.execute()
except FileNotFoundError as e:
    print e.msg
except WrongFormatError as e:
    print e.msg
except MissingKeyError as e:
    print e.msg
except CreateFolderError as e:
    print e.msg
except FolderNotFoundError as e:
    print e.msg
except FileNotWritableError as e:
    print e.msg
except RemoveFolderError as e:
    print e.msg
except RemoveFileError as e:
    print e.msg
except FolderAlreadyExistsError as e:
    print e.msg
except SassError as e:
    print e.msg
