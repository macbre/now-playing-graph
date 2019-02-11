"""
This script parses playlist stream from /data directory and renders a GraphJSON

Simply execute "render_graph"
"""
import logging

from now_playing_graph.graph import models_to_graph_json
from now_playing_graph.models import timeline_to_models
from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline

from . import INPUT_FILE

# MIN_SONGS = 1  # Got a 2996 models (1187 artists and 1809 songs)
MIN_SONGS = 3  # Got a 757 models (188 artists and 569 songs)
# MIN_SONGS = 5  # Got a 391 models (76 artists and 315 songs)


def main():
    """
    Renders a graph
    """
    logger = logging.getLogger('render_graph')

    logger.info("Going to parse a stream from %s", INPUT_FILE)

    # read and parse the stream into a timeline
    timeline = list(kvf_stream_to_timeline(read_gzip(INPUT_FILE)))

    logger.info('Got a timeline with %d entries', len(timeline))
    logger.info(timeline[0])
    logger.info(timeline[-1])

    # now get models for artists and songs
    models = timeline_to_models(timeline, min_songs=MIN_SONGS)

    # some stats
    artists = len([True for model in models if model.get_type() == 'MusicGroup'])
    songs = len([True for model in models if model.get_type() == 'MusicRecording'])

    logger.info('Got a %d models (%d artists and %d songs)', len(models), artists, songs)

    # ok, now render the graph
    graph_json = models_to_graph_json(models, as_json=True, json_indent=False)

    print('// {} artists and {} songs'.format(artists, songs))
    print('var graph={};'.format(graph_json))
