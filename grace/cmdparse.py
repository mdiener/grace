import argparse
import textwrap
from utils import load_json


class CommandLineParser(object):
    def __init__(self):
        self._instantiate_parser()
        self._add_arguments()

    def _instantiate_parser(self):
        self._parser = argparse.ArgumentParser(description=textwrap.dedent(self._get_description()), epilog=textwrap.dedent(self._get_epilog()), formatter_class=argparse.RawDescriptionHelpFormatter)

    def _get_description(self):
        return '''\
Grace is a toolchain to work with rich JavaScript applications.
It provides several tools for developers to create applications
in a fast and clean manner.'''

    def _get_epilog(self):
        return '''\
Task Commands
-------------
The following tasks can be specified through the task command.
    build       Builds the project and places the output in ./build/ProjectName.
    deploy      First build and then deploy the project to the path
                specified in the deployment_path option in your project.cfg file.
    autodeploy  Execute a deploy task upon any change int the src directory.
    jsdoc       Build the jsDoc of the project.
    zip         Build and then zip the output and put it into the path
                specified by the zip_path option in your project.cfg file.
    Clean       Clean the build output.
    test        Build all the tests.
    test:deploy Build and then deploy the tests.
    test:zip    Build and then zip the tests
    upload      Upload the project to the specified server.

Overwrite Commands
------------------
Most of the configuration options specified by either the project.cfg or the
global grace.cfg can be overwritten on the command line. They take the form:
option=new_value

The following options can be overwritten:
deployment_path
zip_path
doc_path
minify_js       Accepts true or false
minify_css      Accepts true or false
autolint        Accepts true or false
urls:upload
credentials:username
credentials:password

Example:
python manage.py deploy --overwrite deployment_path=/tmp/deployment --overwrite minify_js=true
python manage.py build -o minify_css=true


Further Reading
---------------
For more information visit https://www.github.com/mdiener/grace'
'''

    def _add_arguments(self):
        self._parser.add_argument('task', help='Executes the given task.')
        self._parser.add_argument('--test-cases', help='Build only the specified test cases (separated by a semicolon).')
        self._parser.add_argument('--overwrite', '-o', action='append', help='Overwrite the specified configuration option.')
        self._parser.add_argument('--stack-trace', '-s', action='store_true', help='Provides a full stack trace instead of just an error message.')

    def get_arguments(self):
        args = self._parser.parse_args()

        overwrites = {}

        if args.overwrite is not None:
            for overwrite in args.overwrite:
                overwrite = overwrite.split('=')

                if len(overwrite) != 1:
                    key = overwrite[0]
                    value = overwrite[1]

                    def parse_nested_key(holder, keychain, value):
                        if len(keychain) == 1:
                            holder[keychain[0]] = value
                        else:
                            if keychain[0] not in holder:
                                holder[keychain[0]] = {}
                            parse_nested_key(holder[keychain[0]], keychain[1:], value)

                        return holder

                    if len(key.split(':')) > 1:
                        keychain = key.split(':')
                        key = keychain[0]
                        value = parse_nested_key({}, keychain[1:], value)

                    try:
                        value = load_json(value)
                    except:
                        pass

                    overwrites[key] = value

        return args.task, args.test_cases, overwrites, args.stack_trace
