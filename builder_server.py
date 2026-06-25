"""
INXOTIVE Web Builder Server
============================
Standalone FastAPI server on port 7777.
Builder + Client Portal.
"""

import sys, os
from pathlib import Path

sys.path.insert(0, str(Path.home() / "market-api"))
sys.path.insert(0, str(Path.home() / "inxotive-builder"))

# Load env secrets
_env_secrets = Path.home() / ".env_secrets"
if _env_secrets.exists():
    for line in _env_secrets.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import json, re
from datetime import datetime

from builder import (
    load_data, list_clients, get_client, create_client, update_client, delete_client,
    list_templates, get_template,
    list_sites, get_site, create_site, update_site_config, build_site, deploy_site, set_site_domain, delete_site,
    list_assets, upload_asset, delete_asset,
    generate_portal_token, verify_portal_token,
    generate_multi_page_site, save_multi_page_site,
)

app = FastAPI(title="INXOTIVE Builder", version="1.0")


# ── HTML Pages ──

@app.get("/", response_class=HTMLResponse)
async def builder_root():
    # Check possible locations — prefer cwd + explicit paths
    for p in [
        Path.cwd(),                               # current working directory
        Path("/opt/inxotive/builder"),           # VPS: /opt/inxotive/builder/
        Path("/opt/market-api"),                 # VPS fallback
        Path.home() / "inxotive-builder",       # laptop: ~/inxotive-builder/
        Path.home() / "market-api",              # laptop fallback
    ]:
        path = p / "builder.html"
        if path.exists():
            return HTMLResponse(path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Builder not found</h1>", status_code=404)


@app.get("/editor", response_class=HTMLResponse)
async def editor_page():
    """Split-panel editor page."""
    for p in [Path.home() / "inxotive-builder", Path.home() / "market-api"]:
        path = p / "editor.html"
        if path.exists():
            return HTMLResponse(path.read_text())
    return HTMLResponse("<h1>Editor not found</h1>", status_code=404)


@app.get("/client-portal", response_class=HTMLResponse)
async def client_portal_page():
    cp_path = Path.home() / "market-api" / "client-portal.html"
    if cp_path.exists():
        return HTMLResponse(cp_path.read_text())
    return HTMLResponse("<h1>Client Portal not found</h1>", status_code=404)


@app.get("/portal/{token}", response_class=HTMLResponse)
async def client_portal_token(token: str):
    """Serve client portal with token-based access."""
    result = verify_portal_token(token)
    if not result:
        return HTMLResponse("""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <title>Akses Tidak Valid</title>
        <style>body{font-family:sans-serif;background:#0f172a;color:#e2e8f0;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center}
        h1{color:#ef4444}a{color:#38bdf8}</style></head>
        <body><div><h1>🔒 Token Tidak Valid</h1><p>Link akses tidak ditemukan atau sudah kedaluwarsa.</p>
        <p><a href="/client-portal">Kembali ke Portal</a></p></div></body></html>""", status_code=404)

    cp_path = Path.home() / "market-api" / "client-portal.html"
    if cp_path.exists():
        html = cp_path.read_text()
        # Inject client data
        html = html.replace("<!-- CLIENT_DATA -->", json.dumps(result, ensure_ascii=False))
        return HTMLResponse(html)
    return HTMLResponse("<h1>Client Portal not found</h1>", status_code=404)


# ── Templates ──

@app.get("/api/templates")
async def api_templates():
    return {"templates": list_templates()}


@app.get("/api/templates/{tid}")
async def api_template_detail(tid: str):
    t = get_template(tid)
    if t is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return t


@app.get("/api/themes/visuals")
async def api_theme_visuals(industry: str = ""):
    from builder import list_theme_visuals
    return {"themes": list_theme_visuals(industry)}


@app.get("/api/stock/search")
async def api_stock_search(q: str = "hero", count: int = 4):
    """Search free stock images by keyword. No API key needed."""
    try:
        from web_engine.illustration_resolver import search_images, list_industry_images
        urls = search_images(q, count=min(count, 12))
        if not urls:
            return {"query": q, "count": 0, "images": [], "suggestions": list(list_industry_images().keys())}
        return {"query": q, "count": len(urls), "images": urls}
    except ImportError:
        return {"error": "Image resolver not available"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/stock/categories")
async def api_stock_categories():
    """List all available stock image categories."""
    try:
        import sys
        sys.path.insert(0, str(Path.home() / "market-api"))
        from web_engine.illustration_resolver import list_industry_images
        return list_industry_images()
    except ImportError:
        return {"error": "Image resolver not available"}
    except Exception as e:
        return {"error": str(e)}


# ── Design API ──

@app.post("/api/design/generate")
async def api_design_generate(data: dict):
    """Generate a website from natural language description.
    Uses AI Orchestrator + Section Assembler for full AI-powered design.
    """
    try:
        prompt = data.get("prompt", "").strip()
        template_id = data.get("template", "landing-tech")
        design_system = data.get("design_system")
        model = data.get("model", "9router-gemini-flash")
        images = data.get("images", [])
        site_only = data.get("site_only", False)  # If True, only create site config, not full HTML

        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        # ── Use AI Orchestrator + Assembler ──
        try:
            from ai_orchestrator import AIOrchestrator
            from ai_assembler import SectionAssembler

            orchestrator = AIOrchestrator()
            spec = await orchestrator.generate_spec(prompt, model)

            if spec and spec.get("sections"):
                # Assemble full HTML
                assembler = SectionAssembler()
                html = assembler.assemble(spec)

                # Extract site name
                site_name = prompt.split()[:5]
                site_name = " ".join(site_name).title()[:40]

                # Create site
                from builder import create_site, update_site_config
                site_data = {
                    "name": site_name,
                    "template": template_id,
                    "theme": design_system or spec.get("brand", "inxotive"),
                    "config": {
                        "name": site_name,
                        "brand": spec.get("brand", "inxotive"),
                        "sections": spec.get("sections", []),
                        "ai_generated": True,
                        "model": model,
                        "prompt": prompt,
                    }
                }
                site = create_site(site_data)

                if site and site.get("id"):
                    # Save the generated HTML
                    import os
                    from pathlib import Path
                    clients_dir = Path.home() / "clients"
                    site_dir = clients_dir / f"site-{site_name.lower().replace(' ', '-')[:30]}"
                    site_dir.mkdir(parents=True, exist_ok=True)
                    (site_dir / "index.html").write_text(html)

                    update_site_config(site["id"], site_data["config"])

                    # Log prompt
                    try:
                        import httpx as _httpx
                        _ = _httpx.post("http://localhost:7777/api/design/prompt-log", json={
                            "prompt": prompt[:200], "model": model,
                            "siteId": site["id"], "success": True
                        }, timeout=2)
                    except Exception:
                        pass

                    return {
                        "success": True,
                        "siteId": site["id"],
                        "html": html[:500] + "..." if len(html) > 500 else html,
                        "message": f'✅ Situs "{site_name}" berhasil dibuat dengan AI!'
                    }
        except ImportError:
            # ai_orchestrator/assembler not available — use fallback
            pass
        except Exception as e:
            # Log error but still fallback gracefully
            import logging
            logging.warning(f"AI Orchestrator failed (fallback to old method): {e}")

        # ── Fallback: Original parsing method ──
        site_config = await parse_design_prompt(prompt, template_id, design_system, model)
        from builder import create_site, update_site_config
        site_name = site_config.get("name") or _extract_name(prompt)
        site_data = {
            "name": site_name,
            "template": template_id,
            "theme": design_system or "inxotive",
            "config": site_config
        }
        site = create_site(site_data)

        if site and site.get("id"):
            update_site_config(site["id"], site_config)
            return {
                "success": True,
                "siteId": site["id"],
                "message": f'Situs "{site_name}" berhasil dibuat!'
            }
        else:
            return {"success": False, "error": "Gagal membuat site"}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/design/edit")
async def api_design_edit(data: dict):
    """Edit existing site using AI instruction.
    Accepts siteId + instruction → modifies site config → returns updated preview.
    """
    try:
        site_id = data.get("siteId", "").strip()
        instruction = data.get("instruction", "").strip()
        model = data.get("model", "9router-gemini-flash")

        if not site_id or not instruction:
            raise HTTPException(status_code=400, detail="siteId and instruction required")

        from builder import get_site, update_site_config
        site = get_site(site_id)
        if not site:
            return {"success": False, "error": "Site not found"}

        # Use AI to adjust sections based on instruction
        try:
            from ai_orchestrator import AIOrchestrator
            orchestrator = AIOrchestrator()

            # Generate a refined spec based on instruction + existing config
            context = f"{instruction} (site: {site.get('name', '')})"
            spec = await orchestrator.generate_spec(context, model)

            if spec and spec.get("sections"):
                config = site.get("config", {})
                config["sections"] = spec["sections"]
                if spec.get("brand"):
                    config["brand"] = spec["brand"]
                config["ai_refined"] = True
                config["ai_model"] = model
                update_site_config(site_id, config)

                return {
                    "success": True,
                    "siteId": site_id,
                    "message": f'Site "{site.get("name", "")}" berhasil diperbarui!'
                }
        except ImportError:
            pass

        return {"success": False, "error": "AI edit failed - fallback to manual editing"}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/design/clone")
async def api_design_clone(data: dict):
    """Clone an existing website and adapt to brand.
    Body: {"url": "https://example.com", "brand": "inxotive", "name": "My Clone"}
    Pipeline: capture → extract styles → analyze layout → map to SectionSpec → render via SectionAssembler.
    """
    url = data.get("url", "").strip()
    brand_name = data.get("brand", "inxotive").strip()
    site_name = data.get("name", "").strip() or "Cloned Site"

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # Import CloneEngine from market-api
        import sys as _sys
        from pathlib import Path as _Path
        _sys.path.insert(0, str(_Path.home() / "market-api"))
        from web_engine.clone_engine import CloneEngine

        # Run clone pipeline (steps 1-3: capture, extract styles, analyze)
        engine = CloneEngine(brand_name=brand_name)
        reference = await engine.capture_reference(url)
        if not reference or not reference.get("success"):
            return {"success": False, "error": reference.get("error", "Failed to capture website")}

        styles = await engine.extract_styles(url)
        analysis = await engine.analyze_layout(
            reference.get("screenshot_b64", ""),
            reference.get("page_info", {}),
        )

        page_info = reference.get("page_info", {})
        page_title = page_info.get("title", site_name)

        # Map analysis to SectionSpec format for SectionAssembler
        from ai_orchestrator import AIOrchestrator
        orchestrator = AIOrchestrator()

        # Use fallback spec (generates sections with default content)
        # Then override colors and brand from clone analysis
        analysis_sections = analysis.get("sections", []) if isinstance(analysis, dict) else []
        section_types = [s.get("type", "hero") for s in analysis_sections if isinstance(s, dict)]
        if not section_types:
            section_types = ["hero", "features", "testimonials", "cta", "contact"]

        spec = orchestrator._fallback_spec(page_title, "general", section_types)
        spec["brand"] = brand_name

        # Override colors from extracted styles
        if isinstance(analysis, dict):
            color_palette = analysis.get("color_palette", {})
            if color_palette and isinstance(color_palette, dict):
                spec["colors"] = {
                    "primary": color_palette.get("primary", "#6366f1"),
                    "secondary": color_palette.get("secondary", "#8b5cf6"),
                    "accent": color_palette.get("accent", "#f59e0b"),
                }

        # Render via SectionAssembler
        from ai_assembler import SectionAssembler
        assembler = SectionAssembler()
        html = assembler.assemble(spec, brand_name)

        # Create builder site
        from builder import create_site, update_site_config
        site_data = {
            "name": page_title[:40] or site_name,
            "template": "landing-tech",
            "theme": brand_name,
            "config": {
                "name": page_title[:40] or site_name,
                "brand": brand_name,
                "sections": spec.get("sections", []),
                "ai_generated": True,
                "model": "clone-engine",
                "source_url": url,
                "clone_analysis": analysis if isinstance(analysis, dict) else {},
            }
        }
        site = create_site(site_data)

        if site and site.get("id"):
            update_site_config(site["id"], site_data["config"])
            return {
                "success": True,
                "siteId": site["id"],
                "name": page_title[:40] or site_name,
                "html": html[:500] + "..." if len(html) > 500 else html,
                "message": f'✅ Site cloned as "{page_title[:40] or site_name}"!'
            }
        else:
            return {"success": False, "error": "Failed to create builder site"}

    except ImportError as e:
        return {"success": False, "error": f"Clone engine not available: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/design/models")
async def api_design_models():
    """List available AI models for design generation."""
    return {
        "models": {
            "9router": [
                {"id": "9router-gemini-flash", "name": "Gemini 3 Flash", "provider": "9Router (Google)", "badge": "⚡ Fast"},
                {"id": "9router-nemotron", "name": "Nemotron 3 Ultra", "provider": "9Router (NVIDIA)", "badge": "🎯 Best"},
                {"id": "9router-claude", "name": "Claude Haiku 4.5", "provider": "9Router (Anthropic)", "badge": "🧠 Smart"},
                {"id": "9router-deepseek", "name": "DeepSeek V4", "provider": "9Router", "badge": "🐋 Deep"},
            ],
            "local": [
                {"id": "local-qwen", "name": "Qwen2.5 7B", "provider": "Ollama VPS (qwen2.5)", "badge": "💻 VPS"},
            ],
            "api": [
                {"id": "api-gemini", "name": "Gemini 3 Flash", "provider": "Direct API", "badge": "☁️ API"},
                {"id": "api-claude", "name": "Claude Opus 4.8", "provider": "Direct API", "badge": "💰 Premium"},
            ]
        }
    }


@app.get("/api/design/projects")
async def api_design_projects():
    """List projects for the design page."""
    from builder import list_sites
    sites = list_sites()
    return {
        "projects": [{
            "id": s["id"],
            "name": s.get("name", "Untitled"),
            "template": s.get("template", ""),
            "status": s.get("status", "draft"),
            "updatedAt": s.get("updated_at", ""),
            "thumbnail": s.get("thumbnail", ""),
            "owner": "You"
        } for s in sites]
    }


# ── Helpers ──

def _extract_name(prompt: str) -> str:
    """Extract a short site name from prompt."""
    words = prompt.split()
    # Take first meaningful words
    name = " ".join(words[:5]) if len(words) > 5 else prompt
    if len(name) > 40:
        name = name[:40]
    return name.strip().title()


async def parse_design_prompt(prompt: str, template_id: str, design_system: str | None, model: str) -> dict:
    """Parse a design prompt into site configuration.

    Uses the selected AI model to extract structured data from the prompt.
    Falls back to simple extraction if AI is unavailable.
    """
    config = {
        "name": _extract_name(prompt),
        "description": prompt,
        "template": template_id,
        "theme": design_system or "inxotive",
        "model_used": model,
        "pages": _detect_pages(prompt),
    }

    # Try AI-based parsing for richer config
    try:
        if model.startswith("local-"):
            # Try Ollama for local model
            ollama_config = await _call_ollama(prompt, template_id)
            if ollama_config:
                config.update(ollama_config)
        elif model.startswith("9router-"):
            # Try 9Router API
            proxy_config = await _call_9router(prompt, template_id, model)
            if proxy_config:
                config.update(proxy_config)
        elif model.startswith("api-"):
            # Try direct API
            api_config = await _call_direct_api(prompt, template_id, model)
            if api_config:
                config.update(api_config)
    except Exception:
        # Fallback to keyword-based config
        config.update(_keyword_config(prompt))

    return config


def _detect_pages(prompt: str) -> list:
    """Detect which pages are mentioned in the prompt."""
    prompt_lower = prompt.lower()
    pages = ["home"]
    keywords = {
        "about": ["about", "tentang", "about us", "story", "cerita"],
        "services": ["service", "layanan", "what we do", "offer", "product"],
        "gallery": ["gallery", "galeri", "portfolio", "work"],
        "blog": ["blog", "article", "artikel", "news", "post"],
        "pricing": ["price", "harga", "paket", "plan", "subscription", "biaya"],
        "contact": ["contact", "kontak", "get in touch", "hubungi"],
        "faq": ["faq", "faqs", "question", "tanya"],
        "testimonials": ["testimonial", "review", "ulasan"],
    }
    for page, keywords_list in keywords.items():
        if any(kw in prompt_lower for kw in keywords_list):
            pages.append(page)
    return list(dict.fromkeys(pages))  # deduplicate preserving order


def _keyword_config(prompt: str) -> dict:
    """Simple keyword-based config extraction as fallback."""
    prompt_lower = prompt.lower()
    config = {}

    # Detect industry
    industries = {
        "healthcare": ["klinik", "dokter", "rumah sakit", "hospital", "medical", "sehat", "health"],
        "fnb": ["restoran", "makanan", "minuman", "cafe", "kafe", "food", "restaurant", "kuliner"],
        "tech": ["teknologi", "startup", "saas", "software", "app", "tech", "digital"],
        "luxury": ["luxury", "mewah", "premium", "eksklusif", "high-end"],
        "education": ["sekolah", "pendidikan", "course", "learning", "belajar", "education", "kursus"],
        "fashion": ["fashion", "pakaian", "clothing", "style", "baju"],
        "fitness": ["fitness", "gym", "olahraga", "sport", "yoga"],
        "wellness": ["spa", "wellness", "salon", "beauty", "kecantikan"],
        "corporate": ["perusahaan", "corporate", "company", "bisnis", "business", "kantor"],
        "creative": ["creative", "kreatif", "art", "seni", "design", "desain"],
    }
    for industry, keywords in industries.items():
        if any(kw in prompt_lower for kw in keywords):
            config["industry"] = industry
            break

    # Detect color vibe
    color_vibes = {
        "dark": ["dark", "gelap", "malam", "night", "black"],
        "bright": ["bright", "cerah", "warna-warni", "colorful"],
        "minimal": ["minimal", "clean", "bersih", "sederhana", "simple", "white"],
        "natural": ["natural", "alam", "hijau", "green", "nature", "organic"],
        "luxury": ["emas", "gold", "mewah", "luxury", "elegan", "elegant"],
    }
    for vibe, keywords in color_vibes.items():
        if any(kw in prompt_lower for kw in keywords):
            config["color_vibe"] = vibe
            break

    return config


async def _call_ollama(prompt: str, template_id: str) -> dict | None:
    """Call Ollama VPS (qwen2.5:7b) for prompt parsing.
    Tries VPS via Tailscale first, falls back to localhost.
    """
    import aiohttp
    import json as j

    OLLAMA_ENDPOINTS = [
        "http://100.78.79.60:11434",   # VPS via Tailscale
        "http://localhost:11434",        # lokal / VPS langsung
    ]
    MODEL = "qwen2.5:7b"

    payload = {
        "model": MODEL,
        "prompt": f"""Extract website configuration from this client description.
Return ONLY valid JSON with these fields: name (string), tagline (string), industry (string).

Description: {prompt}

JSON:""",
        "stream": False,
        "options": {"temperature": 0.1}
    }

    for endpoint in OLLAMA_ENDPOINTS:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{endpoint}/api/generate", json=payload, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        text = data.get("response", "")
                        try:
                            start = text.index('{')
                            end = text.rindex('}') + 1
                            return j.loads(text[start:end])
                        except (ValueError, j.JSONDecodeError):
                            return None
        except Exception:
            continue
    return None


async def _call_9router(prompt: str, template_id: str, model: str) -> dict | None:
    """Call 9Router API for prompt parsing."""
    import aiohttp
    try:
        model_map = {
            "9router-gemini-flash": "google/gemini-2.0-flash-001",
            "9router-nemotron": "nvidia/llama-nemotron-3-ultra",
            "9router-claude": "anthropic/claude-haiku-4-5",
            "9router-deepseek": "deepseek/deepseek-v4",
        }
        api_model = model_map.get(model, "google/gemini-2.0-flash-001")

        async with aiohttp.ClientSession() as session:
            payload = {
                "model": api_model,
                "messages": [
                    {"role": "system", "content": "Extract website config from user description. Respond ONLY with valid JSON: {name, tagline, industry, color_scheme, style}"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 300
            }
            # 9Router endpoint — adjust if needed
            async with session.post(
                "https://9router.com/v1/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {os.environ.get('NINE_ROUTER_API_KEY', '')}"},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    import json as j
                    try:
                        start = content.index('{')
                        end = content.rindex('}') + 1
                        return j.loads(content[start:end])
                    except (ValueError, j.JSONDecodeError):
                        return None
    except Exception:
        return None


async def _call_direct_api(prompt: str, template_id: str, model: str) -> dict | None:
    """Call direct API (Gemini or Claude) for prompt parsing."""
    import aiohttp
    try:
        if "gemini" in model:
            # Google Gemini API
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                return None
            async with aiohttp.ClientSession() as session:
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Extract website config as JSON: {{name, tagline, industry, style}} from: {prompt}"}]
                    }]
                }
                async with session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        import json as j
                        try:
                            start = text.index('{')
                            end = text.rindex('}') + 1
                            return j.loads(text[start:end])
                        except (ValueError, j.JSONDecodeError):
                            return None
        elif "claude" in model:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                return None
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "claude-opus-4-8-20250514",
                    "max_tokens": 300,
                    "messages": [{
                        "role": "user",
                        "content": f"Extract website config as JSON: {{name, tagline, industry, style}} from: {prompt}. Respond only with JSON."
                    }]
                }
                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    json=payload,
                    headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        text = data["content"][0]["text"]
                        import json as j
                        try:
                            start = text.index('{')
                            end = text.rindex('}') + 1
                            return j.loads(text[start:end])
                        except (ValueError, j.JSONDecodeError):
                            return None
    except Exception:
        return None


