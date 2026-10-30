# Practical Project (TP): Design and Query a Skills–Jobs–Profiles Property Graph

**Course:** Property Graphs and Graph Data Modeling  
**Level:** Undergraduate advanced / Master's (adaptable)  
**Suggested duration:** 3–4 lab sessions of 2 hours plus independent work  
**Team:** 2–3 students  
**Technology:** Neo4j + Cypher (or another labeled property graph DB, with equivalent queries)  
**Project type:** Requirements analysis → competency questions → conceptual modeling → graph implementation → querying → reflection

> **Important:** This is an *open-ended design exercise*. There is no single perfect graph schema. Your grade depends on whether your design answers the questions, respects the business rules, and is justified with evidence—not on the number of nodes and relationships.

---

## 1. Context: TalentBridge, a Recruiting Platform

TalentBridge is a fictional recruitment platform used by companies to publish jobs, candidates to maintain professional profiles, and recruiters to shortlist suitable candidates. Today, information is scattered across spreadsheets and forms. The company wants to build a **property graph** to find candidates by skills, experience, geography and job requirements, and to explain *why* a candidate matches a job.

TalentBridge gives your team the following stakeholder statements:

1. A candidate may have several skills; the same skill appears in many profiles and job ads.
2. A candidate may know Python at an advanced level, but only have beginner-level Docker experience.
3. A job can require some skills and merely prefer others. A candidate missing a preferred skill should not be excluded.
4. We want to know **where and when** someone used a skill, not just see a checkbox.
5. Candidates may work at multiple companies over time, sometimes in overlapping or freelance roles.
6. Recruiters should explain which required skills match and which are missing.
7. 'ML', 'machine learning', and 'Machine Learning' may refer to the same skill; 'Java' and 'JavaScript' do not.
8. Some jobs allow remote work; others are onsite in a particular city.
9. A candidate can apply to the same job, withdraw, and possibly reapply. We need a history of those actions.
10. Do not invent candidate competencies. If a skill claim has not been verified, it must be distinguishable from verified evidence.

### 1.1 Your mission

Design and implement a **labeled property graph (LPG)** that addresses the requirements. Begin with the business questions the graph must answer, *then* decide which things deserve nodes, relationships, or properties. Finally, populate the graph, write Cypher queries, and explain your trade-offs.

### 1.2 Scope

**In scope:** Candidate profiles, skills, skill proficiency, evidence of skills, work experience, organizations, jobs, requirements, applications, recruiter searches, locations, and data quality.  
**Out of scope:** Real authentication systems, production-scale CV parsing, salaries/payroll, discrimination-sensitive candidate ranking, production UI, and external recommendation APIs.

**Privacy rule:** Work only with fictional data. Do not use real candidate personal information.

---

## 2. Learning Objectives

By the end of the project you should be able to:

- Translate natural-language business requirements into testable **competency questions (CQs)**.
- Identify potential entities, relationships and attributes, and explain when to model each as a **node, relationship or property**.
- Build an LPG with meaningful labels, relationship directions, properties, IDs and constraints.
- Represent properties of a relationship (e.g., proficiency, requirement priority), and recognize when a relationship needs to become a **first-class node** (e.g., an application with multiple events).
- Model many-to-many relationships and time-aware facts.
- Express graph questions in Cypher and validate answers against test data.
- Evaluate model quality using query coverage, data integrity, extensibility, and explainability.

---

## 3. Phase A: From Requirements to Competency Questions

A **competency question** expresses something the final graph must be able to answer. It is *not* a Cypher query yet. Read each CQ and identify (i) the concepts needed, (ii) their relationships/attributes, (iii) any assumptions or missing business definitions.

### 3.1 Required competency questions

