from build import Build, clean
from deploy import Deploy
from zipit import Zip
from testit import Test
from create import New
from doc import Doc
from update import Update
from upload import Upload
import os
from error import UnknownCommandError
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
    def __init__(self, tasks, config, module):
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

        self._config = config
        self._module = module

        self._config['build'] = False
        self._config['test'] = False

        if len(tasks) == 0:
            raise UnknownCommandError('Need to have at least one task to operate on')

        task = tasks[0]

        if task == 'help':
            self._show_help()
            return

        if task == 'test' or task == 'test:deploy' or task == 'test:zip':
            if len(tasks) > 1:
                self._test_cases = tasks[1].split(':')
            else:
                self._test_cases = None
        else:
            if len(tasks) > 1:
                print 'Only the first argument will be executed. All other arguments are being ignored (except "st" if supplied)'

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

            if not self._build and not self._test and not self._deploy and not self._zip and not self._jsdoc and not self._update and not self._upload and not self._autodeploy:
                raise UnknownCommandError('The provided argument(s) could not be recognized by the manage.py script: ' + ', '.join(tasks))

    def _show_help(self):
        graceconfig = os.path.join(os.path.expanduser('~'), '.graceconfig')

        print 'Grace Help'
        print '=========='
        print 'Grace is a toolchain to work with rich JavaScript applications. It'
        print 'provides several tools for developers to create applications in a'
        print 'fast and clean manner.'
        print '\nUsage'
        print '-----'
        print 'python manage.py [command]'
        print '\nCommands'
        print '--------'
        print 'build\t\tBuilds the project and places the output in ./build/ProjectName.'
        print 'deploy\t\tFirst build and then deploy the project to the path'
        print '\t\tspecified in the deployment_path option in your project.cfg file.'
        print 'autodeploy\tWatch the "src" directory for chances and deploy when anything new has been detected.'
        print 'jsdoc\t\tBuild the jsDoc of the project.'
        print 'zip\t\tBuild and then zip the output and put it into the path'
        print '\t\tspecified by the zip_path option in your project.cfg file.'
        print 'clean\t\tClean the build output.'
        print 'test\t\tBuild all the tests.'
        print 'test:deploy\tBuild and then deploy the tests.'
        print 'test:zip\tBuild and then zip the tests'
        print 'upload\t\tUpload the project to the specified server.'
        print 'st\t\tCan be used with any command to show the full stack trace'
        print '\t\t(in case of an error).'
        print '\nThe global configuration file can be found at: ' + graceconfig
        print '\nFurther Reading'
        print '---------------'
        print 'For more information visit https://www.github.com/mdiener/grace'

    def execute(self):
        if self._clean:
            clean()
            return

        if self._build:
            self.exec_build()

            self._config['build'] = True

            if self._deploy:
                self.exec_deploy(None)
            if self._zip:
                self.exec_zip(None)

                if self._upload:
                    self.exec_upload()

        if self._test:
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
