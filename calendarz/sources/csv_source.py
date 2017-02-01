from StringIO import StringIO
import csv

from calendarz.sources.base_source import BaseSource
from calendarz.sources import exceptions
from calendarz import utils


class CsvSource(BaseSource):

    def get_events(self, log=list()):
        log.append("Downloading CSV file from {}".format(self.url))
        try:
            csvfile = StringIO(self.download())
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
        except exceptions.FailedDownloadException:
            log.append("Failed to download.")
            return

    def download(self):
        res = utils.get_url(self.url)
        if res:
            return res
        else:
            raise exceptions.FailedDownloadException
