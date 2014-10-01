from grace.task import Task
from grace.create import New
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, UnknownCommandError
import sys
import os
from shutil import copy
from pkg_resources import resource_filename


def get_asset_path(asset):
    if not isinstance(asset, basestring):
        raise WrongFormatError('Asset needs to be a string.')

    try:
        assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', asset)))
    except NotImplementedError:
        assetPath = os.path.join(sys.prefix, 'assets', asset)

    return assetPath


def global_config():
    global_config_path = os.path.join(os.path.expanduser('~'), '.graceconfig')
    assetPath = get_asset_path('grace.cfg')

    if not os.path.isfile(global_config_path):
        deployment_path = os.path.join(os.path.expanduser('~'))
        zip_path = os.path.join(os.path.expanduser('~'))
        doc_path = os.path.join(os.path.expanduser('~'))

        if sys.platform.startswith('win32'):
            deployment_path = deployment_path.replace('\\', '\\\\')
            zip_path = zip_path.replace('\\', '\\\\')

        with open(global_config_path, 'w+') as out:
            infile = open(assetPath)
            for line in infile:
                newline = line.replace('##DEPLOYMENTPATH##', deployment_path)
                newline = newline.replace('##ZIPPATH##', zip_path)
                newline = newline.replace('##DOCPATH##', doc_path)

                out.write(newline)

            infile.close()


def port_grace():
    assetPath = get_asset_path('manage.py');

    try:
        copy(assetPath, os.getcwd())
    except:
        print 'Could not create the manage.py file.'


def execute_commands(cmds):
    if 'help' in cmds:
        print_help()
        return

    try:
        cmds.remove('st')
        show_stacktrace = True
    except ValueError:
        show_stacktrace = False

    if len(cmds) < 1:
        print 'Need to provide at least one argument to the manage.py script.\n'
        print_help()
        return

    global_config()
    execute(cmds, show_stacktrace)


def execute_new():
    print 'To set up your project we need a bit more information.'
    print 'The values in brackets are the default values. You can just hit enter if you do not want to change them.\n'

    inputs = new_input()

    try:
        New(inputs['name'], inputs['pluginName'])
        print 'Created the project, type ' + inputs['pluginName'] + ', with name ' + inputs['name'] + '.'
    except:
        raise


def new_input():
    name = raw_input('Please provide a name for your project [MyProject]: ')
    pluginName = raw_input('Select what type (plugin) of project you want to create [default]: ')

    if name == '':
        name = 'MyProject'
    if pluginName == '':
        pluginName = 'default'

    print '\nReview your information:'
    print 'Name: ' + name
    print 'Plugin: ' + pluginName
    okay = raw_input('Are the options above correct? [y]: ')

    if okay != 'y' and okay != '':
        print '\n'
        args = new_input()

    return {
        'name': name,
        'pluginName': pluginName
    }


def execute(args, show_stacktrace):
    if show_stacktrace:
        try:
            task = Task(args)
            task.execute()
        except:
            raise
    else:
        try:
            task = Task(args)
        except FileNotFoundError as e:
            print_error_msg(e.msg)
            return
        except WrongFormatError as e:
            print_error_msg(e.msg)
            return
        except MissingKeyError as e:
            print_error_msg(e.msg)
            return
        except UnknownCommandError as e:
            print_error_msg(e.msg)
            return

        try:
            task.execute()
        except FileNotFoundError as e:
            print_error_msg(e.msg)
        except WrongFormatError as e:
            print_error_msg(e.msg)
        except MissingKeyError as e:
            print_error_msg(e.msg)
        except CreateFolderError as e:
            print_error_msg(e.msg)
        except FolderNotFoundError as e:
            print_error_msg(e.msg)
        except FileNotWritableError as e:
            print_error_msg(e.msg)
        except RemoveFolderError as e:
            print_error_msg(e.msg)
        except RemoveFileError as e:
            print_error_msg(e.msg)
        except FolderAlreadyExistsError as e:
            print_error_msg(e.msg)
        except SassError as e:
            print_error_msg(e.msg)


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
    print 'build\t\tBuilds the project and places the output in ./build/ProjectName.'
    print 'deploy\t\tFirst build and then deploy the project to the path'
    print '\t\tspecified in the deployment_path option in your project.cfg file.'
    print 'jsdoc\t\tBuild the jsDoc of the project.'
    print 'zip\t\tBuild and then zip the output and put it into the path'
    print '\t\tspecified by the zip_path option in your project.cfg file.'
    print 'clean\t\tClean the build output.'
    print 'test\t\tBuild all the tests.'
    print 'test:deploy\tBuild and then deploy the tests.'
    print 'test:zip\tBuild and then zip the tests'
    print 'st\t\tCan be used with any command to show the full stack trace'
    print '\t\t(in case of an error).'
    print '\nFurther Reading'
    print '---------------'
    print 'For more information visit http://www.github.com/mdiener/grace'


def print_error_msg(msg):
    print msg
    print 'For more information type: python manage.py help'
