from build import Build, clean
from deploy import Deploy
from zipit import Zip
from testit import Test
from create import New
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
    def __init__(self, args):
        self._new = False
        self._build = False
        self._with_libs = False
        self._test = False
        self._deploy = False
        self._zip = False
        self._clean = False
        self._bad = False
        self._restrict = []
        self._args = args
        self._root = get_path()

        if args.new:
            self._new = True
            self._name = args.name
            self._type = args.type
        elif args.clean:
            self._clean = True
        else:
            if args.build:
                self._build = True
            if args.test:
                self._test = True
            if args.deploy:
                self._deploy = True
            if args.zip:
                self._zip = True
            if args.bad:
                self._bad = True
                self._build = True
                self._test = True
                self._deploy = True
                self._zip = True

            if not self._build and not self._test and not self._deploy and not self._zip and not self._bad:
                raise UnknownCommandError()

            try:
                self._parse_config()
            except:
                raise

            if args.html:
                self._restrict.append('html')

            if args.js:
                self._restrict.append('js')

            if args.css:
                self._restrict.append('css')

            if args.img:
                self._restrict.append('img')

            if args.lib:
                self._restrict.append('lib')

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

        if 'version' not in self._config:
            raise MissingKeyError('Please specify a version in your config file.')

        if 'minify_js' not in self._config:
            self._config['minify_js'] = False

        if 'minify_css' not in self._config:
            self._config['minify_css'] = False

        if 'type' not in self._config:
            self._type = 'default'
        else:
            self._type = self._config['type']

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
        except:
            raise

        if self._build:
            try:
                b.build_project(self._restrict)
                if plugin:
                    try:
                        plugin.after_build()
                    except AttributeError:
                        pass
                print 'Successfully built the project.'
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
                    b.build_project(self._restrict)
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
                b.build_project(self._restrict)
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
