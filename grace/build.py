import os
from error import FileNotFoundError, CreateFolderError, FileNotWritableError, FileNotReadableError, RemoveFolderError, RemoveFileError, SassError
from shutil import copy2, copytree, rmtree
from slimit import minify
from cssmin import cssmin
import re
import sass
import sys


class Build:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def build_project(self, restrict):
        self._project_build_style_path = os.path.join(self._config['build_path'], 'style')

        if not os.path.exists(self._config['build_path']):
            try:
                os.makedirs(self._config['build_path'])
            except:
                raise CreateFolderError('Could not create the project folder.')

        if restrict:
            for r in restrict:
                try:
                    if r == 'js':
                        self._build_javascript()
                    if r == 'css':
                        self._build_css()
                    if r == 'html':
                        self._build_html()
                    if r == 'img':
                        self._build_images()
                    if r == 'lib':
                        self._build_libraries()
                except:
                    raise
        else:
            try:
                self._build_javascript()
                self._build_css()
                self._build_html()
                self._build_images()
                self._build_libraries()
            except:
                raise

    def _build_javascript(self):
        source = os.path.join(self._cwd, 'src', 'application.js')
        dest = os.path.join(self._config['build_path'], 'application.js')

        if not os.path.exists(source):
            return

        try:
            self._js_string = self._concat_javascript()
        except:
            raise

        if os.path.exists(dest):
            try:
                os.remove(dest)
            except:
                raise RemoveFileError('Could not delete the existing javascript application file.')

        try:
            f = open(dest, 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript file.')

        if self._config['minify_js']:
            minifiedjs = minify(self._js_string, mangle=True, mangle_toplevel=True)
            f.write(minifiedjs)
        else:
            f.write(self._js_string)
        f.close()

    def _concat_javascript(self):
        f = None
        lines = []

        try:
            f = open(os.path.join(self._cwd, 'src', 'application.js'))
        except:
            raise FileNotFoundError('The specified file does not exist: ', os.path.join('src', 'application.js'))

        self._included_js_files = []
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
            match = re.match('\/\/= require ([a-zA-Z\/]+)', line)
            if match:
                sub_f = None

                sub_path = match.group(1)
                if sys.platform.startswith('win32'):
                    sub_path = sub_path.replace('/', '\\')
                sub_path = os.path.join(self._cwd, 'src', 'javascript', sub_path)
                sub_path = sub_path + '.js'

                if sub_path not in self._included_js_files:
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
        source = os.path.join(self._cwd, 'src', 'index.html')
        dest = os.path.join(self._config['build_path'], 'index.html')

        if not os.path.exists(source):
            return

        if os.path.exists(dest):
            try:
                os.remove(dest)
            except:
                raise RemoveFileError('Could not remove the existing html build file.')

        try:
            copy2(source, dest)
        except:
            raise FileNotWritableError('Could not write the html file.')

    def _build_css(self):
        source_scss = os.path.join(self._cwd, 'src', 'style', 'style.scss')
        source_css = os.path.join(self._cwd, 'src', 'style', 'style.css')
        dest = os.path.join(self._config['build_path'], 'style', 'style.css')

        if not os.path.exists(source_css) and not os.path.exists(source_scss):
            return

        if not os.path.exists(self._project_build_style_path):
            try:
                os.makedirs(self._project_build_style_path)
            except:
                raise CreateFolderError('Could not create the style folder.')

        if os.path.exists(source_css):
            try:
                os.remove(dest)
            except:
                raise RemoveFileError('Could not remove the existing css file.')

        if os.path.exists(source_scss):
            try:
                _css_string = sass.compile(filename=source_scss)
            except sass.CompileError as e:
                raise SassError('Could not compile your scss file:\n', e.message[:-1])
            except:
                raise FileNotFoundError('Could not find your scss style file.')

            try:
                f = open(dest, 'w+')
            except:
                raise FileNotWritableError('Could not write the new css file.')

            if self._config['minify_css']:
                minifiedcss = cssmin(_css_string)
                f.write(minifiedcss)
            else:
                f.write(_css_string)

            f.close()
        elif os.path.exists(source_css):
            if self._config['minify_css']:
                try:
                    f = open(source_css, 'r')
                    _css_string = f.read()
                    f.flose()
                    minifiedcss = cssmin(_css_string)

                    try:
                        d = open(dest, 'w+')
                    except:
                        raise FileNotWritableError('Could not write thre new css file.')

                    d.write(minifiedcss)
                    d.close()
                except:
                    raise FileNotReadableError('Could not read the css input file.')
            else:
                try:
                    copy2(source_css, dest)
                except:
                    raise FileNotWritableError('Could not write the new css file.')

    def _build_images(self):
        source = os.path.join(self._cwd, 'src', 'style', 'images')
        dest = os.path.join(self._config['build_path'], 'style', 'images')

        if not os.path.exists(source):
            return

        if not os.path.exists(self._project_build_style_path):
            try:
                os.makedirs(self._project_build_style_path)
            except:
                raise CreateFolderError('Could not create the style folder.')

        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the existing images folder.')

        try:
            copytree(source, dest)
        except:
            raise FileNotWritableError('Could not copy all the images in the image folder.')

    def _build_libraries(self):
        source = os.path.join(self._cwd, 'src', 'lib')
        dest = os.path.join(self._config['build_path'], 'lib')

        if not os.path.exists(source):
            return

        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the existing libraries folder.')

        try:
            copytree(source, dest)
        except:
            raise FileNotWritableError('Could not copy all the libraries.')


def clean():
    if not os.path.exists(os.path.join(os.getcwd(), 'build')):
        return

    try:
        rmtree(os.path.join(os.getcwd(), 'build'))
    except:
        raise RemoveFolderError('Could not remove the build folder.')
