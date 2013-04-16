#! /usr/bin/env python

from sys import exit
import argparse
from task import Task
from error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, CommandLineArgumentError, FolderAlreadyExistsError


parser = argparse.ArgumentParser(description='Tasks to execute')
parser.add_argument('args', action='store', nargs='*')

args = parser.parse_args().args

help = ''
helpargs = ' '.join(args)
if helpargs != 'help':
    help = '`' + helpargs + '` is not a valid command.\n\n'

help = help + 'Syntax: grace [option] command\n\
You can put `dizmo` in front of every command (except help and clean)\n\
to build the project as a dizmo.\n\n\
commands\n\
--------\n\
help\t\t\t\tDisplay this help.\n\
[dizmo] new {name}\t\tCreate a new project with the given name (`MyProject default`)\n\
[dizmo] build\t\t\tBuild the project.\n\
[dizmo] build javascript\tBuild only the JavaScript.\n\
[dizmo] build html\t\tBuild only the HTML.\n\
[dizmo] build css\t\tBuild only the CSS.\n\
[dizmo] build libraries\t\tBuild all the libraries.\n\
[dizmo] build images\t\tBuild all the images.\n\
[dizmo] deploy\t\t\tDeploy the project or dizmo\n\
clean\t\t\t\tClean the directory of any build artefacts.'

try:
    task = Task(args)
except CommandLineArgumentError as e:
    print help
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
