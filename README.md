# Euromed Graph Theory Course

Practical notebooks and resources for the Graph Theory course at Euromed University.

---

## Getting Started — Running the Notebooks on Your Own Machine

Follow the steps below exactly. This project uses **[uv](https://docs.astral.sh/uv/)** as the package manager — it is fast, modern, and handles both Python versions and dependencies for you.

---

### Step 1 — Install `uv`

**`uv` is the only tool you need to install manually.** It will take care of everything else.

Go to the official installation page:

👉 **https://docs.astral.sh/uv/getting-started/installation/**

Choose the instructions for your operating system:

| OS | Quick install command |
|---|---|
| **Windows** (PowerShell) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **macOS / Linux** (Terminal) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

After installation, **close and reopen your terminal**, then verify it works:

```bash
uv --version
```

You should see something like `uv 0.x.x`.

---

### Step 2 — Clone or Download the Course Repository

If you received a zip file, extract it to a folder of your choice.

If you are using Git:

```bash
git clone <repository-url>
cd euromed-graph-course
```

---

### Step 3 — Create the Virtual Environment and Install Dependencies

Inside the project folder, run:

```bash
uv sync
```

This single command will:
- Download **Python 3.12** automatically if you don't have it
- Create a `.venv` virtual environment inside the project folder
- Install all required packages (NetworkX, JupyterLab, pandas, etc.)

> The first run may take a minute or two — subsequent runs are instant.

---

### Step 4 — Launch JupyterLab

```bash
uv run jupyter lab
```

JupyterLab will open in your browser. Navigate to the `notebooks/` folder and open any session notebook.

---

## 📁 Project Structure

```
euromed-graph-course/
│
├── notebooks/
│   ├── session_01/         ← Session 1 notebooks & exercises
│   │   ├── session_01.ipynb
│   │   ├── useCase1-PublicTransportNetwork.ipynb
│   │   ├── useCase2-FinancialTransactionNetwork.ipynb
│   │   ├── useCase3-Social Network.ipynb
│   │   ├── exercices.md
│   │   ├── CheatSheet.md
│   │   └── Glossary.md
│   └── ...
│
├── pyproject.toml          ← Project dependencies (managed by uv)
├── uv.lock                 ← Locked dependency versions (do not edit)
├── .python-version         ← Pinned Python version (3.12)
└── README.md
```

---

## Dependencies

All packages are declared in `pyproject.toml` and locked in `uv.lock`. You do **not** need to install anything manually — `uv sync` handles everything.

Main packages used:

| Package | Purpose |
|---|---|
| `networkx` | Graph creation and analysis |
| `pyvis` | Interactive graph visualisation |
| `jupyterlab` | Running the notebooks |
| `pandas` | Data manipulation |
| `matplotlib` | Plotting |
| `spacy` / `nltk` | Natural Language Processing |
| `scikit-learn` | Machine learning utilities |
| `scipy` | Scientific computing |

---

## ❓ Troubleshooting

**`uv` command not found after installation**
→ Close and reopen your terminal (or restart your IDE).

**JupyterLab opens but the kernel is missing**
→ Make sure you launched it with `uv run jupyter lab`, not a globally installed Jupyter.

**Port already in use**
→ Run `uv run jupyter lab --port 8889` to use a different port.

---

## Useful Links

- [uv documentation](https://docs.astral.sh/uv/)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- [NetworkX documentation](https://networkx.org/documentation/stable/)
- [JupyterLab documentation](https://jupyterlab.readthedocs.io/)
