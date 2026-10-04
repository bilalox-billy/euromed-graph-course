## 14. Exercises

Test your understanding with these progressive exercises.

---

### Exercise 1: Basic MultiGraph Creation-- Easy

**Task:** Create a `MultiGraph` representing a small city's road network:
- Cities: `A`, `B`, `C`, `D`
- Two roads between `A` and `B` (one is a highway, the other a local road)
- One road between `B` and `C`
- One road between `C` and `D`
- A maintenance loop (self-loop) at city `A`

Print the total number of edges and the adjacency view of node `A`.

<details>
<summary>💡 Solution</summary>

```python
import networkx as nx

G = nx.MultiGraph()
G.add_edge("A", "B", type="highway", speed_limit=120)
G.add_edge("A", "B", type="local",   speed_limit=50)
G.add_edge("B", "C", type="highway", speed_limit=90)
G.add_edge("C", "D", type="local",   speed_limit=60)
G.add_edge("A", "A", type="maintenance_loop")  # self-loop

print("Total edges:", G.number_of_edges())   # 5
print("Adjacency of A:", G["A"])
# AdjacencyView({'B': {0: {'type': 'highway', ...}, 1: {'type': 'local', ...}},
#                'A': {0: {'type': 'maintenance_loop'}}})
```
</details>

---

### Exercise 2: Edge Keys and Attribute Access-- Intermediate

**Task:** Build a flight network between 3 airports (`JFK`, `LAX`, `ORD`). Each pair of airports has 2 flights. Then:
1. Find the cheapest flight from `JFK` to `LAX`.
2. Find all flights operated by `"Delta"`.
3. Remove the most expensive `JFK`–`LAX` flight.

<details>
<summary>💡 Solution</summary>

```python
import networkx as nx

F = nx.MultiGraph()
flights = [
    ("JFK", "LAX", {"airline": "Delta",    "price": 280, "flight": "DL101"}),
    ("JFK", "LAX", {"airline": "United",   "price": 320, "flight": "UA202"}),
    ("JFK", "ORD", {"airline": "American", "price": 150, "flight": "AA303"}),
    ("JFK", "ORD", {"airline": "Delta",    "price": 135, "flight": "DL404"}),
    ("LAX", "ORD", {"airline": "United",   "price": 210, "flight": "UA505"}),
    ("LAX", "ORD", {"airline": "American", "price": 195, "flight": "AA606"}),
]
F.add_edges_from(flights)

# 1. Cheapest JFK → LAX
jfk_lax = F["JFK"]["LAX"]
cheapest_key = min(jfk_lax, key=lambda k: jfk_lax[k]["price"])
print(f"Cheapest JFK→LAX: {jfk_lax[cheapest_key]['flight']} at ${jfk_lax[cheapest_key]['price']}")

# 2. Delta flights
delta = [(u, v, k, d) for u, v, k, d in F.edges(keys=True, data=True) if d["airline"] == "Delta"]
print("Delta flights:", [(d["flight"], f"${d['price']}") for _, _, _, d in delta])

# 3. Remove most expensive JFK-LAX flight
priciest_key = max(jfk_lax, key=lambda k: jfk_lax[k]["price"])
F.remove_edge("JFK", "LAX", key=priciest_key)
print(f"JFK-LAX flights remaining: {F.number_of_edges('JFK', 'LAX')}")
```
</details>

---

### Exercise 3: Analysis Challenge-- Hard

**Task:** Given a MultiGraph representing a communication network, write a function that:
1. Identifies all **redundant pairs** (node pairs with more than 1 edge).
2. Calculates the **average number of parallel edges** across all connected pairs.
3. Detects any **self-loop nodes**.

<details>
<summary>💡 Solution</summary>

```python
import networkx as nx

def analyze_multigraph(G):
    """Analyze redundancy and self-loops in a MultiGraph."""
    results = {
        "redundant_pairs": [],
        "avg_parallel_edges": 0,
        "self_loop_nodes": []
    }

    seen_pairs = set()
    total_edges_in_pairs = 0
    num_pairs = 0

    for u, v in G.edges():
        pair = tuple(sorted([u, v]))
        if u == v:
            if u not in results["self_loop_nodes"]:
                results["self_loop_nodes"].append(u)
        elif pair not in seen_pairs:
            seen_pairs.add(pair)
            count = G.number_of_edges(u, v)
            num_pairs += 1
            total_edges_in_pairs += count
            if count > 1:
                results["redundant_pairs"].append((u, v, count))

    results["avg_parallel_edges"] = (
        total_edges_in_pairs / num_pairs if num_pairs > 0 else 0
    )
    return results

# Test
G = nx.MultiGraph()
G.add_edges_from([(1, 2), (1, 2), (1, 2), (2, 3), (3, 4), (3, 4), (4, 4)])
report = analyze_multigraph(G)
print("Redundant pairs:", report["redundant_pairs"])
print(f"Avg parallel edges: {report['avg_parallel_edges']:.2f}")
print("Self-loop nodes:", report["self_loop_nodes"])
```
</details>

---