| ID | Competency question | Priority |
|---|---|---|
| CQ-01 | What skills does a given candidate claim, and what is the proficiency level of each? | Must |
| CQ-02 | Which candidates possess **all mandatory skills** for a given job? | Must |
| CQ-03 | Which candidates satisfy at least 2 of 3 mandatory skills for a job, and which mandatory skills are missing? | Must |
| CQ-04 | Which open jobs require Python and prefer Docker? | Must |
| CQ-05 | What work experiences support a candidate's claim of a particular skill? | Must |
| CQ-06 | Which companies has a candidate worked for, in which roles, and during what periods? | Must |
| CQ-07 | Which candidates are suitable for remote jobs but not available for onsite work in the job's city? | Should |
| CQ-08 | For each job, how many applicants applied, withdrew, or reapplied? | Should |
| CQ-09 | Which candidate skill claims are unverified or lack evidence? | Must |
| CQ-10 | Which skill names/aliases resolve to one canonical skill, without confusing distinct skills? | Must |
| CQ-11 | Which candidates have used Python in a job or project within the last 2 years? | Should |
| CQ-12 | For a given candidate and job, explain the match: met mandatory requirements, unmet mandatory requirements, and matched preferred skills. | Must |

**Stretch CQs** (choose at least two):

- **CQ-13:** Which candidates have worked with both a programming language and a graph database in the **same project**?
- **CQ-14:** Which job requirements have changed over time, and which version was in force when a candidate applied?
- **CQ-15:** Which jobs have no suitable candidates under a clearly defined matching rule?
- **CQ-16:** Which recruiters reviewed an application and what decisions did they make, with timestamps?

### 3.2 Student tasks

1. Create a **CQ analysis matrix** with columns: `CQ ID`, `business intent`, `required graph facts`, `likely traversal`, `ambiguities`, `validation test`.
2. Rewrite **two ambiguous CQs** in more precise, testable language.
3. Define the meaning of **"suitable"** (distinguish hard requirements from soft preferences).
4. Add **three new competency questions** that are useful to TalentBridge and not duplicates of the above.
5. Prioritize the CQs, and justify the priorities in 3–5 sentences.

**Checkpoint A:** The instructor must be able to trace each important model element to at least one CQ or business rule.

---

## 4. Phase B: Make Modeling Decisions Before Writing Cypher

Do **not** start with code. For every item below, choose one or more of: **node**, **property**, **relationship**, or **relationship property**. In some cases, you may need an **intermediate node** to model a complex business object. Document your reasoning.

### 4.1 Decision challenge

| Business concept / information | Questions your design must answer |
|---|---|
| Candidate's name | Does the name need its own identity and connections, or is it an attribute? |
| Skill: `Python` | Is it shared by candidates and jobs? Does it need aliases or categories? |
| Candidate's proficiency in Python | Is proficiency intrinsic to the candidate, intrinsic to Python, or specific to *their relationship*? |
| Job requirement for Python | How will you record **mandatory vs. preferred**, and a minimum proficiency level? |
| Company | Does the same employer appear in many work histories and jobs? |
| Job title | When is a title just text, and when might a reusable role taxonomy be valuable? |
| Work experience | How do you attach role, employer, start/end dates and skill usage to *one particular employment period*? |
| City / location | Would a city need to be reused across candidates, job ads and organizations? |
| Remote-work preference | Is it a profile attribute, a separate entity, or a relationship attribute? What information must it carry? |
| Application | Can you represent multiple applications and their status changes without losing history? |
| Skill alias | How will `ML` map to `Machine Learning`, and how will you prevent false merging? |
| Proof of skill | How will you connect certifications, projects or work experiences to a *specific skill claim*? |
| Verification status | Does status apply to the candidate, the skill, the claim, or a particular piece of evidence? |

### 4.2 Required model design decisions

For **at least eight** rows from the table, complete a decision record:

```text
Concept: Candidate proficiency in Python
Options considered: property on Candidate; property on Skill;
                    property on relationship; separate assessment node
Decision: [your choice]
CQs supported: [IDs]
Justification: [why this representation works]
Trade-off: [what becomes harder?]
Example: [small graph pattern]
```

**Discussion prompts (answer in your report):**

