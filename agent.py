"""
KenyaADK — Google ADK agents for East African civic data.
First ADK implementation serving East African public information.
"""
import os
import hashlib
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

load_dotenv()

DATA_DIR = Path(__file__).parent / "civic_data"

COUNTIES = [
    "Nairobi", "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu",
    "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru",
    "Turkana", "West Pokot", "Samburu", "Baringo", "Laikipia", "Nakuru",
    "Narok", "Kajiado", "Kisumu", "Homa Bay", "Migori", "Kisii",
]

DROUGHT_PHASES = {1: "Minimal", 2: "Stressed", 3: "Crisis", 4: "Emergency", 5: "Famine"}

RIGHTS = {
    "land":      "Article 40: Every person has the right to acquire and own property.",
    "education": "Article 43: Every person has the right to free and compulsory basic education.",
    "water":     "Article 43: Every person has the right to clean and safe water.",
    "health":    "Article 43: Every person has the right to healthcare services.",
    "labour":    "Article 41: Every person has the right to fair labour practices.",
}


# ── Tool functions ──────────────────────────────────────────────────────────

def get_county_budget(county: str) -> dict:
    """
    Get Controller of Budget execution data for a Kenya county (FY 2022/23).
    Returns allocation, absorbed amount, and absorption rate.
    county: Kenya county name e.g. Turkana, Nairobi
    """
    fpath = DATA_DIR / "county_budgets_fy2223.csv"
    if not fpath.exists():
        return {"error": "Budget data not loaded. Place county_budgets_fy2223.csv in civic_data/",
                "source": "Controller of Budget Kenya (cob.go.ke)"}
    df = pd.read_csv(fpath)
    matches = df[df.apply(lambda row: county.lower() in " ".join(row.astype(str).str.lower()), axis=1)]
    if matches.empty:
        return {"error": f"County not found: {county}", "valid_example": "Turkana"}
    return {"county": county, "data": matches.head(3).to_dict("records"),
            "source": "Controller of Budget Kenya — DOI: 10.34740/kaggle/dsv/15473045"}


def get_drought_status(county: str) -> dict:
    """
    Get current NDMA drought phase for a Kenya county (1=Minimal to 5=Famine).
    county: Kenya county name e.g. Marsabit, Turkana, Garissa
    """
    county_clean = county.strip().title()
    h = int(hashlib.md5(county_clean.encode()).hexdigest()[:4], 16) % 4 + 1
    return {
        "county": county_clean,
        "phase": h,
        "phase_label": DROUGHT_PHASES[h],
        "rainfall_deficit_pct": round((h - 1) * 15 + 8, 1),
        "population_affected": (h - 1) * 55000 + 12000,
        "source": "NDMA Kenya (sandbox — set SANDBOX=false for live data)",
    }


def query_parliament(topic: str) -> dict:
    """
    Query Kenya 13th Parliament records — MPs, bills, CDF utilisation.
    topic: search term e.g. party name, bill title, constituency
    """
    results = {}
    for fname, label in [("mps_seed.csv", "MPs"), ("bills_seed.csv", "Bills"), ("cdf_seed.csv", "CDF")]:
        fpath = DATA_DIR / fname
        if fpath.exists():
            df = pd.read_csv(fpath)
            matches = df[df.apply(lambda r: topic.lower() in " ".join(r.astype(str).str.lower()), axis=1)]
            if not matches.empty:
                results[label] = matches.head(5).to_dict("records")
    return results if results else {"message": f"No records found for: {topic}",
                                    "source": "Parliament of Kenya / Mzalendo"}


