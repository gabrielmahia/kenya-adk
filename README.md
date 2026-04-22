# 🤖 KenyaADK — East African AI Agent (Google ADK)

> The first [Google Agent Development Kit (ADK)](https://github.com/google/adk-python) implementation for East African civic data. An intelligent agent that can query Kenya's parliament, county budgets, drought data, and constitutional rights — powered by Gemini, with MCP tools and A2A protocol integration.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-v1.31.1-blue)](https://github.com/google/adk-python)
[![A2A Protocol](https://img.shields.io/badge/A2A-Protocol-green)](https://github.com/a2aproject/A2A)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green)](https://modelcontextprotocol.io)

## Why ADK + East Africa

Google ADK (Apache 2.0) is the same framework powering Google Agentspace and Customer Engagement Suite. KenyaADK is the first application of this framework to East African civic infrastructure — combining ADK's orchestration capabilities with Kenya's public datasets.

**The complete East African AI protocol stack:**

```
                    KenyaADK (Google ADK)
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     MCP tools       A2A agents    Gemini LLM
    (mpesa-mcp)    (kenya-a2a)   (free tier)
          │              │
   M-Pesa payments   Civic data
   SMS alerts        Parliament
   Airtime           Budgets
                     Drought
                     Rights EN/SW
```

## Quickstart

```bash
pip install kenya-adk
# or from source:
git clone https://github.com/gabrielmahia/kenya-adk
cd kenya-adk
pip install -r requirements.txt

export GOOGLE_API_KEY=your_key  # free at aistudio.google.com
adk web  # opens the ADK dev UI
```

## Agents

| Agent | Role | Tools |
|-------|------|-------|
| `BudgetAgent` | County budget absorption analysis | COB data, OCDS query |
| `ParliamentAgent` | MP records, bills, CDF utilisation | Parliament data |
| `DroughtAgent` | NDMA drought phases + SMS alerts | wapimaji-mcp, AT SMS |
| `RightsAgent` | Constitution of Kenya 2010 EN/SW | Bilingual KB |
| `OrchestratorAgent` | Routes queries to specialist agents | All above |

## Example interaction

```
User: "Which counties in northern Kenya are in drought crisis and how can we send SMS alerts to farmers there?"

KenyaADK:
  → DroughtAgent: Marsabit (Phase 3), Turkana (Phase 4), Wajir (Phase 3)
  → MCP tool: sms_send (via mpesa-mcp / Africa's Talking)
  → Response: "3 counties in drought crisis. 1,247 farmers in the database. Ready to send SMS alerts — confirm?"
```

## ADK + MCP + A2A

KenyaADK demonstrates all three complementary protocols:

- **MCP** (agent-to-tool): Uses [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) and [wapimaji-mcp](https://github.com/gabrielmahia/wapimaji-mcp) as tool servers
- **A2A** (agent-to-agent): Integrates with [kenya-a2a](https://github.com/gabrielmahia/kenya-a2a) as a remote agent
- **ADK** (orchestration): Coordinates all agents and tools through Google's framework

## Data

Built on [Kenya Civic Datasets](https://kaggle.com/datasets/gmahia/kenya-civic-data-parliament-budget-saccos):
- DOI: `10.34740/kaggle/dsv/15473045` (Kaggle)
- DOI: `10.57967/hf/8223` (HuggingFace)

## Related

| Repo | Protocol | Description |
|------|----------|-------------|
| [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) | MCP | M-Pesa + AT — 3,240+ PyPI downloads |
| [wapimaji-mcp](https://github.com/gabrielmahia/wapimaji-mcp) | MCP | Kenya drought intelligence |
| [kenya-a2a](https://github.com/gabrielmahia/kenya-a2a) | A2A | Civic data A2A agent |
| [kenya-rag](https://github.com/gabrielmahia/kenya-rag) | RAG | LlamaIndex civic RAG |
| [civic-agent-kit](https://github.com/gabrielmahia/civic-agent-kit) | SDK | Unified East African civic AI SDK |

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: CC BY-NC-ND 4.0
Built on Google ADK (Apache 2.0)
Not affiliated with Google, Parliament of Kenya, or Controller of Budget.
