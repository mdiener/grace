class Error(Exception):
    def __init__(self, msg, arg=None):
        if arg:
            self.msg = msg + arg
        else:
            self.msg = msg

    def __repr__(self):
        return self.msg


class FileNotFoundError(Error):
    pass


class FileNotWritableError(Error):
    pass


class FolderAlreadyExistsError(Error):
    pass


class CreateFolderError(Error):
    pass


class WrongFormatError(Error):
    pass


class MissingKeyError(Error):
    pass