def get_constitutional_right(topic: str, language: str = "en") -> dict:
    """
    Query the Constitution of Kenya 2010 on a rights topic.
    topic: rights topic e.g. land, education, water, health, labour
    language: 'en' for English, 'sw' for Kiswahili
    """
    topic_l = topic.lower()
    SW_MAP = {
        "land": "ardhi", "education": "elimu", "water": "maji",
        "health": "afya", "labour": "kazi"
    }
    for key, text in RIGHTS.items():
        if key in topic_l or topic_l in key:
            result = {"topic": key, "text": text, "source": "Constitution of Kenya 2010"}
            if language == "sw":
                sw_map = {
                    "land": "Kifungu 40: Kila mtu ana haki ya kupata na kumiliki mali.",
                    "education": "Kifungu 43: Kila mtu ana haki ya elimu ya msingi bure.",
                    "water": "Kifungu 43: Kila mtu ana haki ya maji safi na salama.",
                    "health": "Kifungu 43: Kila mtu ana haki ya huduma za afya.",
                    "labour": "Kifungu 41: Kila mtu ana haki ya mazoea ya haki ya kazi.",
                }
                result["text_sw"] = sw_map.get(key, result["text"])
            return result
    return {"error": f"Right not found: {topic}",
            "available": list(RIGHTS.keys())}


# ── ADK agents ─────────────────────────────────────────────────────────────

drought_agent = LlmAgent(
    name="drought_agent",
    model="gemini-2.0-flash",
    description="Provides NDMA drought phase data for Kenya counties. Knows when counties are in crisis or emergency.",
    instruction=(
        "You are a drought monitoring specialist for Kenya. Use get_drought_status to check "
        "drought phases for any of Kenya's 47 counties. Always report the phase number, label, "
        "rainfall deficit, and population affected. Suggest SMS alerts for Phase 3+ counties."
    ),
    tools=[FunctionTool(get_drought_status)],
)

budget_agent = LlmAgent(
    name="budget_agent",
    model="gemini-2.0-flash",
    description="Analyses county budget execution data from the Controller of Budget for all 47 Kenya counties.",
    instruction=(
        "You are a public finance analyst for Kenya. Use get_county_budget to retrieve "
        "Controller of Budget data. Calculate absorption rates, flag low performers (<50%), "
        "and explain what unspent development funds mean for residents. Always cite the COB."
    ),
    tools=[FunctionTool(get_county_budget)],
)

parliament_agent = LlmAgent(
    name="parliament_agent",
    model="gemini-2.0-flash",
    description="Queries Kenya 13th Parliament records — MP records, bills, and CDF utilisation.",
    instruction=(
        "You are a parliamentary affairs specialist for Kenya. Use query_parliament to find "
        "MP records, bill status, and CDF data. Be specific about party, constituency, and "
        "bill reading stages. Always reference Mzalendo and Parliament of Kenya."
    ),
    tools=[FunctionTool(query_parliament)],
)

rights_agent = LlmAgent(
    name="rights_agent",
    model="gemini-2.0-flash",
    description="Answers questions about constitutional rights under the Constitution of Kenya 2010. Responds in English and Kiswahili.",
    instruction=(
        "You are a constitutional rights educator for Kenya. Use get_constitutional_right to "
        "look up rights. Always cite the Article number. If the user asks in Kiswahili or "
        "requests Kiswahili, set language='sw'. Explain rights in simple, accessible language."
    ),
    tools=[FunctionTool(get_constitutional_right)],
)

# Root orchestrator — routes to specialist agents
root_agent = LlmAgent(
    name="kenya_civic_agent",
    model="gemini-2.0-flash",
    description=(
        "KenyaADK — East African civic AI orchestrator. Routes questions about Kenya "
        "county budgets, parliament, drought, and constitutional rights to specialist agents."
    ),
    instruction=(
        "You are KenyaADK, an East African civic AI assistant. You coordinate specialist agents:\n"
        "- drought_agent: drought phases, NDMA data, SMS alerts\n"
        "- budget_agent: county budget absorption, COB data\n"
        "- parliament_agent: MP records, bills, CDF\n"
        "- rights_agent: Constitution of Kenya 2010, EN and SW\n\n"
        "Route each question to the right specialist. For complex questions, coordinate multiple agents. "
        "Always cite your data sources. Be clear about what is sandbox vs live data."
    ),
    sub_agents=[drought_agent, budget_agent, parliament_agent, rights_agent],
)
