from error import FileNotFoundError, WrongFormatError, MissingKeyError, FileNotWritableError, RemoveFolderError, RemoveFileError
import json
import os
import zipfile
import re


class Zip:
    def __init__(self, with_dizmo):
        self._with_dizmo = with_dizmo
        self._cwd = os.getcwd()

        try:
            config_file = open(self._cwd + '/config.json')
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        try:
            self._config = json.load(config_file)
        except:
            raise WrongFormatError('The provided config file could not be parsed.')

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')

        self._build_path = self._cwd + '/build/' + self._config['name']

        self._zip_path = None
        if 'zip_path' in self._config:
            self._zip_path = self._config['zip_path']

    def zip_project(self):
        try:
            self._cleanup()
        except:
            raise

        try:
            if self._with_dizmo:
                z = zipfile.ZipFile(self._cwd + '/build/' + self._config['name'] + '.dizmo', 'a')
            else:
                z = zipfile.ZipFile(self._cwd + '/build/' + self._config['name'] + '.zip', 'a')
        except:
            raise

        for root, dirs, files in os.walk(self._build_path):
            for f in files:
                try:
                    z.write(os.path.join(root, f), self._config['name'] + '/' + re.split(self._build_path, os.path.join(root, f))[1])
                except:
                    raise FileNotWritableError('Could not write to the zip file.')

        z.close()

    def _cleanup(self):
        path_zip = None

        if self._with_dizmo:
            path = self._cwd + '/build/' + self._config['name'] + '.dizmo'
            if self._zip_path:
                path_zip = self._zip_path + '/' + self._config['name'] + '.dizmo'
        else:
            path = self._cwd + '/build/' + self._config['name'] + '.zip'
            if self._zip_path:
                path_zip = self._zip_path + '/' + self._config['name'] + '.zip'

        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                raise RemoveFileError('Could not remove the zip file in build directory.')

        if path_zip:
            if os.path.exists(path_zip):
                try:
                    os.remove(path_zip)
                except:
                    raise RemoveFileError('Could not remove the zip file from the zip path.')
