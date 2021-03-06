from __future__ import print_function
from builtins import input
from past.builtins import basestring
from grace.task import Task
from grace.create import New, Assets
from grace.config import Config
from grace.cmdparse import CommandLineParser
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, ScssError, UnknownCommandError, WrongLoginCredentials, RemoteServerError, KeyNotAllowedError, SubProjectError, ParseError
from grace.utils import isstring
import sys
import os
from shutil import copy, move
from pkg_resources import resource_filename
import logging
import re
import requests
import pip

logging.basicConfig(level=0)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('watchdog').setLevel(logging.WARNING)


if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf8')


def get_asset_path(asset):
    if not isstring(asset):
        raise WrongFormatError('Asset needs to be a string.')

    try:
        assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', asset)))
    except NotImplementedError:
        assetPath = os.path.join(sys.prefix, 'assets', asset)

    return assetPath


def global_config():
    global_config_path = os.path.join(os.path.expanduser('~'), '.grace', 'grace.cfg')
    old_global_config_path = os.path.join(os.path.expanduser('~'), '.graceconfig')
    assetPath = get_asset_path('grace.cfg')

    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.grace')):
        os.makedirs(os.path.join(os.path.expanduser('~'), '.grace'))

    if os.path.exists(old_global_config_path):
        move(old_global_config_path, global_config_path)

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
        print('Could not create the manage.py file.')


def execute_commands(*args):
    execute()


def get_installed_plugins():
    all_dists = pip.commands.list.get_installed_distributions()
    plugins = []

    for dist in all_dists:
        name = dist.project_name.replace('grace_', 'grace-')
        if name.startswith('grace-'):
            plugins.append(name.strip('grace-'))

    return plugins;


def execute_new(args):
    name = ''
    plugin = ''
    skeleton = ''

    try:
        if re.match('^--name=\w+$', args[2]):
            name = args[2][7:]
        elif re.match('^--plugin=\w+$', args[2]):
            plugin = args[2][9:]
        elif re.match('^--skeleton=\w+$', args[2]):
            skeleton = args[2][11:]

        try:
            if re.match('^--name=\w+$', args[3]):
                name = args[3][7:]
            elif re.match('^--plugin=\w+$', args[3]):
                plugin = args[3][9:]
            elif re.match('^--skeleton=\w+$', args[3]):
                skeleton = args[3][11:]
        except:
            pass

        try:
            if re.match('^--name=\w+$', args[4]):
                name = args[4][7:]
            elif re.match('^--plugin=\w+$', args[4]):
                plugin = args[4][9:]
            elif re.match('^--skeleton=\w+$', args[4]):
                skeleton = args[4][11:]
        except:
            pass

    except:
        pass

    inputs = new_input(name, plugin, skeleton)

    module = None
    if inputs['pluginName'] != 'default':
        try:
            module = __import__('grace-' + inputs['pluginName'] + '.plugin')
        except:
            print('Could not find the plugin you selected. Please try again.')
            return

    if module is not None:
        try:
            getattr(module.plugin, 'New')(inputs['name'], inputs['skeleton'])
        except AttributeError:
            New(inputs['name'], inputs['skeleton'])
    else:
        New(inputs['name'], inputs['skeleton'])

    Assets(inputs['name'])
    print('Created the project, type ' + inputs['pluginName'] + ', with name ' + inputs['name'] + ' and skeleton ' + inputs['skeleton'] + '.')


def new_input(name, pluginName, skeleton):
    if name == '' and pluginName == '' and skeleton == '':
        preset = False
        print('To set up your project we need a bit more information.')
        print('The values in brackets are the default values. You can just hit enter if you do not want to change them.\n')
    else:
        preset = True

    if name == '':
        name = input('Please provide a name for your project [MyProject]: ')
        if name == '':
            name = 'MyProject'

    if pluginName == '':
        pluginName = plugin_name_input()

    module = None
    if pluginName != 'default':
        try:
            module = __import__('grace-' + pluginName + '.plugin')
        except AttributeError:
            pass

    if skeleton == '':
        skeleton = skeleton_input(module)

    args = {
        'name': name,
        'pluginName': pluginName,
        'skeleton': skeleton
    }

    if not preset:
        print('\nReview your information:')
        print('Name: ' + name)
        print('Plugin: ' + pluginName)
        print('Skeleton: ' + skeleton)
        okay = input('Are the options above correct? [y]: ')

        if okay != 'y' and okay != '':
            print('\n')
            args = new_input('', '', '')

    return args