# ── PHASE 3c: AI LEARNING LOOP ──
PROMPT_LOG = []       # In-memory prompt history (persist to file in production)
FEEDBACK_LOG = []     # In-memory feedback
MODEL_SCORES = {}     # model_id → { wins: N, total: N, avg_score: float }

PROMPT_LOG_FILE = Path.home() / ".ai_prompt_log.json"


def _load_prompt_log():
    global PROMPT_LOG
    try:
        if PROMPT_LOG_FILE.exists():
            with open(PROMPT_LOG_FILE) as f:
                PROMPT_LOG = json.load(f)
    except Exception:
        PROMPT_LOG = []


def _save_prompt_log():
    try:
        PROMPT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROMPT_LOG_FILE, 'w') as f:
            json.dump(PROMPT_LOG[-500:], f, indent=2)  # Keep last 500
    except Exception:
        pass


@app.post("/api/design/feedback")
async def api_design_feedback(data: dict):
    """Record user feedback on AI-generated design.
    Body: {"siteId": "...", "rating": 1-5, "feedback": "optional text", "prompt": "original prompt", "model": "model used"}
    """
    site_id = data.get("siteId", "").strip()
    rating = data.get("rating", 3)
    feedback_text = data.get("feedback", "").strip()
    prompt = data.get("prompt", "").strip()
    model = data.get("model", "").strip()

    entry = {
        "siteId": site_id,
        "rating": max(1, min(5, rating)),
        "feedback": feedback_text,
        "prompt": prompt,
        "model": model,
        "timestamp": datetime.now().isoformat(),
    }
    FEEDBACK_LOG.append(entry)

    # Update model scores
    if model:
        if model not in MODEL_SCORES:
            MODEL_SCORES[model] = {"wins": 0, "total": 0, "avg_score": 0.0}
        MODEL_SCORES[model]["total"] += 1
        if rating >= 4:
            MODEL_SCORES[model]["wins"] += 1
        MODEL_SCORES[model]["avg_score"] = (
            MODEL_SCORES[model]["wins"] / MODEL_SCORES[model]["total"]
        )

    return {"success": True, "entry": entry}


