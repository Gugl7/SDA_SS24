import networkx as nx
from networkx.algorithms.approximation import treewidth_min_degree
import itertools
import matplotlib.pyplot as plt
import pandas as pd

def find_balanced_separator(G, max_size):
    nodes = list(G.nodes)
    for k in range(1, max_size + 1):
        for separator in itertools.combinations(nodes, k):
            remaining = G.copy()
            remaining.remove_nodes_from(separator)
            if all(len(comp) <= 2 * len(G) / 3 for comp in nx.connected_components(remaining)):
                return separator
    return None

def combine_decompositions(S, decompositions):
    tree = nx.Graph()
    S_node = tuple(S)
    tree.add_node(S_node)
    for decomposition in decompositions:
        root = next(iter(decomposition.nodes))
        tree.add_node(root)
        tree.add_edge(S_node, root)
        tree = nx.compose(tree, decomposition)
    return tree

def tree_decomposition(G):
    if len(G) <= 1:
        trivial_tree = nx.Graph()
        trivial_tree.add_node(tuple(G.nodes))
        return trivial_tree
    
    tw_bound, _ = treewidth_min_degree(G)
    max_separator_size = 2 * tw_bound + 2
    
    S = find_balanced_separator(G, max_separator_size)
    if S is None:
        raise RuntimeError("Failed to find a balanced separator.")
    
    remaining = G.copy()
    remaining.remove_nodes_from(S)
    components = [G.subgraph(comp).copy() for comp in nx.connected_components(remaining)]
    
    decompositions = [tree_decomposition(comp) for comp in components]
    return combine_decompositions(S, decompositions)

def main():
    data = pd.read_csv('data/input.csv', sep=',', header=None)
    G = nx.Graph()
    for row in data.iterrows():
        G.add_edge(int(row[1][0]), int(row[1][1]))
    td = tree_decomposition(G)
    print("Tree decomposition edges:", td.edges)
    string = ""
    for i in range(1, len(td.edges)+1):
        string += 'N'+str(i)+','
    string += '\n'
    i = 1
    for edge in td.edges:
        string += 'N'+str(i)+',,'
        string += str(edge[0][0])+';'
        string += str(edge[1][0])+'\n'
        i += 1
    with open('data/output.csv', 'w') as file:
        file.write(string)

if __name__ == "__main__":
    main()
