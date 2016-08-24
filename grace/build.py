from __future__ import absolute_import
from builtins import object
import os
from .error import FileNotFoundError, CreateFolderError, FileNotWritableError, FileNotReadableError, RemoveFolderError, RemoveFileError, ScssError, ParseError
from shutil import copy2, copytree, rmtree
from grace.py27.slimit import minify
from grace.py27.cssmin import cssmin
from execjs import ProgramError
import re
import scss
import sys
import tempfile
import coffeescript
import traceback


class Build(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def run(self):
        if os.path.exists(self._config['build_path']):
            try:
                rmtree(self._config['build_path'])
            except:
                raise RemoveFolderError('Could not remove existing build directory.')

        try:
            os.makedirs(self._config['build_path'])
        except:
            raise CreateFolderError('Could not create the project folder.')

        try:
            self._build_javascript()
            self._build_style()
            self._build_html()
            self._build_libraries()
            self._copy_assets()
        except:
            raise

    def _build_javascript(self):
        js_name = self._config['js_name'] + '.js'
        source = os.path.join(self._cwd, 'src', js_name)
        dest = os.path.join(self._config['build_path'], js_name)
        js_string = ''

        if not os.path.exists(source):
            source = os.path.join(self._cwd, 'src', 'application.js')
            if not os.path.exists(source):
                source = os.path.join(self._cwd, 'src', 'application.coffee')
                if not os.path.exists(source):
                    return

        if source.endswith('coffee'):
            as_coffee = True
        else:
            as_coffee = False

        try:
            f = open(source)
            self._included_files = []

            js_string = self._gather_javascript(f, as_coffee)
        except:
            raise
        # except FileNotFoundError:
        #     raise
        # except ParseError:
        #     raise
        # except:
        #     raise FileNotFoundError('The specified file does not exist: ', source)
        finally:
            f.close()

        try:
            f = open(dest, 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript file.')

        if self._config['minify_js']:
            js_string = minify(js_string, mangle=True, mangle_toplevel=False)

        f.write(js_string)
        f.close()

    def _concat_javascript(self, source, as_coffee=False):
        f = None
        js_string = ''

        try:
            f = open(source)
        except:
            raise FileNotFoundError('The specified file does not exist: ', source)

        self._included_files = []
        try:
            js_string = self._gather_javascript(f)
        except FileNotFoundError:
            raise
        finally:
            f.close()

        return js_string

    def _gather_javascript(self, f, as_coffee=False):
        lines = []
        include_string = ''
        index = 0
        js_string = ''

        for line in f:
            line = line.replace('##BUILDVERSION##', self._config['version'])

            if as_coffee:
                match = re.match('#= require ([a-zA-Z\/-_]+)', line)
            else:
                match = re.match('\/\/= require ([a-zA-Z\/-_]+)', line)

            if match:
                include_f = None
                include_path = match.group(1)
                files_dir = os.path.join(self._cwd, 'src', 'javascript')
                if not os.path.exists(files_dir):
                    files_dir = os.path.join(self._cwd, 'src', 'coffeescript')
                    if not os.path.exists(files_dir):
                        raise FileNotFoundError('There is not javascript or coffeescript folder present in the src director.')

                if sys.platform.startswith('win32'):
                    include_path = include_path.replace('/', '\\')
                include_path = os.path.join(files_dir, include_path)

                if os.path.exists(include_path + '.js'):
                    include_path = include_path + '.js'
                    include_as_coffee = False
                elif os.path.exists(include_path + '.coffee'):
                    include_path = include_path + '.coffee'
                    include_as_coffee = True
                else:
                    raise FileNotFoundError('The specified file does not exist (as either .js or .coffee): ', include_path)

                if include_path not in self._included_files:
                    self._included_files.append(include_path)

                    include_f = open(include_path)

                    try:
                        include_string = include_string + self._gather_javascript(include_f, include_as_coffee)
                        index += 1
                    except FileNotFoundError:
                        raise
                    finally:
                        include_f.close()
            else:
                lines.append(line)

        js_string = ''.join(lines)
        if as_coffee:
            try:
                js_string = coffeescript.compile(js_string)
            except ProgramError as e:
                filename = f.name.replace(self._cwd, '')[1:]
                msg = ''.join(map(str, e.args)).replace('stdin', filename)

                raise ParseError('Error while parsing CoffeeScript\n' + msg)

        return include_string + js_string

    def _build_html(self):
        source = os.path.join(self._cwd, 'src', 'index.html')
        dest = os.path.join(self._config['build_path'], 'index.html')

        if not os.path.exists(source):
            return

        try:
            copy2(source, dest)
        except:
            raise FileNotWritableError('Could not write the html file.')

    def _build_style(self):
        source = os.path.join(self._cwd, 'src', 'style')
        destination = os.path.join(self._config['build_path'], 'style')

        if not os.path.exists(source):
            return

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

                    namespace = scss.namespace.Namespace()

                    @namespace.declare_alias('dashboard-region')
                    def dashboard():
                        return scss.types.Function(u'control rectangle', u'dashboard-region', quotes=None)

                    @namespace.declare_alias('dashboard-region')
                    def dashboard(val):
                        return scss.types.Function(val.render(), u'dashboard-region', quotes=None)

                    compiler = scss.compiler.Compiler(namespace=namespace)

                    scss_filename = os.path.join(root, f)
                    css_filename = os.path.join(root, f[:-4] + 'css')

                    try:
                        css_string = compiler.compile(scss_filename)
                    except (scss.errors.SassEvaluationError, scss.errors.SassSyntaxError, scss.errors.SassParseError) as e:
                        raise ScssError(traceback.format_exc(0))
                    except scss.errors.SassError as e:
                        elist = traceback.format_exception_only(type(e), e)
                        raise ScssError(''.join(elist))
                    except:
                        raise FileNotFoundError('Could not compile your scss style file.')

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

        try:
            copytree(source, dest)
        except:
            raise FileNotWritableError('Could not copy all the libraries.')

    def _copy_assets(self):
        source = os.path.join(self._cwd, 'assets')
        dest = os.path.join(self._config['build_path'], 'assets')

        if not os.path.exists(source):
            return;

        try:
            copytree(source, dest)
        except:
            raise FileNotWritableError('Could not copy all the asset files.')


def clean():
    if not os.path.exists(os.path.join(os.getcwd(), 'build')):
        return

    try:
        rmtree(os.path.join(os.getcwd(), 'build'))
    except:
        raise RemoveFolderError('Could not remove the build folder.')
