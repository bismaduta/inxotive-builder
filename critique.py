#!/usr/bin/env python3
"""
INXOTIVE Visual Critique Module (Part D)
=========================================
Loop kritik visual untuk builder: menganalisis HTML, menghitung metrik
komposisi, dan memberikan skor rubrik.

Dua mode:
1. HTML-analysis mode (tanpa vision) — analisis struktural dari source HTML
2. Vision mode (dengan Playwright + model vision) — screenshot + kritik

Dijalankan on-demand saat build, BUKAN 24/7.
"""

import re
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

HOME = Path.home()
CRITIQUE_HISTORY_FILE = HOME / ".claude" / "critique_history.json"

# ═══════════════════════════════════════════════════════════════
# RUBRIK PENILAIAN — 8 dimensi, skor 0–3 tiap dimensi
# ═══════════════════════════════════════════════════════════════

RUBRIC = {
    "alignment_variety": {
        "label": "Variasi Alignment",
        "description": "Tidak semua center — ada variasi left/center/right",
        "weight": 1.5,
    },
    "scale_contrast": {
        "label": "Kontras Skala",
        "description": "Ada momen tipografi besar berdampingan kecil",
        "weight": 1.2,
    },
    "rhythm_variety": {
        "label": "Variasi Ritme",
        "description": "Section terasa beda — padding bervariasi, layout berganti",
        "weight": 1.3,
    },
    "focal_point": {
        "label": "Focal Point",
        "description": "Ada satu momen visual dominan per halaman",
        "weight": 1.0,
    },
    "archetype_fit": {
        "label": "Kecocokan Arketipe",
        "description": "Apakah layout sesuai karakter arketipe?",
        "weight": 1.5,
    },
    "spacing_balance": {
        "label": "Keseimbangan Spacing",
        "description": "Whitespace konsisten, tidak sumpek/kosong berlebihan",
        "weight": 1.0,
    },
    "motion_polish": {
        "label": "Motion & Polish",
        "description": "Hover state, transisi, animasi halus",
        "weight": 0.8,
    },
    "client_worthy": {
        "label": "Layak Klien Berbayar",
        "description": "Maukah saya tunjukkan ini ke klien sebagai kesan pertama?",
        "weight": 1.7,
    },
}