@app.get("/api/design/feedback/summary")
async def api_design_feedback_summary():
    """Get feedback summary and model performance."""
    return {
        "total_feedback": len(FEEDBACK_LOG),
        "total_prompts": len(PROMPT_LOG),
        "model_scores": MODEL_SCORES,
        "recommended_model": _get_recommended_model(),
    }


def _get_recommended_model() -> str:
    """Return model with best avg_score (min 3 samples)."""
    best = "9router-gemini-flash"
    best_score = 0.5
    for model_id, stats in MODEL_SCORES.items():
        if stats["total"] >= 3 and stats["avg_score"] > best_score:
            best = model_id
            best_score = stats["avg_score"]
    return best


@app.post("/api/design/prompt-log")
async def api_design_prompt_log(data: dict):
    """Log a prompt → model → output mapping for analysis."""
    entry = {
        "prompt": data.get("prompt", "").strip(),
        "model": data.get("model", "").strip(),
        "siteId": data.get("siteId", "").strip(),
        "success": data.get("success", False),
        "timestamp": datetime.now().isoformat(),
    }
    PROMPT_LOG.append(entry)
    _save_prompt_log()
    return {"success": True}


@app.get("/api/design/prompt-log")
async def api_design_prompt_log_list(limit: int = 20):
    """Get recent prompt log entries."""
    return {"entries": PROMPT_LOG[-limit:]}


