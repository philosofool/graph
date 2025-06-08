from __future__ import annotations

from collections.abc import Hashable, Sequence, Iterator
from typing import Any


class Node:
    """A node (vertex) in a graph."""
    def __init__(self, name: Hashable):
        self.name = name
        self.edges = set()

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

    def adjacent_nodes(self) -> set[Node]:
        """List nodes reachable, 1 step away from, this node."""
        return {edge.node for edge in self.edges}

    def edges_to_node(self, node: Node) -> set[Edge]:
        """Get a set of edges in node which connect to this one directly."""
        return {edge for edge in self.edges if edge.node == node}

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.name == other.name) and (self.edges == other.edges)


class Edge:
    """A directed path to a node."""
    def __init__(self, node: Node, label: Hashable):
        self._node = node
        self._label = label

    def __hash__(self):
        return hash((self.node, self.label))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.node == other.node and self.label == other.label

    @property
    def label(self):
        return self._label

    @property
    def node(self):
        return self._node


class Graph:
    """A collection of nodes and edges, with behaviors to traverse them."""
    def __init__(self):
        self.nodes: dict[Hashable, Node] = {}

    def add_node(self, node: Node):
        """A node to a graph.

        All edge nodes to node are also added. When adding edges to a node that's
        already in the graph, this method will add those edge nodes.
        This is a relatively expensive, and it is preferable to add the edge node
        as a separate call.
        """
        if node.name in self.nodes and self.nodes[node.name] != node:
            raise ValueError(f"Attempt to add {node} to graph, but it is not equivalent to {self.nodes[node.name]}")
        self.nodes[node.name] = node
        for edge_node in node.adjacent_nodes():
            if edge_node not in self:
                self.add_node(edge_node)

    def get_node(self, node_name: Any) -> Node:
        """Return the node with node name.

        Raise KeyError if node is not in the graph.
        """
        return self.nodes[node_name]

    def remove_node(self, node: Node):
        """Remove node from graph and delete any edge from another node to that one.

        Note that all edges to the removed node are also removed.
        The removed node will have no edges and may safely be added to a different
        graph without connecting that graph to this one, if any reference to it
        exits.
        For this reason, it is important not to use a node that could be removed
        as an entrypoint into a graph.
        """
        for other_node in self.nodes.values():
            self._disconnect(node, other_node)  # TODO: this is not the most performant implementation.
            self._disconnect(other_node, node)
        self.nodes.pop(node.name)

    def _disconnect(self, node, edge_node):
        """Remove all edges from node to edge node."""
        # I'm a little skeptical.
        for edge in node.edges_to_node(edge_node):
            node.remove_edge(edge)

    def depth_first_from(self, node: Node) -> Iterator[Node]:
        """Return all nodes reachable from node, in DFS order."""
        stack = [node]
        seen = set()
        while stack:
            cur_node = stack.pop()
            seen.add(cur_node)
            for adj_node in cur_node.adjacent_nodes():
                if adj_node in seen:
                    continue
                stack.append(adj_node)
            yield cur_node

    def depth_first_search(self) -> Iterator[Node]:
        """Yield nodes in depth-first search order.

        If the graph is disconnected, subgraphs are returned in arbitrary order.
        """
        nodes_to_traverse = set(self.nodes.values())
        seen = set()
        while nodes_to_traverse:
            arbitrary_node = next(iter(nodes_to_traverse))
            for node in self.depth_first_from(arbitrary_node):
                if node in seen:
                    continue
                seen.add(node)
                yield node
                nodes_to_traverse.remove(node)

    @classmethod
    def from_dict(cls, nodes: dict[Hashable, Sequence]):
        nodes_cache = {}
        graph = cls()

        def get_cached_node(node_name) -> Node:
            node = nodes_cache.get(node_name, Node(node_name))
            if node_name not in nodes_cache:
                nodes_cache[node_name] = node
            return node

        for node_name, edges in nodes.items():
            node = get_cached_node(node_name)
            for edge_name, label in edges:
                edge_node = get_cached_node(edge_name)
                edge = Edge(edge_node, label)
                node.add_edge(edge)
            graph.add_node(node)

        return graph

    def __contains__(self, node: Node):
        if not isinstance(node, Node):
            return False
        return self.nodes.get(node.name) is not None