import os
from error import WrongFormatError, MissingKeyError, FileNotFoundError, KeyNotAllowedError
from utils import update, load_json
import re

class Config(object):
    def __init__(self):
        self._config = {}

        try:
            self._config = self._load_configurations()
            self._parse_subprojects()
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

    def _parse_subprojects(self):
        if 'embedded_projects' not in self._config:
            self._config['embedded_projects'] = []

        for index, project in enumerate(self._config['embedded_projects']):
            if 'source' in project:
                if isinstance(project['source'], dict):
                    if 'url' not in project['source']:
                        raise MissingKeyError('The provided source is a dict but no url was defined under it.')
                    if 'type' not in project['source']:
                        url = project['source']['url']
                        urltype = 'git'
                        if url.endswith('tar.gz'):
                            urltype = 'tar.gz'
                        if url.endswith('tar'):
                            urltype = 'tar'
                        if url.endswith('zip'):
                            urltype = 'zip'
                        if url.endswith('git'):
                            urltype = 'git'
                        if os.path.exists(url):
                            urltype = 'file'

                        self._config['embedded_projects'][index]['source']['type'] = urltype
                    else:
                        urltype = project['source']['type']
                        if not (urltype == 'tar.gz' and urltype == 'tar' and urltype == 'zip' and urltype == 'git'):
                            raise WrongFormatError('The provided url type is not either zip, tar, tar.gz or git.')
                    if 'branch' not in project['source']:
                        self._config['embedded_projects'][index]['source']['branch'] = 'master'
                    else:
                        if not isinstance(project['source']['branch']):
                            raise WrongFormatError('The provided branch to check out is not a string.')
                elif isinstance(project['source'], str):
                    url = project['source']
                    urltype = 'git'
                    if url.endswith('tar.gz'):
                        urltype = 'tar.gz'
                    if url.endswith('tar'):
                        urltype = 'tar'
                    if url.endswith('zip'):
                        urltype = 'zip'
                    if url.endswith('git'):
                        urltype = 'git'
                    if os.path.exists(url):
                        urltype = 'file'
                    branch = 'master'

                    self._config['embedded_projects'][index]['source'] = {
                        'url': url,
                        'type': urltype,
                        'branch': branch
                    }

                if 'destination' not in project:
                    raise MissingKeyError('The config file defines a source, but no destination was given.')
                else:
                    if not isinstance(project['destination'], str):
                        raise WrongFormatError('Destination has to be a string.')

                if 'options' not in project:
                    self._config['embedded_projects'][index]['options'] = {}

                if self._config['embedded_projects'][index]['source']['type'] == 'file':
                    self._config['embedded_projects'][index]['source']['url'] = os.path.abspath(self._config['embedded_projects'][index]['source']['url'])

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

        return self._preparse_config(update(global_config, local_config))

    def _preparse_config(self, config):
        return config

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