# ── Clients ──

@app.get("/api/clients")
async def api_clients():
    return {"clients": list_clients()}


@app.get("/api/clients/{cid}")
async def api_client_detail(cid: str):
    c = get_client(cid)
    if c is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return c


@app.post("/api/clients")
async def api_create_client(data: dict):
    if not data.get("name"):
        raise HTTPException(status_code=400, detail="Client name is required")
    return create_client(data)


@app.put("/api/clients/{cid}")
async def api_update_client(cid: str, data: dict):
    result = update_client(cid, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return result


@app.delete("/api/clients/{cid}")
async def api_delete_client(cid: str):
    ok = delete_client(cid)
    if not ok:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True}


# ── Sites ──

@app.get("/api/sites")
async def api_sites(status: str = ""):
    return {"sites": list_sites(status_filter=status or None)}


@app.get("/api/sites/{sid}")
async def api_site_detail(sid: str):
    s = get_site(sid)
    if s is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return s


@app.post("/api/sites")
async def api_create_site(data: dict):
    result = create_site(data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return JSONResponse(result, status_code=201)


@app.put("/api/sites/{sid}/config")
async def api_update_site_config(sid: str, data: dict):
    result = update_site_config(sid, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Site not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/api/sites/{sid}/build")
async def api_build_site(sid: str):
    result = build_site(sid)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/api/sites/{sid}/deploy")
async def api_deploy_site(sid: str):
    result = deploy_site(sid)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/api/sites/{sid}/domain")
async def api_set_domain(sid: str, data: dict):
    domain = data.get("domain", "")
    if not domain:
        raise HTTPException(status_code=400, detail="Domain is required")
    result = set_site_domain(sid, domain)
    return result


@app.delete("/api/sites/{sid}")
async def api_delete_site(sid: str):
    ok = delete_site(sid)
    if not ok:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"ok": True}


# ── Preview ──

@app.get("/api/sites/{sid}/preview")
async def api_preview_site(sid: str, page: str = "home"):
    """Render live preview of site. Returns full HTML page.
    AI-generated sites use SectionAssembler (unified CSS vars framework).
    Existing templates use web_engine or dist/.
    """
    from builder import get_site, render_html_site, generate_multi_page_site, load_data

    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    template_id = site.get("template", "landing")
    config = site.get("config", {}) or {}

    # ── AI-generated sites: use SectionAssembler (unified rendering) ──
    if config.get("ai_generated") or config.get("sections"):
        try:
            from ai_assembler import SectionAssembler
            from brand_registry import get_registry

            registry = get_registry()
            theme = site.get("theme", "inxotive")
            brand = registry.get(theme)

            sections_config = config.get("sections", [])
            if sections_config:
                spec = {
                    "brand": theme,
                    "title": site.get("name", "INXOTIVE Design"),
                    "sections": sections_config,
                    "colors": registry.get_colors(theme),
                }
                if brand:
                    spec["fonts"] = brand.fonts

                assembler = SectionAssembler()
                html = assembler.assemble(spec, theme)
                return HTMLResponse(html)
        except ImportError:
            pass
        except Exception as e:
            return HTMLResponse(f"<html><body><h2>Preview Error</h2><pre>{e}</pre></body></html>", status_code=500)

    # ── HTML template: render via web_engine ──
    from builder import TEMPLATE_REGISTRY
    tpl = TEMPLATE_REGISTRY.get(template_id, {})
    if tpl.get("type") == "html":
        content_overrides = {}
        if config:
            content_overrides = {"brand": config.get("brand", {}), "contact": config.get("contact", {})}
        try:
            html = render_html_site(
                template_id,
                brand_name=site.get("name", "INXOTIVE"),
                industry=site.get("industry", "general"),
                content_overrides=content_overrides,
            )
            return HTMLResponse(html)
        except Exception as e:
            return HTMLResponse(f"<html><body><h2>Preview Error</h2><pre>{e}</pre></body></html>", status_code=500)

    # ── React template ──
    site_dir = Path(site.get("directory", ""))
    if not site_dir.exists():
        return HTMLResponse("<html><body><h2>Site directory not found</h2></body></html>", status_code=404)

    dist_index = site_dir / "dist" / "index.html"
    if dist_index.exists():
        html = dist_index.read_text()
        html = html.replace('src="/assets/', 'src="/site-assets/' + sid + '/assets/')
        html = html.replace('href="/assets/', 'href="/site-assets/' + sid + '/assets/')
        return HTMLResponse(html)

    if page != "home":
        dist_page = site_dir / "dist" / f"{page}.html"
        if dist_page.exists():
            return HTMLResponse(dist_page.read_text())

    return HTMLResponse(f"""<!DOCTYPE html><html><head><title>{site.get('name', 'Site')} &mdash; Preview</title>
<style>body{{font-family:sans-serif;background:#0f172a;color:#e2e8f0;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;flex-direction:column}}
h1{{color:#38bdf8;margin-bottom:8px}}p{{color:#94a3b8}}button{{background:#4F46E5;color:white;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px}}</style>
<body><div><h1>&#128640; Site Not Built Yet</h1><p>Click <strong>Build</strong> first to generate the site files.</p></div></body></html>""")


# ── Static asset serving for site previews ──

@app.get("/site-assets/{sid:path}")
async def site_static_assets(sid: str):
    """Serve static assets for site preview (JS/CSS/images from dist/assets/)."""
    from builder import get_site, load_data
    import os

    data = load_data()

    # sid format is "{site_id}/assets/{filepath}"
    parts = sid.split("/", 1)
    site_id = parts[0]
    filepath = parts[1] if len(parts) > 1 else ""

    if not site_id or not filepath:
        raise HTTPException(status_code=400, detail="Invalid path")

    s = data["sites"].get(site_id)
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")

    # Security: prevent path traversal
    resolved = (Path(s["directory"]) / "dist" / filepath).resolve()
    allowed_base = (Path(s["directory"]) / "dist").resolve()
    if not str(resolved).startswith(str(allowed_base)):
        raise HTTPException(status_code=403, detail="Path traversal blocked")
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="Asset not found")

    # Determine media type
    ext = resolved.suffix.lower()
    media_types = {
        ".js": "application/javascript",
        ".css": "text/css",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".json": "application/json",
    }
    mtype = media_types.get(ext, "application/octet-stream")
    return FileResponse(str(resolved), media_type=mtype)


