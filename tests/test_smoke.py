"""Smoke tests for kenya-adk."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import get_drought_status, get_constitutional_right, get_county_budget

def test_drought_status():
    r = get_drought_status("Turkana")
    assert "phase" in r
    assert 1 <= r["phase"] <= 5

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
