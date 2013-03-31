import os
from error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError
import json


class Build:
    def __init__(self):
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

        try:
            os.makedirs(self._cwd + '/build')
        except:
            raise CreateFolderError('Could not create the build folder.')
