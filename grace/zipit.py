from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from .error import FileNotWritableError, RemoveFileError, MissingKeyError
import os
import zipfile


class Zip(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

        if 'zip_path' not in self._config:
            self._zip_path = None
        else:
            self._zip_path = os.path.join(self._config['zip_path'])

        if 'zip_name' not in self._config:
            self._zip_name = self._config['name'] + '-' + self._config['version'] + '.zip'
        else:
            self._zip_name = self._config['zip_name']

    def run(self, testname):
        if self._config['test']:
            if testname is None:
                print('No tests to build.')
                return

            name = self._config['name'] + '_' + testname
            source = os.path.join(self._cwd, 'build', self._config['name'] + '_' + testname)
            zip_name = testname + '_' + self._zip_name
        elif self._config['build']:
            name = self._config['name']
            source = self._config['build_path']
            zip_name = self._zip_name
        else:
            raise MissingKeyError('It seems you are trying to zip a project but neither build nor test were specified. I am sorry but I do not know what to do now.')

        try:
            self._zip(name, source, os.path.join(self._cwd, 'build', zip_name))

            if self._zip_path is not None:
                self._zip(name, source, os.path.join(self._zip_path, zip_name))
        except:
            raise

    def _zip(self, name, source, dest):
        try:
            self._cleanup(dest)
        except:
            raise

        try:
            z = zipfile.ZipFile(dest, 'a', zipfile.ZIP_DEFLATED)
        except RuntimeError as e:
            z = zipfile.ZipFile(dest, 'a')

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
