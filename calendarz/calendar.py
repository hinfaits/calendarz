import string, random
import logging
from datetime import datetime

from google.appengine.ext import ndb
from google.appengine.api import memcache

import icalendar
from werkzeug.security import generate_password_hash, check_password_hash

from calendarz import utils
from calendarz import names
from calendarz import sources

logger = logging.getLogger(__name__)


class Calendar(ndb.Model):
    name = ndb.TextProperty()
    source = ndb.KeyProperty()
    secret_hash = ndb.TextProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)

    def serve_ics(self, flush_cache=False):
        """
        Returns an ics file (str) and a log (list)
        `log` is a list of strings chronologically describing how the 
            ics file came to be
        """
        six_hours = 21600
        log = ["Retrieving from cache."]
        ical = memcache.get(self.name)
        if ical is None or flush_cache:
            if ical is None:
                log.append("Not found in cache")
            ical, log = self.render_ics(log)
            memcache.set(self.name, ical, six_hours)
        return ical, log

    def render_ics(self, log=list()):
        """
        Returns same as serve_ics()
        """
        log.append("Begin rendering calendar {}".format(self.key.id()))
        count = 0
        cal = icalendar.Calendar()
        cal.add('version', '2.0')
        cal.add('x-wr-calname', 'My Calendar')
        cal.add('prodid', '{}'.format(self.name))
        cal.add('x-original-url', 'http://hinfaits.com/')
        cal.add('dtstamp', datetime.now())
        for event_dict in self.source.get().get_events(log):
            count += 1
            log.append("Processing event {}".format(count))
            event = utils.event_from_dict(event_dict, log)
            cal.add_component(event)
        log.append("Processed {} events".format(count))
        return cal.to_ical(), log,

    def new_secret(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        secret = ''.join(random.choice(chars) for _ in range(12))
        self.secret_hash = generate_password_hash(secret)
        return secret

    def check_secret(self, secret):
        return check_password_hash(self.secret_hash, secret)

    @classmethod
    def new(cls):
        """
        Returns a new Calendar object with a unique id
        """
        unique_id = cls._unique_id()
        return cls(id=unique_id, name=unique_id)

    @classmethod
    def get(cls, cal_id):
        return cls.get_by_id(cal_id)

    @classmethod
    def _unique_id(cls):
        while True:
            # There's 1e7+ possible names so guess and check 
            #   should not be too bad
            candidate_id = names.random_pair(6)
            if not cls.get_by_id(candidate_id):
                return candidate_id
