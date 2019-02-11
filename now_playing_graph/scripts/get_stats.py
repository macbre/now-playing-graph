"""
This script parses playlist stream from /data directory and generates some statistics

Simply execute "get_stats"
"""
import logging

from now_playing_graph.stats import get_timeline_stats
from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline

from . import INPUT_FILE


def main():
    """
    Renders a stream statistics
    """
    logger = logging.getLogger('render_graph')
    logger.info("Going to parse a stream from %s", INPUT_FILE)

    in_file = read_gzip(INPUT_FILE)
    timeline = list(kvf_stream_to_timeline(in_file))

    logger.info('Got a timeline with %d entries', len(timeline))

    stats = get_timeline_stats(timeline)

    for key, value in stats.items():
        print("{}: {}\n".format(key, value))
