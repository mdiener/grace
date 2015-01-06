from error import MissingKeyError, RemoveFolderError, FolderNotWritableError
import os
from shutil import rmtree, copytree


class Deploy(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

        if 'deployment_path' not in self._config:
            raise MissingKeyError('Could not find deployment path in config file.')
        else:
            self._deployment_path = self._config['deployment_path']

    def run(self, testname):
        if self._config['test']:
            if testname is None:
                print 'No tests to build.'
                return

            dest = os.path.join(self._deployment_path, self._config['name'] + '_' + testname)
            source = os.path.join(self._cwd, 'build', self._config['name'] + '_' + testname)
        elif self._config['build']:
            dest = os.path.join(self._deployment_path, self._config['name'])
            source = os.path.join(self._cwd, 'build', self._config['name'])
        else:
            raise MissingKeyError('It seems you are trying to deploy a project but neither build nor test were specified. I am sorry but I do not know what to do now.')

        self._deploy(source, dest)

    def _deploy(self, source, dest):
        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the existing deployment path.')

        try:
            copytree(source, dest)
        except:
            raise FolderNotWritableError('Could not copy the build directory to the deployment path.')
