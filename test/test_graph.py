"""
Tests for models.py module
"""
import json

from now_playing_graph.graph import models_to_graph_json, GraphEdge, GraphNode
from now_playing_graph.models import timeline_to_models
from now_playing_graph.stream import kvf_stream_to_timeline

from . import STREAM


def test_models_to_graph_json():
    models = timeline_to_models(kvf_stream_to_timeline(STREAM))

    # as dict
    graph = models_to_graph_json(models)

    print(graph)

    assert len(graph['nodes']) == 9  # 3 artists
    assert len(graph['edges']) == 6  # and 6 songs

    node = graph['nodes'][0]
    assert isinstance(node, GraphNode)
    assert node.caption == 'Eivør Pálsdóttir'
    assert node.type == 'MusicGroup'
    assert node.size == 3

    node = graph['nodes'][-1]
    assert isinstance(node, GraphNode)
    assert node.caption == 'Hon leitar'
    assert node.type == 'MusicRecording'
    assert node.size == 132

    edge = graph['edges'][0]
    assert isinstance(edge, GraphEdge)
    assert edge.caption == 'byArtist'

    # as JSON
    graph = models_to_graph_json(models, as_json=True, json_indent=True)
    print(graph)
    graph = json.loads(graph)

    assert len(graph['nodes']) == 9  # 3 artists
    assert len(graph['edges']) == 6  # and 6 songs

    node = graph['nodes'][0]
    assert node == GraphNode(
        id='5834d4db6',
        caption='Eivør Pálsdóttir',
        size=3,
        type='MusicGroup'
    ).__dict__

    # assert False
