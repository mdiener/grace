import os
from error import WrongFormatError, FileNotFoundError, MissingKeyError, CreateFolderError, RemoveFolderError, FileNotWritableError, RemoveFileError
import json
import re
from shutil import rmtree, copy2, copytree
import plistlib


class Test:
    def __init__(self, testname):
        self._cwd = os.getcwd()
        self._testname = testname

        try:
            config_file = open(self._cwd + '/config.json')
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        try:
            self._config = json.load(config_file)
        except:
            raise WrongFormatError('The provided config file could not be parsed.')

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')

        self._config['name'] = self._config['name'] + '_test'
        self._build_path = self._cwd + '/build'
        self._project_test_path = self._build_path + '/' + self._config['name']

    def _create_build_directory(self):
        if os.path.exists(self._build_path):
            return

        try:
            os.makedirs(self._build_path)
        except:
            raise CreateFolderError('Could not create the build folder.')

    def _clean_previous_tests(self):
        if os.path.exists(self._project_test_path):
            try:
                rmtree(self._project_test_path)
            except:
                raise RemoveFolderError('Could not delete the test folder.')

        try:
            os.makedirs(self._project_test_path)
        except:
            raise CreateFolderError('Could not create the test folder.')

    def build_test(self):
        try:
            self._create_build_directory()
        except:
            raise

        try:
            self._clean_previous_tests()
        except:
            raise

        try:
            self._build_javascript()
        except:
            raise

        try:
            self._build_libraries()
        except:
            raise

        try:
            self._build_html()
        except:
            raise

    def _build_javascript(self):
        self._js_string_lines = []

        if self._testname:
            try:
                self._js_string_lines += self._concat_javascript(self._testname + '.js')
            except:
                raise
        else:
            path = self._cwd + '/test/javascript/'
            files = os.listdir(path)

            for f in files:
                if os.path.isfile(os.path.join(path, f)):
                    try:
                        self._js_string_lines += self._concat_javascript(f)
                    except:
                        raise

        try:
            f = open(self._project_test_path + '/test.js', 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript file.')

        self._js_string = ''.join(self._js_string_lines)
        f.write(self._js_string)
        f.close()

    def _concat_javascript(self, test):
        f = None
        lines = []

        try:
            f = open(self._cwd + '/test/javascript/' + test)
        except:
            raise FileNotFoundError('The specified file does not exist: ', 'src/application.js')

        self._included_js_files = []
        try:
            lines = self._gather_javascript_lines(f)
        except FileNotFoundError:
            raise
        finally:
            f.close()

        return lines

    def _gather_javascript_lines(self, f):
        lines = []

        for line in f:
            if re.match('\/\/include [a-zA-Z\/]+', line):
                sub_f = None

                sub_path = self._cwd + '/src/javascript/' + re.split(' ', line)[1]
                sub_path = sub_path[:-1] + '.js'

                if sub_path in self._included_js_files:
                    return ''

                self._included_js_files.append(sub_path)
                try:
                    sub_f = open(sub_path)
                except:
                    raise FileNotFoundError('The specified file does not exist: ', sub_path)

                try:
                    lines = lines + self._gather_javascript_lines(sub_f)
                except FileNotFoundError:
                    raise
                finally:
                    sub_f.close()
            else:
                lines.append(line)

        return lines

    def _build_html(self):
        if not os.path.exists(self._cwd + '/test/index.html'):
            return

        if os.path.exists(self._project_test_path + '/index.html'):
            try:
                os.remove(self._project_test_path + '/index.html')
            except:
                raise RemoveFileError('Could not remove the existing html test file.')

        try:
            copy2(self._cwd + '/test/index.html', self._project_test_path + '/index.html')
        except:
            raise FileNotWritableError('Could not write the html file.')

    def _build_libraries(self):
        if not os.path.exists(self._cwd + '/test/lib'):
            return

        if os.path.exists(self._project_test_path + '/lib'):
            try:
                rmtree(self._project_test_path + '/lib')
            except:
                raise RemoveFolderError('Could not remove the existing libraries folder.')

        try:
            copytree(self._cwd + '/test/lib', self._project_test_path + '/lib')
        except:
            raise FileNotWritableError('Could not copy all the libraries.')


class TestDizmo:
    def __init__(self):
        self._cwd = os.getcwd()

        try:
            config_file = open(self._cwd + '/config.json')
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        try:
            self._config = json.load(config_file)
        except:
            raise WrongFormatError('The provided config file could not be parsed.')

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')

        self._config['name'] = self._config['name'] + '_test'

        if 'version' not in self._config:
            raise MissingKeyError('Please specify a version in your config file.')

        try:
            dizmo_config_file = open(self._cwd + '/dizmo_config.json')
        except:
            raise FileNotFoundError('Could not find a dizmo config file in this directory.')

        try:
            self._dizmo_config = json.load(dizmo_config_file)
        except:
            raise WrongFormatError('The provided config file could not be parsed.')

        if 'bundle' not in self._dizmo_config:
            raise MissingKeyError('Bundle is missing in dizmo config file.')

        self._build_path = self._cwd + '/build'
        self._project_test_path = self._build_path + '/' + self._config['name']

        self._prepare_plist()

    def _prepare_plist(self):
        if 'width' not in self._dizmo_config:
            self._dizmo_config['width'] = 200
        if 'height' not in self._dizmo_config:
            self._dizmo_config['height'] = 200
        if 'closeBoxInsetX' not in self._dizmo_config:
            self._dizmo_config['closeBoxInsetX'] = 0
        if 'closeBoxInsetY' not in self._dizmo_config:
            self._dizmo_config['closeBoxInsetY'] = 1
        if 'developmentRegion' not in self._dizmo_config:
            self._dizmo_config['developmentRegion'] = 'English'

        self._plist = dict(
            CFBundleDevelopmentRegion=self._dizmo_config['developmentRegion'],
            CFBundleDisplayName=self._config['name'],
            CFBundleIdentifier=self._dizmo_config['bundle'] + '.' + self._config['name'],
            CFBundleName=self._config['name'],
            CFBundleShortVersionString=self._config['version'],
            CFBundleVersion=self._config['version'],
            CloseBoxInsetX=self._dizmo_config['closeBoxInsetX'],
            CloseBoxInsetY=self._dizmo_config['closeBoxInsetY'],
            MainHTML='index.html',
            Width=self._dizmo_config['width'],
            Height=self._dizmo_config['height'],
            KastellanAPIVersion='1.0'
        )

    def build_dizmo(self):
        try:
            plistlib.writePlist(self._plist, self._project_test_path + '/Info.plist')
        except:
            raise FileNotWritableError('Could not write plist to target location: ', self._project_build_path)
