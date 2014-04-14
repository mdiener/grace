from error import FileNotWritableError, RemoveFileError, MissingKeyError
import os
import zipfile


class Zip:
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

    def zip_project(self, testname):
        if self._config['test']:
            if testname is None:
                print 'No tests to build.'
                return

            name = os.path.join(self._config['name'] + '_' + testname)
            source = os.path.join(self._cwd, 'build', self._config['name'] + '_' + testname)
        elif self._config['build']:
            name = self._config['name']
            source = self._config['build_path']
        else:
            raise MissingKeyError('It seems you are trying to zip a project but neither build nor test were specified. I am sorry but I do not know what to do now.')

        try:
            self._zip(name, source, os.path.join(self._cwd, 'build', name + '_v' + self._config['version'] + '.zip'))

            if 'zip_path' in self._config:
                self._zip(name, source, os.path.join(self._config['zip_path'], name + '_v' + self._config['version'] + '.zip'))
        except:
            raise

    def _zip(self, name, source, dest):
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
