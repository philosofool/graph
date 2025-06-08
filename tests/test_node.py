from graph.graph import Edge, Node

from tests.test_graph import nodes, graph   # noqa F401

def test_node_attributes():
    node = Node('a')
    assert node.name == 'a'
    assert hash(node) == hash(node.name)
    assert isinstance(node.edges, set)


def test_node_equality():
    nodeA = Node('a')
    assert nodeA == Node('a')
    assert Node('a') != Node('b')
    assert nodeA is not Node('a'), "It is possible to have two nodes with the same label in different graphs."
    assert nodeA.add_edge(Edge(Node(1), '1')) != Node('a'), "Same label, different edges is a different node."


def test_node_equality_child_class():
    class ChildNode(Node):
        pass

    node = Node(1)
    child_node = ChildNode(1)
    assert isinstance(child_node, Node)
    assert node.name == child_node.name and node.edges == child_node.edges
    assert node != child_node
    assert child_node != node


def test_node_add_to_set():
    a_set = set()
    for i in range(2):
        a_set.add(Node(1))
    assert len(a_set) == 1
    a_set.remove(Node(1))
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


def test_self_adjacent_node(nodes: list[Node]):  # noqa F811  Fixture not recognized by Flake8
    node1 = nodes[0]
    assert node1 not in node1.adjacent_nodes()
    node1.add_edge(Edge(node1, 'self'))
    assert node1 in node1.adjacent_nodes()

def test_edges_to_node():
    node1 = Node(1)
    node2 = Node(2)
    first_edge = Edge(node2, 'first')
    second_edge = Edge(node2, 'second')
    node1.add_edge(first_edge)
    node1.add_edge(second_edge)
    assert node1.edges_to_node(node2) == {first_edge, second_edge}
