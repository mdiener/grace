class Error(Exception):
    def __init__(self, msg='', arg=None):
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


class FileNotReadableError(Error):
    pass


class FolderAlreadyExistsError(Error):
    pass


class FolderNotWritableError(Error):
    pass


class CreateFolderError(Error):
    pass


class RemoveFolderError(Error):
    pass


class FolderNotFoundError(Error):
    pass


class WrongFormatError(Error):
    pass


class MissingKeyError(Error):
    pass


class RemoveFileError(Error):
    pass


class UnknownCommandError(Error):
    pass


class SassError(Error):
    pass


class WrongLoginCredentials(Error):
    pass


class GeneralError(Error):
    pass


class RemoteServerError(Error):
    pass


class NoExectuableError(Error):
    pass


class KeyNotAllowedError(Error):
    pass


class SubProjectError(Error):
    pass
