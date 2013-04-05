from error import MissingKeyError, RemoveFolderError, FileNotWritableError
import os
from shutil import rmtree
import distutils.core


class Deploy:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def deploy_project(self):
        if 'deployment_path' not in self._config:
            raise MissingKeyError('Could not find deployment path in config file.')

        if self._config['test']:
            test_deployment_path = os.path.join(self._config['deployment_path'], self._config['name'] + '_test')
            self._deploy(test_deployment_path, self._config['test_build_path'])

        if self._config['build']:
            build_deployment_path = os.path.join(self._config['deployment_path'], self._config['name'])
            self._deploy(build_deployment_path, self._config['build_path'])

    def _deploy(self, deployment_path, build_path):
        if os.path.exists(deployment_path):
            try:
                rmtree(deployment_path)
            except:
                raise RemoveFolderError('Could not remove the existing deployment path.')

        try:
            distutils.dir_util.copy_tree(build_path, deployment_path)
        except:
            raise FileNotWritableError('Could not copy the build directory to the deployment path.')