def plugin_name_input():
    name = 'default'
    plugins = get_installed_plugins()

    output = 'Select what type (plugin) of project you want to create:'

    if len(plugins) == 0:
        name = input(output + ' default. [default]: ')
        if name == '':
            name = 'default'
    else:
        plugin_string = ''
        for plugin in plugins:
            plugin_string += plugin + ', '
        plugin_string = plugin_string.rstrip(', ')

        if 'dizmo' in plugins:
            name = input(output + ' default, ' + plugin_string + '. [dizmo]: ')
            if name == '':
                name = 'dizmo'
        else:
            name = input(output + ' default, ' + plugin_string + '. [default]: ')
            if name == '':
                name = 'default'

    return name


def skeleton_input(module=None):
    skeletons = ['default']
    if module is not None:
        try:
            skeletons = getattr(module.plugin, 'get_skeleton_names')()
        except AttributeError:
            pass

    skeleton_string = ''
    for s in skeletons:
        skeleton_string += s + ', '
    skeleton_string = skeleton_string[:-2]

    print('Please provide an URL to a skeleton or chose from the list of known skeletons:')
    skeleton = input('Skeletons: ' + skeleton_string + '. [' + skeletons[0] + ']: ')
    if skeleton == '':
        skeleton = skeletons[0]

    return skeleton


def execute(*args):
    global_config()
    config = Config()
    parsedConfig = None
    module = None

    if config.get_type() is not 'default':
        try:
            module = __import__('grace-' + config.get_type() + '.plugin')
        except:
            print_error_msg('Could not load the module of type ' + config.get_type() + '.')
            return

        try:
            config = getattr(module.plugin, 'Config')()
        except AttributeError:
            pass
        except MissingKeyError as e:
            print(e.msg)
            return

    parser = None
    if config.get_type() is not 'default':
        try:
            parser = getattr(module.plugin, 'CommandLineParser')()
            task, test_cases, overwrites, show_stacktrace = parser.get_arguments()
        except AttributeError:
            parser = CommandLineParser()
            task, test_cases, overwrites, show_stacktrace = parser.get_arguments()
    else:
        parser = CommandLineParser()
        task, test_cases, overwrites, show_stacktrace = parser.get_arguments()

    try:
        config.load_overwrites(overwrites)
    except KeyNotAllowedError as e:
        print_error_msg(e.msg)
        return;

    try:
        parsedConfig = config.get_config()
    except (WrongFormatError, MissingKeyError, FileNotFoundError) as e:
        print_error_msg(e.msg)
        return

    if show_stacktrace:
        try:
            task = getattr(module.plugin, 'Task')(task, parsedConfig, module, test_cases)
        except AttributeError:
            task = Task(task, parsedConfig, module, test_cases)

        task.execute()
    else:
        try:
            task = getattr(module.plugin, 'Task')(task, parsedConfig, module, test_cases)
        except UnknownCommandError as e:
            print_error_msg(e.msg)
            return
        except AttributeError:
            try:
                task = Task(task, parsedConfig, module, test_cases)
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
        except (FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, ScssError, WrongLoginCredentials, SubProjectError, ParseError) as e:
            print_error_msg(e.msg)
        except RemoteServerError as e:
            print(e.msg)
        except Exception as e:
            print_error_msg('Could not execute the given task. Something went wrong, please try again!')


def print_error_msg(msg):
    print(msg)
    print('\nFor more information type: python manage.py -h')