def analyze_html(html: str, archetype_key: str = "corporate") -> Dict[str, Any]:
    """
    Analyze HTML source for structural composition metrics.
    No vision model needed — pure HTML/CSS analysis.

    Returns dict of metrics + per-dimension scores.
    """
    if not html:
        return {"error": "Empty HTML", "score": 0}

    # ── Count alignment ──
    centers = len(re.findall(r'text-align:\s*center', html))
    lefts = len(re.findall(r'text-align:\s*left', html))
    rights = len(re.findall(r'text-align:\s*right', html))
    total_align = centers + lefts + rights
    center_ratio = centers / total_align if total_align > 0 else 1.0

    # ── Section analysis ──
    section_pattern = re.compile(r'<section\s[^>]*role="region"[^>]*aria-label="([^"]+)"')
    sections = section_pattern.findall(html)
    section_count = len(sections)
    unique_section_types = len(set(sections))

    # ── Hero analysis ──
    has_split_hero = bool(re.search(r'grid-template-columns:\s*1\.\d+fr\s+\d+\.\d+fr', html))
    has_full_bleed_hero = '90vh;display:flex' in html or 'min-height:90vh' in html
    has_centered_hero = bool(re.search(r'text-align:center[^>]*>\\s*<h1', html))

    # ── Feature layout variety ──
    has_zigzag = 'margin-bottom:var(--space-xxl)' in html and 'grid-template-columns:1fr 1fr' in html
    has_asymmetric = 'grid-column:1/-1' in html
    has_grid_3 = 'grid-3' in html or 'grid-template-columns:repeat(3' in html

    # ── Motion & effects ──
    hover_effects = len(re.findall(r'hover-lift|hover-glow|hover-scale|hover-bright', html))
    animations = len(re.findall(r'vfx-', html))
    has_reveal = 'section--reveal' in html
    has_transitions = 'transition:' in html or 'transition ' in html

    # ── Section count per spacing pattern ──
    compact_count = len(re.findall(r'padding:\s*var\(--space-section-sm\)', html))
    normal_count = len(re.findall(r'padding:\s*var\(--space-section\)', html))
    spacious_count = len(re.findall(r'padding:\s*var\(--space-section-lg\)', html))

    # ── Focal point check ──
    hero_has_large_text = bool(re.search(r'font-size:clamp\([^)]*[45]\.?\d*rem', html))
    has_large_stat = bool(re.search(r'heading-1[^>]*>[^<]{2,}</div>', html))
    has_cta_section = bool(re.search(r'aria-label="Call to Action"', html))
    has_visual_dominance = hero_has_large_text or has_large_stat

    # ── Color contrast (basic) — check if dark bg + light text used ──
    has_dark_section = bool(re.search(r'section--dark|section--accent', html))
    has_gradient = 'var(--brand-gradient)' in html

    # ═══ COMPUTE SCORES (0-3 each) ═══

    # 1. Alignment variety: lower center ratio = higher score
    if center_ratio <= 0.15:
        alignment_score = 3
    elif center_ratio <= 0.30:
        alignment_score = 2
    elif center_ratio <= 0.50:
        alignment_score = 1
    else:
        alignment_score = 0

    # 2. Scale contrast
    if hero_has_large_text and (has_large_stat or has_cta_section):
        scale_score = 3
    elif hero_has_large_text or has_large_stat:
        scale_score = 2
    elif has_cta_section:
        scale_score = 1
    else:
        scale_score = 0

    # 3. Rhythm variety
    rhythm_types = sum([bool(compact_count), bool(normal_count), bool(spacious_count)])
    if rhythm_types >= 2 and section_count >= 6:
        rhythm_score = 3
    elif rhythm_types >= 2 or section_count >= 6:
        rhythm_score = 2
    elif section_count >= 4:
        rhythm_score = 1
    else:
        rhythm_score = 0

    # 4. Focal point
    if has_visual_dominance and hero_has_large_text:
        focal_score = 3
    elif has_visual_dominance:
        focal_score = 2
    elif has_cta_section:
        focal_score = 1
    else:
        focal_score = 0

    # 5. Archetype fit
    archetype_scores = {
        "editorial": {"split": 2, "zigzag": 2, "density_high": 1},
        "bold": {"full_bleed": 2, "grid": 1, "density_low": 1},
        "warm": {"full_bleed": 2, "asymmetric": 1, "carousel": 1},
        "corporate": {"split": 1, "grid": 1, "structured": 1},
    }
    arch_config = archetype_scores.get(archetype_key, {})
    arch_score = 1  # baseline
    if "split" in arch_config and has_split_hero:
        arch_score += 1
    if "full_bleed" in arch_config and has_full_bleed_hero:
        arch_score += 1
    if "zigzag" in arch_config and has_zigzag:
        arch_score += 1
    if "asymmetric" in arch_config and has_asymmetric:
        arch_score += 1
    if "grid" in arch_config and has_grid_3:
        arch_score += 1
    arch_score = min(3, arch_score)

    # 6. Spacing balance
    if compact_count > 0 and spacious_count > 0 and section_count >= 5:
        spacing_score = 3
    elif compact_count > 0 or spacious_count > 0:
        spacing_score = 2
    elif section_count >= 4:
        spacing_score = 1
    else:
        spacing_score = 1

    # 7. Motion & polish
    motion_score = 0
    if hover_effects >= 3:
        motion_score += 1
    if animations >= 3:
        motion_score += 1
    if has_reveal and has_transitions:
        motion_score += 1
    motion_score = min(3, motion_score)

    # 8. Client worthy (composite)
    client_score = 2  # baseline
    if center_ratio <= 0.30 and has_visual_dominance and has_gradient:
        client_score += 1
    if center_ratio > 0.70 or section_count < 4:
        client_score -= 1
    client_score = max(0, min(3, client_score))

    # ═══ Aggregate score ═══
    dimensions = {
        "alignment_variety": alignment_score,
        "scale_contrast": scale_score,
        "rhythm_variety": rhythm_score,
        "focal_point": focal_score,
        "archetype_fit": arch_score,
        "spacing_balance": spacing_score,
        "motion_polish": motion_score,
        "client_worthy": client_score,
    }

    weighted_sum = sum(
        dimensions[k] * RUBRIC[k]["weight"] for k in dimensions
    )
    max_possible = sum(3 * RUBRIC[k]["weight"] for k in dimensions)
    total_score = round((weighted_sum / max_possible) * 100, 1)

    # Generate fix suggestions
    suggestions = []
    if center_ratio > 0.30:
        suggestions.append("Kurangi center alignment — target ≤30% center. Pindahkan body text ke rata kiri.")
    if scale_score < 2:
        suggestions.append("Tambah kontras skala — buat headline hero lebih besar (clamp 5-8rem) atau tambah stat angka besar.")
    if rhythm_score < 2:
        suggestions.append("Variasi padding section — campur compact, normal, dan spacious dalam satu halaman.")
    if focal_score < 2:
        suggestions.append("Tambah focal point visual — hero headline besar atau stat counter menonjol.")
    if arch_score < 2:
        suggestions.append(f"Arketipe {archetype_key} tidak optimal — periksa hero layout dan feature section.")
    if motion_score < 2:
        suggestions.append(f"Tambah hover effects dan animasi — minimal 3 hover-lift di kartu.")

    return {
        "url": "",
        "score": total_score,
        "dimensions": dimensions,
        "metrics": {
            "center_count": centers,
            "left_count": lefts,
            "center_ratio": round(center_ratio, 3),
            "section_count": section_count,
            "unique_sections": unique_section_types,
            "hover_effects": hover_effects,
            "animations_count": animations,
            "has_reveal": has_reveal,
            "has_split_hero": has_split_hero,
            "has_full_bleed_hero": has_full_bleed_hero,
            "has_zigzag_features": has_zigzag,
            "has_asymmetric_layout": has_asymmetric,
            "has_gradient": has_gradient,
            "has_dark_section": has_dark_section,
        },
        "suggestions": suggestions,
        "suggestions_count": len(suggestions),
        "archetype": archetype_key,
    }




