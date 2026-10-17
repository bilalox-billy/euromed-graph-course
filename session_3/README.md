# Session 3 — Property Graphs with Neo4j

This lab connects Python to a **Neo4j** graph database and seeds it with a small e-commerce property graph, then runs a product-recommendation query against it.

---

## 📁 Folder Structure

```
session_3/
│
├── src/
│   ├── load.py            ← Main script: seeds the graph & runs the query
│   └── neo4j_config.py    ← Reads connection settings from .env
│
├── neo4j-lab/
│   └── cypher/
│       ├── constraints.cypher          ← Uniqueness constraints
│       ├── query.cypher                ← Recommendation query
│       ├── nodes/
│       │   ├── categories.cypher
│       │   ├── customers.cypher
│       │   ├── orders.cypher
│       │   └── products.cypher
│       └── relationships/
│           ├── belongs_to.cypher
│           ├── contains.cypher
│           ├── placed.cypher
│           ├── similar_to.cypher
│           └── subcategory_of.cypher
│
├── pdf_course/            ← Session slides (PDF)
└── README.md             

---

## Prerequisites

### 1 — Neo4j Running Locally

You need a running **Neo4j instance** before executing any Python code.

**Option A — Neo4j Desktop (recommended for beginners)**
1. Download and install **Neo4j Desktop** from:  
   👉 https://neo4j.com/download/
2. Open Neo4j Desktop → create a **New Project** → add a **Local DBMS**
3. Set a password you will remember, then click **Start**
4. Your local database is now reachable at `bolt://localhost:7687`

**Option B — Neo4j AuraDB (free cloud instance)**
1. Sign up for free at:  
   👉 https://neo4j.com/cloud/platform/aura-graph-database/
2. Create a **Free instance**, copy the connection URI and credentials shown at creation time

---

### 2 — Python Dependencies

All dependencies are managed by `uv` at the project root. From the **project root folder** (`euromed-graph-course/`), run:

```bash
uv sync
```

This installs everything including the `neo4j` driver and `python-dotenv`.

---

## Configuration — Set Up Your `.env` File

The script reads your Neo4j credentials from a `.env` file located at the **project root**.

1. At the project root, copy the example file:

```bash
cp .env.example .env
```

2. Open `.env` and fill in your values:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j
```

| Variable | Description | Default |
|---|---|---|
| `NEO4J_URI` | Connection URI to your Neo4j instance | `bolt://localhost:7687` |
| `NEO4J_USERNAME` | Your Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | The password you set when creating the database | — |
| `NEO4J_DATABASE` | Database name | `neo4j` |

> **Never commit your `.env` file** — it is already listed in `.gitignore`.

---

## Running the Script

From the **project root**, run:

```bash
uv run python session_3/src/load.py
```

### Expected output

```
  Constraints:
    constraints.cypher
  Nodes:
    categories.cypher
    customers.cypher
    orders.cypher
    products.cypher
  Relationships:
    belongs_to.cypher
    contains.cypher
    placed.cypher
    similar_to.cypher
    subcategory_of.cypher
✓ Seed graph created successfully

--- Alice's Recommendations ---
  Wireless Headphones ($49.99) — bought by 2 similar customer(s)
  ...
```

---

## Explore the Graph in Neo4j Browser

After running the script, open Neo4j Browser to visually explore what was loaded:

- **Neo4j Desktop:** click **Open** → **Neo4j Browser**
- **AuraDB:** go to your instance dashboard → **Open with Neo4j Browser**

Try these Cypher queries to get started:

```cypher
-- See everything (limit to 50 nodes)
MATCH (n) RETURN n LIMIT 50

-- See all customers and their orders
MATCH (c:Customer)-[:PLACED]->(o:Order) RETURN c, o

-- See the full schema
CALL db.schema.visualization()
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `AuthError` | Check your `NEO4J_PASSWORD` in `.env` |
| `ServiceUnavailable` | Make sure Neo4j is running and `NEO4J_URI` is correct |
| `ModuleNotFoundError: neo4j` | Run `uv sync` from the project root |
| `FileNotFoundError` on a `.cypher` file | Make sure you run the script from the **project root**, not from inside `session_3/src/` |
| `.env not found` | Place your `.env` file at the project root, not inside `session_3/` |
