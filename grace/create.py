from error import FileNotWritableError, FolderAlreadyExistsError, FolderNotFoundError, CreateFolderError
import os
from shutil import copytree
import sys
import re
from pkg_resources import resource_filename


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


class New:
    def __init__(self, projectName, plugin=None, type='default'):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()
        self._plugin = plugin
        self._type = type

        if plugin:
            try:
                self._skeleton_path = plugin.skeleton_path()
            except NotImplementedError:
                try:
                    self._skeleton_path = resource_filename(__name__, os.path.join('skeleton', 'default'))
                except NotImplementedError:
                    self._skeleton_path = os.path.join(sys.prefix, 'skeleton', 'default')
        else:
            try:
                self._skeleton_path = resource_filename(__name__, os.path.join('skeleton', 'default'))
            except NotImplementedError:
                self._skeleton_path = os.path.join(sys.prefix, 'skeleton', 'default')

        self._projectPath = os.path.join(self._cwd, self._projectName)
        self._deployment_path = os.path.join(os.path.expanduser('~'))
        self._zip_path = os.path.join(os.path.expanduser('~'))
        self._doc_path = os.path.join(os.path.expanduser('~'))

        if sys.platform.startswith('win32'):
            self._deployment_path = self._deployment_path.replace('\\', '\\\\')
            self._zip_path = self._zip_path.replace('\\', '\\\\')

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

        if not os.path.exists(self._skeleton_path):
            raise FolderNotFoundError('Could not find the skeleton: ', self._skeleton_path)

        try:
            copytree(self._skeleton_path, os.path.join(self._cwd, self._projectName))
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
        with open(os.path.join(p, outfilename), 'w+') as out:
            infile = open(os.path.join(p, f))
            for line in infile:
                newline = line.replace('#DEPLOYMENTPATH', self._deployment_path)
                newline = newline.replace('#ZIPPATH', self._zip_path)
                newline = newline.replace('#PROJECTNAME', self._projectName)
                newline = newline.replace('#DOCPATH', self._doc_path)

                if self._plugin:
                    try:
                        newline = self._plugin.new_replace_line(newline)
                    except AttributeError:
                        pass

                out.write(newline)

            infile.close()

        try:
            os.remove(os.path.join(p, f))
        except:
            raise FileNotWritableError('Could not delete the initial replace file.')
