import os
from error import WrongFormatError, MissingKeyError, FileNotFoundError
import re
import json

class Config(object):
    def __init__(self):
        try:
            self._parse_global_config()
            self._parse_local_config()
        except:
            raise

    def _parse_config_file(self, config_file):
        strings = []
        for line in config_file:
            if not re.search('^\s*//.*', line):
                strings.append(line)

        try:
            return json.loads(''.join(strings))
        except:
            raise WrongFormatError('The provided configuration file could not be parsed.')

    def _parse_global_config(self):
        config_path = os.path.join(os.path.expanduser('~'), '.graceconfig')

        try:
            config_file = open(os.path.join(config_path))
        except:
            self._global_config = {}
            print 'No global configuration file found, using local one for all values.'
            return

        try:
            self._global_config = self._parse_config_file(config_file)
        except:
            raise

        if 'minify_js' not in self._global_config:
            self._global_config['minify_js'] = False
        else:
            if not isinstance(self._global_config['minify_js'], bool):
                self._global_config['minify_js'] = False

        if 'minify_css' not in self._global_config:
            self._global_config['minify_css'] = False
        else:
            if not isinstance(self._global_config['minify_css'], bool):
                self._global_config['minify_css'] = False

    def _parse_local_config(self):
        cwd = os.getcwd()

        try:
            config_file = open(os.path.join(cwd, 'project.cfg'))
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        try:
            self._config = self._parse_config_file(config_file)
        except:
            raise

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')
        else:
            if not isinstance(self._config['name'], unicode):
                raise WrongFormatError('The name key in your config file must be a string!')
            else:
                if len(self._config['name']) == 0:
                    raise WrongFormatError('The name key in your config file must be at least one character long.')

        if 'version' not in self._config:
            raise MissingKeyError('Please specify a version in your config file.')
        else:
            if not isinstance(self._config['version'], unicode):
                raise WrongFormatError('The version key in your config file needs to be a string!')

        if 'minify_js' not in self._config:
            self._config['minify_js'] = self._global_config['minify_js']
        else:
            if not isinstance(self._config['minify_js'], bool):
                self._config['minify_js'] = False

        if 'minify_css' not in self._config:
            self._config['minify_css'] = self._global_config['minify_css']
        else:
            if not isinstance(self._config['minify_css'], bool):
                self._config['minify_css'] = False

        if 'type' not in self._config:
            self._config['type'] = 'default'
        else:
            if not isinstance(self._config['type'], unicode):
                self._config['type'] = 'default'
            else:
                if len(self._config['type']) == 0:
                    self._config['type'] = 'default'

        if 'js_name' not in self._config:
            self._config['js_name'] = 'application'
        else:
            if not isinstance(self._config['js_name'], unicode):
                self._config['js_name'] = 'application'
            else:
                if len(self._config['js_name']) == 0:
                    self._config['js_name'] = 'application'

        if 'test_cases' not in self._config:
            self._config['test_cases'] = None

        self._config['build_path'] = os.path.join(cwd, 'build', self._config['name'])

    def get_config(self):
        config = dict(self._global_config.items() + self._config.items())
        return config
