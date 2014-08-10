import os
from error import FileNotFoundError, CreateFolderError, FileNotWritableError, FileNotReadableError, RemoveFolderError, RemoveFileError, SassError
from shutil import copy2, copytree, rmtree
from slimit import minify
from cssmin import cssmin
import re
import sass
import sys
import tempfile


class Build:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def build_project(self):
        if not os.path.exists(self._config['build_path']):
            try:
                os.makedirs(self._config['build_path'])
            except:
                raise CreateFolderError('Could not create the project folder.')

        try:
            self._build_javascript()
            self._build_style()
            self._build_html()
            self._build_libraries()
        except:
            raise

    def _build_javascript(self):
        js_name = self._config['js_name'] + '.js'
        source = os.path.join(self._cwd, 'src', js_name)
        dest = os.path.join(self._config['build_path'], js_name)

        if not os.path.exists(source):
            source = os.path.join(self._cwd, 'src', 'application.js')
            if not os.path.exists(source):
                return

        try:
            self._js_string = self._concat_javascript(source)
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
            self._js_string = minify(self._js_string, mangle=True, mangle_toplevel=True)

        f.write(self._js_string.encode('utf-8'))
        f.close()

    def _concat_javascript(self, source):
        f = None
        lines = []

        try:
            f = open(source)
        except:
            raise FileNotFoundError('The specified file does not exist: ', source)

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
            line = line.decode('utf-8')
            line = line.replace('##BUILDVERSION##', self._config['version'])

            match = re.match('\/\/= require ([a-zA-Z\/-_]+)', line)
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

        lines.append('\n')
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

    def _build_style(self):
        source = os.path.join(self._cwd, 'src', 'style')
        destination = os.path.join(self._config['build_path'], 'style')

        if not os.path.exists(source):
            return

        if os.path.exists(destination):
            try:
                rmtree(destination)
            except:
                raise RemoveFolderError('Could not remove the existing style folder.')

        temp_style_dir = tempfile.mkdtemp()

        try:
            copytree(source, os.path.join(temp_style_dir, 'style'))
        except:
            raise CreateFolderError('Could not copy your style folder to a temporary location.')

        self._work_css_files(os.path.join(temp_style_dir, 'style'))

        try:
            copytree(os.path.join(temp_style_dir, 'style'), destination)
        except:
            CreateFolderError('Could not copy the style folder from the temporary location.')

        try:
            rmtree(temp_style_dir)
        except:
            RemoveFolderError('Could not remove your temporary style folder.')

    def _work_css_files(self, folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f.endswith('.scss'):
                    scss_filename = os.path.join(root, f)
                    css_filename = os.path.join(root, f[:-4] + 'css')

                    try:
                        css_string = sass.compile(filename=scss_filename)
                    except sass.CompileError as e:
                        raise SassError('Could not compile your scss file:\n', e.message[:-1])
                    except:
                        raise FileNotFoundError('Could not find your scss style file.')

                    try:
                        css_file = open(css_filename, 'w+')
                    except:
                        raise FileNotWritableError('Could not write the new css file:\n' + css_filename)

                    if self._config['minify_css']:
                        css_string = cssmin(css_string)

                    css_file.write(css_string)
                    css_file.close();

                    try:
                        os.remove(scss_filename)
                    except:
                        raise FileNotWritableError('Could not remove already converted scss file:\n' + scss_filename)
                elif f.endswith('.css'):
                    if self._config['minify_css']:
                        css_filename = os.path.join(root, f)

                        try:
                            css_file = open(f, 'r')
                        except:
                            raise FileNotReadableError('Could not read your css file:\n' + css_filename)

                        css_string = f.read()
                        css_file.close()

                        try:
                            os.remove(css_file)
                        except:
                            raise FileNotWritableError('Could not remove your non-minified css file:\n' + css_filename)

                        try:
                            css_file = open(css_filename, 'w+')
                        except:
                            FileNotWritableError('Could not write to the new minified css file:\n' + css_filename)

                        css_string = cssmin(css_string)
                        css_file.write(css_string)
                        css_file.close()

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
