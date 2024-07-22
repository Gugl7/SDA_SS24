import random
import networkx as nx
from itertools import combinations

def max_cardinality_search_ordering(G):
    """Max Cardinality Search heuristic for vertex ordering."""
    G = G.copy()
    ordering = [None] * len(G)
    labeled_nodes = set()
    
    current_node = random.choice(list(G.nodes))
    ordering[len(G) - 1] = current_node
    labeled_nodes.add(current_node)
    
    for i in range(len(G) - 2, -1, -1):
      max_neighbors = -1
      next_node = None
      
      for node in G.nodes:
        if node not in labeled_nodes:
          labeled_neighbors = sum(1 for neighbor in G.neighbors(node) if neighbor in labeled_nodes)
          if labeled_neighbors > max_neighbors:
            max_neighbors = labeled_neighbors
            next_node = node
      
      ordering[i] = next_node
      labeled_nodes.add(next_node)
    
    return ordering


def greedy(G, method="min_degree"):
  """Greedy heuristic for treewidth ordering."""
  G = G.copy()
  ordering = []
  nodes = list(G.nodes)
  while nodes:
    if method == "min_degree":
      v = min_degree(G)
    elif method == "min_fill":
      v = min_fill(G)
    ordering.append(v)
    G.remove_node(v)
    nodes.remove(v)
  return ordering

def min_degree(G):
  """Return the node with the minimum degree in the graph G."""
  return ((sorted(G.degree, key=lambda x: x[1])[0][0]))

def min_fill(G):
  """Return the node with the minimum fill in the graph G."""
  return min(G.nodes, key=lambda node: sum(1 for u, v in combinations(G.neighbors(node), 2) if not G.has_edge(u, v)))

if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (3, 4), (3, 5), (4, 5), (5, 6)])
    
    print("Min Degree Ordering:", greedy(G, method="min_degree"))
    print("Min Fill Ordering:", greedy(G, method="min_fill"))
    print("Max Cardinality Search Ordering:", max_cardinality_search_ordering(G))