def check_prerelease_readiness(html: str, archetype_key: str = None) -> dict:
    """
    Pre-release checklist gate — setiap build harus lulus semua item.
    Diadaptasi dari ui-ux-pro-max checklist + temuan internal.
    """
    checks = {}
    
    # 1. No emoji icons (must use SVGs)
    emoji_icons = ["🚀", "🔒", "🎨", "📊", "🤖", "📱", "⭐", "✨", "🔥", "💡", "✅", "💰", "🎯"]
    found_emojis = []
    for emoji in emoji_icons:
        count = html.count(emoji)
        if count > 0:
            found_emojis.append(f"{emoji}({count})" if count > 0 else "")
    checks["no_emoji_icons"] = {
        "pass": len(found_emojis) == 0,
        "detail": "Ikon SVG konsisten" if len(found_emojis) == 0 else f"Ditemukan emoji: {', '.join(found_emojis)}"
    }
    
    # 2. No placeholder images (unsplash or stock images)
    placeholder_patterns = ["placehold.co", "via.placeholder.com", "dummyimage.com"]
    found_placeholders = [p for p in placeholder_patterns if p in html]
    checks["no_placeholder_images"] = {
        "pass": len(found_placeholders) == 0,
        "detail": "Tidak ada placeholder kosong" if len(found_placeholders) == 0 else f"Placeholder ditemukan: {found_placeholders}"
    }
    
    # 3. Has stock images (unsplash)
    has_stock_images = "unsplash.com" in html or "images.unsplash" in html
    checks["has_stock_images"] = {
        "pass": has_stock_images,
        "detail": "Gambar nyata dari stock" if has_stock_images else "Tidak ada gambar stock — fallback warna brand"
    }
    
    # 4. Archetype fidelity — section order matches archetype
    # (heuristic: check if section wrapper exists)
    has_section_wrappers = 'data-section-type="' in html
    section_types = re.findall(r'data-section-type="([^"]+)"', html) if has_section_wrappers else []
    checks["has_structure"] = {
        "pass": len(section_types) >= 4,
        "detail": f"{len(section_types)} section terdefinisi" if section_types else "Struktur section tidak terdeteksi"
    }
    
    # 5. No obvious contrast issues — subtext shouldn't use text-muted on light bg
    # (heuristic: check for common low-contrast patterns)
    low_contrast_patterns = ['color:#888', 'color:#999', 'color:#aaa', 'opacity:0.3']
    found_low = 0
    for pat in low_contrast_patterns:
        found_low += html.count(pat)
    checks["contrast_minimum"] = {
        "pass": found_low < 5,
        "detail": f"Pattern low-contrast: {found_low} (target <5)" if found_low >= 5 else "Kontras terjaga"
    }
    
    # 6. Has hover/transition effects
    has_transitions = "transition:" in html
    checks["has_transitions"] = {
        "pass": has_transitions,
        "detail": "Transisi terdefinisi" if has_transitions else "Tidak ada transisi"
    }
    
    # 7. Responsive meta tag
    has_responsive_meta = 'name="viewport"' in html
    checks["responsive_meta"] = {
        "pass": has_responsive_meta,
        "detail": "Viewport meta ada" if has_responsive_meta else "Missing viewport meta"
    }
    
    # Summary
    all_pass = all(v["pass"] for v in checks.values())
    checks["_summary"] = {
        "pass": all_pass,
        "passed": sum(1 for v in checks.values() if isinstance(v, dict) and v.get("pass")),
        "total": sum(1 for k, v in checks.items() if not k.startswith("_")),
    }
    
    return checks

