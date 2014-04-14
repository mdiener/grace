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
        self._build = False
        self._jsdoc = False
        self._test = False
        self._deploy = False
        self._zip = False
        self._clean = False
        self._bad = False

        task = tasks[0]
        if task == 'test' or task == 'test:deploy' or task == 'test:zip':
            if len(tasks) > 1:
                self._test_cases = tasks[1]
            else:
                self._test_cases = None
        else:
            if len(tasks) > 1:
                print 'Only the test command supports multiple commands. Otherwise only the first command will be executed.'


        if task == 'clean':
            self._clean = True
        else:
            if task == 'build':
                self._build = True
            if task == 'jsdoc':
                self._jsdoc = True
            if task == 'deploy':
                self._build = True
                self._deploy = True
            if task == 'zip':
                self._build = True
                self._zip = True
            if task == 'test':
                self._test = True
            if task == 'test:deploy':
                self._test = True
                self._deploy = True
            if task == 'test:zip':
                self._test = True
                self._zip = True

            self._root = get_path()
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
            if self._test_cases is not None:
                self._config['test_cases'] = self._test_cases.split(';')
            else:
                self._config['test_cases'] = None

            self._config['test'] = True
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
                plugin.pass_config(self._config)
            except:
                raise
        else:
            plugin = None

        if self._build:
            try:
                self.exec_build(plugin)

                if self._deploy:
                    self.exec_deploy(plugin, None)
                if self._zip:
                    self.exec_zip(plugin, None)
            except:
                raise

        if self._test:
            testnames = self._config['test_cases']

            if testnames is None:
                testnames = []
                for testname in os.listdir(os.path.join(os.getcwd(), 'test', 'tests')):
                    testnames.append(testname[5:-3])

            for testname in testnames:
                try:
                    self.exec_test(plugin, testname)
                    if self._deploy:
                        self.exec_deploy(plugin, testname)
                    if self._zip:
                        self.exec_zip(plugin, testname)
                except:
                    raise

        if self._jsdoc:
            try:
                self.exec_jsdoc(plugin)
            except:
                raise


    def exec_build(self, plugin):
        try:
            b = Build(self._config)
            b.build_project()
        except:
            raise

        if plugin:
            try:
                plugin.after_build()
            except AttributeError:
                pass

        print 'Successfully built the project.'


    def exec_deploy(self, plugin, testname):
        try:
            d = Deploy(self._config)
            d.deploy_project(testname)
        except:
            raise

        if plugin:
            try:
                plugin.after_deploy(testname)
            except AttributeError:
                pass

        if testname is not None:
            print 'Successfully deployed the test: ' + testname + '.'
        else:
            print 'Successfully deployed the project.'


    def exec_zip(self, plugin, testname):
        try:
            z = Zip(self._config)
            z.zip_project(testname)
        except:
            raise

        if plugin:
            try:
                plugin.after_zip(testname)
            except AttributeError:
                pass

        if testname is not None:
            print 'Successfully zipped the test: ' + testname + '.'
        else:
            print 'Successfully zipped the project.'


    def exec_test(self, plugin, testname):
        try:
            t = Test(self._config)
            t.build_test(testname)
        except:
            raise

        if plugin:
            try:
                plugin.after_test(testname)
            except AttributeError:
                pass

        if testname is not None:
            print 'Successfully built the test: ' + testname + '.'
        else:
            print 'Successfully built the test.'


    def exec_jsdoc(self, plugin):
        try:
            doc = Doc(self._config)
            doc.build_doc()
        except:
            raise

        if plugin:
            try:
                plugin.after_doc()
            except AttributeError:
                pass

        print 'Successfully built the JSDoc documentation.'
