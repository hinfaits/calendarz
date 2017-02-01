class BaseSourceException(Exception):
    pass

class InvalidUrlException(BaseSourceException):
    pass

class FailedDownloadException(BaseSourceException):
    pass