@app.get("/api/sites/{sid}/preview-frame")
async def api_preview_frame(sid: str):
    """Return the preview iframe HTML inject for builder UI."""
    from builder import get_site
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    template_id = site.get("template", "landing")

    # Check if site has multi-page
    pages = site.get("pages", ["home"])
    page_buttons = "".join([f'<button class="pv-page-btn {"active" if p == "home" else ""}" onclick="previewPage(\'{p}\')">{p.title()}</button>' for p in pages])

    html = f"""<!DOCTYPE html>
<html><head><style>
body{{margin:0;padding:0;background:#0f172a;font-family:sans-serif}}
.pv-container{{display:flex;flex-direction:column;height:100vh}}
.pv-toolbar{{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#1e293b;border-bottom:1px solid #334155;flex-wrap:wrap}}
.pv-toolbar .pv-title{{color:#e2e8f0;font-size:13px;font-weight:600;margin-right:auto}}
.pv-toolbar button{{padding:4px 12px;border-radius:4px;border:1px solid #475569;background:#334155;color:#cbd5e1;font-size:12px;cursor:pointer}}
.pv-toolbar button.active{{background:#4F46E5;border-color:#4F46E5;color:white}}
.pv-toolbar button:hover{{background:#475569}}
.pv-toolbar .pv-badge{{font-size:10px;padding:2px 8px;border-radius:999px;background:#059669;color:white}}
.pv-iframe-wrapper{{flex:1;overflow:hidden}}
.pv-iframe-wrapper iframe{{width:100%;height:100%;border:none;background:white}}
.pv-devices{{display:flex;gap:4px}}
.pv-devices button{{padding:4px 8px;font-size:11px}}
</style></head><body>
<div class="pv-container">
  <div class="pv-toolbar">
    <span class="pv-title">&#128269; {site.get('name', 'Preview')}</span>
    <span class="pv-badge">{template_id}</span>
    <div class="pv-devices">
      <button onclick="setPreviewWidth('100%')" class="active" id="pv-d-desktop">&#128187; Desktop</button>
      <button onclick="setPreviewWidth('768px')" id="pv-d-tablet">&#128241; Tablet</button>
      <button onclick="setPreviewWidth('375px')" id="pv-d-mobile">&#128241; Mobile</button>
    </div>
    <div style="display:flex;gap:4px">{page_buttons}</div>
    <button onclick="refreshPreview()">&#128260; Refresh</button>
  </div>
  <div class="pv-iframe-wrapper" style="display:flex;justify-content:center;background:#1e293b">
    <iframe id="pv-frame" src="/api/sites/{sid}/preview" style="max-width:100%;height:100%"></iframe>
  </div>
</div>
<script>
function setPreviewWidth(w) {{document.getElementById('pv-frame').style.width=w;
  document.querySelectorAll('.pv-devices button').forEach(b=>b.classList.remove('active'));
  if(w=='100%') document.getElementById('pv-d-desktop').classList.add('active');
  else if(w=='768px') document.getElementById('pv-d-tablet').classList.add('active');
  else document.getElementById('pv-d-mobile').classList.add('active');}}
function refreshPreview() {{document.getElementById('pv-frame').src='/api/sites/{sid}/preview?t='+Date.now()}}
function previewPage(p) {{document.getElementById('pv-frame').src='/api/sites/{sid}/preview?page='+p+'&t='+Date.now();
  document.querySelectorAll('.pv-page-btn').forEach(b=>b.classList.remove('active'));
  event.target.classList.add('active');}}
</script>
</div></body></html>"""
    return HTMLResponse(html)


# ── Assets ──

@app.get("/api/assets")
async def api_assets(site_id: str = ""):
    return {"assets": list_assets(site_id=site_id or None)}


@app.post("/api/assets/upload")
async def api_upload_asset(request: Request):
    try:
        form = await request.form()
        client_id = form.get("client_id", "")
        site_id = form.get("site_id", "")
        file = form.get("file")
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        if not site_id:
            raise HTTPException(status_code=400, detail="site_id is required")
        content = await file.read()
        result = upload_asset(client_id, site_id, file.filename, content, file.content_type or "")
        return result, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/assets/file/{aid}")
async def api_asset_file(aid: str):
    data = load_data()
    a = data["assets"].get(aid)
    if not a:
        raise HTTPException(status_code=404, detail="Asset not found")
    fp = Path(a.get("path", ""))
    if not fp.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(str(fp), media_type=a.get("content_type") or "application/octet-stream",
                        filename=a.get("filename", "file"))


@app.delete("/api/assets/{aid}")
async def api_delete_asset(aid: str):
    ok = delete_asset(aid)
    if not ok:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"ok": True}


# ── Client Portal ──

@app.post("/api/portal/token")
async def api_generate_portal_token(data: dict):
    cid = data.get("client_id", "")
    if not cid:
        raise HTTPException(status_code=400, detail="client_id is required")
    token = generate_portal_token(cid)
    return {"token": token, "portal_url": f"/portal/{token}"}


@app.get("/api/portal/verify/{token}")
async def api_verify_portal_token(token: str):
    result = verify_portal_token(token)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid or expired token")
    return result


@app.post("/api/portal/request")
async def api_portal_request(data: dict):
    """Submit a change request from client portal."""
    token = data.get("token", "")
    if not token:
        raise HTTPException(status_code=400, detail="token is required")
    result = verify_portal_token(token)
    if not result:
        raise HTTPException(status_code=403, detail="Invalid token")

    client = result.get("client", {})
    sites = result.get("sites", [])
    message = data.get("message", "")
    request_type = data.get("type", "revisi")

    # Format for Discord
    site_names = ", ".join(s.get("name", "-") for s in sites)
    webhook_url = os.environ.get("DISCORD_WEBHOOK", "")
    if webhook_url:
        try:
            import httpx as _httpx
            payload = {
                "content": (
                    f"📩 **Client Request — {client.get('name', 'Unknown')}**\n"
                    f"**Client:** {client.get('name', '-')} ({client.get('company', '-')})\n"
                    f"**Site:** {site_names}\n"
                    f"**Type:** {request_type}\n"
                    f"**Message:** {message[:1500]}"
                ),
                "username": "Client Portal"
            }
            _httpx.post(webhook_url, json=payload, timeout=10)
        except:
            pass

    return {"success": True, "message": "Request sent to INXOTIVE team"}


# ── Dashboard stats ──

@app.get("/api/stats")
async def api_stats():
    """Quick stats for builder overview."""
    data = load_data()
    sites = data.get("sites", {})
    clients = data.get("clients", {})
    assets = data.get("assets", {})
    return {
        "clients": len(clients),
        "sites": len(sites),
        "assets": len(assets),
        "live_sites": sum(1 for s in sites.values() if s.get("status") == "deployed"),
        "built_sites": sum(1 for s in sites.values() if s.get("status") == "built"),
        "contacted_clients": sum(1 for c in clients.values() if c.get("status") == "contacted"),
        "won_clients": sum(1 for c in clients.values() if c.get("status") == "won"),
    }


    # ── Live Preview ──

@app.get("/api/preview/{sid}")
async def api_preview(sid: str):
    """Serve built site HTML with base tag for assets."""
    data = load_data()
    s = data["sites"].get(sid)
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")
    site_dir = Path(s.get("directory", ""))
    dist_idx = site_dir / "dist" / "index.html"
    if dist_idx.exists():
        html = dist_idx.read_text()
        # Strip leading / from absolute paths so base tag can resolve them
        html = html.replace('src="/', 'src="')
        html = html.replace('href="/', 'href="')
        # THEN inject base tag for relative paths
        html = html.replace("<head>", '<head><base href="/api/preview/%s/">' % sid)
        return HTMLResponse(html)
    bs = build_site(sid)
    if bs.get("success") and dist_idx.exists():
        html = dist_idx.read_text()
        html = html.replace('src="/', 'src="')
        html = html.replace('href="/', 'href="')
        html = html.replace("<head>", '<head><base href="/api/preview/%s/">' % sid)
        return HTMLResponse(html)
    return HTMLResponse('<div style="padding:40px;text-align:center;color:#64748b;font-family:sans-serif"><h2>No Preview</h2><p>Build the site first</p></div>')


@app.get("/api/preview/{sid}/{file_path:path}")
async def api_preview_file(sid: str, file_path: str):
    """Serve any static file from dist/ (JS, CSS, favicon, images)."""
    from fastapi.responses import FileResponse
    import mimetypes
    data = load_data()
    s = data["sites"].get(sid)
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")
    base = Path(s.get("directory", "")) / "dist"
    for try_path in [base / file_path, base / "assets" / file_path]:
        if try_path.exists():
            mt, _ = mimetypes.guess_type(str(try_path))
            return FileResponse(str(try_path), media_type=mt or "application/octet-stream")
    raise HTTPException(status_code=404, detail="Not found")


# ── Part C: Per-Section Editor Controls ──

