import os
from error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError
import json
from shutil import copy2, copytree, rmtree
import re
import sass
import plistlib


class Build:
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

        self._build_path = self._cwd + '/build'
        self._project_build_path = self._build_path + '/' + self._config['name']

    def _create_build_directory(self):
        if os.path.exists(self._build_path):
            return

        try:
            os.makedirs(self._build_path)
        except:
            raise CreateFolderError('Could not create the build folder.')

    def build_project(self, restrict=None):
        try:
            self._create_build_directory()
        except:
            raise

        if not os.path.exists(self._project_build_path):
            try:
                os.makedirs(self._project_build_path)
            except:
                raise CreateFolderError('Could not create the project folder.')

        try:
            if restrict == 'javascript':
                self._build_javascript()
            elif restrict == 'css':
                self._build_css()
            elif restrict == 'html':
                self._build_html()
            elif restrict == 'images':
                self._build_images()
            elif restrict == 'libraries':
                self._build_libraries()
            elif restrict is None:
                self._build_javascript()
                self._build_libraries()
                self._build_css()
                self._build_html()
                self._build_images()
            else:
                raise WrongFormatError('Please provide either javascript, css, html or images as the subtask for building a project.')
        except:
            raise

    def _build_javascript(self):
        if not os.path.exists(self._cwd + '/src/application.js'):
            return

        try:
            self._js_string = self._concat_javascript()
        except FileNotFoundError:
            raise
        except FolderNotFoundError:
            raise

        if os.path.exists(self._project_build_path + '/application.js'):
            try:
                os.remove(self._project_build_path + '/application.js')
            except:
                raise RemoveFileError('Could not delete the existing javascript application file.')

        try:
            f = open(self._project_build_path + '/application.js', 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript file.')

        f.write(self._js_string)

    def _concat_javascript(self):
        f = None
        lines = []

        try:
            f = open(self._cwd + '/src/application.js')
        except:
            raise FileNotFoundError('The specified file does not exist: ', 'src/application.js')

        try:
            lines = self._gather_javascript_lines(f)
        except FileNotFoundError:
            raise
        finally:
            f.close()

        return ''.join(lines)

    def _gather_javascript_lines(self, f):
        lines = []

        for line in f:
            if re.match('\/\/include:[a-zA-Z\/]+', line):
                sub_f = None

                sub_path = self._cwd + '/src/javascript/' + re.split(' ', line)[1]
                sub_path = sub_path[:-1] + '.js'
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
        if not os.path.exists(self._cwd + '/src/index.html'):
            return

        if os.path.exists(self._project_build_path + '/index.html'):
            try:
                os.remove(self._project_build_path + '/index.html')
            except:
                raise RemoveFileError('Could not remove the existing html build file.')

        try:
            copy2(self._cwd + '/src/index.html', self._project_build_path + '/index.html')
        except:
            raise FileNotWritableError('Could not write the html file.')

    def _build_css(self):
        if not os.path.exists(self._cwd + '/src/style/style.scss') and not os.path.exists(self._cwd + '/src/style/style.css'):
            return

        if not os.path.exists(self._project_build_path + '/style'):
            try:
                os.makedirs(self._project_build_path + '/style')
            except:
                raise CreateFolderError('Could not create the style folder.')

        if os.path.exists(self._project_build_path + '/style/style.css'):
            try:
                os.remove(self._project_build_path + '/style/style.css')
            except:
                raise RemoveFileError('Could not remove the existing css file.')

        if os.path.exists(self._cwd + '/src/style/style.scss'):
            try:
                _css_string = sass.compile(filename=self._cwd + '/src/style/style.scss')
            except:
                raise FileNotFoundError('Could not find your scss style file.')

            try:
                f = open(self._project_build_path + '/style/style.css', 'w+')
            except:
                raise FileNotWritableError('Could not write the new css file.')

            f.write(_css_string)
            f.close()
        elif os.path.exists(self._cwd + '/src/style/style.css'):
            try:
                copy2(self._cwd + '/src/style/style.css', self._project_build_path + '/style/style.css')
            except:
                raise FileNotWritableError('Could not write the new css file.')

    def _build_images(self):
        if not os.path.exists(self._cwd + '/src/style/images'):
            return

        if not os.path.exists(self._project_build_path + '/style'):
            try:
                os.makedirs(self._project_build_path + '/style')
            except:
                raise CreateFolderError('Could not create the style folder.')

        if os.path.exists(self._project_build_path + '/style/images'):
            try:
                rmtree(self._project_build_path + '/style/images')
            except:
                raise RemoveFolderError('Could not remove the existing images folder.')

        try:
            copytree(self._cwd + '/src/style/images', self._project_build_path + '/style/images')
        except:
            raise FileNotWritableError('Could not copy all the images in the image folder.')

    def _build_libraries(self):
        if not os.path.exists(self._cwd + '/src/lib'):
            return

        if os.path.exists(self._project_build_path + '/lib'):
            try:
                rmtree(self._project_build_path + '/lib')
            except:
                raise RemoveFolderError('Could not remove the existing libraries folder.')

        try:
            copytree(self._cwd + '/src/lib', self._project_build_path + '/lib')
        except:
            raise FileNotWritableError('Could not copy all the libraries.')


class BuildDizmo:
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
        self._project_build_path = self._build_path + '/' + self._config['name']

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
            plistlib.writePlist(self._plist, self._project_build_path + '/Info.plist')
        except:
            raise FileNotWritableError('Could not write plist to target location: ', self._project_build_path)


def clean():
    if not os.path.exists(os.getcwd() + '/build'):
        return

    try:
        rmtree(os.getcwd() + '/build')
    except:
        raise RemoveFolderError('Could not remove the build folder.')
