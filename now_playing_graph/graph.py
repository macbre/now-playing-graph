"""
Turned a set of models into a graph / GraphJSON structure
"""
# http://netflix.github.io/falcor/documentation/jsongraph.html
import json

from dataclasses import dataclass

from .models import BaseModel


@dataclass
class GraphNode:
    """
    Represents graph node
    """
    id: str
    caption: str
    type: str
    size: int = 1


@dataclass
class GraphEdge:
    """
    Represents graph edge
    """
    source: str
    target: str
    caption: str


def models_to_graph_json(models, as_json=False, json_indent=False):
    """
    :type models list[BaseModel]
    :type as_json bool
    :type json_indent bool
    :rtype: dict|str
    """
    # https://github.com/macbre/schema-org-graph/blob/master/
    # grapher/grapher/scripts/query_football_graph.py#L212-L262

    # graph nodes
    nodes = [
        GraphNode(
            id=model.get_hash(),
            caption=model.name,
            type=model.get_type(),
            size=model.get_size()
        )
        for model in models
    ]

    # graph edges
    edges = []

    for model in models:
        for relation, target in model.relations.items():
            assert isinstance(target, BaseModel)

            edges.append(GraphEdge(
                source=model.get_hash(),
                target=target.get_hash(),
                caption=relation
            ))

    if not as_json:
        return {
            'nodes': nodes,
            'edges': edges,
        }

    graph = {
        # https://www.bruceeckel.com/2018/09/16/json-encoding-python-dataclasses/
        'nodes': [node.__dict__ for node in nodes],
        'edges': [edge.__dict__ for edge in edges],
    }

    return json.dumps(graph, indent=True if json_indent else None)
