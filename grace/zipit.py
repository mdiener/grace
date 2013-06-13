from error import FileNotWritableError, RemoveFileError
import os
import zipfile


class Zip:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def zip_project(self):
        if self._config['test']:
            name = self._config['name'] + '_test'
            source = self._config['test_build_path']

            try:
                self._zip(source, name)
            except:
                raise

        if self._config['build']:
            name = self._config['name']
            source = self._config['build_path']

            try:
                self._zip(source, name)
            except:
                raise

    def _zip(self, source, name):
        try:
            dest = os.path.join(self._config['zip_path'], name + '_v' + self._config['version'] + '.zip')
        except:
            dest = os.path.join(self._cwd, 'build', name + '_v' + self._config['version'] + '.zip')

        try:
            self._cleanup(dest)
        except:
            raise

        try:
            z = zipfile.ZipFile(dest, 'a')
        except:
            raise

        for root, dirs, files in os.walk(source):
            for f in files:
                tmpfilename = os.path.join(root, f).split(source)[1][1:]
                zipfilename = os.path.join(name, tmpfilename)
                try:
                    z.write(os.path.join(root, f), zipfilename)
                except:
                    raise FileNotWritableError('Could not write to the zip file.')

        z.close()

    def _cleanup(self, path):

        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                raise RemoveFileError('Could not remove the zip file in build directory.')
