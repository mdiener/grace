from error import CreateFolderError, FileNotWritableError, RemoveFolderError
import pyjsdoc
import os
from shutil import rmtree


class Doc:
    def __init__(self, global_config, config):
        self._cwd = os.getcwd()
        self._config = config
        self._global_config = global_config

        if 'doc_path' not in self._config:
            if 'doc_path' not in self._global_config:
                self._doc_path = None
            else:
                self._doc_path = os.path.join(self._global_config['doc_path'], self._config['name'], 'JSDoc')
        else:
            self._doc_path = os.path.join(self._config['doc_path'], self._config['name'], 'JSDoc')

        self._lib_path = os.path.join(self._cwd, 'src', 'lib')

    def build_doc(self, with_libs=False):
        source = os.path.join(self._cwd, 'src', 'javascript')
        dest = os.path.join(self._cwd, self._config['build_path'], 'JSDocs')

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

        if with_libs:
            jsdoc = pyjsdoc.CodeBaseDoc([source, self._lib_path])
        else:
            jsdoc = pyjsdoc.CodeBaseDoc([source])

        try:
            jsdoc.save_docs(output_dir=dest)
        except:
            raise FileNotWritableError('Could not write the docs to into the build directory.')

        if self._doc_path is not None:
            try:
                jsdoc.save_docs(output_dir=self._doc_path)
            except:
                raise FileNotWritableError('Could not write the docs to target directory (' + self._doc_path + ').')
