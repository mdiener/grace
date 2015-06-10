from build import Build, clean
from deploy import Deploy
from zipit import Zip
from testit import Test
from create import New
from doc import Doc
from update import Update
from upload import Upload
from lint import Lint
import os
from error import UnknownCommandError, NoExectuableError, FolderNotFoundError
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, exec_build, exec_deploy):
        self._exec_build = exec_build
        self._exec_deploy = exec_deploy

    def on_any_event(self, event):
        print('Building and deploying project ...')
        self._exec_build(True)
        self._exec_deploy(None, True)


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
                raise UnknownCommandError('The provided argument(s) could not be recognized by the manage.py script: ' + ', '.join(tasks))

    def execute(self):
        if self._clean:
            clean()
            return

        if self._build:
            if self._config['autolint']:
                valid = self.exec_lint(True)
                if not valid:
                    print 'The JavaScript could not be linted and therefor no building will happen. Fix all errors mentioned by autolint (or be evil and remove the autolint option).'
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

            self._config['build'] = True
            src_dir = os.path.join(os.getcwd(), 'src')
            event_handler = ChangeHandler(self.exec_build, self.exec_deploy)
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