- When does a **property** become a **node**? Provide two concrete examples from this project.
- When is a **relationship property** sufficient, and when should an association become a **node**?
- Is duplicating a skill name on every job and candidate a good idea? Why or why not?
- Should `Job`, `JobPosting` and `JobRole` be the same concept? Decide for the current scope.
- How will your design distinguish *unknown*, *not verified*, and *verified false*?
- What is your policy for missing dates, open-ended employment periods, and duplicate data?

**Checkpoint B:** Submit a hand-drawn or digital conceptual graph and a one-page design rationale **before implementing the database**.

---

## 5. Phase C: Design the Graph Schema

You are responsible for the schema. The lists below are *candidates to evaluate*, **not** an answer key and **not** mandatory node labels.

**Potential concepts:** Candidate, Profile, Skill, SkillCategory, Alias, Organization, Job, Location, WorkExperience, Project, Certification, Application, ApplicationEvent, Recruiter, SkillAssessment, Evidence.

**Potential connections:** claims skill, requires skill, prefers skill, employed by, worked on, demonstrated skill in, located in, published by, applied to, reviewed by, supported by evidence.

### 5.1 Minimum schema specification

Include:

1. A **diagram** with node labels, relationship types and directions, major properties, and cardinalities.
2. A **schema dictionary**: meaning of each label/relation/property, data type, whether required, allowed values, and uniqueness rules.
3. A stable **ID strategy** for nodes (do not use display names as universal IDs).
4. At least **three constraints** (e.g., uniqueness or existence where supported) and **two useful indexes**, explaining the queries they help.
5. An explicit strategy for **time** (employment periods, job status, application history).
6. An explicit strategy for **skill normalization**, **evidence**, and **provenance**.

**Reminder:** Neo4j labels do not automatically create a formal ontology. Your schema documentation defines the intended business meaning.

---

## 6. Phase D: Starter Dataset

Use the following **synthetic input records** as source material. **These are not graph tables to copy directly**: transform them according to your own model. You may add attributes, relationships and intermediate entities where justified.

### 6.1 Candidates

| Candidate ID | Name | Home city | Remote available | Onsite cities |
|---|---|---|---|---|
| C01 | Amina Idrissi | Rabat | Yes | Rabat, Casablanca |
| C02 | Youssef Karim | Casablanca | Yes | Casablanca |
| C03 | Sara Haddad | Fez | Yes | Fez |
| C04 | Omar Naji | Rabat | No | Rabat |
| C05 | Lina Faris | Marrakech | Yes | Marrakech, Rabat |
| C06 | Adam Benali | Casablanca | No | Casablanca |

### 6.2 Canonical skills and aliases

| Skill ID | Canonical label | Category | Known aliases |
|---|---|---|---|
| S01 | Python | Programming | Python 3 |
| S02 | Cypher | Query language | Neo4j Cypher |
| S03 | Neo4j | Graph database | Neo4j DB |
| S04 | Docker | DevOps | Docker Engine |
| S05 | Machine Learning | AI | ML, machine learning |
| S06 | SQL | Query language | Structured Query Language |
| S07 | Java | Programming | Java SE |
| S08 | JavaScript | Programming | JS |
| S09 | RDF | Knowledge representation | Resource Description Framework |

### 6.3 Candidate skill claims

Level scale: **1 = beginner**, **2 = intermediate**, **3 = advanced**. `Verified` means independent evidence was checked; `Unverified` means there is a claim without completed verification. Verification is **not equivalent to proficiency**.

| Candidate | Skill | Level | Verification |
|---|---|---|---|
| C01 | S01 | 3 | Verified |
| C01 | S03 | 3 | Verified |
| C01 | S02 | 2 | Verified |
| C01 | S04 | 1 | Unverified |
| C02 | S01 | 2 | Verified |
| C02 | S06 | 3 | Verified |
| C02 | S04 | 3 | Verified |
| C03 | S01 | 3 | Verified |
| C03 | S05 | 3 | Verified |
| C03 | S04 | 2 | Unverified |
| C04 | S07 | 3 | Verified |
| C04 | S08 | 2 | Verified |
| C05 | S01 | 3 | Verified |
| C05 | S09 | 3 | Verified |
| C05 | S03 | 2 | Unverified |
| C06 | S06 | 3 | Verified |
| C06 | S08 | 3 | Verified |

