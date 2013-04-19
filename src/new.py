from error import FileNotWritableError, FolderAlreadyExistsError, FolderNotFoundError, CreateFolderError
import os
from shutil import copytree
import sys
import re


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


class New:
    def __init__(self, projectName, newtype='default'):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()
        self._type = newtype

        self._projectPath = os.path.join(self._cwd, self._projectName)

        try:
            self._copy_structure()
        except:
            raise

        try:
            self._replace_strings()
        except:
            raise

    def _copy_structure(self):
        if os.path.exists(os.path.join(self._cwd, self._projectName)):
            raise FolderAlreadyExistsError('There is already a folder with the projectname present!')

        if not os.path.exists(os.path.join(self._root, 'skeletons', self._type)):
            raise FolderNotFoundError('Could not find the skeleton: ', self._type)

        try:
            copytree(os.path.join(self._root, 'skeletons', self._type), os.path.join(self._cwd, self._projectName))
        except:
            raise CreateFolderError('Could not create the folders for the new project.')

    def _replace_strings(self):
        file_list = []
        for path, dirs, files in os.walk(self._projectPath):
            for f in files:
                file_list.append({
                    'file': f,
                    'path': path
                })

        for entry in file_list:
            if re.search('_X.', entry['file']):
                try:
                    self._replace(entry)
                except:
                    raise

    def _replace(self, fileObject):
        f = fileObject['file']
        p = fileObject['path']

        outfilename = f.replace('_X', '')
        with open(os.path.join(p, outfilename), 'wr') as out:
            infile = open(os.path.join(p, f))
            for line in infile:
                newline = line.replace('#DEPLOYMENTPATH', os.path.join(os.path.expanduser('~'), '.local', 'share', 'data', 'futureLAB', 'dizmode', 'InstalledWidgets'))
                newline = newline.replace('#ZIPPATH', os.path.join(os.path.expanduser('~'), 'Documents', 'dizmos'))
                newline = newline.replace('#PROJECTNAME', self._projectName)

                out.write(newline)

            infile.close()

        try:
            os.remove(os.path.join(p, f))
        except:
            raise FileNotWritableError('Could not delete the initial replace file.')
