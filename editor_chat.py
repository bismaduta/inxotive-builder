"""
EDITOR CHAT — Sambungkan natural language ke action system via 9Router.
Phase 2: LLM menerima instruksi → ACTION JSON → validasi → state update.

Alur:
  Chat "buat lebih hijau"
  → POST /api/editor/chat
  → LLM (9Router) dengan system prompt
  → Parse ACTION: {...} dari response
  → Validasi tiap action
  → Return actions untuk diaplikasikan
"""

import json
import os
import re
import httpx
from typing import List, Dict, Tuple, Optional

# ═══════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════

NINE_ROUTER_URL = "http://localhost:20128/v1/chat/completions"
DEFAULT_MODEL = "qwen2.5:7b"  # Cukup untuk parsing → action JSON
FALLBACK_MODEL = "qwen2.5:3b"

def _get_api_key() -> str:
    """Get 9Router API key from environment or .env_secrets."""
    key = os.environ.get("NINE_ROUTER_API_KEY", "")
    if not key:
        try:
            with open(os.path.expanduser("~/.env_secrets")) as f:
                for line in f:
                    if "NINE_ROUTER_API_KEY" in line:
                        key = line.split("=", 1)[1].strip()
                        break
        except Exception:
            pass
    return key


# ═══════════════════════════════════════════
# SYSTEM PROMPT — ini yang membuat LLM jadi "editor"
# ═══════════════════════════════════════════

SYSTEM_PROMPT = """Kamu adalah asisten EDITOR WEBSITE INXOTIVE. Tugasmu mengubah instruksi natural user menjadi ACTION JSON yang bisa dieksekusi.

ATURAN PENTING:
1. Kamu HANYA boleh mengeluarkan ACTION dalam format di bawah.
2. JANGAN menulis HTML, CSS, atau kode apapun.
3. JANGAN menjelaskan — keluarkan ACTION SAJA.
4. Setiap perubahan = SATU action. Kalau user minta beberapa hal, keluarkan beberapa action.
5. Action yang tidak valid akan ditolak oleh sistem.

FORMAT ACTION:
ACTION: {"action": "<action_type>", "target": "<target_path>", "value": "<value>"}

ACTION TYPES & TARGETS:

1. set_text — Ubah teks
   Target: hero.headline, hero.subtext, hero.eyebrow, hero.cta, features.heading, about.heading, about.body, cta.heading, cta.subtext, cta.button

2. set_color — Ubah warna brand
   Target: design.brand_primary, design.brand_secondary, design.brand_accent
   Value: hex color (#RRGGBB) — PASTIKAN kontras cukup!

3. swap_variant — Ganti layout section
   Target: hero (value: split/centered/full-bleed/video/showcase)
   Target: features (value: grid/zigzag/asymmetric-2col/showcase/icon-grid)
   Target: about (value: standard/right-image/split)
   Target: pricing (value: default/compact)
   Target: testimonials (value: default/carousel)

4. toggle_section — Tampil/sembunyikan section
   Target: hero/features/stats/about/testimonials/pricing/faq/cta/contact/team/gallery/process/logos
   Value: true (tampil) / false (sembunyi)

5. set_density — Ubah kerapatan section
   Target: density
   Value: xl/lg/md/sm

6. set_font — Ganti font
   Target: design.font_display atau design.font_body

CONTOH:
User: "Buat hero lebih hijau"
ACTION: {"action": "set_color", "target": "design.brand_primary", "value": "#2F5E3A"}

User: "Ganti judul hero jadi Garden Dining"
ACTION: {"action": "set_text", "target": "hero.headline", "value": "Garden Dining Bali"}

User: "Bikin lebih santai"
ACTION: {"action": "set_density", "target": "density", "value": "xl"}
ACTION: {"action": "swap_variant", "target": "features", "value": "zigzag"}

User: "Sembunyikan section tim"
ACTION: {"action": "toggle_section", "target": "team", "value": false}

Ingat: HANYA keluarkan ACTION: {...} — tidak ada teks lain!"""


# ═══════════════════════════════════════════
# LLM CHAT
# ═══════════════════════════════════════════

async def chat_to_actions(instruction: str, context: dict = None) -> Tuple[List[dict], str]:
    """
    Kirim instruksi ke Ollama lokal, parse ACTION JSON dari response.
    Gratis, cepat, pribadi — semua data tetap di server sendiri.

    Returns: (valid_actions, raw_response)
    """
    # Build prompt with context
    prompt = SYSTEM_PROMPT
    if context:
        prompt += f"\n\nKONDISI SAAT INI:\n- Brand/Site: {context.get('brand', 'unknown')}"
        hero = context.get("hero", {})
        if hero:
            prompt += f"\n- Hero headline: {hero.get('headline', '')[:60]}"
        feat = context.get("features", {})
        if feat:
            prompt += f"\n- Features heading: {feat.get('heading', '')[:60]}"
    prompt += f"\n\nSEKARANG:\nUser: {instruction}\n"

    # Try Ollama first (fast, free, private)
    models_to_try = ["qwen2.5:3b", "llama3.1:8b"]
    last_error = ""

    for model in models_to_try:
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                resp = await client.post("http://localhost:11434/api/generate", json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,
                    "options": {"num_predict": 300}
                })
                if resp.status_code < 400:
                    text = resp.json().get("response", "")
                    if text.strip():
                        actions = _parse_actions(text)
                        if actions:
                            return actions, text
                        # If no actions found but response exists
                        last_error = f"Tidak ada action yang bisa diparse dari: {text[:100]}..."
                else:
                    last_error = f"Model {model} error: {resp.status_code}"
        except Exception as e:
            last_error = f"Model {model}: {e}"
            continue

    return [], f"Maaf, gagal memproses. {last_error}"


# ═══════════════════════════════════════════
# PARSER: LLM response → actions
# ═══════════════════════════════════════════

def _parse_actions(llm_text: str) -> List[dict]:
    """Parse ACTION: {...} dari LLM response."""
    actions = []
    seen = set()

    for match in re.finditer(r'ACTION:\s*(\{.*?\})(?:\n|$|\))', llm_text, re.DOTALL):
        try:
            action = json.loads(match.group(1))
            # Dedup by action+target
            key = f"{action.get('action')}_{action.get('target')}"
            if key not in seen:
                seen.add(key)
                actions.append(action)
        except (json.JSONDecodeError, KeyError):
            continue

    return actions


def format_actions_for_llm(actions: List[dict]) -> str:
    """Format actions jadi teks untuk ditampilkan ke user."""
    lines = []
    for a in actions:
        act = a.get("action", "").replace("_", " ")
        target = a.get("target", "")
        value = a.get("value", "")
        if isinstance(value, str) and len(value) > 30:
            value = value[:30] + "..."
        lines.append(f"  • {act} → {target}: {value}")
    return "\n".join(lines)


if __name__ == "__main__":
    import asyncio

    async def test():
        print("=== TEST: Editor Chat via 9Router ===")
        actions, raw = await chat_to_actions("buat lebih hijau", {"brand": "gimora", "hero": {"headline": "Warung Modern"}})
        print(f"Actions: {len(actions)}")
        for a in actions:
            print(f"  {a}")
        if not actions:
            print(f"Raw: {raw[:200]}")

    asyncio.run(test())
