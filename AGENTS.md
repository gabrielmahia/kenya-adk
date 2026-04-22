# AGENTS.md — KenyaADK

## Purpose
First Google ADK (Apache 2.0) implementation for East African civic data.

## Agent structure
- `root_agent` (kenya_civic_agent) — orchestrator, routes to specialists
  - `drought_agent` — NDMA drought phases
  - `budget_agent` — Controller of Budget data
  - `parliament_agent` — 13th Parliament records
  - `rights_agent` — Constitution of Kenya 2010 EN/SW

## Run
```bash
adk run agent.py          # CLI
adk web agent.py          # ADK dev UI
adk api_server agent.py   # REST API
```

## Data
Place CSVs in civic_data/ — download from DOI: 10.34740/kaggle/dsv/15473045

## Rules
- Never fabricate civic data
- Always cite sources (COB, NDMA, Parliament of Kenya, Constitution)
- SANDBOX=true by default for drought data
