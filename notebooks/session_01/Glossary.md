# Graph Theory Glossary — Session 01

> A reference guide for all core graph concepts covered in Session 01.  
> All examples use real-world analogies — **no Python code**.

---

## Table of Contents

1. [Graph (Formal Definition)](#1-graph-formal-definition)
2. [Vertex / Node](#2-vertex--node)
3. [Edge / Link / Arc](#3-edge--link--arc)
4. [Undirected Graph](#4-undirected-graph)
5. [Directed Graph (DiGraph)](#5-directed-graph-digraph)
6. [Weighted Graph](#6-weighted-graph)
7. [MultiGraph](#7-multigraph)
8. [MultiDiGraph](#8-multidigraph)
9. [Bipartite Graph](#9-bipartite-graph)
10. [DAG — Directed Acyclic Graph](#10-dag--directed-acyclic-graph)
11. [Hypergraph](#11-hypergraph)
12. [Node Attribute](#12-node-attribute)
13. [Edge Attribute](#13-edge-attribute)
14. [Graph Attribute](#14-graph-attribute)
15. [Degree](#15-degree)
16. [In-Degree](#16-in-degree)
17. [Out-Degree](#17-out-degree)
18. [Successor](#18-successor)
19. [Predecessor](#19-predecessor)
20. [Self-Loop](#20-self-loop)
21. [Parallel Edges (Multi-edges)](#21-parallel-edges-multi-edges)
22. [Edge Key](#22-edge-key)
23. [Path](#23-path)
24. [Adjacency](#24-adjacency)

---

## 1. Graph (Formal Definition)

A **graph** `G` is defined as an ordered pair:

```
G = (V, E)
```

Where:
- **V** is a finite, non-empty set of **vertices** (also called *nodes*)
- **E ⊆ V × V** is a set of **edges** (also called *links* or *arcs*), each connecting two vertices

An edge between vertex `u` and vertex `v` is written as `(u, v)`.

### Real-World Example
A **road map** where:
- **V** = {Paris, Lyon, Marseille, Bordeaux, Toulouse}
- **E** = {(Paris, Lyon), (Lyon, Marseille), (Marseille, Toulouse), ...}

Each city is a node; each road connecting two cities is an edge.

---

## 2. Vertex / Node

A **vertex** (plural: *vertices*), also called a **node**, is the fundamental unit of a graph. Nodes represent entities in the domain being modelled.

### Real-World Examples

| Domain | What a Node Represents |
|---|---|
| Social network | A person |
| Road network | A city or intersection |
| Internet | A web page or server |
| Biology | A protein or gene |
| Finance | A bank account or company |

### Key Properties
- Nodes can store additional information via **attributes** (see §12).
- Every graph must have at least one node.
- Nodes can exist in isolation — without any edges.

---

## 3. Edge / Link / Arc

An **edge** connects two nodes and represents a **relationship** or **interaction** between them. Depending on the graph type, edges may be:

| Term | Context |
|---|---|
| **Edge** | General term (undirected graphs) |
| **Arc** | Often used in directed graphs |
| **Link** | Common in network science |

### Real-World Examples

| Domain | What an Edge Represents |
|---|---|
| Social network | A friendship or follow |
| Road network | A road between two cities |
| Web | A hyperlink between pages |
| Finance | A monetary transaction |
| Biology | A protein–protein interaction |

---

## 4. Undirected Graph

An **undirected graph** is a graph where edges have **no direction**. The relationship between two nodes is **symmetric**: if `A` is connected to `B`, then `B` is equally connected to `A`.

```
Edge (A, B) = Edge (B, A)   ← same edge, no direction
```

### Real-World Example: Friendship Network

```
Alice ——— Bob
  |         |
Carol ——— Dave
```

- Alice is friends with Bob → Bob is friends with Alice.
- The friendship is mutual and has no "from" or "to".

### When to Use
Use an undirected graph when the **relationship is symmetric**:
- Friendships on Facebook
- Roads between cities (you can drive both ways)
- Co-authorship networks (if A co-authored with B, then B co-authored with A)

---

## 5. Directed Graph (DiGraph)

A **directed graph** (also called a **digraph**) is a graph where every edge has a **direction** — from a source node to a target node. The relationship is **asymmetric**: `A → B` does not necessarily imply `B → A`.

```
(u, v) ≠ (v, u)   ← direction matters
```

### Real-World Example: Twitter Follow Graph

```
Alice ──→ Bob
  ↑         |
Carol ←── Dave
```

- Alice **follows** Bob, but Bob may **not follow** Alice back.
- Each arrow has a clear **source** and a clear **target**.

### When to Use
Use a directed graph when the **relationship is asymmetric** or has a direction:
- Twitter/Instagram follows (A follows B ≠ B follows A)
- Web links (page A links to page B ≠ page B links to page A)
- Money transfers (A pays B ≠ B pays A)
- Task dependencies (Task A must complete before Task B)

---

## 6. Weighted Graph

A **weighted graph** is a graph where each edge carries a **numeric value** called a **weight**. The weight quantifies the strength, cost, distance, or capacity of the relationship.

```
G = (V, E, w)
```

Where `w: E → ℝ` is a function assigning a real number to each edge.

### Real-World Example: Road Network (km)

```
Paris ——465km——→ Lyon
  |                 |
580km            315km
  |                 |
Bordeaux ←244km— Toulouse ←405km— Marseille
```

Each edge carries the **distance in kilometres** between two cities.

### Common Weight Meanings

| Domain | Weight Meaning |
|---|---|
| Road network | Distance or travel time |
| Social network | Interaction frequency or friendship strength |
| Financial network | Transaction amount |
| Text / NLP | Word co-occurrence count |
| Logistics | Shipping cost or capacity |

---

## 7. MultiGraph

A **MultiGraph** is an **undirected graph** that allows:
- **Multiple edges** between the same pair of nodes (called *parallel edges* or *multi-edges*)
- **Self-loops** (an edge from a node to itself)

```
G = (V, E)   where E is a multiset — the same pair can appear more than once
```

| Feature | Simple Graph | MultiGraph |
|---|---|---|
| Self-loops | ✅ Allowed | ✅ Allowed |
| Parallel edges | ❌ Not allowed | ✅ Allowed |
| Edge keys to distinguish parallel edges | ❌ No | ✅ Yes |

### Real-World Example: Transportation Network

```
Paris ═══════ London
       ║     ║
       rail  air
```

Between Paris and London there exist multiple distinct connections:
- A **train** route
- An **airplane** route  
- A **ferry** route (via Channel)

All three are separate edges between the same two nodes — a simple graph could only store one.

### When to Use a MultiGraph
- Two cities are connected by multiple roads or flight routes.
- Two people share multiple independent relationships (friend **and** colleague).
- Multiple financial transactions occur between the same two accounts.
- Chemical resonance structures require multiple bond types between the same atoms.

---

## 8. MultiDiGraph

A **MultiDiGraph** combines the properties of a **DiGraph** and a **MultiGraph**:
- Edges are **directed** (have a source and target)
- **Multiple directed edges** can exist between the same ordered pair of nodes
- **Self-loops** are allowed

### Real-World Example: Airline Network

```
Paris ──Lufthansa──→ Berlin
Paris ──Air France──→ Berlin
Paris ←──EasyJet───  Berlin
```

Between Paris and Berlin:
- Two different airlines fly **Paris → Berlin** (parallel directed edges)
- One airline flies **Berlin → Paris** (opposite direction)

A simple DiGraph could only store one edge per direction; a MultiDiGraph stores all of them.

---

## 9. Bipartite Graph

A **bipartite graph** is a graph whose nodes can be divided into **two disjoint sets** `A` and `B`, such that every edge connects a node in `A` to a node in `B`. **No edge connects two nodes within the same set.**

```
V = A ∪ B,   E ⊆ A × B
```

### Real-World Example: User–Movie Ratings

```
Set A (Users)      Set B (Movies)
Alice  ─────────── The Matrix
Alice  ─────────── Inception
Bob    ─────────── The Matrix
Carol  ─────────── Inception
```

- Users and movies are in **separate sets**.
- Edges only exist **between** users and movies (a rating relationship).
- No edge connects two users or two movies.

### Common Bipartite Applications
- User–product purchase networks (e-commerce)
- Author–paper networks (academic)
- Actor–film networks (cinema)
- Student–course enrollment

---

## 10. DAG — Directed Acyclic Graph

A **DAG** is a **directed graph** with **no directed cycles**. Starting from any node and following directed edges, it is **impossible to return** to the same node.

```
A → B → D
A → C → D → E
```

> No path loops back on itself.

### Real-World Examples

| Example | Nodes | Edges |
|---|---|---|
| Task dependencies | Tasks | "must be done before" |
| Git commit history | Commits | "parent of" |
| Taxonomies / ontologies | Categories | "is a sub-category of" |
| Build systems (Make, Gradle) | Build targets | "depends on" |
| Course prerequisites | Courses | "is a prerequisite for" |

### Key Properties
- Has a **topological ordering** (a linear ordering of nodes that respects all edge directions)
- Widely used in **scheduling**, **workflow** systems, and **machine learning** (computation graphs)

---

## 11. Hypergraph

A **hypergraph** generalises a graph by allowing an edge (called a **hyperedge**) to connect **more than two nodes** simultaneously.

```
Standard edge: (A, B)           — connects 2 nodes
Hyperedge:     (A, B, C, D)     — connects 4 nodes at once
```

### Real-World Example: Group Membership

- In a standard graph, you can only model pairwise relationships.
- In a hypergraph, a **single hyperedge** can represent an entire **project team**:

```
Hyperedge "Project Alpha" = {Alice, Bob, Carol, Dave}
```

All four people belong to the same project group — a relationship that cannot be faithfully represented by pairwise edges alone.

### Common Hypergraph Applications
- Research collaborations (a paper with N authors)
- Social groups or communities
- Chemical reactions (multiple reactants → multiple products)

---

## 12. Node Attribute

A **node attribute** is a **key–value pair** stored directly on a node. Attributes allow nodes to carry rich metadata about the entity they represent.

### Real-World Example: Academic Network

| Node | `age` | `department` | `role` |
|---|---|---|---|
| Alice | 30 | CS | Professor |
| Bob | 25 | CS | PhD Student |
| Carol | 28 | Math | Researcher |
| Dave | 32 | Physics | Professor |

Each node (person) carries additional information about who they are.

### Practical Uses
- Filter or colour nodes by category (e.g., all Professors in blue)
- Scale node size based on a numeric attribute (e.g., age, citation count)
- Run attribute-aware algorithms (e.g., find all nodes in the "CS" department)

---

## 13. Edge Attribute

An **edge attribute** is a **key–value pair** stored on an edge. Attributes allow edges to carry metadata about the relationship they represent.

### Real-World Example: Academic Collaboration Network

| Edge | `relation` | `papers` |
|---|---|---|
| Alice → Bob | supervises | — |
| Alice → Carol | collaborates | 3 |
| Bob → Carol | co-authors | 1 |
| Carol → Dave | collaborates | 2 |

### Common Edge Attributes

| Attribute | Meaning |
|---|---|
| `weight` | Strength, distance, or cost |
| `relation` | Type of relationship (friend, colleague, …) |
| `since` / `timestamp` | When the relationship began |
| `papers` | Number of joint publications |
| `amount` | Transaction value in financial graphs |
| `mode` | Transport mode (rail, air, road) |

---

## 14. Graph Attribute

A **graph attribute** is metadata stored on the **graph object itself** — not on any individual node or edge. It describes the graph as a whole.

### Real-World Example

A transportation network graph might carry:
- `name = "French Railway Network"`
- `year = 2026`
- `country = "France"`

### Difference from Node/Edge Attributes

| Scope | Stored on | Example |
|---|---|---|
| Graph attribute | The entire graph | `name`, `version`, `description` |
| Node attribute | A single node | `age`, `department` |
| Edge attribute | A single edge | `weight`, `relation` |

---

## 15. Degree

The **degree** of a node in an **undirected graph** is the **number of edges** connected to that node.

```
degree(v) = number of edges incident to v
```

### Real-World Example: Friendship Network

```
Alice ──── Bob ──── Dave
  │                  │
Carol ─────────────────
```

| Node | Connections | Degree |
|---|---|---|
| Alice | Bob, Carol | 2 |
| Bob | Alice, Dave | 2 |
| Carol | Alice, Dave | 2 |
| Dave | Bob, Carol | 2 |

A high-degree node is often called a **hub** — it is highly connected and typically plays a central role in the network.

---

## 16. In-Degree

The **in-degree** of a node in a **directed graph** is the **number of edges pointing INTO** that node (i.e., edges for which this node is the target).

```
in_degree(v) = number of edges (u → v)
```

### Real-World Example: Twitter Follow Graph

```
Dave ──→ Alice ←── Carol
Alice ──→ Bob
```

| Node | Who Points to It | In-Degree |
|---|---|---|
| Alice | Dave, Carol | 2 |
| Bob | Alice | 1 |
| Carol | — | 0 |
| Dave | — | 0 |

A high in-degree in a follow network = **popular account** (many people follow you).

---

## 17. Out-Degree

The **out-degree** of a node in a **directed graph** is the **number of edges pointing OUT FROM** that node (i.e., edges for which this node is the source).

```
out_degree(v) = number of edges (v → u)
```

### Real-World Example: Twitter Follow Graph

```
Alice ──→ Bob
Alice ──→ Carol
Dave ──→ Alice
```

| Node | Whom It Points To | Out-Degree |
|---|---|---|
| Alice | Bob, Carol | 2 |
| Dave | Alice | 1 |
| Bob | — | 0 |
| Carol | — | 0 |

A high out-degree = **active account** (follows many people).

---

## 18. Successor

In a **directed graph**, the **successors** of a node `v` are all nodes `u` such that there exists a **directed edge from `v` to `u`**.

```
successors(v) = { u | (v → u) ∈ E }
```

In other words, successors are the **direct neighbours reachable by following outgoing edges**.

### Real-World Example: Twitter

```
Alice ──→ Bob
Alice ──→ Carol
```

- Successors of **Alice** = {Bob, Carol}  (the accounts Alice follows)
- Successors of **Bob** = {} (Bob follows nobody)

---

## 19. Predecessor

In a **directed graph**, the **predecessors** of a node `v` are all nodes `u` such that there exists a **directed edge from `u` to `v`**.

```
predecessors(v) = { u | (u → v) ∈ E }
```

In other words, predecessors are the **direct neighbours that point into this node**.

### Real-World Example: Twitter

```
Carol ──→ Alice
Dave ──→ Alice
```

- Predecessors of **Alice** = {Carol, Dave}  (the accounts that follow Alice)
- Predecessors of **Dave** = {} (nobody follows Dave)

---

## 20. Self-Loop

A **self-loop** is an edge that connects a node **to itself**.

```
(A, A)   ← an edge from A back to A
```

### Real-World Examples
- A person who emails themselves (reminders).
- A web page that links to itself.
- In a knowledge graph: an entity that has a reflexive relation ("is related to itself").
- In a MultiGraph: representing a concept like "self-reflection" between two identical entities.

> **Note:** Self-loops are **allowed** in MultiGraphs and MultiDiGraphs, and in some simple graph implementations, but are typically excluded from "simple graph" definitions in pure mathematics.

---

## 21. Parallel Edges (Multi-edges)

**Parallel edges** (also called **multi-edges**) are two or more **distinct edges connecting the same pair of nodes**. Each parallel edge can carry **different attributes**.

```
A ═══ B      ← two separate edges exist between A and B
```

### Real-World Example: Airline Routes

Between **London** and **New York**:
- British Airways flight (economy class)
- British Airways flight (business class)  
- Virgin Atlantic flight

All three are real, distinct connections — three parallel edges between the same two cities.

### Why It Matters
A **simple graph** would collapse all these into a single edge, losing the distinction. A **MultiGraph** preserves each one individually, along with its specific attributes (airline, class, price, departure time).

---

## 22. Edge Key

In a **MultiGraph** or **MultiDiGraph**, an **edge key** is a **unique identifier** that distinguishes parallel edges between the same pair of nodes.

```
(A, B, key=0)   ← first edge between A and B
(A, B, key=1)   ← second (parallel) edge between A and B
(A, B, key=2)   ← third (parallel) edge between A and B
```

Keys are typically **integers** assigned automatically (starting from 0), but can also be **custom strings** for better readability.

### Real-World Example

```
(Paris, London, key="rail")   → the train route
(Paris, London, key="air")    → the airplane route
(Paris, London, key="ferry")  → the ferry route
```

Using descriptive keys makes it easy to access a specific connection without confusion.

---

## 23. Path

A **path** is a sequence of nodes `v₁, v₂, ..., vₙ` where each consecutive pair `(vᵢ, vᵢ₊₁)` is connected by an edge, and **no node appears more than once**.

```
Alice → Bob → Dave → Eve    ← a valid path
```

### Related Terms

| Term | Definition |
|---|---|
| **Walk** | A sequence of nodes connected by edges; nodes/edges may repeat |
| **Trail** | A walk where **edges** do not repeat (nodes may) |
| **Path** | A trail where **nodes** do not repeat |
| **Cycle** | A path that starts and ends at the same node |
| **Shortest path** | The path between two nodes with the fewest edges (or lowest total weight) |

### Real-World Example: Navigation

The **shortest path** from your home to the office avoids revisiting the same intersection twice and minimises total distance — that is a shortest path in a weighted graph.

---

## 24. Adjacency

Two nodes `u` and `v` are **adjacent** (or **neighbours**) if there exists at least one edge directly connecting them.

```
u and v are adjacent ⟺ (u, v) ∈ E
```

### Real-World Example: Social Network

```
Alice ──── Bob ──── Carol
```

- Alice and Bob are **adjacent** (direct friends).
- Alice and Carol are **NOT adjacent** (they only share a friend in common — Bob).

### Adjacency Matrix

An **adjacency matrix** `A` of a graph with `n` nodes is an `n × n` matrix where:

```
A[i][j] = 1   if node i and node j are connected
A[i][j] = 0   otherwise
```

For the example above:

|  | Alice | Bob | Carol |
|---|---|---|---|
| **Alice** | 0 | 1 | 0 |
| **Bob** | 1 | 0 | 1 |
| **Carol** | 0 | 1 | 0 |

---

## Quick Reference Table

| Concept | Symbol / Notation | Key Property |
|---|---|---|
| Graph | G = (V, E) | Nodes + Edges |
| Undirected Graph | (u,v) = (v,u) | Symmetric relationships |
| Directed Graph (DiGraph) | (u,v) ≠ (v,u) | Asymmetric relationships |
| Weighted Graph | w: E → ℝ | Each edge has a numeric value |
| MultiGraph | E is a multiset | Parallel edges allowed (undirected) |
| MultiDiGraph | Directed + parallel edges | Parallel directed edges allowed |
| Bipartite Graph | V = A ∪ B, E ⊆ A × B | Two-part structure |
| DAG | Directed, no cycles | Used in scheduling & workflows |
| Hypergraph | Hyperedges connect >2 nodes | Group relationships |
| Node attribute | node[key] = value | Metadata on a node |
| Edge attribute | edge[key] = value | Metadata on an edge |
| Graph attribute | G.graph[key] = value | Metadata on the whole graph |
| Degree | deg(v) | Edges connected to v (undirected) |
| In-degree | in_deg(v) | Edges pointing INTO v |
| Out-degree | out_deg(v) | Edges pointing OUT FROM v |
| Successor | u where v → u | Outgoing neighbours of v |
| Predecessor | u where u → v | Incoming neighbours of v |
| Self-loop | (v, v) | Edge from node to itself |
| Parallel edge | Multiple (u,v) | Same pair, multiple edges |
| Edge key | (u,v,key) | Distinguishes parallel edges |
| Path | v₁ → v₂ → … → vₙ | No repeated nodes |
| Adjacency | (u,v) ∈ E | Two nodes directly connected |
