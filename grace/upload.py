import os
from utils import get_path
from error import MissingKeyError
from pkg_resources import resource_filename


class Upload:
    def __init__(self, global_config, config):
        self._cwd = os.getcwd()
        self._root = get_path()
        self._config = config
        self._global_config = global_config

        if 'upload_url' not in self._config:
            if 'upload_url' not in self._global_config:
                raise MissingKeyError('Could not find an upload url in either the global or local configuration file.')

    def upload_project(self):

