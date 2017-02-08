from google.appengine.ext import ndb

from calendarz.sources import exceptions
from calendarz import utils

class BaseSource(ndb.Model):
    url = ndb.TextProperty()

    def __init__(self, **kwargs):
        super(BaseSource, self).__init__(**kwargs)
        if kwargs.get('url'):
            if utils.validate_url(kwargs.get('url')):
                self.url = kwargs.get('url')
            else:
                raise exceptions.InvalidUrlException

    def get_events(self, log=list()):
        """
        Returns an iterable of all events from this source
        """
        raise NotImplementedError("This is an abstract method.")

    def download(self):
        res = utils.get_url(self.url)
        if res:
            return res
        else:
            raise exceptions.FailedDownloadException
