from sage.all import Graph
from sage.graphs.graph_decompositions.tree_decomposition import make_nice_tree_decomposition

graph = Graph({0: [1], 1: [0, 2, 3], 2: [1, 4, 5], 3: [1, 5, 6], 4: [2, 5], 5: [2, 3, 4, 6], 6: [3, 5]})
graph = Graph({0: [1], 1:[0, 2], 2:[1]})
tw = graph.treewidth()
tree_decomp = graph.treewidth(certificate=True, k=1, algorithm="sage")

print("Tree decomposition:", tree_decomp.vertices())