@app.post("/api/sites/{sid}/section/{idx}/regenerate")
async def api_section_regenerate(sid: str, idx: int, data: dict = {}):
    """
    Regenerate ONE section with a different random variant.
    Returns just the section HTML, not the full page.
    """
    from css_framework import generate_archetype_page
    from brand_registry import get_registry
    import re

    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    theme = site.get("theme", "inxotive")
    registry = get_registry()
    brand = registry.get(theme)
    if not brand:
        raise HTTPException(status_code=400, detail=f"Unknown brand: {theme}")

    arch_config = registry.get_archetype_config(theme)
    section_order = arch_config["section_order"]

    if idx < 0 or idx >= len(section_order):
        raise HTTPException(status_code=400, detail=f"Invalid section index {idx}, max {len(section_order)-1}")

    section_type = section_order[idx]
    name = site.get("name", "INXOTIVE")

    # Generate a full page, then extract just the requested section
    try:
        full_html = generate_archetype_page(theme)
        # Find section wrapper with matching data-section-idx
        pattern = f'<div class="section-wrapper" data-section-idx="{idx}"[^>]*>.*?</div>\\s*</div>\\s*(?=</?div|<section|$)'
        # Simpler: find by wrapping markers
        section_match = re.search(
            f'<div class="section-wrapper" data-section-idx="{idx}"[^>]*>.*?</div>\\s*</div>',
            full_html, re.DOTALL
        )
        if section_match:
            return {"idx": idx, "section_type": section_type, "html": section_match.group(0)}
        else:
            # Fallback: regenerate with a different variant
            return {"idx": idx, "section_type": section_type, "html": f"<!-- Section {idx}: {section_type} regenerated -->"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regeneration failed: {e}")


@app.post("/api/sites/{sid}/section/{idx}/variant")
async def api_section_variant(sid: str, idx: int, data: dict = {}):
    """
    Change section variant layout.
    Body: {"variant": "zigzag"} — switches section to alternate layout variant.
    """
    valid_variants = {
        "hero": ["split", "centered", "full-bleed"],
        "features": ["grid-3", "zigzag", "asymmetric-2col"],
        "about": ["standard", "right-image", "text-only"],
        "testimonials": ["grid", "carousel"],
        "cta": ["centered", "compact"],
        "team": ["grid", "carousel"],
        "footer": ["standard", "compact"],
    }

    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    from brand_registry import get_registry
    registry = get_registry()
    arch_config = registry.get_archetype_config(site.get("theme", "inxotive"))
    section_order = arch_config["section_order"]

    if idx < 0 or idx >= len(section_order):
        raise HTTPException(status_code=400, detail=f"Invalid section index {idx}")
    section_type = section_order[idx]

    valid_variants = {
        "hero": ["split", "centered", "full-bleed"],
        "features": ["grid-3", "zigzag", "asymmetric-2col"],
        "about": ["standard", "right-image", "text-only"],
        "testimonials": ["grid", "carousel"],
        "cta": ["centered", "compact"],
        "team": ["grid", "carousel"],
        "footer": ["standard", "compact"],
    }

    variant = data.get("variant", "")
    allowed = valid_variants.get(section_type, [])
    if not variant or (allowed and variant not in allowed):
        return {"error": f"Invalid variant '{variant}' for section '{section_type}'. Allowed: {allowed}",
                "section_type": section_type, "allowed_variants": allowed}

    # Store variant preference in site config
    try:
        site_config = site.get("config", {})
        if not site_config:
            site_config = {}
        if "section_variants" not in site_config:
            site_config["section_variants"] = {}
        site_config["section_variants"][str(idx)] = variant
        update_site_config(sid, {"section_variants": site_config["section_variants"]})
        return {"idx": idx, "section_type": section_type, "variant": variant, "applied": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set variant: {e}")


@app.post("/api/sites/{sid}/section/{idx}/adjust")
async def api_section_adjust(sid: str, idx: int, data: dict = {}):
    """
    Adjust section properties.
    Body: {"align": "left", "density": "compact", "hidden": false}
    """
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    from brand_registry import get_registry
    registry = get_registry()
    arch_config = registry.get_archetype_config(site.get("theme", "inxotive"))
    section_order = arch_config["section_order"]

    if idx < 0 or idx >= len(section_order):
        raise HTTPException(status_code=400, detail=f"Invalid section index {idx}")

    section_type = section_order[idx]
    adjustments = {}

    # Valid align values
    if "align" in data and data["align"] in ("left", "center", "right"):
        adjustments["align"] = data["align"]

    # Valid density
    if "density" in data and data["density"] in ("compact", "normal", "spacious"):
        adjustments["density"] = data["density"]

    # Hidden toggle
    if "hidden" in data and isinstance(data["hidden"], bool):
        adjustments["hidden"] = data["hidden"]

    if not adjustments:
        return {"error": "No valid adjustments provided", "allowed": {"align": ["left","center","right"], "density": ["compact","normal","spacious"], "hidden": "bool"}}

    # Store adjustments in site config
    try:
        site_config = site.get("config", {})
        if not site_config:
            site_config = {}
        if "section_adjustments" not in site_config:
            site_config["section_adjustments"] = {}
        existing = site_config["section_adjustments"].get(str(idx), {})
        existing.update(adjustments)
        site_config["section_adjustments"][str(idx)] = existing
        update_site_config(sid, {"section_adjustments": site_config["section_adjustments"]})
        return {"idx": idx, "section_type": section_type, "adjustments": adjustments, "applied": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to adjust section: {e}")



@app.post("/api/sites/{sid}/section/reorder")
async def api_section_reorder(sid: str, data: dict = {}):
    """Reorder sections. Body: {"order": ["hero", "features", "cta", ...]}"""
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    new_order = data.get("order", [])
    if not new_order:
        raise HTTPException(status_code=400, detail="Order array required")

    from brand_registry import get_registry
    registry = get_registry()
    arch_config = registry.get_archetype_config(site.get("theme", "inxotive"))
    valid_sections = arch_config["section_order"]

    # Validate all sections exist
    for sec in new_order:
        if sec not in valid_sections:
            raise HTTPException(status_code=400, detail=f"Invalid section: {sec}")

    # Store in site config
    site_config = site.get("config", {})
    if not site_config:
        site_config = {}
    site_config["section_order"] = new_order
    update_site_config(sid, {"section_order": new_order})

    return {"success": True, "order": new_order}


@app.get("/api/sites/{sid}/sections")
async def api_site_sections(sid: str):
    """Get section info for a site. Returns available types, current order, variants."""
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Use brand_registry as single source of truth
    from brand_registry import get_registry, get_section_variants
    registry = get_registry()
    theme = site.get("theme", "inxotive")
    arch_config = registry.get_archetype_config(theme)
    section_order = arch_config["section_order"]
    site_config = site.get("config", {}) or {}
    hidden = site_config.get("section_adjustments", {})

    sections = []
    for idx, sec_type in enumerate(section_order):
        sections.append({
            "index": idx,
            "type": sec_type,
            "name": sec_type.title(),
            "variants": get_section_variants(sec_type),
            "hidden": hidden.get(str(idx), {}).get("hidden", False),
        })

    return {
        "theme": theme,
        "order": section_order,
        "sections": sections,
        "archetype": arch_config["name"],
    }


@app.post("/api/sites/{sid}/critique")
async def api_site_critique(sid: str):
    """Run visual critique on a site's generated page."""
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    from critique import analyze_html, save_critique, format_critique_report
    from brand_registry import get_registry

    # Build the site first to get fresh HTML
    build_result = build_site(sid)
    if not build_result.get("success"):
        # Try to get existing dist HTML
        site_dir = Path(site.get("directory", ""))
        dist_index = site_dir / "dist" / "index.html"
        if not dist_index.exists():
            raise HTTPException(status_code=400, detail="Build your site first. No built HTML found.")

    # Read built HTML
    site_dir = Path(site.get("directory", ""))
    dist_index = site_dir / "dist" / "index.html"
    if not dist_index.exists():
        raise HTTPException(status_code=400, detail="No built HTML found. Build the site first.")

    html = dist_index.read_text()
    theme = site.get("theme", "inxotive")
    archetype_key = registry.get_archetype(theme)

    result = analyze_html(html, archetype_key)
    entry = save_critique(sid, result)
    report_md = format_critique_report(result)

    return {
        "critique": result,
        "report": report_md,
        "entry": entry,
    }



@app.get("/api/render/{template_id}")
async def api_render_html(template_id: str, brand: str = "INXOTIVE", industry: str = "general"):
    """Render an HTML template via web_engine. No build needed."""
    try:
        from builder import render_html_site, TEMPLATE_REGISTRY
        if template_id not in TEMPLATE_REGISTRY:
            raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
        tpl = TEMPLATE_REGISTRY[template_id]
        if tpl.get("type") != "html":
            return HTMLResponse(f'<div style="padding:40px;text-align:center;font-family:sans-serif"><p>This is a React template. Use /api/preview/{id} after build.</p></div>')
        html = render_html_site(template_id, brand_name=brand, industry=industry)
        return HTMLResponse(html)
    except ImportError:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse("Web engine not available. Install market-api first.", status_code=503)
    except Exception as e:
        return HTMLResponse(f'<div style="padding:40px;text-align:center;font-family:sans-serif"><p>Render error: {e}</p></div>')


@app.get("/api/render")
async def api_list_html_templates():
    """List all available HTML templates (web_engine)."""
    try:
        from builder import TEMPLATE_REGISTRY
        html_templates = []
        for key, tpl in TEMPLATE_REGISTRY.items():
            if tpl.get("type") == "html":
                html_templates.append({
                    "id": key,
                    "label": tpl["label"],
                    "description": tpl["description"],
                    "industry": tpl.get("industry", "general"),
                    "default_theme": tpl["default_theme"],
                    "themes": tpl.get("themes", []),
                })
        return {"templates": html_templates, "count": len(html_templates)}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/preview/{sid}/save")
async def api_preview_save(sid: str, data: dict):
    """Save config + build + return preview URL. Only saves non-empty fields to prevent overwrite."""
    # Filter out empty/None values from form data to prevent config overwrite
    filtered = {}
    for k, v in data.items():
        if v is None:
            continue
        if isinstance(v, dict):
            # For nested dicts (brand, contact, etc.) — filter empty values
            nested = {nk: nv for nk, nv in v.items() if nv is not None and nv != ""}
            if nested:
                filtered[k] = nested
        elif isinstance(v, list):
            if v:  # Only include non-empty lists
                filtered[k] = v
        elif isinstance(v, (str, int, float, bool)):
            if v != "" and v is not False:
                filtered[k] = v
    if not filtered:
        raise HTTPException(status_code=400, detail="No fields to save")

    save_result = update_site_config(sid, filtered)
    if save_result is None:
        raise HTTPException(status_code=404, detail="Site not found")
    build_result = build_site(sid)
    if not build_result.get("success"):
        raise HTTPException(status_code=400, detail="Build failed")
    return {"preview_url": "/api/preview/" + sid, "build_status": "ok"}



import sys as _sys
from fastapi.responses import HTMLResponse, PlainTextResponse

PREMIUM_BRANDS_CACHE = None

def _get_brands_list():
    global PREMIUM_BRANDS_CACHE
    if PREMIUM_BRANDS_CACHE is not None:
        return PREMIUM_BRANDS_CACHE
    try:
        from css_framework import ALL_BRANDS
        PREMIUM_BRANDS_CACHE = [
            {
                "slug": slug,
                "name": data.get("name", slug),
                "primary": data.get("primary", "#6366f1"),
                "secondary": data.get("secondary", "#8b5cf6"),
                "accent": data.get("accent", "#f59e0b"),
                "bg": data.get("bg", "#ffffff"),
            }
            for slug, data in ALL_BRANDS.items()
        ]
    except Exception:
        PREMIUM_BRANDS_CACHE = [
            {"slug": s, "name": s.capitalize(), "primary": "#6366f1", "secondary": "#8b5cf6", "accent": "#f59e0b"}
            for s in ["inxotive","tech","fnb","healthcare","luxury","apple","stripe","vercel","figma","notion","nike"]
        ]
    return PREMIUM_BRANDS_CACHE


@app.get("/api/premium/brands")
async def api_premium_brands():
    return {"brands": _get_brands_list()}


# ── EDITOR API ──
_editor_states = {}  # site_id → state dict
_editor_undo = {}  # site_id → UndoStack

def _get_editor_state(site_id: str) -> dict:
    """Get or initialize editor state for a site."""
    if site_id not in _editor_states:
        from css_framework import generate_archetype_page
        from content_models import SiteContent
        from copy_templates import get_copy
        # Build initial state from brand
        from css_framework import BRAND_INDUSTRY_MAP
        industry = BRAND_INDUSTRY_MAP.get(site_id, "business")
        copy = get_copy(industry)
        state = {
            "brand": site_id,
            "tagline": copy.get("hero", {}).get("eyebrow", ""),
            "hero": {
                "headline": copy.get("hero", {}).get("headline", site_id),
                "subtext": copy.get("hero", {}).get("subtext", ""),
                "eyebrow": copy.get("hero", {}).get("eyebrow", ""),
                "cta": copy.get("hero", {}).get("cta", "Mulai Sekarang"),
            },
            "features": {
                "heading": copy.get("features", {}).get("heading", ""),
                "subtext": copy.get("features", {}).get("subtext", ""),
                "items": [{"title": i.get("title",""), "desc": i.get("desc","")} for i in copy.get("features", {}).get("items", [])],
            },
            "sections": {},
        }
        _editor_states[site_id] = state
        from editor_actions import UndoStack
        _editor_undo[site_id] = UndoStack()
    return _editor_states[site_id]


@app.post("/api/editor/action")
async def api_editor_action(data: dict):
    """Apply single action to editor state."""
    site_id = data.get("site_id", "luxury")
    action = data.get("action", {})

    from editor_actions import validate_action, apply_action

    state = _get_editor_state(site_id)
    valid, error = validate_action(action, state)
    if not valid:
        return {"status": "error", "error": error}

    from editor_actions import UndoStack
    undo = _editor_undo.get(site_id)
    if undo:
        undo.push(state)

    new_state, error = apply_action(action, state)
    if error:
        return {"status": "error", "error": error}

    _editor_states[site_id] = new_state
    return {"status": "ok", "state": new_state, "undo": undo.to_dict() if undo else None}


@app.post("/api/editor/batch")
async def api_editor_batch(data: dict):
    """Apply batch of actions."""
    site_id = data.get("site_id", "luxury")
    actions = data.get("actions", [])

    from editor_actions import validate_action, apply_action
    state = _get_editor_state(site_id)

    from editor_actions import UndoStack
    undo = _editor_undo.get(site_id)
    if undo:
        undo.push(state)

    results = []
    for action in actions:
        valid, error = validate_action(action, state)
        if not valid:
            results.append({"action": action, "status": "error", "error": error})
            continue
        new_state, error = apply_action(action, state)
        if error:
            results.append({"action": action, "status": "error", "error": error})
        else:
            state = new_state
            results.append({"action": action, "status": "ok"})

    _editor_states[site_id] = state
    return {"status": "ok", "state": state, "results": results, "undo": undo.to_dict() if undo else None}


@app.get("/api/editor/state/{site_id}")
async def api_editor_state(site_id: str):
    """Get current editor state."""
    state = _get_editor_state(site_id)
    from editor_actions import UndoStack
    undo = _editor_undo.get(site_id)
    return {"status": "ok", "state": state, "undo": undo.to_dict() if undo else None}


@app.post("/api/editor/undo")
async def api_editor_undo(data: dict):
    """Undo last action."""
    site_id = data.get("site_id", "luxury")
    undo = _editor_undo.get(site_id)
    if undo and undo.can_undo:
        state = undo.undo()
        _editor_states[site_id] = state
        return {"status": "ok", "state": state, "undo": undo.to_dict()}
    return {"status": "error", "error": "Tidak ada yang bisa di-undo"}


@app.post("/api/editor/redo")
async def api_editor_redo(data: dict):
    """Redo undone action."""
    site_id = data.get("site_id", "luxury")
    undo = _editor_undo.get(site_id)
    if undo and undo.can_redo:
        state = undo.redo()
        _editor_states[site_id] = state
        return {"status": "ok", "state": state, "undo": undo.to_dict()}
    return {"status": "error", "error": "Tidak ada yang bisa di-redo"}


@app.get("/api/editor/preview/{site_id}")
async def api_editor_preview(site_id: str):
    """Generate preview HTML from current editor state."""
    from css_framework import generate_archetype_page
    html = generate_archetype_page(site_id)
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)


@app.post("/api/editor/chat")
async def api_editor_chat(data: dict):
    """Receive chat instruction, run through Ollama, return actions."""
    site_id = data.get("site_id", "luxury")
    instruction = data.get("instruction", "")

    if not instruction.strip():
        return {"status": "error", "error": "Instruksi kosong"}

    from editor_chat import chat_to_actions
    state = _get_editor_state(site_id)
    actions, raw = await chat_to_actions(instruction, state)

    if not actions:
        return {"status": "error", "error": "Tidak bisa memproses instruksi", "raw": raw}

    return {"status": "ok", "actions": actions, "raw": raw}


@app.get("/api/premium/html/{slug}")
async def api_premium_html(slug: str, template: str = "landing", download: bool = False):
    try:
        from css_framework import generate_archetype_page, generate_premium_page
        # Try archetype-aware generator first
        try:
            html = generate_archetype_page(slug)
        except Exception:
            html = generate_premium_page(slug)
        headers = {"X-Content-Type-Options": "nosniff"}
        if download:
            headers["Content-Disposition"] = f'attachment; filename="premium-{slug}.html"'
        return HTMLResponse(content=html, headers=headers)
    except ImportError:
        return HTMLResponse(
            content=f"<html><body style='padding:40px;font-family:sans-serif'><h2>Premium Engine Not Available</h2></body></html>",
            status_code=503,
        )
    except Exception as e:
        return HTMLResponse(
            content=f"<html><body style='padding:40px;font-family:sans-serif'><h2>Error</h2><p>{e}</p></body></html>",
            status_code=500,
        )


@app.get("/api/premium/css/{slug}")
async def api_premium_css(slug: str):
    try:
        from css_framework import generate_framework
        css = generate_framework(slug)
        return PlainTextResponse(
            content=css,
            media_type="text/css",
            headers={"Content-Disposition": f'attachment; filename="framework-{slug}.css"'},
        )
    except Exception as e:
        return PlainTextResponse(content=f"/* Error: {e} */", status_code=500, media_type="text/css")


@app.post("/api/premium/deploy/{slug}")
async def api_premium_deploy(slug: str, data: dict = {}):
    """
    Generate premium HTML for brand slug and deploy to Vercel.
    POST /api/premium/deploy/inxotive
    Optional body: {"project_name": "my-project"}
    """
    import tempfile, subprocess as _sp

    token = os.environ.get("VERCEL_TOKEN", "")
    if not token:
        raise HTTPException(status_code=503, detail="VERCEL_TOKEN not configured")

    # 1. Generate premium HTML with archetype
    try:
        from css_framework import generate_archetype_page, generate_premium_page
        try:
            html = generate_archetype_page(slug)
        except Exception:
            html = generate_premium_page(slug)
    except ImportError:
        raise HTTPException(status_code=503, detail="Premium engine not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTML generation failed: {e}")

    # 2. Write to /tmp/premium-deploy-<slug>/
    deploy_dir = Path(f"/tmp/premium-deploy-{slug}")
    deploy_dir.mkdir(parents=True, exist_ok=True)

    (deploy_dir / "index.html").write_text(html, encoding="utf-8")

    vercel_json = {
        "version": 2,
        "name": data.get("project_name", f"inxotive-premium-{slug}"),
        "builds": [{"src": "index.html", "use": "@vercel/static"}],
        "routes": [{"src": "/(.*)", "dest": "/index.html"}],
    }
    (deploy_dir / "vercel.json").write_text(json.dumps(vercel_json, indent=2))

    # 3. Deploy via npx vercel
    try:
        result = _sp.run(
            ["npx", "vercel", "--token", token, "--yes", "--prod"],
            cwd=str(deploy_dir),
            capture_output=True,
            text=True,
            timeout=180,
            env={**os.environ, "VERCEL_TOKEN": token},
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # Extract URL — last non-empty line of stdout that starts with https
        url = ""
        for line in reversed(stdout.splitlines()):
            line = line.strip()
            if line.startswith("https://"):
                url = line
                break

        if result.returncode == 0 and url:
            return {
                "success": True,
                "url": url,
                "slug": slug,
                "deploy_dir": str(deploy_dir),
                "stdout": stdout[-800:],
            }
        else:
            return {
                "success": False,
                "slug": slug,
                "returncode": result.returncode,
                "stdout": stdout[-800:],
                "stderr": stderr[-800:],
            }
    except _sp.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Deploy timed out (180s)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deploy error: {e}")


# ── Multi-Page ──

@app.post("/api/sites/{sid}/multi-page")
async def api_multi_page_generate(sid: str, data: dict = {}):
    """Generate multi-page site for existing site."""
    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    pages = data.get("pages", ["home", "about", "services", "contact"])
    result = generate_multi_page_site(
        sid,
        template_id=site.get("template"),
        brand_name=site.get("name", "INXOTIVE"),
        industry=site.get("industry", "general"),
        brand_color=site.get("theme_color", "4F46E5"),
        pages=pages,
        content_overrides=data.get("content", {}),
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # Save to disk
    saved = save_multi_page_site(sid, result.get("pages", {}))
    return {"generation": result, "saved": saved}


@app.get("/api/sites/{sid}/pages")
async def api_site_pages(sid: str):
    """List pages for a multi-page site."""
    data = load_data()
    s = data["sites"].get(sid)
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"multi_page": s.get("multi_page", False), "pages": s.get("pages", ["home"])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)


# ── Pipeline ──

@app.get("/api/pipeline")
async def api_pipeline():
    """Get pipeline data from pipeline_status.json"""
    path = Path.home() / "inxotive-office" / "pipeline_status.json"
    if not path.exists():
        return {"leads": {}}
    data = json.loads(path.read_text())
    leads = {}
    for key, val in data.items():
        leads[key] = {
            "id": key,
            "name": val.get("name", key),
            "company": val.get("company", ""),
            "industry": val.get("industry", ""),
            "stage": val.get("stage", "intake"),
            "tags": val.get("tags", []),
            "contact": val.get("contact", {}),
            "logs": val.get("logs", []),
            "created": val.get("created", ""),
            "updated": val.get("updated", ""),
        }
    return {"leads": leads}

# ── Part E: Feedback Loop ──

@app.post("/api/feedback")
async def api_record_feedback(data: dict):
    """Record client feedback about a delivery."""
    from feedback_loop import record_feedback, distill_feedback
    if not data.get("client") or not data.get("site_id"):
        raise HTTPException(status_code=400, detail="client and site_id are required")
    entry = record_feedback(
        client_name=data.get("client", ""),
        site_id=data.get("site_id", ""),
        archetype=data.get("archetype", ""),
        feedback_type=data.get("type", "revision"),
        section_type=data.get("section", ""),
        variant=data.get("variant", ""),
        notes=data.get("notes", ""),
        rating=data.get("rating", 3),
    )
    return {"entry": entry, "message": "Feedback recorded"}


@app.get("/api/feedback")
async def api_get_feedback():
    """Get all feedback with distilled preferences."""
    from feedback_loop import load_feedback
    data = load_feedback()
    return data


@app.post("/api/feedback/distill")
async def api_distill_feedback():
    """Distill all feedback into archetype weights and variant preferences."""
    from feedback_loop import distill_feedback
    result = distill_feedback()
    return result


@app.get("/api/feedback/report")
async def api_feedback_report():
    """Get formatted feedback loop report."""
    from feedback_loop import format_feedback_report
    return {"report": format_feedback_report()}


@app.get("/api/pipeline/lead/{lead_id}")
async def api_pipeline_lead(lead_id: str):
    """Get detail for one pipeline lead."""
    path = Path.home() / "inxotive-office" / "pipeline_status.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Pipeline not found")
    data = json.loads(path.read_text())
    val = data.get(lead_id)
    if not val:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        "lead": {
            "id": lead_id,
            "name": val.get("name", lead_id),
            "company": val.get("company", ""),
            "industry": val.get("industry", ""),
            "stage": val.get("stage", "intake"),
            "tags": val.get("tags", []),
            "contact": val.get("contact", {}),
            "logs": val.get("logs", []),
            "created": val.get("created", ""),
            "updated": val.get("updated", ""),
        }
    }
