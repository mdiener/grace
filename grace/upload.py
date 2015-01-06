import os
from utils import get_path
from error import MissingKeyError, WrongLoginCredentials
from pkg_resources import resource_filename
import requests
import getpass
import json


class Upload(object):
    def __init__(self, config):
        self._cwd = os.getcwd()
        self._root = get_path()
        self._config = config

        if 'upload_url' not in self._config:
            raise MissingKeyError('Could not find an upload url in either the global or local configuration file.')
        else:
            self._url = self._config['upload_url']

    def run(self):
        if 'upload_username' not in self._config:
            username = raw_input('Please provide the username for your upload server (or leave blank if none is required): ')
        else:
            username = self._config['upload_username']

        if 'upload_password' not in self._config:
            password = getpass.getpass('Please provide the password for your upload server (or leave blank if none is required): ')
        else:
            password = self._config['upload_password']

        self._session = requests.Session()
        self._session.headers.update({'Content-type': 'application/json'})

        data = {}

        if username is not '':
            data['username'] = username
        if password is not '':
            data['password'] = password

        self._session.post(self._url + '/oauth/login', data=json.dumps(data), hooks=dict(response=self._auth_response))

    def _auth_response(self, r, *args, **kwargs):
        if r.status_code is not 200:
            raise WrongLoginCredentials('Could not log in with the given credentials.')

        print 'Login was successful.'

        zip_name = self._config['name'] + '_v' + self._config['version'] + '.zip'
        zip_path = os.path.join(self._cwd, 'build', zip_name)
        if not os.path.exists(zip_path):
            raise FileNotFoundError('Could not find the zip file. Please check if "' + zip_path + '" exists.')

        try:
            zip_file = open(zip_path, 'rb')
        except:
            raise GeneralError('Something went wrong while opening the zip file. Please try again.')

        self._session.post(self._url + '/dizmo', files={'archive': (zip_name, zip_file)}, hooks=dict(response=self._upload_response))

    def _upload_response(self, r, *args, **kwargs):
        if r.status_code is not 200:
            raise FileUploadError('Could not upload the file to the server. Please try again.')

        print 'Upload successful.'
