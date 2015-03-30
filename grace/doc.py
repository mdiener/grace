from error import CreateFolderError, FileNotWritableError, RemoveFolderError
import pyjsdoc
import os
from shutil import rmtree


class Doc(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._config = config

        if 'doc_path' not in self._config:
            self._doc_path = None
        else:
            self._doc_path = os.path.join(self._config['doc_path'], self._config['name'])

        self._lib_path = os.path.join(self._cwd, 'src', 'lib')

    def run(self, with_libs=False):
        source = os.path.join(self._cwd, 'src', 'javascript')
        dest = os.path.join(self._cwd, 'build', 'JSDocs')

        if not os.path.exists(self._config['build_path']):
            try:
                os.makedirs(self._config['build_path'])
            except:
                raise CreateFolderError('Could not create the project folder.')

        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the JSDoc folder.')

        try:
            os.makedirs(dest)
        except:
            raise CreateFolderError('Could not create the doc folder in your build directory.')

        if with_libs:
            jsdoc = pyjsdoc.CodeBaseDoc([source, self._lib_path])
        else:
            jsdoc = pyjsdoc.CodeBaseDoc([source])

        try:
            jsdoc.save_docs(output_dir=dest)
        except:
            raise FileNotWritableError('Could not write the docs to the build directory.')

        if self._doc_path is not None:
            if os.path.exists(self._doc_path):
                try:
                    rmtree(self._doc_path)
                except:
                    raise RemoveFolderError('Could not remove the current JSDoc folder.')

            if not os.path.exists(self._doc_path):
                try:
                    os.makedirs(self._doc_path)
                except:
                    raise CreateFolderError('Could not create the doc folder at "' + self._doc_path + '".')

            try:
                jsdoc.save_docs(output_dir=self._doc_path)
            except:
                raise FileNotWritableError('Could not write the docs to target directory (' + self._doc_path + ').')
