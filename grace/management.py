from grace.task import Task
from grace.error import FileNotFoundError, WrongFormatError, MissingKeyError, CreateFolderError, FolderNotFoundError, FileNotWritableError, RemoveFolderError, RemoveFileError, FolderAlreadyExistsError, SassError, UnknownCommandError
from sys import exit


def execute_commands(cmds):
    execute(cmds)


def execute_new():
    print 'To set up your project we need a bit more information.\n'
    print 'The values in brackets are the default values. You can just hit enter if you do not want to change them.\n\n'

    tasks = new_input()
    execute(tasks)


def new_input():
    name = raw_input('Please provide a name for you project [MyProject]: ')
    type = raw_input('Select what type of project you want to create [default]: ')
    print '\nReview your information:\n'
    print 'Name: ' + name + '\n'
    print 'Type: ' + type
    okay = raw_input('Are the options above correct? [y]: ')

    if okay == 'n':
        print '\n'
        args = new_input()

    if name == '':
        name = 'MyProject'
    if type == '':
        type = 'default'

    return {
        'new': True,
        'name': name,
        'type': type
    }


def execute(args):
    try:
        task = Task(args)
    except FileNotFoundError as e:
        print e.msg
        return
    except WrongFormatError as e:
        print e.msg
        return
    except MissingKeyError as e:
        print e.msg
        return

    try:
        task.execute()
    except FileNotFoundError as e:
        print e.msg
    except WrongFormatError as e:
        print e.msg
    except MissingKeyError as e:
        print e.msg
    except CreateFolderError as e:
        print e.msg
    except FolderNotFoundError as e:
        print e.msg
    except FileNotWritableError as e:
        print e.msg
    except RemoveFolderError as e:
        print e.msg
    except RemoveFileError as e:
        print e.msg
    except FolderAlreadyExistsError as e:
        print e.msg
    except SassError as e:
        print e.msg