def save_critique(site_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
    """Save critique result to history file."""
    history = {}
    if CRITIQUE_HISTORY_FILE.exists():
        try:
            history = json.loads(CRITIQUE_HISTORY_FILE.read_text())
        except (json.JSONDecodeError, Exception):
            history = {}

    entry = {
        "site_id": site_id,
        "timestamp": datetime.now().isoformat(),
        "score": result.get("score", 0),
        "dimensions": result.get("dimensions", {}),
        "metrics": result.get("metrics", {}),
        "suggestions": result.get("suggestions", []),
        "archetype": result.get("archetype", ""),
    }

    if site_id not in history:
        history[site_id] = []
    history[site_id].append(entry)

    # Keep only last 50 entries per site
    if len(history[site_id]) > 50:
        history[site_id] = history[site_id][-50:]

    CRITIQUE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    CRITIQUE_HISTORY_FILE.write_text(json.dumps(history, indent=2))
    return entry


def get_critique_history(site_id: str = None) -> List[Dict[str, Any]]:
    """Get critique history, optionally filtered by site_id."""
    if not CRITIQUE_HISTORY_FILE.exists():
        return []
    try:
        history = json.loads(CRITIQUE_HISTORY_FILE.read_text())
        if site_id:
            return history.get(site_id, [])
        # Flatten all
        all_entries = []
        for sid, entries in history.items():
            for e in entries:
                e["site_id"] = sid
                all_entries.append(e)
        return sorted(all_entries, key=lambda x: x.get("timestamp", ""), reverse=True)
    except (json.JSONDecodeError, Exception):
        return []


def format_critique_report(result: Dict[str, Any]) -> str:
    """Format critique result as readable markdown."""
    score = result.get("score", 0)
    dims = result.get("dimensions", {})
    metrics = result.get("metrics", {})
    suggestions = result.get("suggestions", [])
    arch = result.get("archetype", "unknown")

    # Score bar (visual)
    bar_len = 20
    filled = round(score / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    lines = [
        f"## 🎨 Visual Critique Report",
        f"",
        f"**Arketipe:** {arch}",
        f"**Score:** {score}/100",
        f"**Bar:** [{bar}]",
        f"",
        f"### Per-Dimension Scores",
    ]

    for key, dim in RUBRIC.items():
        s = dims.get(key, 0)
        bar_s = "●" * s + "○" * (3 - s)
        lines.append(f"- {bar_s} **{dim['label']}:** {s}/3 — {dim['description']}")

    lines.extend([
        "",
        "### Metrics",
        f"- Center:Left ratio: {metrics.get('center_ratio', 'N/A')} (target ≤0.30)",
        f"- Sections: {metrics.get('section_count', 0)} ({metrics.get('unique_sections', 0)} unique types)",
        f"- Hero: {'Split' if metrics.get('has_split_hero') else 'Full-bleed' if metrics.get('has_full_bleed_hero') else 'Centered'}",
        f"- Features: {'Zigzag' if metrics.get('has_zigzag_features') else 'Asymmetric' if metrics.get('has_asymmetric_layout') else 'Grid'}",
        f"- Hover effects: {metrics.get('hover_effects', 0)}",
        f"- Animations: {metrics.get('animations_count', 0)}",
        f"- Dark section: {'Yes' if metrics.get('has_dark_section') else 'No'}",
        f"- Gradient: {'Yes' if metrics.get('has_gradient') else 'No'}",
    ])

    if suggestions:
        lines.extend([
            "",
            "### Suggested Fixes",
        ])
        for i, s in enumerate(suggestions, 1):
            lines.append(f"{i}. {s}")

    if score >= 80:
        verdict = "✅ **Excellent!** — Layak ditunjukkan ke klien."
    elif score >= 60:
        verdict = "⚠️ **Good, but could be better.** — Perbaiki beberapa hal sebelum ke klien."
    else:
        verdict = "❌ **Needs improvement.** — Belum layak klien. Terapkan saran di atas."

    lines.extend([
        "",
        f"### Verdict",
        f"{verdict}",
    ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="INXOTIVE Visual Critique")
    parser.add_argument("file", nargs="?", help="HTML file to critique")
    parser.add_argument("--url", "-u", help="URL to critique (fetches HTML first)")
    parser.add_argument("--archetype", "-a", default="corporate", help="Archetype key for scoring")
    parser.add_argument("--history", action="store_true", help="Show critique history")
    parser.add_argument("--site", "-s", help="Filter history by site ID")
    parser.add_argument("--save", action="store_true", help="Save critique result")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    if args.history:
        entries = get_critique_history(args.site)
        if not entries:
            print("No critique history found.")
        else:
            print(f"Found {len(entries)} critique entries.")
            for e in entries[:10]:
                print(f"  {e.get('timestamp','')[:19]} | Site: {e.get('site_id','')} | Score: {e.get('score',0)}")
        exit(0)

    html_content = ""
    if args.file:
        html_content = Path(args.file).read_text()
    elif args.url:
        import urllib.request
        html_content = urllib.request.urlopen(args.url).read().decode("utf-8")
    else:
        # Read from stdin
        import sys
        html_content = sys.stdin.read()

    if not html_content.strip():
        print("No HTML content provided")
        exit(1)

    result = analyze_html(html_content, args.archetype)

    if args.save:
        save_critique("cli", result)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_critique_report(result))
