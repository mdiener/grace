from error import FileNotFoundError, FolderAlreadyExistsError, CreateFolderError, FileNotWritableError
import os
from sys import exit
from shutil import copy
import sys


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


class New:
    def __init__(self, projectName):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()
        self._files = Files(projectName, self._root, self._cwd)
        self._structure = Structure(projectName, self._cwd)

        try:
            self._structure.create()
        except CreateFolderError as e:
            print e.msg
            exit()

        try:
            self._files.write()
        except FileNotWritableError as e:
            print e.msg
            exit()


class Structure:
    def __init__(self, projectName, cwd):
        self._projectName = projectName
        self._cwd = cwd

    def create(self):
        projectPath = self._cwd + '/' + self._projectName
        if os.path.exists(projectPath):
            raise FolderAlreadyExistsError('The folder for this project already exists.')

        try:
            os.makedirs(projectPath)
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath)

        try:
            os.makedirs(projectPath + '/src')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src')

        try:
            os.makedirs(projectPath + '/src/lib')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/lib')

        try:
            os.makedirs(projectPath + '/src/lib/jquery')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/lib/jquery')

        try:
            os.makedirs(projectPath + '/src/lib/joose')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/lib/joose')

        try:
            os.makedirs(projectPath + '/src/style')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/style')

        try:
            os.makedirs(projectPath + '/src/style/images')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/images')

        try:
            os.makedirs(projectPath + '/src/javascript')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/src/javascript')

        try:
            os.makedirs(projectPath + '/test')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test')

        try:
            os.makedirs(projectPath + '/test/lib')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test/lib')

        try:
            os.makedirs(projectPath + '/test/lib/jquery')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test/lib/jquery')

        try:
            os.makedirs(projectPath + '/test/lib/joose')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test/lib/joose')

        try:
            os.makedirs(projectPath + '/test/lib/qunit')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test/lib/qunit')

        try:
            os.makedirs(projectPath + '/test/javascript')
        except:
            raise CreateFolderError('Could not create the folder: ', projectPath + '/test/javascript')


class Files:
    def __init__(self, projectName, root, cwd):
        self._projectName = projectName
        self._root = root
        self._cwd = cwd

        try:
            self._load_string()
        except FileNotFoundError as e:
            print e.msg
            exit()

        self._prepare_write_arrays()

    def _load_string(self):
        try:
            _jsfile = open(self._root + '/files/application.js')
        except:
            raise FileNotFoundError('Could not find the main javascript file.')

        try:
            _htmlfile = open(self._root + '/files/main.html')
        except:
            raise FileNotFoundError('Could not find the html source file.')

        try:
            _testhtmlfile = open(self._root + '/files/test.html')
        except:
            raise FileNotFoundError('Could not find the test html source file.')

        try:
            _configfile = open(self._root + '/files/config.json')
        except:
            raise FileNotFoundError('Could not find the config source file.')

        self._js_string = self._parse(_jsfile)
        self._html_string = self._parse(_htmlfile)
        self._test_html_string = self._parse(_testhtmlfile)
        self._config_string = self._parse(_configfile)

        _jsfile.close()
        _htmlfile.close()
        _testhtmlfile.close()
        _configfile.close()

    def _parse(self, f):
        lines = []

        for line in f:
            lines.append(line.replace('#PROJECTNAME', self._projectName))

        return ''.join(lines)

    def _prepare_write_arrays(self):
        projectPath = self._cwd + '/' + self._projectName

        self._string = [{
            'path': projectPath + '/src/application.js',
            'content': self._js_string
        }, {
            'path': projectPath + '/src/index.html',
            'content': self._html_string
        }, {
            'path': projectPath + '/test/index.html',
            'content': self._test_html_string
        }, {
            'path': projectPath + '/config.json',
            'content': self._config_string
        }]

        self._copy = [{
            'source': self._root + '/files/jquery.min.js',
            'dest': projectPath + '/src/lib/jquery/jquery.min.js'
        }, {
            'source': self._root + '/files/jquery.js',
            'dest': projectPath + '/test/lib/jquery/jquery.js'
        }, {
            'source': self._root + '/files/qunit.js',
            'dest': projectPath + '/test/lib/qunit/qunit.js'
        }, {
            'source': self._root + '/files/qunit.css',
            'dest': projectPath + '/test/lib/qunit/qunit.css'
        }, {
            'source': self._root + '/files/joose.min.js',
            'dest': projectPath + '/src/lib/joose/joose.min.js'
        }, {
            'source': self._root + '/files/joose.js',
            'dest': projectPath + '/test/lib/joose/joose.js'
        }, {
            'source': self._root + '/files/style.scss',
            'dest': projectPath + '/src/style/style.scss'
        }]

    def write(self):
        for entry in self._string:
            try:
                f = open(entry['path'], 'w+')
            except:
                raise FileNotWritableError('Could not write to file location: ', entry['path'])

            f.write(entry['content'])

        for entry in self._copy:
            try:
                copy(entry['source'], entry['dest'])
            except:
                raise FileNotWritableError('Could not write to file location: ', entry['dest'])
