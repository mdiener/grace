import os
import plistlib
from error import FileNotWritableError, MissingKeyError, RemoveFolderError
from shutil import move, rmtree


class Dizmo:
    def __init__(self):
        self._dizmo_deployment_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'data', 'futureLAB', 'dizmode', 'InstalledWidgets')
        if os.name == 'nt':
            self._dizmo_deployment_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'futureLAB', 'dizmode', 'InstalledWidgets')
            self._dizmo_deployment_path = self._dizmo_deployment_path.replace('/', '//')

    def pass_config(self, config):
        self._config = config
        try:
            self._check_config()
        except:
            raise

        self._bundle_name = self._dizmo_config['bundle_identifier'].split('.')
        self._bundle_name = self._bundle_name[len(self._bundle_name) - 1]

    def _check_config(self):
        if 'dizmo_settings' not in self._config:
            raise MissingKeyError('Could not find settings for dizmo.')

        self._dizmo_config = self._config['dizmo_settings']

        if 'development_region' not in self._dizmo_config:
            raise MissingKeyError('Specify a development region in your config file under `dizmo_settings`.')

        if 'display_name' not in self._dizmo_config:
            raise MissingKeyError('Specify a display name in your config file under `dizmo_settings`.')

        if 'bundle_identifier' not in self._dizmo_config:
            raise MissingKeyError('Specify a bundle identifier in your config file under `dizmo_settings`.')

        if 'width' not in self._dizmo_config:
            raise MissingKeyError('Specify a width in your config file under `dizmo_settings`.')

        if 'height' not in self._dizmo_config:
            raise MissingKeyError('Specify a height in your config file under `dizmo_settings`.')

        if 'box_inset_x' not in self._dizmo_config:
            raise MissingKeyError('Specify a box inset x in your config file under `dizmo_settings`.')

        if 'box_inset_y' not in self._dizmo_config:
            raise MissingKeyError('Specify a box inset y in your config file under `dizmo_settings`.')

        if 'api_version' not in self._dizmo_config:
            raise MissingKeyError('Specify an api version in your config file under `dizmo_settings`.')

        if 'main_html' not in self._dizmo_config:
            raise MissingKeyError('Specify a main html in your config file under `dizmo_settings`.')

    def _get_plist(self, test=False):
        if test:
            display_name = self._dizmo_config['display_name'] + ' Test'
            identifier = self._dizmo_config['bundle_identifier'] + '.test'
        else:
            display_name = self._dizmo_config['display_name']
            identifier = self._dizmo_config['bundle_identifier']

        return dict(
            CFBundleDevelopmentRegion=self._dizmo_config['development_region'],
            CFBundleDisplayName=display_name,
            CFBundleIdentifier=identifier,
            CFBundleName=self._bundle_name,
            CFBundleShortVersionString=self._config['version'],
            CFBundleVersion=self._config['version'],
            CloseBoxInsetX=self._dizmo_config['box_inset_x'],
            CloseBoxInsetY=self._dizmo_config['box_inset_y'],
            MainHTML=self._dizmo_config['main_html'],
            Width=self._dizmo_config['width'],
            Height=self._dizmo_config['height'],
            KastellanAPIVersion=self._dizmo_config['api_version']
        )

    def after_build(self):
        plist = self._get_plist()
        path = self._config['build_path']

        try:
            plistlib.writePlist(plist, os.path.join(path, 'Info.plist'))
        except:
            raise FileNotWritableError('Could not write plist to target location: ', path)

    def after_test(self):
        plist = self._get_plist(test=True)
        path = self._config['test_build_path']

        try:
            plistlib.writePlist(plist, os.path.join(path, 'Info.plist'))
        except:
            raise FileNotWritableError('Could not write plist to target location: ', path)

    def new_replace_line(self, line):
        line = line.replace('#DIZMODEPLOYMENTPATH', self._dizmo_deployment_path)

        return line

    def after_deploy(self):
        if self._config['test']:
            source = os.path.join(self._config['deployment_path'], self._config['name'] + '_test')
            dest = os.path.join(self._config['deployment_path'], self._dizmo_config['bundle_identifier'] + '.test')

            try:
                self._move_deploy(source, dest)
            except:
                raise

        if self._config['build']:
            source = os.path.join(self._config['deployment_path'], self._config['name'])
            dest = os.path.join(self._config['deployment_path'], self._dizmo_config['bundle_identifier'])

            try:
                self._move_deploy(source, dest)
            except:
                raise

    def _move_deploy(self, source, dest):
        if os.path.exists(dest):
            try:
                rmtree(dest)
            except:
                raise RemoveFolderError('Could not remove the deploy folder.')

        try:
            move(source, dest)
        except:
            raise FileNotWritableError('Could not move the deploy target to the dizmo path.')

    def after_zip(self):
        if self._config['test']:
            try:
                self._move_zip(self._config['name'] + '_test')
            except:
                raise

        if self._config['build']:
            try:
                self._move_zip(self._config['name'])
            except:
                raise

    def _move_zip(self, name):
        try:
            source = os.path.join(self._config['zip_path'], name + '.zip')
            dest = os.path.join(self._config['zip_path'], name + '.dzm')
        except:
            source = os.path.join(os.getcwd(), 'build', name + '.zip')
            dest = os.path.join(os.getcwd(), 'build', name + '.dzm')

        if os.path.exists(dest):
            try:
                os.remove(dest)
            except:
                raise FileNotWritableError('Could not remove the old dizmo zip file.')

        try:
            move(source, dest)
        except:
            raise FileNotWritableError('Could not move the zip target to the dizmo path.')
