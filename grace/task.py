from build import Build, clean
from deploy import Deploy
from zipit import Zip
from testit import Test
from create import New
from doc import Doc
import os
import json
import re
from error import FileNotFoundError, WrongFormatError, MissingKeyError, UnknownCommandError
import sys


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


class Task:
    def __init__(self, tasks):
        self._new = False
        self._build = False
        self._jsdoc = False
        self._with_libs = False
        self._test = False
        self._deploy = False
        self._zip = False
        self._clean = False
        self._bad = False

        if 'new' in tasks:
            self._new = True
            self._name = tasks['name']
            self._type = tasks['type']
        if 'build' in tasks:
            self._build = True
        if 'jsdoc' in tasks:
            self._jsdoc = True
        if 'deploy' in tasks:
            self._deploy = True
        if 'test' in tasks:
            self._test = True
        if 'zip' in tasks:
            self._zip = True
        if 'clean' in tasks:
            self._clean = True
        if 'bad' in tasks:
            self._bad = True

        self._root = get_path()
        if not self._new and not self._clean:
            if self._bad:
                self._build = True
                self._test = True
                self._deploy = True
                self._zip = True
                self._jsdoc = True
            if not self._build and not self._test and not self._deploy and not self._zip and not self._jsdoc:
                raise UnknownCommandError()

            try:
                self._parse_config()
            except:
                raise

    def _parse_config(self):
        cwd = os.getcwd()

        try:
            config_file = open(os.path.join(cwd, 'project.cfg'))
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        strings = []
        for line in config_file:
            if not re.search('^\s*//.*', line):
                strings.append(line)

        try:
            self._config = json.loads(''.join(strings))
        except:
            raise WrongFormatError('The provided config file could not be parsed.')

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')
        else:
            if not isinstance(self._config['name'], unicode):
                raise WrongFormatError('The name key in your config file must be a string!')
            else:
                if len(self._config['name']) == 0:
                    raise WrongFormatError('The name key in your config file must be at least one character long.')

        if 'version' not in self._config:
            raise MissingKeyError('Please specify a version in your config file.')
        else:
            if not isinstance(self._config['version'], unicode):
                raise WrongFormatError('The version key in your config file needs to be a string!')

        if 'minify_js' not in self._config:
            self._config['minify_js'] = False
        else:
            if not isinstance(self._config['minify_js'], bool):
                self._config['minify_js'] = False

        if 'minify_css' not in self._config:
            self._config['minify_css'] = False
        else:
            if not isinstance(self._config['minify_css'], bool):
                self._config['minify_css'] = False

        if 'type' not in self._config:
            self._type = 'default'
        else:
            if not isinstance(self._config['type'], unicode):
                self._type = 'default'
            else:
                if len(self._config['type']) == 0:
                    self._type = 'default'
                else:
                    self._type = self._config['type']

        if 'js_name' not in self._config:
            self._config['js_name'] = 'application'
        else:
            if not isinstance(self._config['js_name'], unicode):
                self._config['js_name'] = 'application'
            else:
                if len(self._config['js_name']) == 0:
                    self._config['js_name'] = 'application'

        self._config['build_path'] = os.path.join(cwd, 'build', self._config['name'])
        if self._build or not self._test and self._deploy or not self._test and self._zip:
            self._config['build'] = True
        else:
            self._config['build'] = False

        if self._test:
            try:
                self._config['testname'] = self._args.testname
            except:
                self._config['testname'] = None

            self._config['test'] = True
            self._config['test_build_path'] = os.path.join(cwd, 'build', self._config['name'] + '_test')
        else:
            self._config['test'] = False

    def execute(self):
        if self._clean:
            try:
                clean()
            except:
                raise
            return

        if self._type != 'default':
            module = __import__('grace-' + self._type + '.plugin')
            try:
                plugin = getattr(module.plugin, self._type.title())()
            except:
                raise
        else:
            plugin = None

        if self._new:
            try:
                New(self._name, plugin, self._type)
                print 'Created the project with name ' + self._name + '.'
            except:
                raise
            return

        if plugin:
            try:
                plugin.pass_config(self._config)
            except:
                raise

        try:
            b = Build(self._config)
            t = Test(self._config)
            d = Deploy(self._config)
            z = Zip(self._config)
            doc = Doc(self._config)
        except:
            raise

        if self._build:
            try:
                b.build_project()
                if plugin:
                    try:
                        plugin.after_build()
                    except AttributeError:
                        pass
                print 'Successfully built the project.'
            except:
                raise

        if self._jsdoc:
            try:
                doc.build_doc()
                if plugin:
                    try:
                        plugin.after_doc()
                    except AttributeError:
                        pass
                print 'Successfully built the JSDoc documentation.'
            except:
                raise

        if self._test:
            try:
                t.build_test()
                if plugin:
                    try:
                        plugin.after_test()
                    except AttributeError:
                        pass
                print 'Successfully built the tests.'
            except:
                raise

        if self._deploy:
            if not self._build and not self._test:
                try:
                    b.build_project()
                    if plugin:
                        try:
                            plugin.after_build()
                        except AttributeError:
                            pass
                    print 'Successfully built the project.'
                except:
                    raise

            try:
                d.deploy_project()
                if plugin:
                    try:
                        plugin.after_deploy()
                    except AttributeError:
                        pass
                print 'Successfully deployed the project.'
            except:
                raise

        if self._zip:
            if not self._build and not self._test:
                b.build_project()
                if plugin:
                    try:
                        plugin.after_build()
                    except AttributeError:
                        pass
                print 'Successfully built the project.'

            try:
                z.zip_project()
                if plugin:
                    try:
                        plugin.after_zip()
                    except AttributeError:
                        pass
                print 'Successfully zipped the project.'
            except:
                raise
