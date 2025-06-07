import pytest

import numpy as np
from philosofool.graph.graph import Node, Edge, Graph

def test_node_attributes():
    node = Node('a')
    assert node.name == 'a'
    assert hash(node) == hash(node.name)
    assert isinstance(node.edges, set)

def test_node_equality():
    assert Node('a') == Node('a')
    assert Node('a') != Node('b')

def test_node_add_to_set():
    a_set = set()
    for i in range(2):
        a_set.add(Node(1))
    assert len(a_set) == 1
    a_set.remove(Node(1))
    assert not a_set

def test_edge_add_to_set():
    a_set = set()
    for i in range(2):
        a_set.add(Edge(Node(1), 1))
    assert len(a_set) == 1
    a_set.remove(Edge(Node(1), 1))
    assert not a_set

def test_add_edge():
    node = Node('a')
    edge = Edge(node, 'self')
    node.add_edge(edge)
    assert len(node.edges) == 1
    assert edge in node.edges, "The edge should be in the node edges."
    node.add_edge(edge)
    assert len(node.edges) == 1, "Adding the same edge twice has no effect."

def test_remove_edge():
    node = Node('a')
    edge = Edge(node, 'self')
    node.add_edge(edge)
    node.remove_edge(edge)
    assert edge not in node.edges

def test_adjacent_nodes():
    node = Node(0)
    assert node.adjacent_nodes() == set()
    node.add_edge(Edge(Node(1), '1'))
    assert node.adjacent_nodes() == {Node(1)}
    node.add_edge(Edge(node, None))
    assert node.adjacent_nodes() == {Node(1), node}

def test_disconnect():
    """Remove all edges leading to node."""
    node1 = Node(1)
    node2 = Node(2)
    first_edge = Edge(node2, 'first')
    second_edge = Edge(node2, 'second')
    node1.add_edge(first_edge)
    node1.add_edge(second_edge)
    node1.disconnect(node2)
    assert node2 not in node1.adjacent_nodes()

def test_edges_to_node():
    node1 = Node(1)
    node2 = Node(2)
    first_edge = Edge(node2, 'first')
    second_edge = Edge(node2, 'second')
    node1.add_edge(first_edge)
    node1.add_edge(second_edge)
    assert node1.edges_to_node(node2) == {first_edge, second_edge}

def test_edge_attributes():
    edge = Edge(Node('a'), label=None)
    assert edge.node == Node('a')
    assert edge.label is None

def test_edge_equality():
    node = Node('node')
    edge = Edge(node, 'label')
    assert edge == Edge(node, 'label')
    assert edge != Edge(node, 'different label')
    assert edge != Edge(Node('other_node'), 'label')
    assert edge != Edge(Node('other node'), 'different label')

def test_graph():
    graph = Graph()
    assert graph.nodes == {}

def test_add_node():
    graph = Graph()
    assert graph.nodes == {}
    node = Node(1)
    graph.add_node(node)
    assert graph.nodes == {node.name: node}

    node2 = Node(2)
    node3 = Node(3)
    node2.add_edge(Edge(node3, '3'))
    graph.add_node(node2)
    assert node2 in graph
    assert node3 in graph

    similar_node = Node(1)
    similar_node.add_edge(Edge(similar_node, 'self'))
    with np.testing.assert_raises(ValueError, msg='Adding a node with the same label that is not equivalent should be prohibited.'):
        graph.add_node(similar_node)

def test_graph_add_edge_to_graphed_node():
    graph = Graph()
    node1 = Node(1)
    graph.add_node(node1)
    node2 = Node(2)
    edge = Edge(node2, '2')
    node1.add_edge(edge)
    assert node2 not in graph, "Adding a edge to node in a graph will not add that edge-node to the graph."
    graph.add_node(node1)
    assert node2 in graph, "Redundantly adding a node to a graph will add missing edge-nodes."

def test_get_node():
    graph = Graph()
    graph.add_node(Node(1))
    assert graph.get_node(Node(1)) == Node(1)
    with np.testing.assert_raises(KeyError):
        assert graph.get_node(Node(0))

def test_in_graph():
    graph = Graph()
    assert 1 not in graph
    assert Node(1) not in graph
    graph.add_node(Node(1))
    assert 1 not in graph
    assert Node(1) in graph

def test_remove_node():
    graph = Graph()
    graph.add_node(Node(1))
    graph.remove_node(Node(1))
    assert Node(1) not in graph

    node1 = Node(1)
    node2 = Node(2)
    # node3 = Node(3)
    node1.add_edge(Edge(node2, 'first'))
    node1.add_edge(Edge(node2, 'second'))
    node2.add_edge(Edge(node1, 'first'))
    graph.add_node(node1)
    graph.add_node(node2)
    graph.remove_node(node1)
    assert node1 not in node2.adjacent_nodes()
    assert node2 not in node1.adjacent_nodes()
    assert node1 not in graph

@pytest.fixture
def graph() -> Graph:
    graph = Graph.from_dict({
        1: [(2, '2'), (3, '3')],
        3: [(4, '4')]
    })
    return graph

@pytest.fixture
def nodes(graph):
    return [graph.nodes[i] for i in range(1, 5)]

def test_from_dict_creates_nodes(graph):
    assert isinstance(graph, Graph)
    assert len(graph.nodes) == 4
    node1, node2, node3, node4 = graph.nodes.values()
    for node in node1, node2, node3, node4:
        assert isinstance(node, Node)

def test_from_dict_adjacent_nodes(nodes):
    node1, node2, node3, node4 = nodes

    assert node2 in node1.adjacent_nodes()
    assert node3 in node1.adjacent_nodes()
    assert node4 not in node2.adjacent_nodes()

    assert node4 in node3.adjacent_nodes()
    assert not node4.adjacent_nodes()
    assert not node2.adjacent_nodes()

def test_from_dict_edges(nodes):
    node1, node2, node3, node4 = nodes

    assert any(Edge(node2, '2') == edge for edge in node1.edges)
    assert any(Edge(node3, '3') == edge for edge in node1.edges)
    assert len(node1.edges) == 2
    assert any(Edge(node4, '4') == edge for edge in node3.edges)
    assert len(node3.edges) == 1
    assert not node4.edges
    assert not node2.edges


def test_depth_first_search(graph, nodes):
    node1, node2, node3, node4 = nodes

    nodes = []
    for node in graph.depth_first_search(node1):
        nodes.append(node)
    assert nodes.index(node1) == 0, "Node 1 should be the first one reached."
    assert nodes.index(node3) < nodes.index(node4), "node three will be reached before it's edge-node (node4)"
    if nodes.index(node3) > nodes.index(node2):
        assert nodes[1] == node2, "Node 2 must be second if it's before node 3."
    else:
        assert nodes[3] == node2, "Node 2 must be last it it's after node 3."