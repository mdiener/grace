from error import FileNotFoundError, WrongFormatError, MissingKeyError, RemoveFolderError, FileNotWritableError
import json
import os
from shutil import rmtree
import distutils.core


class Deploy:
    def __init__(self, with_dizmo, as_test):
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

        if as_test:
            self._config['name'] = self._config['name'] + '_test'

        if 'deployment_path' not in self._config:
            raise MissingKeyError('Could not find deployment path in config file.')

        self._build_path = self._cwd + '/build/' + self._config['name']

        if self._with_dizmo:
            try:
                dizmo_config_file = open(self._cwd + '/dizmo_config.json')
            except:
                raise FileNotFoundError('Could not find a dizmo config file in this directory.')

            try:
                self._dizmo_config = json.load(dizmo_config_file)
            except:
                raise WrongFormatError('The provided config file could not be parsed.')

            if 'bundle' not in self._dizmo_config:
                raise MissingKeyError('Bundle is missing in dizmo config file.')

            self._deployment_path = self._config['deployment_path'] + '/' + self._dizmo_config['bundle'] + '.' + self._config['name']
        else:
            self._deployment_path = self._config['deployment_path'] + '/' + self._config['name']

    def deploy_project(self):
        if os.path.exists(self._deployment_path):
            try:
                rmtree(self._deployment_path)
            except:
                raise RemoveFolderError('Could not remove the existing deployment path.')

        try:
            distutils.dir_util.copy_tree(self._build_path, self._deployment_path)
        except:
            raise FileNotWritableError('Could not copy the build directory to the deployment path.')
