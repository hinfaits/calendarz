class BaseSourceException(Exception):
    """
    Base exception raised by a Source class
    """

class InvalidUrlException(BaseSourceException):
    """
    Raised when an invalid URL is detected
    """

class FailedDownloadException(BaseSourceException):
    """
    Raised when downloading from `self.url` results in an error
    """