### 6.4 Organizations and job ads

| Org ID | Organization | City |
|---|---|---|
| O01 | Atlas Data Labs | Rabat |
| O02 | NorthStar Analytics | Casablanca |
| O03 | GraphWorks | Marrakech |

| Job ID | Title | Organization | Mode | Onsite city | Status |
|---|---|---|---|---|---|
| J01 | Graph Data Engineer | O01 | Hybrid | Rabat | Open |
| J02 | ML Engineer | O02 | Remote | — | Open |
| J03 | Data Analyst | O02 | Onsite | Casablanca | Open |
| J04 | Knowledge Graph Specialist | O03 | Remote | — | Closed |

**Interpretation for this project:** `Remote` jobs do not require an onsite city; `Onsite` jobs require availability in their city; `Hybrid` jobs also require availability in their city. You may critique this simplified rule, but must apply it consistently in the required queries.

### 6.5 Job requirements

| Job | Skill | Mandatory? | Minimum level |
|---|---|---|---|
| J01 | S01 | Yes | 2 |
| J01 | S03 | Yes | 2 |
| J01 | S02 | Yes | 2 |
| J01 | S04 | No | 1 |
| J02 | S01 | Yes | 3 |
| J02 | S05 | Yes | 2 |
| J02 | S04 | No | 2 |
| J03 | S06 | Yes | 3 |
| J03 | S01 | No | 2 |
| J04 | S09 | Yes | 2 |
| J04 | S03 | Yes | 2 |

**Matching rule for baseline tests:** A mandatory skill is met when the candidate has a *verified* skill claim with level **at least** the minimum. A preferred skill contributes to explanation but does not affect mandatory eligibility. The geography rule is separate from the skill rule. Closed jobs cannot accept new applications.

### 6.6 Work experiences and evidence

| Experience ID | Candidate | Organization | Role | Start | End | Skills used |
|---|---|---|---|---|---|---|
| E01 | C01 | O01 | Graph Developer | 2024-01-01 | 2025-12-31 | S01, S03, S02 |
| E02 | C02 | O02 | Data Engineer | 2023-03-01 | — | S01, S06, S04 |
| E03 | C03 | O02 | ML Intern | 2025-01-01 | 2025-10-31 | S01, S05 |
| E04 | C04 | O01 | Backend Developer | 2022-02-01 | 2024-09-30 | S07, S08 |
| E05 | C05 | O03 | KG Consultant | 2025-06-01 | — | S01, S09 |
| E06 | C06 | O02 | BI Analyst | 2024-06-01 | — | S06, S08 |

Each `Skills used` cell means that the experience is **potential evidence** for that skill. Students must decide how to model the connection and whether such evidence is sufficient to justify `Verified` status. **Do not silently derive verification from employment.**

### 6.7 Applications and events

| Event ID | Candidate | Job | Timestamp (UTC) | Event |
|---|---|---|---|---|
| AEV01 | C01 | J01 | 2026-09-01T09:00:00Z | Applied |
| AEV02 | C02 | J01 | 2026-09-02T10:30:00Z | Applied |
| AEV03 | C02 | J01 | 2026-09-04T11:00:00Z | Withdrawn |
| AEV04 | C02 | J01 | 2026-09-06T08:00:00Z | Reapplied |
| AEV05 | C03 | J02 | 2026-09-07T09:00:00Z | Applied |
| AEV06 | C06 | J03 | 2026-09-07T13:00:00Z | Applied |

**History requirement:** Preserve the original events and their timestamps; do not overwrite the event sequence with only the latest status. You decide how to identify application attempts and whether `Reapplied` starts a new attempt.

### 6.8 Dataset extension

