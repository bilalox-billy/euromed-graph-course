# Mini-Project — Wikipedia Topic Graph

## Phase 1 · Knowledge Graph Systems

| | |
|---|---|
| **Estimated time** | 3–4 hours |
| **Work mode** | Individual or pairs |
| **Deliverables** | 1 Jupyter Notebook + 1 Report (PDF or Markdown, max 4 pages) |
| **Due** | End of Week 2 |

---

## Project Overview

> Build a **topic knowledge graph** from 200 Wikipedia articles, analyze its structure, identify key concepts, and produce a publication-quality visualization.


You will apply all the skills from session_1 and session_2 — graph construction, NLP preprocessing, centrality analysis, community detection, and visualization — in one cohesive end-to-end pipeline.

### Pipeline Summary

```
Wikipedia articles
        ↓
  NLP preprocessing (named entity recognition + keyword extraction)
        ↓
  Three graphs: Article Similarity · Entity Co-occurrence · Keyword Co-occurrence
        ↓
  Graph analysis: centrality · communities · path analysis
        ↓
  Visualizations: static dashboard · interactive graph
        ↓
  Insight report
```

---

## Part 1 — Data Collection

### 1.1 Choose a Domain

Select **one domain** from the table below. If you would like to propose a different topic, you must get instructor approval first.

| Option | Domain | Suggested Seed Articles |
|---|---|---|
| **A** | Artificial Intelligence | Artificial intelligence, Machine learning, Deep learning, Neural network, Natural language processing |
| **B** | Biomedical | Cancer, DNA, Protein, Immune system, Vaccine |
| **C** | History & Politics | World War II, United Nations, Democracy, Cold War, European Union |
| **D** | Science & Physics | Quantum mechanics, Relativity, Black hole, Particle physics, Thermodynamics |
| **E** | Technology Companies | Google, Apple Inc., Microsoft, Amazon, Meta Platforms |

### 1.2 Crawl Wikipedia

Using the `wikipedia-api` Python library, perform a **BFS (Breadth-First Search) crawl** starting from your seed articles:

- Collect a minimum of **150 articles**, targeting **200**
- For each article, store the **first 1 000 words** of the article text
- Follow up to **15–20 linked pages** per article during the BFS expansion
- Respect a polite crawl rate (add a short delay between requests)
- Save the collected corpus to a **JSON file** so you do not need to re-crawl

**Expected output:** A JSON file mapping each article title to its text.

---

## Part 2 — Graph Construction

Build **three complementary graphs** from your corpus. Each graph captures a different level of semantic relationship.

### 2.1 Article Similarity Graph (Document-level)

- Represent each Wikipedia article as a **TF-IDF vector**
- Compute **cosine similarity** between every pair of articles
- Add an edge between two articles if their similarity exceeds a chosen **threshold** (e.g. 0.12 — justify your choice)
- Edge weight = cosine similarity score
- Nodes = article titles; Node attributes = article metadata

**Questions to address:**
- What threshold did you choose and why?
- How does changing the threshold affect graph density?

### 2.2 Entity Co-occurrence Graph (Sentence-level)

- Use **spaCy** to extract **named entities** from each article (focus on types: PERSON, ORG, GPE, PRODUCT, WORK_OF_ART, EVENT)
- Two entities are connected if they **appear in the same sentence**
- Edge weight = number of times they co-occur
- Node attributes = entity type, number of articles the entity appears in
- Filter the graph to keep only entities that appear in **at least 2 articles** and have **degree ≥ 2**

**Questions to address:**
- How many unique entities were extracted before filtering? After?
- Which entity types dominate your domain?

### 2.3 Keyword Co-occurrence Graph (Word-level)

- Extract meaningful tokens from all articles (alphabetic, length ≥ 4, not stop words)
- Two words are connected if they appear within a **sliding window** of 5 words in the same article
- Edge weight = number of times the pair co-occurs across all articles
- Keep only edges with weight **≥ 5** (or a threshold you justify)

