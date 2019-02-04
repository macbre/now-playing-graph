"""
Functions that transform a stream of JSON data fetched from radio stations
into a timeline list
"""
import logging
import json

# https://docs.python.org/dev/library/datetime.html#datetime.datetime.fromisoformat / Python 3.7!
from datetime import datetime

# https://docs.python.org/3.7/library/gzip.html#module-gzip
from gzip import GzipFile

from .timeline import TimelineEntry


logger = logging.getLogger(__file__)


def read_gzip(filename: str):
    """
    :type filename str
    :rtype: list[str]
    """
    with GzipFile(filename, mode='r') as handler:
        for line in handler:
            yield bytes(line).decode('utf-8')


def read_text(filename: str):
    """
    :type filename str
    :rtype: list[str]
    """
    with open(filename, mode='rt') as handler:
        for line in handler:
            yield line


def kvf_stream_to_timeline(lines):
    """
    :type lines list[str]
    :rtype: list[TimelineEntry]
    """
    last_updated = current_entry = None

    for line_no, line in enumerate(lines):
        # ignore lines without a prefix
        # data: {"updated":"2019-01-22T20:31:37.973","now":..}}
        if not line.startswith('data: {'):
            continue

        try:
            # remove "data: " suffix
            data = json.loads(line.strip()[6:])
        except json.decoder.JSONDecodeError as ex:
            logger.error('JSON parsing failed at line #%d: "%s"', line_no, line.strip(), exc_info=True)
            raise ex

        current_updated = data['updated']

        # has the track changed recently?
        if current_updated != last_updated:
            # print(data)

            # update it
            last_updated = current_updated

            # no song is currently being played
            # data: {
            #   "updated":"2019-01-22T20:57:50.475",
            #   "now":{"artist":{},"title":{},
            #   "start":{}},"next":{"artist":{},"title":{},"start":{}}
            # }
            if not data['now']['start']:
                # we were not able to get the duration of the previous song, take it now
                if current_entry.duration < 0:
                    end = datetime.fromisoformat(data['updated'])
                    duration = (end - current_entry.played_at).total_seconds()

                    current_entry.duration = int(duration)
                    yield current_entry

                continue

            start = datetime.fromisoformat(data['now']['start'])

            try:
                # calculate a diff of now['start] and next['start'] -> song duration
                end = datetime.fromisoformat(data['next']['start'])

                # 2019-01-22 20:27:22.318000 / 2019-01-22 20:31:36.810000
                # 0:04:14.492000
                duration = (end - start).total_seconds()

            except TypeError:
                duration = -1

            # build the next timeline entry
            current_entry = TimelineEntry(
                artist_name=data['now']['artist'],
                song_title=data['now']['title'],
                duration=int(duration),
                played_at=start
            )

            # we got the next entry as well, so we managed to calculate
            # the duration of the current song
            if current_entry.duration > 0:
                yield current_entry