Create **at least 4 additional candidates, 2 organizations, 3 jobs, 5 skills, 5 experiences, 8 skill claims and 6 application events**. Include one intentionally tricky case from each category:

- Duplicate display names but different IDs.
- One skill alias that could be incorrectly merged.
- One person with overlapping work experiences.
- One mandatory skill claim that is unverified.
- One reapplication or status reversal.

Record your added synthetic data in CSV or Cypher and explain your assumptions.

---

## 7. Phase E — Implementation in Neo4j

Create your graph using reproducible Cypher scripts. Organize your work as follows:

```text
team-XX-talentbridge/
├── README.md
├── requirements-and-cqs.md
├── modeling-decisions.md
├── schema-dictionary.md
├── graph-model.png                 # or .svg / .drawio
├── data/
│   ├── source-data.csv             # or multiple normalized CSVs
│   └── assumptions.md
├── cypher/
│   ├── 01_constraints_indexes.cypher
│   ├── 02_load_data.cypher
│   ├── 03_cq_queries.cypher
│   └── 04_validation.cypher
└── report.md
```

**Implementation requirements:**

- Scripts must run on a **fresh, empty database**, in the listed order.
- Use stable IDs and `MERGE` where appropriate to avoid duplicate entities on reruns.
- Include `CREATE CONSTRAINT` and `CREATE INDEX` statements supported by your Neo4j edition/version.
- Store dates as temporal values where supported, not inconsistent free text.
- Use parameterized example queries when reasonable (e.g., `$candidateId`, `$jobId`).
- Document any assumptions about missing values, aliases and verification.
- Do not hard-code CQ answer lists; compute answers from graph traversals.

### 7.1 Illustrative Cypher *syntax only* (not a schema solution)

```cypher
// Replace this generic example with your own justified model.
MERGE (t:Topic {id: 'T001'})
SET t.label = 'Example topic';

MATCH (t:Topic {id: $topicId})
RETURN t.id, t.label;
```

---

## 8. Phase F: Querying and Test-Driven Evaluation

Implement **CQ-01 through CQ-12** in `03_cq_queries.cypher`. Prefix each query with its CQ ID and 1–2 sentences explaining the intended output.

For each CQ, provide:

1. **Cypher query**.
2. **Expected columns** (e.g., candidate ID, job ID, missing skill, evidence).
3. **Expected result** for at least one hand-checked fixture.
4. **One negative/edge test**: what must *not* be returned?
5. **A short explanation** of the traversal and relevant filters.

### 8.1 Required baseline assertions

These are **tests**, not instructions to choose any specific graph structure.

- For **J01**, C01 meets its three mandatory *skill* requirements (Python, Neo4j, Cypher); C02 does not. Geography must be assessed separately.
- For **J02**, C03 meets both mandatory *skill* requirements. C01 does not meet the Machine Learning requirement.
- For **J03**, C02 and C06 meet the mandatory SQL skill requirement; under the given onsite-city rule, both can satisfy the location criterion.
- For **J04**, C05's RDF claim is verified but its Neo4j claim is **unverified**, so it must **not** qualify as meeting all mandatory skill requirements; J04 is closed in any case.
- For **C02/J01**, the application history must reveal **Applied → Withdrawn → Reapplied** in timestamp order.
- A search for canonical **Machine Learning** must handle the alias **ML**; a query for **Java** must not automatically match **JavaScript**.

### 8.2 Quality and performance checks

- Check that no canonical skills have accidental duplicate IDs.
- Check that a job does not accidentally have two conflicting active requirements for the same skill (unless your schema deliberately supports versioning).
- Check that no application event points to a nonexistent candidate or job.
- Demonstrate rerunning ingestion without doubling node counts.
- Use `EXPLAIN` (and optionally `PROFILE`) for **two queries**. Explain how an index or a query rewrite could help, without claiming production benchmarks on this small dataset.

---

## 9. Phase G: Model Review and Change Request

After your first implementation, TalentBridge sends a change request:

