# AI Cognitive Routing Assignment

This project contains all 3 assignment phases in one runnable codebase:

1. Phase 1: route a post to the best bot persona.
2. Phase 2: generate post content using a LangGraph flow.
3. Phase 3: produce a defense reply that resists prompt injection.

## Project Structure

```text
ai-cognitive-routing/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
├── run_project.sh
├── router/
│   └── vector_router.py
├── engine/
│   ├── langgraph_flow.py
│   └── tools.py
├── combat/
│   └── rag_defense.py
├── data/
│   └── personas.py
├── logs/
│   └── execution_logs.md
└── tests/
    └── test_project.py
```

## Step-by-Step Setup (Bash)

Run these commands in order.

### 1) Move into the project folder

If your terminal is already inside the project, skip this.

```bash
cd ai-cognitive-routing
```

### 2) Create a virtual environment

```bash
python3 -m venv venv
```

### 3) Activate the virtual environment

Recommended (project-local venv):

```bash
source venv/bin/activate
```

Alternative (if you intentionally use a parent-level venv):

```bash
source ../venv/bin/activate
```

### 4) Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 5) Create .env file (if needed)

```bash
cp .env.example .env
```

## What To Run

### Option A: Run everything with one command

From inside the project folder:

```bash
./run_project.sh
```

From the parent folder:

```bash
./ai-cognitive-routing/run_project.sh
```

What the script does:
- prefers project-local `venv` Python first
- falls back to parent `venv` if needed
- creates project `venv` if no virtual environment exists
- installs dependencies only when missing
- runs `main.py` and prints all 3 phase outputs

### Option B: Run manually

```bash
python3 main.py
```

This executes:
1. Phase 1 routing test
2. Phase 2 LangGraph generation test
3. Phase 3 defense reply test

Execution output is also appended to `logs/execution_logs.md`.

## Run Unit Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Troubleshooting

### Error: requirements file not found

If you see:

`ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`

Your terminal is not in the project folder.

Fix:

```bash
cd /Users/v.saikiranreddy/Desktop/ai-cognitive-routing/ai-cognitive-routing
python3 -m pip install -r requirements.txt
```

### Error: python command not found

Use `python3` instead of `python`:

```bash
python3 main.py
```

## Phase Implementation Map

- Phase 1 Router: `router/vector_router.py`
  - API: `route_post_to_bots(post_content, threshold=0.85)`
- Phase 2 LangGraph: `engine/langgraph_flow.py` and `engine/tools.py`
  - mock tool: `mock_searxng_search(query: str)`
- Phase 3 RAG Defense: `combat/rag_defense.py`
  - API: `generate_defense_reply(bot_persona, parent_post, comment_history, human_reply)`

## Submission Checklist

- code for all 3 phases
- `requirements.txt`
- `.env.example` with sample keys only
- `logs/execution_logs.md` with execution output
- `README.md` with setup + run steps

## README Sync Policy

If files/folders are added, removed, or moved, update this README in the same change.
