import os
from utils import get_path
from shutil import copytree, rmtree
from error import FolderNotFoundError, FolderNotWritableError, FileNotFoundError, FileNotWritableError
from pkg_resources import resource_filename
import sys


class Update(object):
    def __init__(self, config, test=False, target=None):
        self._cwd = os.getcwd()
        self._root = get_path()
        self._config = config
        self._test = test
        self._target = target

        try:
            self._skeleton_path = resource_filename(__name__, os.path.join('skeleton', 'default'))
        except NotImplementedError:
            self._skeleton_path = os.path.join(sys.prefix, 'skeleton', 'default')

        try:
            self._assetPath = os.path.join(resource_filename(__name__, os.path.join('assets', 'manage.py')))
        except NotImplementedError:
            self._assetPath = os.path.join(sys.prefix, 'assets', 'manage.py')

        self._projectName = self._config['name']
        if 'deployment_path' in self._config:
            self._deployment_path = self._config['deployment_path']
        else:
            self._deployment_path = ''
        if 'zip_path' in self._config:
            self._zip_path = self._config['zip_path']
        else:
            self._zip_path = ''
        if 'doc_path' in self._config:
            self._doc_path = self._config['doc_path']
        else:
            self._doc_path = ''

    def run(self):
        if self._target is None:
            print 'Do you really want to update all files? Changes to any files you might have done will be lost in the process!'
            ack = raw_input('Continue: yes/[no] ')
            if ack is not 'yes':
                print 'Canceling update.'
                sys.exit()

            print 'Updating everything ...'

            self._update_all()

        if self._target is 'libs':
            print 'Updating libs directory ...'
            self._update_libs()

        if self._target is 'html':
            print 'Updating index.html file ...'
            self._update_html()

        if self._target is 'config':
            print 'Update project.cfg file ...'
            self._update_config()

        if self._target is 'javascript':
            print 'Update JavaScript files ...'
            self._update_javascript()

        if self._target is 'css':
            print 'Update css files ...'
            self._update_css()

    def _update_all(self):
        if not self._test:
            try:
                self.update_css()
                self.update_config()
            except:
                raise

        try:
            self.update_libs()
            self.update_html()
            self.update_javascript()
        except:
            raise

    def _update_config(self):
        new_config_path = os.path.join(self._skeleton_path, 'project_X.cfg')
        current_config_path = os.path.join(self._cwd, 'project.cfg')

        if not os.path.exists(new_config_path):
            raise FileNotFoundError('Could not find the new project config file at: ' + new_config_path)

        if os.path.exists(current_config_path):
            try:
                os.remove(current_config_path)
            except:
                raise RemoveFileError('Could not remove the old project.cfg file at: ' + current_config_path)

        self._replace_lines_and_copy(new_config_path, current_config_path)

    def _update_libs(self):
        if self._test:
            new_libs_dir = os.path.join(self._skeleton_path, 'test', 'lib')
            current_libs_dir = os.path.join(self._cwd, 'test', 'lib')
        else:
            new_libs_dir = os.path.join(self._skeleton_path, 'src', 'lib')
            current_libs_dir = os.path.join(self._cwd, 'src', 'lib')

        if not os.path.exists(new_libs_dir):
            return

        try:
            self._update_files(new_libs_dir, current_libs_dir)
        except:
            raise

    def _update_html(self):
        if self._test:
            new_html_path = os.path.join(self._skeleton_path, 'test', 'index_X.html')
            current_html_path = os.path.join(self._cwd, 'test', 'index.html')
        else:
            new_html_path = os.path.join(self._skeleton_path, 'src', 'index_X.html')
            current_html_path = os.path.join(self._cwd, 'src', 'index.html')

        if not os.path.exists(new_html_path):
            raise FileNotFoundError('Could not find the new html file at: ' + new_html_path)

        if os.path.exists(current_html_path):
            try:
                os.remove(current_html_path)
            except:
                raise RemoveFileError('Could not remove the old index.html file at: ' + current_html_path)

        self._replace_lines_and_copy(new_html_path, current_html_path)

    def _update_javascript(self):
        if self._test:
            new_javascript_dir = os.path.join(self._skeleton_path, 'test', 'javascript')
            current_javascript_dir = os.path.join(self._cwd, 'test', 'javascript')
        else:
            new_javascript_dir = os.path.join(self._skeleton_path, 'src', 'javascript')
            current_javascript_dir = os.path.join(self._cwd, 'src', 'javascript')
            new_js_app_file = os.path.join(self._skeleton_path, 'src', 'application_X.js')
            current_js_app_file = os.path.join(self._cwd, 'src', 'application.js')

        if not self._test:
            try:
                os.remove(current_js_app_file)
            except:
                raise FileNotWritableError('Could not remove the old js application file.')
            self._replace_lines_and_copy(new_js_app_file, current_js_app_file)

        if not os.path.exists(new_javascript_dir):
            return

        try:
            self._update_files(new_javascript_dir, current_javascript_dir)
        except:
            raise

    def _update_css(self):
        new_css_dir = os.path.join(self._skeleton_path, 'src', 'style')
        current_css_dir = os.path.join(self._cwd, 'src', 'style')

        if not os.path.exists(new_css_dir):
            return

        try:
            self._update_files(new_css_dir, current_css_dir)
        except:
            raise

    def _update_files(self, in_dir, out_dir):
        for path, dirs, files in os.walk(in_dir):
            for f in files:
                file_in_path = os.path.join(path, f)
                directory = path.split(in_dir)[1][1:]
                file_out_path = os.path.join(out_dir, directory, f.replace('_X', ''))
                dir_out_path = os.path.join(out_dir, directory)

                if not os.path.exists(dir_out_path):
                    try:
                        os.makedirs(dir_out_path)
                    except OSError as exc:
                        if exc.errno == errno.EEXIST and os.path.isdir(dir_out_path):
                            pass
                        else:
                            raise
                else:
                    try:
                        os.remove(file_out_path)
                    except:
                        if os.path.exists(file_out_path):
                            raise FileNotWritableError('Could not remove the old file at: ' + file_out_path)

                self._replace_lines_and_copy(file_in_path, file_out_path)

    def _replace_lines_and_copy(self, file_in_path, file_out_path):
        with open(file_out_path, 'w+') as file_out:
            file_in = open(file_in_path)

            for line in file_in:
                try:
                    newline = line.replace('##DEPLOYMENTPATH##', self._deployment_path)
                    newline = newline.replace('##ZIPPATH##', self._zip_path)
                    newline = newline.replace('##PROJECTNAME##', self._projectName)
                    newline = newline.replace('##PROJECTNAME_TOLOWER##', self._projectName.lower())
                    newline = newline.replace('##DOCPATH##', self._doc_path)
                except UnicodeDecodeError as exc:
                    newline = line

                file_out.write(newline)

        file_in.close()