> "We now want to track a candidate's **skill proficiency over time**. Someone could be beginner in 2024 and advanced in 2026. We also need to know **who assessed the skill**, the assessment date, and its evidence. A candidate can disagree with an assessment."

**Tasks:**

1. Identify which assumptions in your original schema no longer hold.
2. Propose a **minimal schema evolution** that preserves history.
3. Draw a **before/after subgraph** for one candidate's Python skill.
4. Add one CQ about historical proficiency and write its Cypher query.
5. Explain whether an assessment is best modeled as a property, relationship with properties, or node **in your evolved design**.
6. Document how existing data is migrated or interpreted, including unknown assessor/date values.

**Do not delete older claims or assessments simply to keep the latest value.**

---

## 10. Deliverables and Submission

Submit a single ZIP file named `team-XX-talentbridge.zip` containing the repository structure from Section 7.

**Main report** (recommended 8–12 pages excluding code) should contain:

1. Concise requirements summary and assumptions.
2. CQ analysis matrix and three additional CQs.
3. Conceptual diagram and final physical LPG schema.
4. Eight or more **node/relationship/property decision records**.
5. Schema dictionary, identity rules, temporal rules and provenance approach.
6. Data-loading instructions and dataset extensions.
7. CQ coverage table: `CQ → graph pattern → query file/section → test result`.
8. Three example explanations of candidate–job matches, including at least one rejection.
9. Before/after design for the change request.
10. Limitations and **two alternative modeling choices** you considered.

**Short presentation:** 8–10 minutes per team plus 5 minutes of questions. Demonstrate 2–3 live Cypher queries and defend one controversial modeling choice.

---

## 11. Assessment Rubric (100 points)

| Criterion | Points | Evidence |
|---|---:|---|
| Requirements understanding and CQ precision | 15 | CQ matrix, ambiguities, new questions |
| Modeling decisions and rationale | 25 | Eight justified decisions, alternatives, trade-offs |
| Schema coherence and integrity | 15 | Diagram, dictionary, IDs, temporal model, constraints |
| Correct implementation and reproducible loading | 15 | Cypher scripts, rerun safety, coherent test data |
| CQ query correctness and test quality | 20 | Twelve CQ queries, positive/negative fixtures, explanations |
| Schema evolution and critical reflection | 10 | Change request, history, migration and limitations |
| **Total** | **100** | |

**Penalties may apply** for non-reproducible scripts, unexplained copied graph models, invented verification facts, or queries that return hard-coded answers instead of traversing graph facts.

---

## 12. Instructor Facilitation Notes (No Reference Solution)

**Session 1 — Understand before modeling:** Review requirements, challenge ambiguous business terms and review the CQ analysis matrix. Ask students to distinguish an entity from an attribute using CQ traceability.

**Session 2 — Design debate:** Teams present alternative graph patterns. Prompt: "Why is proficiency not a property of the shared Skill node?" and "How do repeated applications affect the design?" Approve conceptual models only after justified decisions.

**Session 3 — Implement and query:** Inspect identity constraints, loading repeatability and mandatory/optional skill distinctions. Run baseline assertions; ask for counterexamples.

**Session 4 — Evolution and defense:** Deliver the assessment-history change request. Ask each group to defend its minimal migration and historical query.

**Optional differentiation:** Beginners complete CQ-01–CQ-10 and conceptual modeling; advanced students implement all CQs, stretch CQs, query plans, history and evidence provenance.

### Academic integrity and evaluation principle

As you know, multiple valid graph representations are possible. Students must explain *which queries their choices make easier or harder*. A complex graph with many nodes but no CQ justification is not automatically better than a simpler, well-supported model.

---

## 13. Final Student Reflection (Answer Individually)

1. What was your most difficult **node vs. property** decision, and which CQ resolved it?
2. What modeling choice would you change if there were **10 million profiles**?
3. What is one fact your graph **cannot** currently answer reliably?
4. How did you represent the difference between a **claim** and **evidence**?
5. What did the change request teach you about designing for **future questions**?
