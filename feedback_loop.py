#!/usr/bin/env python3
"""
INXOTIVE Feedback Loop Module (Part E)
=======================================
Menyimpan feedback dari delivery nyata, mendistilasi jadi bobot arketipe,
dan menyesuaikan default builder.

Pipeline:
1. Klien/submit feedback → record
2. Distill berkala → update bobot
3. Builder default bergeser sesuai preferensi
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

HOME = Path.home()
FEEDBACK_FILE = HOME / ".claude" / "client_feedback.json"
ARCHETYPE_WEIGHTS_FILE = HOME / ".claude" / "archetype_weights.json"


def load_feedback() -> Dict[str, Any]:
    """Load all feedback entries."""
    if FEEDBACK_FILE.exists():
        try:
            return json.loads(FEEDBACK_FILE.read_text())
        except (json.JSONDecodeError, Exception):
            pass
    return {"feedback": [], "archetype_scores": {}, "variant_preferences": {}}


def save_feedback(data: Dict[str, Any]) -> None:
    """Save feedback data."""
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    FEEDBACK_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def record_feedback(
    client_name: str,
    site_id: str,
    archetype: str,
    feedback_type: str,  # "approve", "reject", "revision"
    section_type: str = "",
    variant: str = "",
    notes: str = "",
    rating: int = 3,  # 1-5
) -> Dict[str, Any]:
    """Record client feedback about a delivery."""
    data = load_feedback()

    entry = {
        "id": f"fb_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "client_name": client_name,
        "site_id": site_id,
        "archetype": archetype,
        "feedback_type": feedback_type,
        "section_type": section_type,
        "variant": variant,
        "notes": notes,
        "rating": max(1, min(5, rating)),
        "created": datetime.now().isoformat(),
    }
    data["feedback"].append(entry)
    save_feedback(data)
    return entry


def distill_feedback() -> Dict[str, Any]:
    """
    Distill all feedback into archetype weights and variant preferences.
    Run periodically (or on-demand after new feedback arrives).
    """
    data = load_feedback()
    feedback = data.get("feedback", [])

    if not feedback:
        return {"status": "no_feedback", "archetype_scores": {}, "variant_preferences": {}}

    # Compute archetype scores from feedback ratings
    archetype_ratings = {}
    for entry in feedback:
        arch = entry.get("archetype", "unknown")
        if arch not in archetype_ratings:
            archetype_ratings[arch] = []
        archetype_ratings[arch].append(entry.get("rating", 3))

    archetype_scores = {}
    for arch, ratings in archetype_ratings.items():
        avg = sum(ratings) / len(ratings)
        score = round((avg / 5) * 100, 1)  # Convert 1-5 to 0-100
        archetype_scores[arch] = {
            "score": score,
            "sample_count": len(ratings),
            "trend": "up" if len(ratings) >= 2 and ratings[-1] > ratings[0] else "stable",
        }

    # Compute variant preferences
    variant_counts = {}
    for entry in feedback:
        section = entry.get("section_type", "")
        variant = entry.get("variant", "")
        fb_type = entry.get("feedback_type", "")

        if not section or not variant:
            continue

        key = f"{section}:{variant}"
        if key not in variant_counts:
            variant_counts[key] = {"approve": 0, "reject": 0, "revision": 0, "total": 0}
        if fb_type in variant_counts[key]:
            variant_counts[key][fb_type] += 1
        variant_counts[key]["total"] += 1

    # Sort: prefer approved, avoid rejected
    variant_preferences = {}
    for key, counts in variant_counts.items():
        approval_rate = counts["approve"] / counts["total"] if counts["total"] > 0 else 0
        variant_preferences[key] = {
            "approval_rate": round(approval_rate, 2),
            "counts": counts,
            "recommended": approval_rate >= 0.6,
        }

    # Save distilled data
    data["archetype_scores"] = archetype_scores
    data["variant_preferences"] = variant_preferences
    save_feedback(data)

    return {
        "status": "ok",
        "total_feedback": len(feedback),
        "archetype_scores": archetype_scores,
        "variant_preferences": variant_preferences,
    }


def get_recommendations(archetype: str = None) -> Dict[str, Any]:
    """Get builder recommendations based on distilled feedback."""
    data = load_feedback()
    result = {"archtype_recommendations": {}, "variant_recommendations": []}

    archetype_scores = data.get("archetype_scores", {})
    variant_prefs = data.get("variant_preferences", {})

    if archetype and archetype in archetype_scores:
        result["archtype_recommendations"][archetype] = archetype_scores[archetype]
    else:
        result["archtype_recommendations"] = archetype_scores

    # Best performing variants
    for key, prefs in variant_prefs.items():
        if prefs.get("recommended"):
            section, variant = key.split(":", 1)
            result["variant_recommendations"].append({
                "section": section,
                "variant": variant,
                "approval_rate": prefs["approval_rate"],
            })

    result["variant_recommendations"].sort(
        key=lambda x: x["approval_rate"], reverse=True
    )
    return result


def format_feedback_report() -> str:
    """Format feedback loop status as readable report."""
    data = load_feedback()
    feedback = data.get("feedback", [])
    arch_scores = data.get("archetype_scores", {})
    var_prefs = data.get("variant_preferences", {})

    if not feedback:
        return "Belum ada feedback tercatat. Feedback akan muncul setelah delivery klien nyata."

    lines = [
        "## 📋 Feedback Loop Report",
        f"",
        f"**Total feedback:** {len(feedback)} entries",
        f"",
        "### Archetype Scores",
    ]

    for arch, info in sorted(arch_scores.items(), key=lambda x: x[1]["score"], reverse=True):
        bar_len = 15
        filled = round(info["score"] / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        lines.append(f"- {arch:15s} [{bar}] {info['score']}% ({info['sample_count']} samples, {info['trend']})")

    if var_prefs:
        lines.extend([
            "",
            "### Variant Preferences",
        ])
        for key, prefs in sorted(var_prefs.items(), key=lambda x: x[1]["approval_rate"], reverse=True)[:10]:
            icon = "✅" if prefs["recommended"] else "⬜"
            lines.append(f"- {icon} {key}: {prefs['approval_rate']*100:.0f}% approval ({prefs['counts']['approve']} approve / {prefs['counts']['reject']} reject)")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="INXOTIVE Feedback Loop")
    parser.add_argument("--record", nargs=4, metavar=("CLIENT", "SITE", "TYPE", "NOTES"),
                        help="Record feedback: client_name site_id feedback_type notes")
    parser.add_argument("--distill", action="store_true", help="Distill feedback into weights")
    parser.add_argument("--report", action="store_true", help="Show feedback report")
    parser.add_argument("--recommend", nargs="?", const="all", metavar="ARCHETYPE",
                        help="Show recommendations for archetype")

    args = parser.parse_args()

    if args.record:
        client, site, fb_type, notes = args.record
        result = record_feedback(client, site, "unknown", fb_type, notes=notes)
        print(f"Feedback recorded: {result['id']}")
        if fb_type in ("approve", "reject"):
            distill_feedback()
            print("Weights updated.")

    if args.distill:
        result = distill_feedback()
        print(f"Distilled {result['total_feedback']} feedback entries.")
        for arch, info in result.get("archetype_scores", {}).items():
            print(f"  {arch}: {info['score']}% ({info['sample_count']} samples)")

    if args.report:
        print(format_feedback_report())

    if args.recommend is not None:
        arch = None if args.recommend == "all" else args.recommend
        recs = get_recommendations(arch)
        print(json.dumps(recs, indent=2))
