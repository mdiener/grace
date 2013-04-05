import os
from error import FileNotFoundError, CreateFolderError, RemoveFolderError, FileNotWritableError, RemoveFileError
import re
from shutil import rmtree, copy2, copytree


class Test:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def _clean_previous_tests(self):
        if os.path.exists(self._config['test_build_path']):
            try:
                rmtree(self._config['test_build_path'])
            except:
                raise RemoveFolderError('Could not delete the test folder.')

        try:
            os.makedirs(self._config['test_build_path'])
        except:
            raise CreateFolderError('Could not create the test folder.')

    def build_test(self):
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

        if self._config['testname']:
            try:
                self._js_string_lines += self._concat_javascript(self._config['testname'] + '.js')
            except:
                raise
        else:
            path = os.path.join(self._cwd, 'test', 'javascript')
            files = os.listdir(path)

            for f in files:
                if os.path.isfile(os.path.join(path, f)):
                    try:
                        self._js_string_lines += self._concat_javascript(f)
                    except:
                        raise

        try:
            f = open(os.path.join(self._config['test_build_path'], 'test.js'), 'w+')
        except:
            raise FileNotWritableError('Could not write the javascript file.')

        self._js_string = ''.join(self._js_string_lines)
        f.write(self._js_string)
        f.close()

    def _concat_javascript(self, test):
        f = None
        lines = []

        try:
            f = open(os.path.join(self._cwd, 'test', 'javascript', test))
        except:
            raise FileNotFoundError('The specified file does not exist: ', os.path.join(self._cwd, 'test', 'javascript', test))

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

                sub_path = os.path.join(self._cwd, 'src', 'javascript', re.split(' ', line)[1])
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
        source = os.path.join(self._cwd, 'test', 'index.html')
        dest = os.path.join(self._config['test_build_path'], 'index.html')
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

    def _build_libraries(self):
        source = os.path.join(self._cwd, 'test', 'lib')
        dest = os.path.join(self._config['test_build_path'], 'lib')

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
