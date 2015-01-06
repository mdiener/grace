import os
from error import FileNotFoundError, CreateFolderError, RemoveFolderError, FileNotWritableError, RemoveFileError
import re
from shutil import rmtree, copy2, copytree
import sys


class Test(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def run(self, testname):
        if testname is None:
            print 'No tests to build.'
            return

        build_path = os.path.join(self._cwd, 'build', self._config['name'] + '_' + testname)
        js_source_path = os.path.join(self._cwd, 'test', 'tests', 'test_' + testname + '.js')

        try:
            self._clean_previous_tests(build_path)
            self._build_javascript(build_path, js_source_path)
            self._build_libraries(build_path)
            self._build_html(build_path)
            self._copy_assets(build_path)
        except:
            raise

    def _clean_previous_tests(self, build_path):
        if os.path.exists(build_path):
            try:
                rmtree(build_path)
            except:
                raise RemoveFolderError('Could not delete the test folder: ' + build_path)

        try:
            os.makedirs(build_path)
        except:
            raise CreateFolderError('Could not create the test folder: ' + build_path)

    def _build_javascript(self, build_path, js_source_path):
        self._js_string_lines = []

        dest = os.path.join(build_path, 'test.js')
        js_string_lines = self._concat_javascript(js_source_path)

        if os.path.exists(dest):
            try:
                os.remove(dest)
            except:
                raise RemoveFileError('Could not delete the existing javascript test file.')


        try:
            f = open(dest, 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript test file.')

        js_string = ''.join(js_string_lines)
        f.write(js_string)
        f.close()

    def _concat_javascript(self, js_source_path):
        f = None
        lines = []

        try:
            f = open(js_source_path)
        except:
            raise FileNotFoundError('The specified file does not exist: ', js_source_path)

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
            match = re.match('\/\/= require ([a-zA-Z\/-_]+)', line)
            if match:
                sub_f = None

                path = match.group(1)
                if sys.platform.startswith('win32'):
                    path = path.replace('/', '\\')

                sub_path = os.path.join(self._cwd, 'test', 'javascript', path + '.js')
                if not os.path.exists(sub_path):
                    sub_path = os.path.join(self._cwd, 'src', 'javascript', path + '.js')

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

    def _build_html(self, build_path):
        source = os.path.join(self._cwd, 'test', 'index.html')
        dest = os.path.join(build_path, 'index.html')
        if not os.path.exists(source):
            return

        if os.path.exists(dest):
            try:
                os.remove(dest)
            except:
                raise RemoveFileError('Could not remove the existing html test file.')

        try:
            copy2(source, dest)
        except:
            raise FileNotWritableError('Could not write the html file.')

    def _build_libraries(self, build_path):
        source = os.path.join(self._cwd, 'test', 'lib')
        dest = os.path.join(build_path, 'lib')

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

    def _copy_assets(self, build_path):
        source = os.path.join(self._cwd, 'assets')
        dest = os.path.join(build_path, 'assets')

        if not os.path.exists(source):
            return

        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the existing assets folder.')

        try:
            copytree(source, dest)
        except:
            raise FileNotWritableError('Could not copy all asset files')
