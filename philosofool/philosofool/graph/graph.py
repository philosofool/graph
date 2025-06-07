from __future__ import annotations

from collections.abc import Hashable, Sequence


class Node:
    def __init__(self, name: Hashable):
        self.name = name
        self.edges = set()

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def remove_edge(self, edge: Edge):
        self.edges.remove(edge)

    def adjacent_nodes(self):
        return {edge.node for edge in self.edges}

    def edges_to_node(self, node: Node):
        return {edge for edge in self.edges if edge.node == node}

    def disconnect(self, node: Node):
        for edge in self.edges_to_node(node):
            self.remove_edge(edge)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.name == other.name) and (self.edges == other.edges)


class Edge:
    def __init__(self, node: Node, label):
        self.node = node
        self.label = label

    def __hash__(self):
        return hash((self.node, self.label))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.node == other.node and self.label == other.label


class Graph:
    def __init__(self):
        self.nodes: dict[Hashable, Node] = {}

    def add_node(self, node: Node):
        if node.name in self.nodes and self.nodes[node.name] != node:
            raise ValueError(f"Attempt to add {node} to graph, but it is not equivalent to {self.nodes[node.name]}")
        self.nodes[node.name] = node
        for edge_node in node.adjacent_nodes():
            if edge_node not in self:
                self.add_node(edge_node)

    def get_node(self, node):
        return self.nodes[node.name]

    def remove_node(self, node: Node):
        """Remove node from graph and delete any edge from another node to that one."""
        for other_node in self.nodes.values():
            node.disconnect(other_node)
            other_node.disconnect(node)
        self.nodes.pop(node.name)

    def depth_first_search(self, node: Node | None):
        """Execute a depth first search of the graph.

        If node is provided, the search begins with node and arrives at the subgraph
        reachable from that node.

        If node is None, the search will traverse all nodes in the graph.
        """

        if node is None:
            arbitrary_node = next(iter(self.nodes.values()))
            return self.depth_first_search(arbitrary_node)
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