from __future__ import print_function
from __future__ import absolute_import
from builtins import input
from builtins import object
import os
from .utils import get_path, write_json
from .error import MissingKeyError, WrongLoginCredentials, FileNotFoundError, RemoteServerError
from pkg_resources import resource_filename
import requests
import getpass

requests.packages.urllib3.disable_warnings()


class Upload(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._root = get_path()
        self._config = config
        self._verify_ssl = False

        self._username = None
        self._password = None

        self._check_config()

    def _check_config(self):
        if 'urls' not in self._config:
            raise MissingKeyError('Could not find url settings in either global or local configuration file.')

        if 'upload' not in self._config['urls']:
            raise MissingKeyError('Could not find an upload url in either the global or local configuration file.')
        else:
            self._upload_url = self._config['urls']['upload']

        if 'login' not in self._config['urls']:
            self._login_url = self._upload_url
        else:
            self._login_url = self._config['urls']['login']

        if 'credentials' in self._config:
            if 'username' in self._config['credentials']:
                self._username = self._config['credentials']['username']
            if 'password' in self._config['credentials']:
                self._password = self._config['credentials']['password']

        if 'zip_name' not in self._config:
            self._zip_name = self._config['name'] + '-' + self._config['version'] + '.zip'
        else:
            self._zip_name = self._config['zip_name']

        self._zip_path = os.path.join(self._cwd, 'build', self._zip_name)

    def run(self):
        self._login()

    def _get_login_information(self):
        data = {}

        if self._username is None:
            self._username = input('Please provide the username for your upload server (or leave blank if none is required): ')

        if self._password is None:
            self._password = getpass.getpass('Please provide the password for your upload server (or leave blank if none is required): ')

        if self._username != '':
            data['username'] = self._username
        if self._password != '':
            data['password'] = self._password

        return data

    def _login(self):
        data = self._get_login_information()

        r = requests.post(self._login_url,
            data=write_json(data),
            headers={'Content-Type': 'application/json'},
            verify=self._verify_ssl
        )

        self._cookies = r.cookies

        self._login_response(r)

    def _login_response(self, r):
        if r.status_code != 200:
            raise WrongLoginCredentials('Could not log in with the given credentials.')

        self._upload()

    def _upload(self):
        if not os.path.exists(self._zip_path):
            raise FileNotFoundError('Could not find the zip file. Please check if "' + self._zip_path + '" exists.')

        try:
            zip_file = open(self._zip_path, 'rb')
        except:
            raise GeneralError('Something went wrong while opening the zip file. Please try again.')

        r = requests.post(self._upload_url,
            files={'file': zip_file},
            cookies=self._cookies,
            verify=self._verify_ssl
        )

        self._upload_response(r)

    def _upload_response(self, r):
        if r.status_code != 201:
            print(r.text)
            raise RemoteServerError('Could not upload the file to the server. Please try again.')
