from error import CommandLineArgumentError
from new import New
from build import Build, BuildDizmo, clean
from deploy import Deploy
from zipit import Zip
from test import Test, TestDizmo


class Task:
    def __init__(self, args):
        if len(args) < 1:
            raise CommandLineArgumentError()

        if args[0] == 'dizmo':
            self._with_dizmo = True
            args.pop(0)

            if len(args) < 1:
                raise CommandLineArgumentError()
        else:
            self._with_dizmo = False

        if args[0] == 'build':
            self._task = 'build'
            try:
                if args[1] == 'javascript':
                    self._subtask = 'javascript'
                elif args[1] == 'html':
                    self._subtask = 'html'
                elif args[1] == 'css':
                    self._subtask = 'css'
                elif args[1] == 'libraries':
                    self._subtask = 'libraries'
                elif args[1] == 'images':
                    self._subtask = 'images'
                else:
                    raise CommandLineArgumentError()
            except:
                self._subtask = None
        elif args[0] == 'new':
            self._task = 'new'
            try:
                self._name = args[1]
            except:
                if self._with_dizmo:
                    self._name = 'MyDizmo'
                else:
                    self._name = 'MyProject'
        elif args[0] == 'clean':
            self._task = 'clean'
        elif args[0] == 'deploy':
            self._task = 'deploy'
            self._subtask = None
        elif args[0] == 'zip':
            self._task = 'zip'
            self._subtask = None
        elif args[0] == 'test':
            self._task = 'test'
            try:
                if args[1] == 'deploy':
                    self._subtask = 'deploy'
                    try:
                        self._testname = args[2]
                    except:
                        self._testname = None
                else:
                    self._subtask = None
                    self._testname = args[1]
            except:
                self._subtask = None
                self._testname = args[1]
        else:
            raise CommandLineArgumentError()

    def execute(self):
        if self._task == 'new':
            try:
                New(self._name, self._with_dizmo)
            except:
                raise
        elif self._task == 'build':
            try:
                self._build()
            except:
                raise
        elif self._task == 'deploy':
            try:
                self._build()
            except:
                raise

            try:
                d = Deploy(self._with_dizmo, False)
                d.deploy_project()
            except:
                raise
        elif self._task == 'zip':
            try:
                self._build()
            except:
                raise

            try:
                z = Zip(self._with_dizmo)
                z.zip_project()
            except:
                raise
        elif self._task == 'clean':
            try:
                clean()
            except:
                raise
        elif self._task == 'test':
            try:
                t = Test(self._testname)
                t.build_test()
            except:
                raise

            if self._with_dizmo:
                try:
                    td = TestDizmo()
                    td.build_dizmo()
                except:
                    raise

            if self._subtask == 'deploy':
                try:
                    d = Deploy(self._with_dizmo, True)
                    d.deploy_project()
                except:
                    raise

    def _build(self):
        try:
            b = Build()
            b.build_project(self._subtask)
        except:
            raise

        if self._with_dizmo:
            try:
                bd = BuildDizmo()
                bd.build_dizmo()
            except:
                raise
