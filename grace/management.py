from grace.task import Task
from grace.create import New, Assets
from grace.config import Config
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, UnknownCommandError, WrongLoginCredentials, FileUploadError
import sys
import os
from shutil import copy
from pkg_resources import resource_filename
import logging
import re
import requests

logging.basicConfig(level=0)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


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
            doc_path = doc_path.replace('\\', '\\\\')

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


def execute_new(args):
    name = ''
    plugin = ''

    try:
        if re.match('^--name=\w+$', args[2]):
            name = args[2][7:]
        elif re.match('^--plugin=\w+$', args[2]):
            plugin = args[2][9:]

        try:
            if re.match('^--name=\w+$', args[3]):
                name = args[3][7:]
            elif re.match('^--plugin=\w+$', args[3]):
                plugin = args[3][9:]
        except:
            pass
    except:
        pass

    inputs = new_input(name, plugin)

    module = None
    if inputs['pluginName'] is not 'default':
        try:
            module = __import__('grace-' + inputs['pluginName'] + '.plugin')
        except:
            print('Could not find the plugin you selected. Please try again.')
            return

    if module is not None:
        try:
            getattr(module.plugin, 'New')(inputs['name'])
        except AttributeError:
            New(inputs['name'])
    else:
        New(inputs['name'])

    Assets(inputs['name'])
    print 'Created the project, type ' + inputs['pluginName'] + ', with name ' + inputs['name'] + '.'


def new_input(name, pluginName):
    if name == '' and pluginName == '':
        preset = False
        print 'To set up your project we need a bit more information.'
        print 'The values in brackets are the default values. You can just hit enter if you do not want to change them.\n'
    else:
        preset = True

    if name is '':
        name = raw_input('Please provide a name for your project [MyProject]: ')
        if name is '':
            name = 'MyProject'

    if pluginName is '':
        pluginName = raw_input('Select what type (plugin) of project you want to create [default]: ')
        if pluginName is '':
            pluginName = 'default'

    if not preset:
        print '\nReview your information:'
        print 'Name: ' + name
        print 'Plugin: ' + pluginName
        okay = raw_input('Are the options above correct? [y]: ')

        if okay != 'y' and okay != '':
            print '\n'
            args = new_input('', '')

    return {
        'name': name,
        'pluginName': pluginName
    }


def execute(args, show_stacktrace=False):
    if show_stacktrace:
        c = Config()
        config = c.get_config()

        module = None
        if config['type'] is not 'default':
            module = __import__('grace-' + config['type'] + '.plugin')
            try:
                c = getattr(module.plugin, 'Config')(config)
                config = c.get_config()
            except AttributeError:
                pass

        try:
            task = getattr(module.plugin, 'Task')(args, config, module)
        except AttributeError:
            task = Task(args, config, module)

        task.execute()
    else:
        try:
            c = Config()
            config = c.get_config()
        except (WrongFormatError, MissingKeyError, FileNotFoundError) as e:
            print_error_msg(e.msg)
            return

        module = None
        if config['type'] is not 'default':
            try:
                module = __import__('grace-' + config['type'] + '.plugin')
            except:
                print_error_msg('Could not load the module of type ' + config['type'] + '.')
                return

            try:
                c = getattr(module.plugin, 'Config')(config)
                config = c.get_config()
            except AttributeError:
                pass
            except (WrongFormatError, MissingKeyError) as e:
                print_error_msg(e.msg)
                return
            except:
                print_error_msg('Could not load the plugin (' + config['type'] + ') configuration.')
                return

        try:
            task = getattr(module.plugin, 'Task')(args, config, module)
        except UnknownCommandError as e:
            print_error_msg(e.msg)
            return
        except AttributeError:
            try:
                task = Task(args, config, module)
            except UnknownCommandError as e:
                print_error_msg(e.msg)
                return
            except:
                print_error_msg('Could not initialize the Task module. Aborting!')
                return
        except:
            print_error_msg('Could not initialize the Task module. Aborting!')
            return

        try:
            task.execute()
        except (FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, WrongLoginCredentials, FileUploadError) as e:
            print_error_msg(e.msg)
        except Exception as e:
            print_error_msg('Could not execute the given task. Something went wrong, please try again!')


def print_help():
    userhome = os.path.join(os.path.expanduser('~'), '.graceconfig')

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
    print 'upload\tUpload the project to the specified server.'
    print 'st\t\tCan be used with any command to show the full stack trace'
    print '\t\t(in case of an error).'
    print '\nThe global configuration file can be found at: ' + userhome
    print '\nFurther Reading'
    print '---------------'
    print 'For more information visit http://www.github.com/mdiener/grace'


def print_error_msg(msg):
    print msg
    print '\nFor more information type: python manage.py help'
