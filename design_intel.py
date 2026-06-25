"""
DESIGN INTELLIGENCE — INXOTIVE x ui-ux-pro-max integration.
Built from 96 industry palettes, 57 font pairs, 100 anti-patterns.

Usage:
  from design_intel import suggest_palette, suggest_font, check_anti_patterns
"""

import json
from pathlib import Path

_DATA = None

def _load():
    global _DATA
    if _DATA is None:
        path = Path(__file__).parent / "design_intelligence.json"
        if path.exists():
            with open(path) as f:
                _DATA = json.load(f)
        else:
            _DATA = {"palettes": {}, "font_pairs": {}, "anti_patterns": {}, "ux_guidelines": [], "archetype_product_map": {}}
    return _DATA

def suggest_palette(industry: str, archetype: str = None) -> dict:
    """Get color palette recommendation for an industry or archetype."""
    data = _load()
    if industry in data["palettes"]:
        return {"source": "industry_match", "palette": data["palettes"][industry]}
    if archetype:
        for product in data.get("archetype_product_map", {}).get(archetype, []):
            if product in data["palettes"]:
                return {"source": f"archetype_{archetype}", "palette": data["palettes"][product]}
    return {"source": "default", "palette": data["palettes"].get("SaaS (General)", {})}

def suggest_font(industry: str, mood: str = "") -> list:
    """Get font pairing recommendations sorted by relevance."""
    data = _load()
    results = []
    for name, info in data["font_pairs"].items():
        score = 0
        if industry.lower() in info["best_for"].lower():
            score += 3
        if mood and mood.lower() in info["mood"].lower():
            score += 2
        if score > 0:
            results.append((score, name, info))
    results.sort(reverse=True)
    return [{"name": r[1], "heading": r[2]["heading"], "body": r[2]["body"], "url": r[2]["url"], "mood": r[2]["mood"]} for r in results[:5]]

def check_anti_patterns(industry: str) -> list:
    """Check for common anti-patterns in generated output."""
    data = _load()
    if industry in data["anti_patterns"]:
        ap = data["anti_patterns"][industry]
        return [{"industry": industry, "anti_patterns": ap["anti_patterns"], "severity": ap["severity"]}]
    return []

def merge_checklist(inxotive_checks: list) -> list:
    """Merge INXOTIVE checklist with ui-ux-pro-max UX guidelines."""
    data = _load()
    extra = [{"category": g["Category"], "issue": g["Issue"], "severity": g["Severity"],
              "do": g["Do"], "dont": g["Don't"]} for g in data["ux_guidelines"][:10]]
    return inxotive_checks + extra