**Questions to address:**
- How does window size affect the graph structure?
- What do the top keywords reveal about the domain?

---

## Part 3 — Graph Analysis

For each of the three graphs, compute the following. The **Entity Co-occurrence Graph** is your main focus.

### 3.1 Structural Analysis

Compute and report these metrics for all three graphs:

| Metric | Description |
|---|---|
| Number of nodes and edges | Size of the graph |
| Density | Proportion of possible edges that exist |
| Number of connected components | Is the graph fully connected? |
| Largest connected component (LCC) size | How much of the graph is reachable? |
| Average degree | Typical connectivity of a node |
| Diameter (of the LCC) | Maximum shortest path length |
| Average clustering coefficient | Tendency to form triangles |
| Average shortest path length (of the LCC) | Typical distance between nodes |

### 3.2 Centrality Analysis

On the **Entity Co-occurrence Graph**, compute the following centrality measures and report the **top 10 nodes** for each:

| Centrality | What it measures |
|---|---|
| **Degree centrality** | How many direct connections a node has |
| **Betweenness centrality** | How often a node lies on the shortest path between others |
| **Closeness centrality** | How quickly a node can reach all other nodes |
| **PageRank** | Importance based on the importance of its neighbours |

For each measure, explain **why the top entities rank highly** in the context of your chosen domain.

### 3.3 Community Detection

Apply **two community detection algorithms** to the Entity Co-occurrence Graph:

1. **Greedy Modularity** — finds communities by maximising modularity
2. **Louvain algorithm** — better suited to weighted graphs

For each algorithm, report:
- Number of communities detected
- Size of the top 5 communities
- Top 5 representative entities per community
- Whether the communities correspond to meaningful semantic sub-topics

### 3.4 Path Analysis — Six Degrees of Separation

Select the **10 highest-degree entities** in the largest connected component of the Entity Graph and:

- Find the **shortest path** between at least 6 pairs of these entities
- Report the path length and the intermediate nodes along each path
- Discuss whether your domain shows "small-world" behaviour (short average distances despite large size)

---

## Part 4 — Visualization

Produce two types of visualizations using the **Entity Co-occurrence Graph** as your primary subject.

### 4.1 Static Dashboard (matplotlib)

Create a **2×2 panel figure** containing:

| Panel | Content |
|---|---|
| Top-left | Entity network — nodes coloured by community, sized by PageRank |
| Top-right | Degree distribution histogram |
| Bottom-left | Horizontal bar chart of top 15 entities by PageRank |
| Bottom-right | Bar chart of community sizes |

Requirements:
- All panels must have clear **titles, axis labels, and a legend** where applicable
- Only label the **top 15 nodes by PageRank** in the network panel (to avoid clutter)
- Save the figure as `miniproject_dashboard.png` at 150 dpi or higher

### 4.2 Interactive Graph (pyvis)

Create an interactive HTML visualization of the entity graph:

- Node **colour** = entity type (PERSON, ORG, GPE, etc. — use a consistent colour scheme)
- Node **size** = PageRank score (scaled to a readable range)
- Node **tooltip** = entity name, type, degree, number of articles, PageRank score
- Edge **width** = co-occurrence weight (capped at a maximum for readability)
- Save as `miniproject_interactive.html`

The interactive graph should be **explorable** — a reader should be able to hover over nodes and zoom into communities.

---

## Part 5 — Insight Report

Write a **maximum 4-page report** (PDF or Markdown) structured as follows:

### Section 1 · Data Collection *(~0.5 pages)*

- How many articles did you collect? Which seed topics did you use?
- What is the average article length in words?
- What percentage of articles fall in the largest connected component of the article graph?

### Section 2 · Graph Statistics *(~1 page)*

Fill in the following comparison table from your Part 3 results:

| Metric | Article Graph | Entity Graph | Keyword Graph |
|---|---|---|---|
| Nodes | | | |
| Edges | | | |
| Density | | | |
| # Components | | | |
| Avg Degree | | | |
| Avg Clustering Coefficient | | | |

