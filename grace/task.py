from build import Build, clean
from deploy import Deploy
from zipit import Zip
from testit import Test
from create import New
from doc import Doc
from update import Update
from upload import Upload
from lint import Lint
from utils import update
import os
from error import UnknownCommandError, NoExectuableError, FolderNotFoundError, SubProjectError
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import git
from tempfile import mkdtemp
import subprocess
import shlex
import zipfile
import tarfile
from shutil import rmtree
import requests
import json
import threading


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, exec_autodeploy):
        self._exec_autodeploy = exec_autodeploy

    def on_any_event(self, event):
        t = threading.Thread(target=self._exec_autodeploy)
        t.start()


class Task(object):
    def __init__(self, task, config, module, test_cases):
        self._build = False
        self._jsdoc = False
        self._test = False
        self._deploy = False
        self._zip = False
        self._clean = False
        self._bad = False
        self._update = False
        self._update_test = False
        self._update_target = None
        self._upload = False
        self._autodeploy = False
        self._lint = False
        self._overwrite_args = []

        self._config = config
        self._module = module

        self._config['build'] = False
        self._config['test'] = False
        self._test_cases = test_cases

        if task == 'clean':
            self._clean = True
        else:
            if task == 'build':
                self._build = True
            if task == 'jsdoc':
                self._jsdoc = True
            if task == 'deploy':
                self._build = True
                self._deploy = True
            if task == 'zip':
                self._build = True
                self._zip = True
            if task == 'test':
                self._test = True
            if task == 'test:deploy':
                self._test = True
                self._deploy = True
            if task == 'test:zip':
                self._test = True
                self._zip = True
            if task == 'update':
                self._update = True
            if task == 'update:libs':
                self._update = True
                self._update_target = 'libs'
            if task == 'update:html':
                self._update = True
                self._update_target = 'html'
            if task == 'update:config':
                self._update = True
                self._update_target = 'config'
            if task == 'update:javascript':
                self._update = True
                self._update_target = 'javascript'
            if task == 'update:css':
                self._update = True
                self._update_target = 'css'
            if task == 'update:test':
                self._update = True
                self._update_test = True
            if task == 'update:test:libs':
                self._update = True
                self._update_test = True
                self._update_target = 'libs'
            if task == 'update:test:html':
                self._update = True
                self._update_test = True
                self._update_target = 'html'
            if task == 'update:test:javascript':
                self._update = True
                self._update_test = True
                self._update_target = 'javascript'
            if task == 'upload':
                self._build = True
                self._zip = True
                self._upload = True
            if task == 'autodeploy':
                self._autodeploy = True
            if task == 'lint':
                self._lint = True

            if not self._build and not self._test and not self._deploy and not self._zip and not self._jsdoc and not self._update and not self._upload and not self._autodeploy and not self._lint:
                raise UnknownCommandError('The provided argument could not be recognized by the manage.py script: ' + task)

    def _execute_subproject(self, project):
        if 'source' not in project:
            return

        if self._build or self._autodeploy:
            options = self._gather_option_string(project)
            print('Building sub-project located at: ' + project['source']['url'])
            if project['source']['type'] == 'file':
                sourcedir = project['source']['url']
                self._build_subproject(sourcedir, project['destination'], options)
            if project['source']['type'] == 'git':
                sourcedir = mkdtemp()
                try:
                    repo = git.Repo.clone_from(project['source']['url'], sourcedir, branch=project['source']['branch'])
                    self._build_subproject(sourcedir, project['destination'], options)
                except git.exc.GitCommandNotFound:
                    raise UnknownCommandError('Could not find the git executable in your path. Please make sure git is installed and accessible through the console.')
                except git.exc.GitCommandError as e:
                    raise UnknownCommandError('Something went wrong while executing git.')
                except:
                    raise UnknownCommandError('Failed for an unknown reason. Please try again.')
                finally:
                    rmtree(sourcedir)
            if project['source']['type'] == 'tar' or project['source']['type'] == 'zip' or project['source']['type'] == 'tar.gz':
                sourcedir = mkdtemp()
                sourcearchive = os.path.join(sourcedir, 'source')
                projecttype = project['source']['type']
                try:
                    r = requests.get(project['source']['url'], stream=True)

                    with open(sourcearchive, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                                f.flush()

                    if projecttype == 'tar':
                        tf = tarfile.open(sourcearchive, mode='r')
                        dirname = os.path.join(sourcedir, tf.getnames()[0])
                        tf.extractall(sourcedir)
                    if projecttype == 'tar.gz':
                        tf = tarfile.open(sourcearchive, mode='r:gz')
                        dirname = os.path.join(sourcedir, tf.getnames()[0])
                        tf.extractall(sourcedir)
                    if projecttype == 'zip':
                        z = zipfile.ZipFile(sourcearchive, 'r')
                        dirname = os.path.join(sourcedir, z.namelist()[0])
                        z.extractall(sourcedir)

                    self._build_subproject(dirname, project['destination'], options)

                except requests.exceptions.ConnectionError as e:
                    raise GeneralError('Could not download the source tar file.')
                    return
                finally:
                    rmtree(sourcedir)

    def _build_subproject(self, path, destination, options):
        cwd = os.getcwd()
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not os.path.isabs(destination):
            destination = os.path.abspath(destination)
        os.chdir(path)
        options += ' -o zip_path=' + destination
        args = 'python manage.py zip ' + options

        n = open(os.devnull, 'w')
        try:
            popen = subprocess.Popen(shlex.split(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = popen.communicate()
            if error != '':
                raise Exception()
        except:
            raise SubProjectError('Could not execute the sub project at location: "' + path + '". Pleas try again.')
        finally:
            n.close()
            os.chdir(cwd)

    def _gather_option_string(self, project):
        string = ''

        if 'options' in project:
            for key, value in project['options']:
                if key != 'zip_path':
                    string += '-o ' + key + '=' + value + ' '

        string += '-o autolint=false'
        return string

    def _build_subprojects(self):
        subproject_infos = os.path.join(os.path.expanduser('~'), '.grace', 'subprojects.json')
        if len(self._config['embedded_projects']) > 0:
            with open(subproject_infos, 'w+') as f:
                try:
                    infos = json.load(f)
                except:
                    infos = {
                        'parent': os.getcwd()
                    }

            new_subprojects = []
            for project in self._config['embedded_projects']:
                build_it = True
                if infos['parent'] == project['source']['url']:
                    build_it = False
                else:
                    if 'subprojects' in infos:
                        for processed_project in infos['subprojects']:
                            if processed_project == project['source']:
                                build_it = False
                                break

                new_subprojects.append(project['source'])

                if build_it:
                    infos['subprojects'] = new_subprojects

                    if os.path.exists(subproject_infos):
                        os.remove(subproject_infos)

                    with open(subproject_infos, 'w+') as f:
                        f.write(json.dumps(infos))

                    self._execute_subproject(project)

            if self._build or self._autodeploy:
                print('')

        with open(subproject_infos, 'w+') as f:
            try:
                infos = json.load(f)
            except:
                infos = {}

        if 'parent' in infos:
            if infos['parent'] == os.getcwd():
                os.remove(subproject_infos)
        else:
            os.remove(subproject_infos)

    def execute(self):
        self._build_subprojects()

        if self._clean:
            clean()
            return

        if self._build:
            if self._config['autolint']:
                valid = self.exec_lint(False)
                if not valid:
                    print 'The JavaScript could not be linted and therefore no building will happen. Fix all errors mentioned by autolint (or be evil and remove the autolint option).'
                    return

            self.exec_build()

            self._config['build'] = True

            if self._deploy:
                self.exec_deploy(None)
            if self._zip:
                self.exec_zip(None)

                if self._upload:
                    self.exec_upload()

        if self._test:
            if not os.path.exists(os.path.join(os.getcwd(), 'test')):
                print 'No tests to build found.'
                return
            else:
                if not os.path.exists(os.path.join(os.getcwd(), 'test', 'tests')):
                    print 'No tests to build found.'
                    return

            if self._test_cases is None:
                self._test_cases = self._config['test_cases']

            if self._test_cases is None:
                self._test_cases = []
                for test_case in os.listdir(os.path.join(os.getcwd(), 'test', 'tests')):
                    self._test_cases.append(test_case[5:-3])

            for test_case in self._test_cases:
                self.exec_test(test_case)

                self._config['test'] = True

                if self._deploy:
                    self.exec_deploy(test_case)
                if self._zip:
                    self.exec_zip(test_case)

        if self._jsdoc:
            self.exec_jsdoc()

        if self._update:
            self.exec_update(self._update_target)

        if self._autodeploy:
            print('Watching the source directory for any changes ... (Hit Ctrl+c to exit)\n')

            autodeploy_dir = os.path.join(os.path.expanduser('~'), '.grace', 'autodeploy')
            if not os.path.exists(autodeploy_dir):
                os.mkdir(autodeploy_dir)
            else:
                rmtree(autodeploy_dir)
                os.mkdir(autodeploy_dir)

            self._config['build'] = True
            src_dir = os.path.join(os.getcwd(), 'src')
            event_handler = ChangeHandler(self.exec_autodeploy)
            observer = Observer()
            observer.schedule(event_handler, src_dir, recursive=True)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()

            observer.join()

        if self._lint:
            print('Linting the source directory.')

            self.exec_lint()

    def exec_autodeploy(self):
        deploying_flag = os.path.join(os.path.expanduser('~'), '.grace', 'autodeploy', 'deploying')
        changes_flag = os.path.join(os.path.expanduser('~'), '.grace', 'autodeploy', 'changes_detected')

        if os.path.exists(deploying_flag):
            if not os.path.exists(changes_flag):
                f = open(changes_flag, 'a')
                try:
                    os.utime(changes_flag, None)
                finally:
                    f.close()

            return
        else:
            f = open(deploying_flag, 'a')
            try:
                os.utime(deploying_flag, None)
            finally:
                f.close()

        if self._config['autolint']:
            valid = self.exec_lint(True)
            if not valid:
                os.remove(deploying_flag)
                print 'The JavaScript could not be linted and therefore no building/deploying will happen.'
                return

        self.exec_build()
        self.exec_deploy(None)

        os.remove(deploying_flag)

        if os.path.exists(changes_flag):
            os.remove(changes_flag)
            self.exec_autodeploy()

    def exec_build(self, silent=False):
        if self._module is not None:
            try:
                b = getattr(self._module.plugin, 'Build')(self._config)
            except AttributeError:
                b = Build(self._config)
        else:
            b = Build(self._config)

        b.run()

        if not silent:
            print('Successfully built the project.')

    def exec_deploy(self, testname, silent=False):
        if self._module is not None:
            try:
                d = getattr(self._module.plugin, 'Deploy')(self._config)
            except AttributeError:
                d = Deploy(self._config)
        else:
            d = Deploy(self._config)

        d.run(testname)

        if not silent:
            if testname is not None:
                print 'Successfully deployed the test: ' + testname + '.'
            else:
                print 'Successfully deployed the project.'

    def exec_zip(self, testname, silent=False):
        if self._module is not None:
            try:
                z = getattr(self._module.plugin, 'Zip')(self._config)
            except AttributeError:
                z = Zip(self._config)
        else:
            z = Zip(self._config)

        z.run(testname)

        if not silent:
            if testname is not None:
                print 'Successfully zipped the test: ' + testname + '.'
            else:
                print 'Successfully zipped the project.'

    def exec_test(self, testname, silent=False):
        if self._module is not None:
            try:
                t = getattr(self._module.plugin, 'Test')(self._config)
            except AttributeError:
                t = Test(self._config)
        else:
            t = Test(self._config)

        t.run(testname)

        if not silent:
            if testname is not None:
                print 'Successfully built the test: ' + testname + '.'
            else:
                print 'Successfully built the test.'

    def exec_jsdoc(self, silent=False):
        if self._module is not None:
            try:
                d = getattr(self._module.plugin, 'Doc')(self._config)
            except AttributeError:
                d = Doc(self._config)
        else:
            d = Doc(self._config)

        d.run()

        if not silent:
            print 'Successfully built the JSDoc documentation.'

    def exec_upload(self, silent=False):
        if self._module is not None:
            try:
                u = getattr(self._module.plugin, 'Upload')(self._config)
            except AttributeError:
                u = Upload(self._config)
        else:
            u = Upload(self._config)

        u.run()

        if not silent:
            print 'Successfully uploaded the project.'

    def exec_lint(self, silent=False):
        if self._module is not None:
            try:
                l = getattr(self._module.plugin, 'Lint')(self._config)
            except AttributeError:
                l = Lint(self._config)
        else:
            l = Lint(self._config)

        if not silent:
            print('Linting source directory ...')

        try:
            l.run()
        except NoExectuableError:
            if not silent:
                print 'No node executable found. Make sure either nodejs or node is executable from the command line.'
            return True

        return l.lint_valid

    def exec_update(self, target):
        print 'Please be aware that an update will replace anything you have done to the files.'
        ack = raw_input('Continue: yes/[no] ')

        if ack != 'yes':
            print 'Canceling update.'
            sys.exit()

        if self._module is not None:
            try:
                u = getattr(self._module.plugin, 'Update')(self._config, target)
            except AttributeError:
                u = Update(self._config, self._update_test, target)
        else:
            u = Update(self._config, self._update_test, target)

        u.run()

        print 'Successfully updated the project.'
