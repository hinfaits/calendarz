import json 

from calendarz.sources.base_source import BaseSource
from calendarz.sources import exceptions
from calendarz import utils


class JsonSource(BaseSource):

    def get_events(self, log=list()):
        log.append("Downloading JSON file from {}".format(self.url))
        try:
            jsonfile = self.download()
            return list(json.loads(jsonfile))
        except ValueError:
            log.append("Failed to decode JSON, maybe this isn't JSON at all?")
            return list()
        except exceptions.FailedDownloadException:
            log.append("Failed to download.")
            return list()

    def download(self):
        res = utils.get_url(self.url)
        if res:
            return res
        else:
            raise exceptions.FailedDownloadException
