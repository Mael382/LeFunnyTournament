from typing import Any

from collections.abc import Iterable

import networkx as nx


def max_weighted_matching(nodes: Iterable, edges: Iterable[tuple[Any, Any, int | float]]) -> set[tuple[Any, Any]]:
    """
    ...

    :param nodes: ...
    :param edges: ...
    :return: ...
    """
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)
    return nx.max_weight_matching(graph, maxcardinality=True, weight="weight")
