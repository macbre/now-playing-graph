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

    edge = graph['edges'][0]
    assert isinstance(edge, GraphEdge)
    assert edge.caption == 'byArtist'

    # as JSON
    graph = json.loads(models_to_graph_json(models, as_json=True, json_indent=True))
    print(graph)

    assert len(graph['nodes']) == 9  # 3 artists
    assert len(graph['edges']) == 6  # and 6 songs

    # assert False
