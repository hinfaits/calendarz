import logging
from urlparse import urlparse

from google.appengine.api import urlfetch

import icalendar
import dateutil.parser

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 10

def validate_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme)


def parse_datetime(dt_string):
    """
    Parse `dt_string` in to a timezone-aware datetime.datetime object. 
    Inputs `dt_string` without timezone info will have UTC tzinfo added.

    Suggested Inputs
        ISO 8601 DT strings         - 2017-01-12T10:22:25+0000
        This human readable format  - dd-MMM-yy hh:mm +tztz - eg 04-Feb-17 11:30 -0700
    """
    parsed = dateutil.parser.parse(dt_string)
    if parsed.tzinfo:
        return parsed.astimezone(dateutil.tz.tzutc())
    else:
        return parsed.replace(tzinfo=dateutil.tz.tzutc())

def datetime_to_string(dt_object):
    return dt_object.strftime("%d-%b-%Y %H:%M:%S %z")


def event_from_dict(info_dict, log=list()):
    """
    Parse `info_dict` in to a icalendar.event object, ignoring empty fields
    """
    event = icalendar.Event()
    for key, value in info_dict.iteritems():
        if not key or not value:
            log.append("Skipping info [{} => {}]".format(key, value))

        # for component in ("dtstamp", "dtstart", "dtend",):
        #     if key.lower() == component:
        #         dt = parse_datetime(value)
        #         log.append("Parsed {} : {}".format(component, datetime_to_string(dt)))
        #         event.add(component, dt)
        #         continue

        # for component in ("uid", "duration", "summary", "description",
        #                   "location", "geo",):
        #     if key.lower() == component:
        #         log.append("Parsed {} : {}".format(component, value))
        #         event.add(component, value)
        #         continue

        elif key.lower() == 'uid':
            log.append("Parsed uid : {}".format(value))
            event.add('uid', value)
        elif key.lower() == 'dtstamp':
            dt = parse_datetime(value)
            log.append("Parsed dtstamp : {}".format(datetime_to_string(dt)))
            event.add('dtstamp', dt)
        elif key.lower() == 'dtstart':
            dt = parse_datetime(value)
            log.append("Parsed dtstart : {}".format(datetime_to_string(dt)))
            event.add('dtstart', parse_datetime(value))
        elif key.lower() == 'dtend':
            dt = parse_datetime(value)
            log.append("Parsed dtend : {}".format(datetime_to_string(dt)))
            event.add('dtend', parse_datetime(value))
        elif key.lower() == 'duration':
            log.append("Parsed duration : {}".format(value))
            event.add('duration', value)
        elif key.lower() == 'summary':
            log.append("Parsed summary : {}".format(value))
            event.add('summary', value)
        elif key.lower() == 'description':
            log.append("Parsed description : {}".format(value))
            event.add('description', value)
        elif key.lower() == 'location':
            log.append("Parsed location : {}".format(value))
            event.add('location', value)
        elif key.lower() == 'geo':
            log.append("Parsed geo : {}".format(value))
            event.add('geo', value)
        else:
            log.append("Failed to parse info [{} => {}]".format(key, value))

    return event


def get_url(url):
    """
    Fetch `url` and return response data if http response = 200 or return None
    """
    logger.debug("Fetching URL: %s", url)
    try:
        urlfetch.set_default_fetch_deadline(HTTP_TIMEOUT)
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            return result.content
        else:
            logger.warning("Got bad response %s", result.status_code)
    except urlfetch.Error:
        logger.exception("Caught exception fetching url")
