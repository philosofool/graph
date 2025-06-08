from graph.graph import Edge, Node
import numpy as np


def test_edge_add_to_set():
    a_set = set()
    for i in range(2):
        a_set.add(Edge(Node(1), 1))
    assert len(a_set) == 1
    a_set.remove(Edge(Node(1), 1))
    assert not a_set


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


def test_edge_equality_similar_edge():
    node = Node('node')
    edge = Edge(node, 'label')
    other_node = Node('node')
    assert edge == Edge(other_node, 'label'), "Since other_node == node, this is the same edge."
    other_node.add_edge(Edge(other_node, 'self'))
    assert edge != Edge(other_node, 'label'), "If other node changes, these are not the same edge anymore."


def test_edge_properties_immutable():
    edge = Edge(Node(1), '1')
    with np.testing.assert_raises(AttributeError):
        edge.label = '2'
    with np.testing.assert_raises(AttributeError):
        edge.node = Node(1)