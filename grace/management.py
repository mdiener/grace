from grace.task import Task
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, UnknownCommandError
import sys
import os
from shutil import copy
from pkg_resources import resource_filename


def port_grace():
    try:
        assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', 'manage.py')))
    except NotImplementedError:
        assetPath = os.path.join(sys.prefix, 'assets', 'manage.py')

    try:
        copy(assetPath, os.getcwd())
    except:
        print 'Could not create the manage.py file.'


def execute_commands(cmds):
    if 'help' in cmds:
        print_help()
        return

    execute(cmds)


def execute_new():
    print 'To set up your project we need a bit more information.'
    print 'The values in brackets are the default values. You can just hit enter if you do not want to change them.\n'

    tasks = new_input()
    execute(tasks)


def new_input():
    name = raw_input('Please provide a name for you project [MyProject]: ')
    type = raw_input('Select what type of project you want to create [default]: ')

    if name == '':
        name = 'MyProject'
    if type == '':
        type = 'default'

    print '\nReview your information:'
    print 'Name: ' + name
    print 'Type: ' + type
    okay = raw_input('Are the options above correct? [y]: ')

    if okay != 'y' and okay != '':
        print '\n'
        args = new_input()

    return {
        'new': True,
        'name': name,
        'type': type
    }


def execute(args):
    try:
        task = Task(args)
    except FileNotFoundError as e:
        print e.msg
        return
    except WrongFormatError as e:
        print e.msg
        return
    except MissingKeyError as e:
        print e.msg
        return
    except UnknownCommandError as e:
        print 'One of the following commands is not recognized: "' + ', '.join(args) + '"'
        return

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


def print_help():
    print 'Grace Help'
    print '=========='
    print 'Grace is a toolchain to work with rich JavaScript applications. It'
    print 'provides several tools for developers to create applications in a'
    print 'fast and clean manner.'
    print '\nUsage'
    print '-----'
    print 'python manage.py [command]'
    print '\nCommands'
    print '--------\n'
    print 'build\tBuilds the project and places the output in ./build/ProjectName.'
    print 'deploy\tFirst build and then deploy the project to the path'
    print '\tspecified in the deployment_path option in your project.cfg file.'
    print 'jsdoc\tBuild the jsDoc of the project.'
    print 'zip\tBuild and then zip the output and put it into the path'
    print '\tspecified by the zip_path option in your project.cfg file.'
    print 'clean\tClean the build output.'
    print 'test\tBuild all the tests.'
    print 'bad\tDo a build, test, jsdoc, deploy and zip together.'
    print '\nFurther Reading'
    print '---------------'
    print 'For more information visit http://www.github.com/mdiener/grace'
