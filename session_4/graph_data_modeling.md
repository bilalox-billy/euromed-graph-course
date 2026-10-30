# Graph Data Modeling Fundamentals

> **Based on:** [Neo4j GraphAcademy — Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals)  
> **Estimated time:** 2–3 hours  
> **Prerequisites:** Cypher Fundamentals (`cypher_fundamentals.md`)

---

> *"A model is a hypothesis. The data is the experiment. The query is the test."*

---

## Table of Contents

- [Module 1 — Building a Domain Graph](#module-1--building-a-domain-graph)
  - [Lesson 1: What Is Graph Data Modeling?](#lesson-1-what-is-graph-data-modeling)
  - [Lesson 2: The Golden Rule](#lesson-2-the-golden-rule)
  - [Lesson 3: Modeling Nodes](#lesson-3-modeling-nodes)
  - [Lesson 4: Modeling Relationships](#lesson-4-modeling-relationships)
  - [Lesson 5: Coming from a Relational Model](#lesson-5-coming-from-a-relational-model)
- [Module 2 — Testing and Refactoring the Model](#module-2--testing-and-refactoring-the-model)
  - [Lesson 1: Why Test a Model?](#lesson-1-why-test-a-model)
  - [Lesson 2: The Four Types of Questions](#lesson-2-the-four-types-of-questions)
  - [Lesson 3: Five Refactoring Patterns](#lesson-3-five-refactoring-patterns)
- [Module 3 — From Domain Graph to Knowledge Graph](#module-3--from-domain-graph-to-knowledge-graph)
  - [Lesson 1: Lexical Graphs](#lesson-1-lexical-graphs)
  - [Lesson 2: Entity Graphs](#lesson-2-entity-graphs)
  - [Lesson 3: Ontologies](#lesson-3-ontologies)
  - [Lesson 4: The Three Layers Together](#lesson-4-the-three-layers-together)
- [Modeling Decision Reference](#modeling-decision-reference)
- [Exercises](#exercises)

---

## Module 1 — Building a Domain Graph

---

### Lesson 1: What Is Graph Data Modeling?

Graph data modeling is the process of **translating your domain — and the questions your application needs to ask about it — into nodes, relationships, and properties.**

It is not a one-time activity. A first model captures what you know today. It gets refined as new questions arrive, new parts of the domain emerge, and real data is tested against it.

#### The Iterative Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    Model your         Check against       Refine: add a         │
│    domain        →    a real question  →  node, relationship, ──┤
│                                           or property           │
│                            ↑                                    │
│                            └──── next question ────────────────┘
│
└─────────────────────────────────────────────────────────────────┘
```

The payoff for doing this deliberately — rather than letting a model grow by accident — shows up later:

- Queries follow **direct relationships** instead of reconstructing them at read time
- The model **stays extensible** as new requirements arrive
- Refactoring is **targeted**, not from scratch

#### Why Not Design It All Up Front?

You cannot anticipate every question your application will ask. The best models are grown, not designed — each question you test teaches you something the diagram never could.

---

### Lesson 2: The Golden Rule

> **Every part of a graph model should follow one pattern:**
>
> ```
> (Noun) -[:VERB]-> (Noun)
> ```

| Part | Role | Example |
|---|---|---|
| Node | A **noun** — a thing in your domain | `Person`, `Movie`, `Order` |
| Relationship | A **verb** — what one thing does to another | `ACTED_IN`, `PLACED`, `BELONGS_TO` |

#### Reading Your Model Out Loud

Read any relationship in your model as a sentence. If it makes sense, the direction is right:

```
✅  (Alice)       -[:WATCHED]->   (Inception)       → "Alice watched Inception"
✅  (Tom Hanks)   -[:ACTED_IN]->  (Forrest Gump)    → "Tom Hanks acted in Forrest Gump"
❌  (Forrest Gump)-[:ACTED_IN]->  (Tom Hanks)       → "Forrest Gump acted in Tom Hanks" ✗
```

If the sentence sounds wrong, the direction is wrong. Fix it now — direction is much cheaper to reverse in a model than in a populated database.

#### Anchor Nodes

Not every noun in your domain carries equal weight. An **anchor node** is one your questions keep returning to — the node most paths in your model start from.

| Domain | Anchor Nodes |
|---|---|
| Movie recommendations | `Person`, `Movie` |
| E-commerce | `Customer`, `Order` |
| Manufacturing | `Part`, `Supplier` |
| Banking | `Account`, `Transaction` |

A query usually begins by matching an anchor node, then traverses outward to reach the answer:

```cypher
-- Starts at Movie (anchor) → reaches Genre
MATCH (m:Movie {title: "Forrest Gump"})-[:IN_GENRE]->(g:Genre)
RETURN g.name

-- Starts at Person (anchor) → reaches Movie
MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m:Movie)
RETURN m.title
```

`Genre` and `User` are reached — they are not directly matched. They exist to answer questions about anchor nodes.

---

### Lesson 3: Modeling Nodes

#### From Domain Description to Nodes

The **nouns** in a plain-language description of your domain become your nodes.

**Movie recommendations domain:**
> *"A movie has a title and a release year. People act in and direct movies. Movies belong to genres."*

→ Nodes: `Movie`, `Person`, `Genre`

**Retail domain:**
> *"A customer places orders. Orders contain products."*

→ Nodes: `Customer`, `Order`, `Product`

#### Labels — Classifying Your Nodes

A **label** categorizes a node. A node can carry **multiple labels**.

```
Tom Hanks  →  :Person         (everyone in the domain)
           →  :Person:Actor   (has acted in something)
           →  :Person:Director (has directed something)
```

Why does this matter?

```cypher
-- Without specific labels: must check every Person's relationships
MATCH (p:Person)-[:DIRECTED]->()
RETURN p.name

-- With a specific label: no relationship scan needed
MATCH (d:Director)
RETURN d.name
```

Specific labels make queries faster and more expressive.

#### Properties — Facts About a Node

A **property** is a key–value pair attached to a node. Neo4j supports:

| Type | Example |
|---|---|
| String | `title: "Forrest Gump"` |
| Integer | `released: 1994` |
| Float | `rating: 8.8` |
| Boolean | `available: true` |
| Date | `createdAt: date("2024-01-15")` |
| List | `genres: ["Drama", "Romance"]` |

#### The Critical Decision: Property or Node?

This is the most important modeling judgment you will make. Use this decision tree:

```
Is the attribute a simple fact that only describes one thing?
│
├── YES → Keep it as a PROPERTY on the node
│         Example: Movie.released = 1994
│
└── NO → Ask: does it connect to many nodes,
│        have its own properties, or need
│        to be queried independently?
│
         ├── YES → Promote it to a NODE
         │         Example: Genre — many movies share it,
         │         you query "all movies in Drama"
         │
         └── NO → Keep it as a property
```

**Side-by-side comparison:**

| Attribute | Stays as Property | Promoted to Node |
|---|---|---|
| `released` (year) | ✅ — only describes the movie | ❌ — no reason to query years independently |
| `language` | ❌ — many movies share it; rename in one place | ✅ — `(:Language {name: "English"})` |
| `genre` | ❌ — shared across many movies | ✅ — `(:Genre {name: "Drama"})` |
| `runtime` | ✅ — simple fact about one movie | ❌ — no need to query runtimes independently |

#### Unique Properties and Constraints

Some properties **identify** a node — no two nodes with the same label should share that value.

```cypher
-- Create a uniqueness constraint
CREATE CONSTRAINT FOR (m:Movie) REQUIRE m.movieId IS UNIQUE;

-- Node key: combination of properties that is unique together
CREATE CONSTRAINT FOR (ol:OrderLine) REQUIRE (ol.orderId, ol.product) IS NODE KEY;
```

> 💡 A uniqueness constraint also creates an **index** automatically — lookups by that property stay fast as your data grows.

---

### Lesson 4: Modeling Relationships

#### Direction

A relationship's direction should match how you would naturally say it as a sentence:

```
✅  (Tom Hanks)   -[:ACTED_IN]->  (Forrest Gump)
❌  (Forrest Gump)-[:ACTED_IN]->  (Tom Hanks)
```

When Cypher queries traverse a relationship, direction matters for performance — store it once in the natural direction.

#### Relationship Properties

A relationship can carry its own properties — use them when a fact **belongs to the connection itself**, not to either node alone:

```
(Tom Hanks)-[:ACTED_IN {role: "Forrest Gump", salary: 500000}]->(Forrest Gump the movie)
```

- `role` is not Tom Hanks's property (he plays different roles in different movies)
- `role` is not the movie's property (the movie has many roles)
- `role` belongs to **this specific connection** — the actor in this movie

#### Symmetric Relationships

Some relationships are inherently symmetric:

```
(Inception)-[:SIMILAR_TO]->(The Matrix)
```

If `Inception` is similar to `The Matrix`, then `The Matrix` is similar to `Inception`. **Store it once in either direction** and query without specifying direction:

```cypher
MATCH (m:Movie {title: "Inception"})-[:SIMILAR_TO]-(other:Movie)
RETURN other.title
```

Not every symmetric-looking relationship is actually symmetric:

```
(Christopher Nolan)-[:INFLUENCED_BY]->(Stanley Kubrick)
```

Influence does not automatically run both ways — this must be stated explicitly.

#### Inferred vs. Stored Relationships

| Type | Description | Example |
|---|---|---|
| **Inferred** | Derived from existing structure without a direct relationship | Co-starring actors share a `ACTED_IN` connection through `Movie` |
| **Indirect** | Answered by traversing through intermediate nodes | Person's genres: `Person → ACTED_IN → Movie → IN_GENRE → Genre` |
| **Materialized** | Stored directly as an explicit relationship | `(Alice)-[:CO_STARRED_WITH]->(Robin)` — created once, read many times |

#### When to Materialize a Connection

```
Ask the connection frequently and the path is expensive?
│
├── YES → Materialize it as a direct relationship
│         Store CO_STARRED_WITH once; avoid the join on every profile load
│
└── NO → Leave it as an indirect or inferred connection
          A person appears in a handful of movies → genres are cheap to reach
```

---

### Lesson 5: Coming from a Relational Model

If you already have a relational database, here is the conceptual mapping:

| Relational Concept | Graph Equivalent |
|---|---|
| Table | Node label |
| Row | Node |
| Column | Node property |
| Foreign key | Relationship |
| JOIN table | Intermediate node or relationship with properties |
| Primary key | Unique property + constraint |
| Index | Index on a property |

**Relational model:**

```
PERSON table          REVIEW table            MOVIE table
id: 1, name: Alice    person_id: 1,           id: 9, title: Inception
                      movie_id: 9, rating: 5
```

Finding Alice's rating of Inception requires **two joins** through `REVIEW`.

**Graph model:**

```
(Alice:Person)-[:RATED {rating: 5}]->(Inception:Movie)
```

The connection **is** the structure — no join needed at query time.

---

## Module 2 — Testing and Refactoring the Model

---

### Lesson 1: Why Test a Model?

> *"Labels, properties, and relationships are decisions about shape — they don't prove the model works."*

A model that looks correct on a diagram is still just a hypothesis. Testing it means:

1. Adding a small amount of **real-looking sample data**
2. Writing the **actual questions** the model is supposed to answer as Cypher queries
3. Running them and checking whether the results are correct

You don't need a full production dataset. A handful of nodes and relationships is enough to expose:
- A property under the wrong name
- A relationship pointing the wrong direction
- A missing node or relationship type entirely

#### Minimal Sample Data to Seed Your Model

```cypher
-- Create sample nodes
MERGE (:Person {name: "Tom Hanks",   born: 1956})
MERGE (:Person {name: "Robin Wright", born: 1966})
MERGE (:Movie  {title: "Forrest Gump", released: 1994, movieId: "fg001"})
MERGE (:Movie  {title: "Cast Away",    released: 2000, movieId: "ca001"})
MERGE (:Genre  {name: "Drama"})

-- Create sample relationships
MATCH (p:Person {name: "Tom Hanks"}),   (m:Movie {title: "Forrest Gump"})
MERGE (p)-[:ACTED_IN {role: "Forrest Gump"}]->(m)

MATCH (p:Person {name: "Robin Wright"}), (m:Movie {title: "Forrest Gump"})
MERGE (p)-[:ACTED_IN {role: "Jenny Curran"}]->(m)

MATCH (m:Movie {title: "Forrest Gump"}), (g:Genre {name: "Drama"})
MERGE (m)-[:IN_GENRE]->(g)
```

Now run your questions and check the output — if anything is wrong, fix it here with 10 nodes, not later with 10 million.

---

### Lesson 2: The Four Types of Questions

Every question your use case needs answered falls into one of four categories. Recognizing the category tells you what modeling decision it's testing.

---

#### 🔍 Type 1 — Lookup and Retrieval

**Pattern:** Find one specific thing by a known value.

```cypher
MATCH (m:Movie {title: "Forrest Gump"})
RETURN m
```

**What it tests:** Whether the right property is indexed or marked unique.
**Modeling signal:** If this is slow, add a uniqueness constraint or index on that property.

---

#### 🔗 Type 2 — Connection Questions

**Pattern:** How do two things relate to each other?

```cypher
-- Which genres has Tom Hanks appeared in?
MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m:Movie)-[:IN_GENRE]->(g:Genre)
RETURN DISTINCT g.name
```

**What it tests:** Whether the right relationships and intermediate nodes exist.
**Modeling signal:** If the path is missing, you need a new relationship or node. If the path is too expensive, consider materializing it.

---

#### 📊 Type 3 — Aggregation and Ranking

**Pattern:** Summarize or rank across many things.

```cypher
-- Top 10 highest-rated movies
MATCH (m:Movie)<-[r:RATED]-()
RETURN m.title, avg(r.rating) AS avgRating
ORDER BY avgRating DESC
LIMIT 10
```

**What it tests:** Whether aggregated values should be precomputed and stored directly on a node.
**Modeling signal:** If this query is run on every page load, store `avgRating` directly on `Movie` and update it when new ratings arrive.

---

#### 🌐 Type 4 — Traversal and Recommendation

**Pattern:** Reach things through a chain of connections.

```cypher
-- Movies similar to Forrest Gump (through shared genres and actors)
MATCH (m:Movie {title: "Forrest Gump"})-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(similar:Movie)
WHERE similar <> m
RETURN similar.title, count(g) AS sharedGenres
ORDER BY sharedGenres DESC
LIMIT 5
```

**What it tests:** Whether the model has hub nodes or shortcut relationships to avoid fan-out.
**Modeling signal:** If this traversal explodes into too many intermediate matches, introduce a hub node or a precomputed shortcut relationship.

---

### Lesson 3: Five Refactoring Patterns

When a question exposes a gap, one (or more) of these five patterns fixes it.

---

#### Pattern 1 — Add a Specific Label

**Problem:** A query filters `Person` nodes by whether they directed something — on every run.

**Before:**
```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
WHERE p.name STARTS WITH 'C'
RETURN p.name, m.title
```

This scans all `Person` nodes, then filters. With millions of people, this is slow.

**Refactor:** Add a `Director` label to people who directed something.

```cypher
MATCH (p:Person)-[:DIRECTED]->()
SET p:Director
```

**After:**
```cypher
MATCH (d:Director)
WHERE d.name STARTS WITH 'C'
RETURN d.name
```

The label narrows the candidate set **before** traversing a single relationship. `Person` still applies — nothing is lost.

---

#### Pattern 2 — Extract a Hub Node

**Problem:** A relationship property (`rating`) has grown beyond what a property can carry — it needs its own identity, its own properties, and its own relationships.

**Before:**
```
(User)-[:RATED {rating: 5, text: "Masterpiece"}]->(Movie)
```

A rating on a relationship cannot be liked, commented on, or shared by other users.

**Refactor:** Promote the rating to a `Review` node.

```
(User)-[:WROTE]->(Review)-[:REVIEWS]->(Movie)
                  |
                  +--> [:LIKED_BY]->(User)
```

**After:**
```cypher
-- Other users can now like a review
MATCH (u:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(m:Movie {title: "Forrest Gump"})
OPTIONAL MATCH (r)<-[:LIKED_BY]-(liker:User)
RETURN r.text, r.rating, count(liker) AS likes
```

---

#### Pattern 3 — Normalize a Property into a Node

**Problem:** A property value (`language: "English"`) is repeated across thousands of nodes. Renaming it requires updating every node.

**Before:**
```
(:Movie {title: "Forrest Gump", language: "English"})
(:Movie {title: "Cast Away",    language: "English"})
(:Movie {title: "Amélie",       language: "French"})
```

**Refactor:** Extract `language` into a shared `Language` node.

```cypher
MATCH (m:Movie) WHERE m.language IS NOT NULL
MERGE (l:Language {name: m.language})
MERGE (m)-[:IN_LANGUAGE]->(l)
REMOVE m.language
```

**After:**
```cypher
-- Find all English-language movies
MATCH (l:Language {name: "English"})<-[:IN_LANGUAGE]-(m:Movie)
RETURN m.title
```

Renaming "English" to "en" now touches **one node**, not thousands.

---

#### Pattern 4 — Precompute an Aggregate

**Problem:** A query that scans and averages all ratings for a movie runs on every page load.

**Before:**
```cypher
MATCH (m:Movie {title: "Forrest Gump"})<-[r:RATED]-()
RETURN avg(r.rating) AS avgRating
```

With millions of ratings, this is expensive on every request.

**Refactor:** Store `avgRating` directly on the `Movie` node and update it when new ratings arrive.

```cypher
-- Store the precomputed average
MATCH (m:Movie {title: "Forrest Gump"})<-[r:RATED]-()
WITH m, avg(r.rating) AS avg
SET m.avgRating = avg

-- Now reads are instant
MATCH (m:Movie {title: "Forrest Gump"})
RETURN m.avgRating
```

---

#### Pattern 5 — Add a Shortcut Relationship

**Problem:** A two-hop path is used on every profile page load.

**Before:**
```cypher
-- "Which actors has this person worked with?"
MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(co:Person)
RETURN co.name, count(m) AS sharedMovies
```

This traverses every Tom Hanks movie and all actors in each.

**Refactor:** Precompute and store `CO_STARRED_WITH` directly.

```cypher
-- Create shortcut relationships (run once, or on new data)
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(b:Person)
WHERE id(a) < id(b)
MERGE (a)-[:CO_STARRED_WITH]->(b)
```

**After:**
```cypher
-- One hop instead of two
MATCH (p:Person {name: "Tom Hanks"})-[:CO_STARRED_WITH]-(co:Person)
RETURN co.name
```

#### Refactoring Decision Map

```
Question is slow or the model can't answer it → Which pattern?
│
├── Query filters a label by relationship existence?
│   └── Pattern 1: Add a specific label (Director, Actor, ...)
│
├── Relationship property needs its own properties or relationships?
│   └── Pattern 2: Extract a hub node (Review, Transaction, ...)
│
├── Property value is repeated across many nodes?
│   └── Pattern 3: Normalize into a shared node (Language, Category, ...)
│
├── Aggregation recomputed on every read?
│   └── Pattern 4: Precompute and store on the node (avgRating, totalOrders, ...)
│
└── Multi-hop path traversed on every read?
    └── Pattern 5: Add a shortcut relationship (CO_STARRED_WITH, ...)
```

---

## Module 3 — From Domain Graph to Knowledge Graph

---

> *A domain graph knows that a review exists. A knowledge graph knows what the review says, who is mentioned in it, and how those entities connect to everything else.*

---

### Lesson 1: Lexical Graphs

Everything you have modeled so far describes **structured facts**: a person acted in a movie, a customer placed an order. But real use cases often involve **unstructured content** — reviews, plot summaries, support tickets, reports — that does not reduce to a clean set of properties.

A **lexical graph** brings that content into the model by representing it as graph structure rather than a text blob.

#### Step 1 — Chunking

The first step is splitting a document into pieces small enough to reason about individually. Each chunk becomes its own node:

```
"Tom Hanks was incredible in this role, and the ending still gets me every time."
         │
         ▼
┌─────────────────────────────────────┐     ┌────────────────────────────────────────┐
│ Chunk 1                             │────▶│ Chunk 2                                │
│ "Tom Hanks was incredible in        │     │ "...and the ending still gets me       │
│  this role..."                      │     │  every time."                          │
└─────────────────────────────────────┘     └────────────────────────────────────────┘
         │                                           │
         └───────────────────┬───────────────────────┘
                             │
                      (:Review {id: "r1"})
```

```cypher
-- Model a document with its chunks
MERGE (r:Review {id: "r1", text: "..."})
MERGE (c1:Chunk {id: "r1_c1", text: "Tom Hanks was incredible in this role..."})
MERGE (c2:Chunk {id: "r1_c2", text: "...and the ending still gets me every time."})
MERGE (r)-[:CONTAINS]->(c1)
MERGE (r)-[:CONTAINS]->(c2)
MERGE (c1)-[:NEXT]->(c2)
```

#### Step 2 — Hierarchical Structure

For longer content with sections and headings, model the hierarchy directly:

```
(:Document)
    │
    ├──[:HAS_SECTION]──▶ (:Section {title: "Plot"})
    │                           │
    │                    ├──[:CONTAINS]──▶ (:Chunk)
    │                    └──[:CONTAINS]──▶ (:Chunk)
    │
    └──[:HAS_SECTION]──▶ (:Section {title: "Reception"})
                                │
                         └──[:CONTAINS]──▶ (:Chunk)
```

This lets a query target a specific section instead of scanning the entire document.

#### Why Chunks Instead of Full Text?

| Full-text blob | Lexical graph |
|---|---|
| Can only ask "does this review exist?" | Can ask "what does this review say about Tom Hanks?" |
| Cannot locate where something is mentioned | Can find the exact chunk and its context |
| Cannot link content to other graph nodes | Chunks connect directly to entity nodes |
| Cannot reason about order or structure | `[:NEXT]` relationships preserve sequence |

---

### Lesson 2: Entity Graphs

A **lexical graph** tells you where text lives. An **entity graph** tells you **who and what** is mentioned inside that text — and connects them to each other and to your domain graph.

#### Entity Extraction

Named entities are extracted from each chunk using NLP (spaCy, an LLM, or another tool). The same entity mentioned in multiple chunks resolves to **one node**:

```
Chunk 1: "Tom Hanks was incredible..."
Chunk 2: "...reminds me of his work in Cast Away..."

         ↓ extract entities ↓

(:Person {name: "Tom Hanks"})       ← one node, not two
(:Movie  {name: "Cast Away"})
```

#### Connecting Mentions Back to Text

```cypher
MERGE (p:Person {name: "Tom Hanks"})
MERGE (c1:Chunk {id: "r1_c1"})
MERGE (c1)-[:MENTIONS]->(p)

MERGE (c2:Chunk {id: "r1_c2"})
MERGE (c2)-[:MENTIONS]->(p)
```

Tom Hanks is mentioned twice, but he is still one node. The `[:MENTIONS]` relationships carry the connection from both chunks back to the same person.

#### Entities That Don't Yet Exist in the Domain Graph

When NLP extracts a new entity from text that **does not exist anywhere in the domain graph**, it becomes a new node:

```
Text: "...the ending, set in Savannah, moved me deeply."

→ (:Location {name: "Savannah"})   ← new node, not previously in the graph
→ (:Theme {name: "Redemption"})    ← new node, extracted as a concept
```

This is what makes a question like **"which reviews discuss redemption as a theme?"** or **"which actors filmed in Savannah?"** answerable — the entity graph created these nodes from unstructured text.

#### Domain, Lexical, and Entity Layers: A Connected Example

```
DOMAIN GRAPH
(Tom Hanks:Person)-[:ACTED_IN]->(Forrest Gump:Movie)

LEXICAL GRAPH
(Review r1)-[:CONTAINS]->(Chunk c1)-[:NEXT]->(Chunk c2)

ENTITY GRAPH
(Chunk c1)-[:MENTIONS]->(Tom Hanks:Person)   ← same Tom Hanks node as domain graph
(Chunk c2)-[:MENTIONS]->(Savannah:Location)
(Tom Hanks:Person)-[:FILMED_IN]->(Savannah:Location)  ← extracted from text
```

`Tom Hanks` is **one node across all three layers**. A single query can move from the structured domain fact (`ACTED_IN`) to the text that mentions him (`MENTIONS`) to a new fact extracted from that text (`FILMED_IN`) — in one traversal, without leaving the graph.

---

### Lesson 3: Ontologies

As a model grows — more contributors, more domains, automated processes writing to the graph — consistency becomes a real problem. An **ontology** is the agreed vocabulary that solves it.

> *An ontology isn't the data itself. It's the rules for what's allowed to exist and how it fits together.*

#### The Problem It Solves

Without an ontology, two contributors — or two LLM calls — can produce:

```
(:Location {name: "Savannah"})   ← added by contributor A
(:Place    {name: "Nashville"})  ← added by contributor B
```

A query for `(:Location)` will never find Nashville. A query for `(:Place)` will never find Savannah. The model silently fragments.

With an ontology: **`Location` is the agreed label**. Both nodes use it. Every query finds both.

#### Type Hierarchies

An ontology arranges labels from general to specific. Specific types inherit the identity of their general parent:

```
Person
├── Actor        (every Actor is a Person)
└── Director     (every Director is a Person)
```

```cypher
-- A node can carry all applicable labels
MERGE (p:Person:Actor:Director {name: "Clint Eastwood"})

-- Queries at any level in the hierarchy still work
MATCH (p:Person  {name: "Clint Eastwood"}) RETURN p  -- ✅ found
MATCH (a:Actor   {name: "Clint Eastwood"}) RETURN a  -- ✅ found
MATCH (d:Director{name: "Clint Eastwood"}) RETURN d  -- ✅ found
```

The hierarchy makes this a **deliberate rule** — not a coincidence from two labels being applied to the same node.

#### A Shared Vocabulary

An ontology settles naming before it becomes a problem:

| Question | Without ontology | With ontology |
|---|---|---|
| Customer or Client? | Both exist, queries miss half | `Customer` — one label |
| Movie or Film? | Both exist | `Movie` — one label |
| Location or Place? | Both exist | `Location` — one label |

Established vocabularies like [Schema.org](https://schema.org) define standard types for `Person`, `Movie`, `Organization`, and more — borrowing them gives you interoperability with external data for free.

#### Ontologies and GenAI Applications

When a **large language model** extracts entities from text and writes them into your graph, nothing stops it from calling the same kind of place `Location` one run and `Place` the next — unless you give it a fixed vocabulary.

```
Without ontology:
  Run 1: (:Location {name: "Savannah"})
  Run 2: (:Place    {name: "Nashville"})  ← LLM chose a different label

With ontology (fixed schema passed to the LLM):
  Run 1: (:Location {name: "Savannah"})
  Run 2: (:Location {name: "Nashville"})  ← consistent
```

The same fixed vocabulary matters for **querying** the graph with an LLM. A GenAI application generating Cypher against your graph — to answer a natural-language question — can rely on labels staying the same across every part of the graph, rather than guessing which of several near-identical types the data actually landed under.

---

### Lesson 4: The Three Layers Together

The domain graph, lexical graph, and entity graph are not three separate models. They are **three layers of the same model**, connected to each other through shared nodes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1 — DOMAIN GRAPH                                                     │
│                                                                             │
│  (Tom Hanks:Person) ─[:ACTED_IN]─▶ (Forrest Gump:Movie)                   │
│                                            │                                │
│                                     [:IN_GENRE]                             │
│                                            ▼                                │
│                                      (Drama:Genre)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                      │                           │
              [:MENTIONED_IN]              [:MENTIONED_IN]
                      │                           │
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAYER 2 — LEXICAL GRAPH                                                    │
│                                                                             │
│  (Review r1) ─[:CONTAINS]─▶ (Chunk c1) ─[:NEXT]─▶ (Chunk c2)             │
│                                  │                       │                  │
│                           [:MENTIONS]             [:MENTIONS]               │
│                                  │                       │                  │
└──────────────────────────────────┼───────────────────────┼──────────────────┘
                                   │                       │
┌──────────────────────────────────┼───────────────────────┼──────────────────┐
│  LAYER 3 — ENTITY GRAPH          │                       │                  │
│                                  ▼                       ▼                  │
│  (Tom Hanks:Person) ─[:FILMED_IN]─▶ (Savannah:Location)                   │
│                                                                             │
│    ↑ same Tom Hanks node as Layer 1                                        │
│      ↑ new node — extracted from text, did not exist in the domain graph   │
└─────────────────────────────────────────────────────────────────────────────┘
```

A single query can now cross all three layers:

```cypher
-- "Which reviews mention Tom Hanks, and what new locations did they surface?"
MATCH (p:Person {name: "Tom Hanks"})
MATCH (c:Chunk)-[:MENTIONS]->(p)
MATCH (r:Review)-[:CONTAINS]->(c)
MATCH (c)-[:MENTIONS]->(loc:Location)
RETURN r.id, collect(loc.name) AS locationsDiscovered
```

This query starts from a structured domain fact (`Person`), dives into unstructured content (`Chunk`), and surfaces newly extracted knowledge (`Location`) — all in one traversal.

---

## Modeling Decision Reference

### Property vs. Node

| Signal | Decision |
|---|---|
| Only describes one thing | Property |
| Shared by many nodes | Node |
| Has its own properties | Node |
| Queried independently | Node |
| Simple scalar value | Property |

### Relationship vs. Intermediate Node

| Signal | Decision |
|---|---|
| Simple fact about a connection | Relationship property |
| Needs its own properties | Hub node |
| Needs its own relationships | Hub node |
| Needs unique identity | Hub node |

### Store vs. Compute

| Signal | Decision |
|---|---|
| Aggregation run occasionally | Compute at query time |
| Aggregation run on every page load | Precompute on node |
| Two-hop traversal rarely needed | Leave indirect |
| Two-hop traversal on every request | Materialize as shortcut relationship |

### Property vs. Shortcut Relationship for Domain Concepts

| Signal | Decision |
|---|---|
| Fact unique to one node | Property |
| Fact shared / repeated across nodes | Normalize to node |
| Connection needs identity | Hub node |
| Connection accessed in many paths | Shortcut relationship |

---

## Exercises

Work through these in Neo4j Browser against a dataset of your choice (`:play movies` to use the Movies dataset).

### Exercise Set 1 — Model a New Domain

Choose one of these domains and build a domain graph from scratch:

**Option A — Spotify-style Music Platform**
> Artists release albums. Albums contain tracks. Users create playlists. Playlists contain tracks. Users follow artists and other users.

**Option B — University Course System**
> Students enroll in courses. Courses are taught by professors. Courses belong to departments. Courses may have prerequisites.

**Option C — Hospital Network**
> Patients are admitted to hospitals. Doctors treat patients. Treatments use medications. Medications belong to drug categories.

For your chosen domain:
1. List all the **nouns** → candidate nodes
2. List all the **verbs** → candidate relationships
3. Identify **anchor nodes**
4. Decide which attributes are **properties** vs. **nodes**
5. Write Cypher to create a sample dataset (at least 5 of each node type, 10 relationships)

### Exercise Set 2 — Test Your Model

Write one question of each type against your model from Exercise 1:

1. A **lookup** question (find one specific thing)
2. A **connection** question (how two things relate)
3. An **aggregation** question (summarize across many things)
4. A **traversal** question (reach things through a chain)

Run each as a Cypher query. If any query returns nothing or wrong results, identify the gap and fix the model.

### Exercise Set 3 — Apply Refactoring Patterns

Using the Movies dataset:

1. **Pattern 1 (Specific label):** Add a `Director` label to all `Person` nodes who have a `DIRECTED` relationship. Then rewrite a query to use `(:Director)` instead of `(:Person)-[:DIRECTED]->()`.

2. **Pattern 2 (Hub node):** The `RATED` relationship has a `rating` property. Extract it into a `Review` node. Rewrite the "average rating" query to use the new model.

3. **Pattern 3 (Normalize):** Many `Movie` nodes have a `languages` property. Extract it into `Language` nodes with `IN_LANGUAGE` relationships.

4. **Pattern 4 (Precompute):** Compute the average rating for each movie and store it as `avgRating` on the `Movie` node. Compare query time before and after.

5. **Pattern 5 (Shortcut):** Create `CO_STARRED_WITH` relationships between actors who appeared in the same movie. Use `id(a) < id(b)` to avoid duplicates.

### Exercise Set 4 — Knowledge Graph Extension

Starting from your domain graph built in Exercise 1:

1. Add a **lexical layer**: create a `Document` node (a review, report, or description), split it into `Chunk` nodes with `[:CONTAINS]` and `[:NEXT]` relationships.
2. Add an **entity layer**: manually extract 3–5 entities from the text and create `[:MENTIONS]` relationships from chunks to entities.
3. Write a query that crosses all three layers: start from a domain node, traverse to a chunk, and return the entities mentioned.
4. Identify two labels in your model that could benefit from an **ontology** (a type hierarchy). Define the hierarchy and apply it.

---

## 📚 Further Reading

| Resource | Link |
|---|---|
| GraphAcademy — Graph Data Modeling Fundamentals | https://graphacademy.neo4j.com/courses/modeling-fundamentals |
| GraphAcademy — Cypher Fundamentals | https://graphacademy.neo4j.com/courses/cypher-fundamentals |
| Neo4j Graph Data Modeling Guide | https://neo4j.com/docs/getting-started/data-modeling/ |
| Schema.org — Standard Vocabularies | https://schema.org |
| Neo4j Ontology & Knowledge Graph Blog | https://neo4j.com/blog/knowledge-graph/ |
| Cypher Refactoring Patterns | https://neo4j.com/developer/graph-database/ |

---

*Previous: `cypher_fundamentals.md` — Cypher query language*
*Next: `TP_Property_Graph_Skills_Jobs_Profiles.md` — Design a real Skills–Jobs–Profiles property graph*
