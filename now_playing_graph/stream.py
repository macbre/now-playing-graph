"""
Functions that transform a stream of JSON data fetched from radio stations
into a timeline list
"""
import json

# https://docs.python.org/3.7/library/gzip.html#module-gzip
from gzip import GzipFile


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
    :rtype: list[dict]
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
            print(data)

            # yield the next timeline entry
            yield dict(
                artist_name=data['now']['artist'],
                song_title=data['now']['title'],
            )

            # update it
            last_updated = current_updated
