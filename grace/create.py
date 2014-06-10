from error import FileNotWritableError, FolderAlreadyExistsError, FolderNotFoundError, CreateFolderError, FileNotFoundError
import os
from shutil import copytree, copy
import sys
import re
from pkg_resources import resource_filename
from utils import get_path


class New:
    def __init__(self, projectName, pluginName='default'):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()
        self._type = pluginName

        if pluginName != 'default':
            module = __import__('grace-' + pluginName + '.plugin')
            try:
                plugin = getattr(module.plugin, self._type.title())()
            except:
                raise
        else:
            plugin = None

        self._plugin = plugin

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

        try:
            self._assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', 'manage.py')))
        except NotImplementedError:
            self._assetPath = os.path.join(sys.prefix, 'assets', 'manage.py')

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

        if not os.path.exists(self._assetPath):
            raise FileNotFoundError('Could not find the manage.py asset.')

        try:
            copytree(self._skeleton_path, os.path.join(self._cwd, self._projectName))
        except:
            raise CreateFolderError('Could not create the folders for the new project.')

        try:
            copy(self._assetPath, os.path.join(self._cwd, self._projectName))
        except:
            raise FileNotWritableError('Could not create the manage.py file.')

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
                newline = line.replace('##DEPLOYMENTPATH##', self._deployment_path)
                newline = newline.replace('##ZIPPATH##', self._zip_path)
                newline = newline.replace('##PROJECTNAME##', self._projectName)
                newline = newline.replace('##PROJECTNAME_TOLOWER##', self._projectName.lower())
                newline = newline.replace('##DOCPATH##', self._doc_path)

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
