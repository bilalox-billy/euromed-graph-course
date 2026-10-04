## Summary Cheat Sheet

```python
import networkx as nx

G = nx.MultiGraph()

# ── CREATION ───────────────────────────────────────────────
G = nx.MultiGraph()                          # empty
G = nx.MultiGraph(name="My Graph")          # with attributes
G = nx.MultiGraph([(1,2),(1,2),(2,3)])       # from edge list

# ── NODES ─────────────────────────────────────────────────
G.add_node("A", color="red")                 # single node + attr
G.add_nodes_from(["B", "C"], size=10)        # multiple nodes
G.remove_node("A")                           # remove + its edges
G.has_node("B")                              # True/False
"B" in G                                     # True/False (shortcut)

# ── EDGES ──────────────────────────────────────────────────
key = G.add_edge(1, 2, weight=5)             # returns edge key
keys = G.add_edges_from([(1,2),(2,3)])       # multiple edges
G.add_weighted_edges_from([(1,2,5),(1,2,9)])# with weights
G.remove_edge(1, 2)                          # remove 1 edge (lowest key)
G.remove_edge(1, 2, key=1)                  # remove specific key
G.has_edge(1, 2)                             # any edge between 1-2?
G.has_edge(1, 2, key=0)                      # specific edge?

# ── ACCESS ─────────────────────────────────────────────────
G[1][2]                      # {key: attr_dict, ...} for all 1-2 edges
G[1][2][0]                   # attr dict for edge key=0
G.edges[1, 2, 0]             # same (read-only view)
G.get_edge_data(1, 2, key=0) # returns dict or None

# ── ITERATION ──────────────────────────────────────────────
list(G.nodes())                          # all nodes
list(G.edges())                          # (u, v) pairs (may repeat!)
list(G.edges(keys=True))                 # (u, v, key) tuples
list(G.edges(keys=True, data=True))      # (u, v, key, attr_dict)
list(G.edges(data="weight"))             # (u, v, weight_value)

# ── COUNTING ───────────────────────────────────────────────
len(G)                        # number of nodes
G.number_of_nodes()           # number of nodes
G.number_of_edges()           # total edges (counts parallel!)
G.number_of_edges(1, 2)       # edges between specific pair
G.size()                      # same as number_of_edges()
G.size(weight="weight")       # sum of weights
G.degree()                    # DegreeView (parallel edges counted)
G.degree(1)                   # degree of node 1

# ── COPIES & CONVERSIONS ───────────────────────────────────
H = G.copy()                  # deep copy
V = G.copy(as_view=True)      # lightweight view
sub = G.subgraph([1, 2])      # subgraph on nodes
DG = G.to_directed()          # → MultiDiGraph
SG = nx.Graph(G)              # → simple Graph (drops parallels!)
```

---

## 📚 Further Reading

| Resource | Link |
|---|---|
| NetworkX MultiGraph API | [networkx.org/…/multigraph.html](https://networkx.org/documentation/stable/reference/classes/multigraph.html) |
| NetworkX Tutorial | [networkx.org/documentation/stable/tutorial.html](https://networkx.org/documentation/stable/tutorial.html) |
| Graph Theory (Wikipedia) | [en.wikipedia.org/wiki/Multigraph](https://en.wikipedia.org/wiki/Multigraph) |
| NetworkX MultiDiGraph | [networkx.org/…/multidigraph.html](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) |

---