import os
from error import WrongFormatError, MissingKeyError, FileNotFoundError, KeyNotAllowedError
from utils import update, load_json
import re

class Config(object):
    def __init__(self):
        self._config = {}

        try:
            self._config = self._load_configurations()
        except:
            raise

        if 'type' not in self._config:
            self._config['type'] = 'default'
        else:
            if not isinstance(self._config['type'], str):
                self._config['type'] = 'default'
            else:
                if len(self._config['type']) == 0:
                    self._config['type'] = 'default'

    def get_type(self):
        return self._config['type']

    def load_overwrites(self, overwrites):
        self._config = self._update_config(self._config, overwrites)

    def get_config(self):
        self._parse_config()
        return self._config

    def _load_configurations(self):
        config_file = None
        cwd = os.getcwd()
        local_config = None
        global_config = None
        config_path = os.path.join(os.path.expanduser('~'), '.grace', 'grace.cfg')

        try:
            config_file = open(os.path.join(config_path))
        except:
            self._global_config = {}
            print('No global configuration file found, using local one for all values.')
            return

        try:
            global_config = self._parse_config_file(config_file)
        except:
            raise

        try:
            config_file = open(os.path.join(cwd, 'project.cfg'))
        except:
            raise FileNotFoundError('Could not find a config file in this directory.')

        try:
            local_config = self._parse_config_file(config_file)
        except:
            raise

        return update(global_config, local_config)

    def _check_update_keys(self, updates):
        if 'name' in updates:
            raise KeyNotAllowedError('Can not overwrite the name configuration option.')
        if 'version' in updates:
            raise KeyNotAllowedError('Can not overwrite the version configuration option.')

    def _update_config(self, config, updates):
        try:
            self._check_update_keys(updates)
        except:
            raise

        return update(config, updates)

    def _parse_config_file(self, config_file):
        strings = []
        for line in config_file:
            if not re.search('^\s*//.*', line):
                strings.append(line)

        try:
            return load_json(''.join(strings))
        except:
            raise WrongFormatError('The provided configuration file could not be parsed.')

    def _parse_config(self):
        cwd = os.getcwd()

        if 'name' not in self._config:
            raise MissingKeyError('Name of the project needs to be in the config file.')
        else:
            if not isinstance(self._config['name'], str):
                raise WrongFormatError('The name key in your config file must be a string!')
            else:
                if len(self._config['name']) == 0:
                    raise WrongFormatError('The name key in your config file must be at least one character long.')

        if 'version' not in self._config:
            raise MissingKeyError('Please specify a version in your config file.')
        else:
            if not isinstance(self._config['version'], str):
                raise WrongFormatError('The version key in your config file needs to be a string!')

        if 'minify_js' not in self._config:
            self._config['minify_js'] = False
        else:
            if not isinstance(self._config['minify_js'], bool):
                self._config['minify_js'] = False

        if 'minify_css' not in self._config:
            self._config['minify_css'] = False
        else:
            if not isinstance(self._config['minify_css'], bool):
                self._config['minify_css'] = False

        if 'linter' not in self._config:
            self._config['linter'] = 'jshint'
        else:
            if not isinstance(self._config['linter'], str):
                raise WrongFormatError('The linter key has to be a string.')

            if self._config['linter'] != 'jslint':
                if self._config['linter'] != 'jshint':
                    raise WrongFormatError('The linter key has to be either "jslint", "jshint" or undfined (missing).')

        if 'lintoptions' not in self._config:
            self._config['lintoptions'] = {}
        else:
            if not isinstance(self._config['lintoptions'], dict):
                raise WrongFormatError('The lintoptions key has to be a dict (object).')

        if 'autolint' not in self._config:
            self._config['autolint'] = True
        else:
            if not isinstance(self._config['autolint'], bool):
                raise WrongFormatError('The autolint key has to be a boolean.')

        if 'js_name' not in self._config:
            self._config['js_name'] = 'application'
        else:
            if not isinstance(self._config['js_name'], str):
                self._config['js_name'] = 'application'
            else:
                if len(self._config['js_name']) == 0:
                    self._config['js_name'] = 'application'

        if 'test_cases' not in self._config:
            self._config['test_cases'] = None

        self._config['build_path'] = os.path.join(cwd, 'build', self._config['name'])