Then discuss:
- Which graph is the most sparse? Which is the most clustered? Why?
- What do these structural differences tell us about how these three graph types represent knowledge?

### Section 3 · Key Findings *(~1.5 pages)*

Answer **all** of the following questions:

1. Who are the **top 5 most important entities** by PageRank in your domain? Why are they central?
2. How many communities were detected? Do they correspond to meaningful sub-topics you can name?
3. What is the average shortest path between any two top-10 entities? Does your graph show small-world behaviour?
4. Was there any **unexpected entity** in the top 10 by any centrality measure? Explain.
5. Do the Greedy Modularity and Louvain algorithms agree on community assignments? Where do they differ?

### Section 4 · Visualization Analysis *(~0.5 pages)*

- Include your dashboard image and a screenshot of the interactive graph
- What does the community colouring reveal about the structure of your domain?
- Which layout or visual encoding was most informative, and why?

### Section 5 · Reflection *(~0.5 pages)*

- What are the **limitations** of co-occurrence graphs as knowledge representations?
- What information is **lost** in co-occurrence that would be preserved in a proper knowledge graph with typed relations?
- How would a **dependency-parsed graph** (Subject–Predicate–Object triples) improve upon what you built?

---

## Submission Checklist

Submit a single folder (or zip file) named `miniproject_<your_name>/` containing:

- [ ] `miniproject.ipynb` — clean, fully executed Jupyter notebook (all cells run, no errors)
- [ ] `wikipedia_articles.json` — the collected corpus
- [ ] `miniproject_dashboard.png` — the 4-panel static analysis figure
- [ ] `miniproject_interactive.html` — the interactive pyvis graph
- [ ] `entity_centrality_results.csv` — centrality scores table exported from the notebook
- [ ] `report.pdf` or `report.md` — the 4-page insight report
- [ ] *(Bonus)* any additional files for the bonus task (see below)

> ⚠️ **The notebook must be clean**: restart the kernel and run all cells from top to bottom before submitting. Remove any debug print statements.

---

## Grading Rubric

| Criterion | Weight | What We Look For |
|---|---|---|
| **Data Collection** | 15% | ≥ 150 articles collected, saved, and inspected |
| **Graph Construction** | 25% | All 3 graphs built correctly with justified parameters |
| **Analysis** | 30% | Centrality, communities, and paths computed and interpreted — not just reported |
| **Visualization** | 15% | Clear, labeled, publication-quality figures |
| **Report Quality** | 15% | Concise, answers all required questions, shows genuine understanding |

**Bonus (+10%):** Build a **4th graph** — a bipartite graph connecting articles to their top-10 keywords (extracted using any method covered in class). Project this bipartite graph onto the article layer to produce an article similarity graph, and compare it with the TF-IDF similarity graph from Part 2.1. Are the groupings consistent? Where do they disagree?

---

## References

You are expected to cite relevant sources in your report. The following are a starting point:

- **Wikipedia API Python library** — https://wikipedia-api.readthedocs.io/
- **Mihalcea & Tarau (2004)** — *TextRank: Bringing Order into Text* — https://aclanthology.org/W04-3252/
- **Blondel et al. (2008)** — *Fast unfolding of communities in large networks* (Louvain) — https://doi.org/10.1088/1742-5468/2008/10/P10008
- **Clauset, Newman & Moore (2004)** — *Finding community structure in very large networks* — https://doi.org/10.1103/PhysRevE.70.066111
- **Milgram (1967)** — *The Small World Problem* (six degrees of separation) — https://doi.org/10.1037/e400002009-005
- **Barabási & Albert (1999)** — *Emergence of scaling in random networks* — https://doi.org/10.1126/science.286.5439.509
- **NetworkX community algorithms** — https://networkx.org/documentation/stable/reference/algorithms/community.html

---

*For any questions, open an issue on the course repository or contact your instructor before the deadline.*
