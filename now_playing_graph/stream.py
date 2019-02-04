"""
Functions that transform a stream of JSON data fetched from radio stations
into a timeline list
"""
import json

# https://docs.python.org/dev/library/datetime.html#datetime.datetime.fromisoformat / Python 3.7!
from datetime import datetime

# https://docs.python.org/3.7/library/gzip.html#module-gzip
from gzip import GzipFile

from .timeline import TimelineEntry


def read_gzip(filename):
    """
    :type filename str
    :rtype: list[str]
    """
    with GzipFile(filename, mode='r') as handler:
        for line in handler:
            yield bytes(line).decode('utf-8')


def kvf_stream_to_timeline(lines):
    """
    :type lines list[str]
    :rtype: list[TimelineEntry]
    """
    last_updated = None

    for line in lines:
        # ignore lines without a prefix
        # data: {"updated":"2019-01-22T20:31:37.973","now":..}}
        if not line.startswith('data: '):
            continue

        # remove "data: " suffix
        line = line.strip()[6:]
        data = json.loads(line)

        current_updated = data['updated']

        # has the track changed recently?
        if current_updated != last_updated:
            # print(data)

            # calculate a diff of now['start] and next['start'] -> song duration
            start = datetime.fromisoformat(data['now']['start'])
            end = datetime.fromisoformat(data['next']['start'])

            # 2019-01-22 20:27:22.318000 / 2019-01-22 20:31:36.810000
            # 0:04:14.492000
            duration = (end - start).total_seconds()

            # yield the next timeline entry
            yield TimelineEntry(
                artist_name=data['now']['artist'],
                song_title=data['now']['title'],
                duration=int(duration)
            )

            # update it
            last_updated = current_updated
