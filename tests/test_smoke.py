"""Smoke tests for kenya-adk."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import get_constitutional_right, get_county_budget, get_drought_status


def test_drought_status_is_labelled_synthetic():
    # The previous test only checked 1 <= phase <= 5, which passes for any invented number and so blessed the fabrication.
    r = get_drought_status("Turkana")
    assert r["is_synthetic"] is True and "NOT NDMA" in r["source"]
    assert "population_affected" not in r          # a fabricated humanitarian figure
    assert "SANDBOX=false" not in r["source"]      # no live mode exists; the variable is never read


def test_drought_tool_description_does_not_claim_real_data():
    # The docstring is what the LLM reads as the tool description.
    doc = get_drought_status.__doc__
    assert "DEMO" in doc and "NOT NDMA" in doc and "Get current NDMA" not in doc


def test_module_makes_no_priority_claim():
    import agent
    assert "First" not in (agent.__doc__ or "")

def test_rights_en():
    r = get_constitutional_right("water", "en")
    assert "Article" in r.get("text", "")

def test_rights_sw():
    r = get_constitutional_right("maji", "sw")
    assert "error" not in r or "Kifungu" not in str(r)

def test_budget_no_data():
    r = get_county_budget("Nairobi")
    # Should return error or data — not raise
    assert isinstance(r, dict)
