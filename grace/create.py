from error import FileNotWritableError, FolderAlreadyExistsError, FolderNotFoundError, CreateFolderError, FileNotFoundError, GeneralError
import os
from shutil import copytree, copy, rmtree
import sys
import re
from pkg_resources import resource_filename
from utils import get_path
import requests
import tempfile
import zipfile


class Assets(object):
    def __init__(self, projectName):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()

        try:
            self._assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', 'manage.py')))
        except NotImplementedError:
            self._assetPath = os.path.join(sys.prefix, 'assets', 'manage.py')

        self._projectPath = os.path.join(self._cwd, self._projectName)

        self._copy_assets()

    def _copy_assets(self):
        if not os.path.exists(self._assetPath):
            raise FileNotFoundError('Could not find the manage.py asset.')

        try:
            copy(self._assetPath, os.path.join(self._cwd, self._projectName))
        except:
            raise FileNotWritableError('Could not create the manage.py file.')


class New(object):
    def __init__(self, projectName, skeleton):
        self._projectName = projectName
        self._root = get_path()
        self._cwd = os.getcwd()

        if skeleton == 'default':
            self._skeleton_url = 'https://github.com/mdiener/grace-skeleton/archive/default.zip'

        self._download_skeleton()

        self._projectPath = os.path.join(self._cwd, self._projectName)

        self._copy_structure()
        self._replace_strings()

        try:
            rmtree(self._tmp_path)
        except:
            pass

    def _download_skeleton(self):
        self._tmp_path = tempfile.mkdtemp()
        zip_path = os.path.join(self._tmp_path, 'skeleton.zip')

        r = requests.get(self._skeleton_url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

        try:
            z = zipfile.ZipFile(zip_path, 'r')
            z.extractall(self._tmp_path)
        except:
            raise GeneralError('Could not unzip the downloaded file. Something went wrong, please try again.')

        self._skeleton_path = os.path.join(self._tmp_path, z.namelist()[0])
        z.close()

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
                newline = line.replace('##PROJECTNAME##', self._projectName)
                newline = newline.replace('##PROJECTNAME_TOLOWER##', self._projectName.lower())

                out.write(newline)

            infile.close()

        try:
            os.remove(os.path.join(p, f))
        except:
            raise FileNotWritableError('Could not delete the initial replace file.')
