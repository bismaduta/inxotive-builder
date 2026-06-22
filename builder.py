"""
INXOTIVE Web Agency Builder — Core Engine
==========================================
Data layer, template ops, Vercel deploy, site management.

Storage: ~/.agency_data.json (JSON file, flat collections)
"""

import json, os, shutil, uuid, subprocess, time, re
from pathlib import Path
from datetime import datetime

# ── Paths ──
HOME = Path.home()
DATA_FILE = HOME / ".agency_data.json"
TEMPLATES_DIR = HOME / "templates"
CLIENTS_DIR = HOME / "clients"
ASSETS_DIR = HOME / "client-assets"

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
VERCEL_TEAM = "bismadutas-projects"

# ── Template Registry ──
TEMPLATE_REGISTRY = {
    # ── React Templates (Vite + site.config.js) ──
    "klinik": {
        "label": "Klinik",
        "dir": "klinik-template",
        "description": "Klinik, puskesmas, rumah sakit umum",
        "default_theme": "clinical-trust",
        "themes": ["clinical-trust", "warm-family", "precision-lab", "heritage-care", "fresh-apotek", "premium-resto"],
        "type": "react",
    },
    "apotek": {
        "label": "Apotek",
        "dir": "apotek-template",
        "description": "Apotek, toko obat, health store",
        "default_theme": "fresh-apotek",
        "themes": ["clinical-trust", "warm-family", "precision-lab", "heritage-care", "fresh-apotek", "premium-resto"],
        "type": "react",
    },
    "lab": {
        "label": "Laboratorium",
        "dir": "lab-template",
        "description": "Lab diagnostik, lab kesehatan",
        "default_theme": "precision-lab",
        "themes": ["clinical-trust", "warm-family", "precision-lab", "heritage-care", "fresh-apotek", "premium-resto"],
        "type": "react",
    },
    "landing": {
        "label": "Landing Page",
        "dir": "landing-template",
        "description": "Landing page bisnis umum, restoran, jasa",
        "default_theme": "warm-family",
        "themes": ["clinical-trust", "warm-family", "precision-lab", "heritage-care", "fresh-apotek", "premium-resto"],
        "type": "react",
    },
    # ── HTML Templates (web_engine rendered, no build needed) ──
    "landing-healthcare": {
        "label": "Klinik Sehat",
        "dir": None,
        "description": "Landing page modern untuk klinik/dokter",
        "default_theme": "healthcare",
        "themes": ["healthcare", "minimal", "corporate"],
        "type": "html",
        "industry": "healthcare",
    },
    "landing-fnb": {
        "label": "Warung Modern",
        "dir": None,
        "description": "Landing page restoran dengan gallery makanan",
        "default_theme": "fnb",
        "themes": ["fnb", "luxury", "creative", "minimal"],
        "type": "html",
        "industry": "fnb",
    },
    "landing-tech": {
        "label": "Startup Teknologi",
        "dir": None,
        "description": "Landing page SaaS dengan pricing dan showcase",
        "default_theme": "tech",
        "themes": ["tech", "inxotive", "corporate", "minimal"],
        "type": "html",
        "industry": "tech",
    },
    "landing-luxury": {
        "label": "Luxury Brand",
        "dir": None,
        "description": "Landing premium dengan design elegan",
        "default_theme": "luxury",
        "themes": ["luxury", "minimal", "creative", "nature"],
        "type": "html",
        "industry": "luxury",
    },
    "landing-education": {
        "label": "Edukasi Cerdas",
        "dir": None,
        "description": "Landing page kursus dan pendidikan",
        "default_theme": "tech",
        "themes": ["tech", "creative", "minimal", "nature"],
        "type": "html",
        "industry": "education",
    },
    "landing-fitness": {
        "label": "Fitness Pro",
        "dir": None,
        "description": "Landing page gym/fitness bold design",
        "default_theme": "creative",
        "themes": ["creative", "tech", "corporate", "minimal"],
        "type": "html",
        "industry": "general",
    },
    "landing-restaurant": {
        "label": "Restaurant Elite",
        "dir": None,
        "description": "Landing premium fine dining",
        "default_theme": "fnb",
        "themes": ["fnb", "luxury", "creative", "minimal"],
        "type": "html",
        "industry": "fnb",
    },
    "company-profile": {
        "label": "Company Profile",
        "dir": None,
        "description": "Profil perusahaan lengkap 10 sections",
        "default_theme": "corporate",
        "themes": ["corporate", "inxotive", "minimal", "tech"],
        "type": "html",
        "industry": "general",
    },
    "company-profile-healthcare": {
        "label": "Profil Klinik",
        "dir": None,
        "description": "Profil klinik dengan team dan fasilitas",
        "default_theme": "healthcare",
        "themes": ["healthcare", "corporate", "minimal", "nature"],
        "type": "html",
        "industry": "healthcare",
    },
    "web-app-saas": {
        "label": "SaaS Dashboard",
        "dir": None,
        "description": "Landing page SaaS premium dengan pricing",
        "default_theme": "tech",
        "themes": ["tech", "inxotive", "corporate", "minimal"],
        "type": "html",
        "industry": "tech",
    },
    "ecommerce-fashion": {
        "label": "Fashion Store",
        "dir": None,
        "description": "Toko fashion online dengan gallery",
        "default_theme": "creative",
        "themes": ["creative", "luxury", "minimal", "tech"],
        "type": "html",
        "industry": "fashion",
    },
    "portfolio-gallery": {
        "label": "Portfolio Gallery",
        "dir": None,
        "description": "Portfolio/galeri karya",
        "default_theme": "minimal",
        "themes": ["minimal", "creative", "inxotive", "tech"],
        "type": "html",
        "industry": "general",
    },
    "booking-scheduling": {
        "label": "Booking Scheduling",
        "dir": None,
        "description": "Halaman booking dengan form dan paket",
        "default_theme": "inxotive",
        "themes": ["inxotive", "tech", "creative", "minimal"],
        "type": "html",
        "industry": "general",
    },
    "landing-wellness": {
        "label": "Wellness Spa",
        "dir": None,
        "description": "Landing spa/wellness dengan pricing",
        "default_theme": "nature",
        "themes": ["nature", "luxury", "minimal", "creative"],
        "type": "html",
        "industry": "general",
    },
    "event-landing": {
        "label": "Event Conference",
        "dir": None,
        "description": "Landing page event dengan timeline",
        "default_theme": "tech",
        "themes": ["tech", "creative", "corporate", "inxotive"],
        "type": "html",
        "industry": "general",
    },
    "longform-sales": {
        "label": "Longform Sales",
        "dir": None,
        "description": "Longform sales page premium",
        "default_theme": "inxotive",
        "themes": ["inxotive", "luxury", "corporate", "minimal"],
        "type": "html",
        "industry": "general",
    },
    "blog-default": {
        "label": "Blog Standar",
        "dir": None,
        "description": "Blog dengan timeline dan newsletter",
        "default_theme": "minimal",
        "themes": ["minimal", "tech", "creative", "nature"],
        "type": "html",
        "industry": "general",
    },
    "ecommerce-store": {
        "label": "Toko Online",
        "dir": None,
        "description": "Toko online dengan cart dan checkout",
        "default_theme": "tech",
        "themes": ["tech", "creative", "inxotive", "corporate"],
        "type": "html",
        "industry": "fashion",
    },
    "booking-packages": {
        "label": "Booking Paket",
        "dir": None,
        "description": "Booking paket wisata",
        "default_theme": "nature",
        "themes": ["nature", "luxury", "creative", "tech"],
        "type": "html",
        "industry": "general",
    },
    "ecommerce-checkout": {
        "label": "Checkout Premium",
        "dir": None,
        "description": "Trustworthy minimal checkout dengan comparison table",
        "default_theme": "inxotive",
        "themes": ["inxotive", "creative", "minimal", "tech"],
        "type": "html",
        "industry": "general",
    },
    "dashboard-agency": {
        "label": "Dashboard Agency",
        "dir": None,
        "description": "Dashboard admin dengan sidebar, stat cards, data table, dan activity feed",
        "default_theme": "inxotive",
        "themes": ["inxotive", "creative", "minimal", "tech"],
        "type": "html",
        "industry": "general",
    },
}

# ── Visual Theme Data for Theme Picker ──
BRAND_VISUALS = {
    "inxotive": {"name": "INXOTIVE", "primary": "#4F46E5", "font": "Plus Jakarta Sans", "vibe": "Digital Agency", "industry": ["tech", "general"]},
    "healthcare": {"name": "Healthcare", "primary": "#059669", "font": "Inter", "vibe": "Clean & Trustworthy", "industry": ["healthcare"]},
    "fnb": {"name": "FnB", "primary": "#EA580C", "font": "Space Grotesk", "vibe": "Warm & Appetizing", "industry": ["fnb", "restaurant"]},
    "luxury": {"name": "Luxury", "primary": "#B8860B", "font": "Playfair Display", "vibe": "Exclusive & Refined", "industry": ["luxury", "fashion"]},
    "tech": {"name": "Tech", "primary": "#2563EB", "font": "Inter", "vibe": "Innovative & Fast", "industry": ["tech", "saas"]},
    "creative": {"name": "Creative", "primary": "#FF6B6B", "font": "DM Sans", "vibe": "Vibrant & Playful", "industry": ["creative", "fashion"]},
    "minimal": {"name": "Minimal", "primary": "#1A1A1A", "font": "Inter", "vibe": "Pure & Quiet", "industry": ["general", "portfolio"]},
    "corporate": {"name": "Corporate", "primary": "#1B3A5C", "font": "Work Sans", "vibe": "Professional B2B", "industry": ["corporate", "tech"]},
    "nature": {"name": "Nature", "primary": "#4A7C59", "font": "DM Sans", "vibe": "Calm & Organic", "industry": ["wellness", "nature", "general"]},
    "education": {"name": "Education", "primary": "#6366F1", "font": "Plus Jakarta Sans", "vibe": "Friendly Approachable", "industry": ["education"]},
    "fashion": {"name": "Fashion", "primary": "#EC4899", "font": "Space Grotesk", "vibe": "Bold & Stylish", "industry": ["fashion"]},
    "fitness": {"name": "Fitness", "primary": "#DC2626", "font": "Inter", "vibe": "Energetic & Powerful", "industry": ["fitness", "sports"]},
}


def list_theme_visuals(industry: str = "") -> list:
    """Return all theme visuals, optionally filtered by industry."""
    visuals = []
    for key, v in BRAND_VISUALS.items():
        if industry and industry not in v["industry"]:
            continue
        visuals.append({
            "key": key,
            "name": v["name"],
            "primary_color": v["primary"],
            "font": v["font"],
            "vibe": v["vibe"],
            "industry": v["industry"],
        })
    return sorted(visuals, key=lambda x: x["name"])


# ════════════════════════════════════════════════════════════════
# DATA LAYER
# ════════════════════════════════════════════════════════════════

def _default_data() -> dict:
    return {
        "clients": {},
        "sites": {},
        "assets": {},
        "deployments": {},
        "domains": {},
        "portal_tokens": {},
        "_meta": {"version": 2, "created": datetime.now().isoformat()},
    }


def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            raw = json.loads(DATA_FILE.read_text())
            # Migrate if needed
            if "_meta" not in raw:
                raw["_meta"] = {"version": 1, "migrated": datetime.now().isoformat()}
            # Ensure all collections exist
            for k in _default_data():
                if k not in raw:
                    raw[k] = {} if k != "_meta" else _default_data()["_meta"]
            return raw
        except (json.JSONDecodeError, Exception):
            pass
    data = _default_data()
    save_data(data)
    return data


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def _gen_id() -> str:
    return uuid.uuid4().hex[:12]


def _now() -> str:
    return datetime.now().isoformat()


# ════════════════════════════════════════════════════════════════
# CLIENTS
# ════════════════════════════════════════════════════════════════

def list_clients():
    data = load_data()
    return sorted(
        [
            {
                "id": cid,
                "name": c.get("name", ""),
                "company": c.get("company", ""),
                "industry": c.get("industry", ""),
                "status": c.get("status", "prospect"),
                "tags": c.get("tags", []),
                "created": c.get("created", ""),
                "updated": c.get("updated", ""),
                "site_count": sum(1 for s in data["sites"].values() if s.get("client_id") == cid),
            }
            for cid, c in data["clients"].items()
        ],
        key=lambda c: c.get("created", ""),
        reverse=True,
    )


def get_client(client_id: str):
    data = load_data()
    c = data["clients"].get(client_id)
    if not c:
        return None
    sites = []
    for sid, s in data["sites"].items():
        if s.get("client_id") == client_id:
            sites.append({**s, "id": sid})
    deployments = []
    for d in data["deployments"].values():
        for s in sites:
            if d.get("site_id") == s["id"]:
                deployments.append(d)
    return {**c, "id": client_id, "sites": sites, "deployments": deployments[:10]}


def create_client(data_in: dict) -> dict:
    data = load_data()
    cid = _gen_id()
    client = {
        "name": data_in.get("name", ""),
        "company": data_in.get("company", ""),
        "industry": data_in.get("industry", ""),
        "contact": {
            "wa": data_in.get("wa", ""),
            "email": data_in.get("email", ""),
            "phone": data_in.get("phone", ""),
        },
        "source": data_in.get("source", "direct"),
        "status": data_in.get("status", "prospect"),
        "notes": data_in.get("notes", ""),
        "tags": data_in.get("tags", []),
        "created": _now(),
        "updated": _now(),
    }
    data["clients"][cid] = client
    save_data(data)
    return {"id": cid, **client}


def update_client(client_id: str, data_in: dict) -> dict:
    data = load_data()
    c = data["clients"].get(client_id)
    if not c:
        return None
    for field in ["name", "company", "industry", "source", "status", "notes", "tags"]:
        if field in data_in:
            c[field] = data_in[field]
    if any(k in data_in for k in ["wa", "email", "phone"]):
        c["contact"] = {
            "wa": data_in.get("wa", c["contact"].get("wa", "")),
            "email": data_in.get("email", c["contact"].get("email", "")),
            "phone": data_in.get("phone", c["contact"].get("phone", "")),
        }
    c["updated"] = _now()
    data["clients"][client_id] = c
    save_data(data)
    return {"id": client_id, **c}


def delete_client(client_id: str) -> bool:
    data = load_data()
    if client_id not in data["clients"]:
        return False
    # Also remove related sites, assets, etc
    for sid in list(data["sites"].keys()):
        if data["sites"][sid].get("client_id") == client_id:
            del data["sites"][sid]
    for aid in list(data["assets"].keys()):
        if data["assets"][aid].get("client_id") == client_id:
            del data["assets"][aid]
    del data["clients"][client_id]
    save_data(data)
    return True


# ════════════════════════════════════════════════════════════════
# TEMPLATES
# ════════════════════════════════════════════════════════════════

def list_templates():
    result = []
    for key, tpl in TEMPLATE_REGISTRY.items():
        tpl_type = tpl.get("type", "react")
        if tpl_type == "html":
            result.append({
                "id": key,
                "label": tpl["label"],
                "description": tpl["description"],
                "default_theme": tpl["default_theme"],
                "themes": tpl["themes"],
                "type": "html",
                "industry": tpl.get("industry", "general"),
                "exists_on_disk": True,
            })
        else:
            tpl_dir = TEMPLATES_DIR / tpl["dir"]
            exists = tpl_dir.exists()
            result.append({
                "id": key,
                "label": tpl["label"],
                "description": tpl["description"],
                "default_theme": tpl["default_theme"],
                "themes": tpl["themes"],
                "type": "react",
                "exists_on_disk": exists,
            })
    return result


def render_html_site(template_id: str, brand_name: str = "INXOTIVE",
                     industry: str = "general", brand_color: str = "4F46E5",
                     content_overrides: dict = None) -> str:
    """Render an HTML template via web_engine. No build step needed.
    Returns full HTML page ready to serve directly."""
    try:
        import sys as _sys
        _sys.path.insert(0, str(HOME / "market-api"))
        import asyncio
        from web_engine.templates import render_template

        async def _render():
            return await render_template(template_id, brand_name=brand_name,
                                          content_overrides=content_overrides)

        # Handle both sync and async call contexts
        try:
            loop = asyncio.get_running_loop()
            # Already in async context — schedule and wait
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, _render())
                return future.result(timeout=30)
        except RuntimeError:
            # No running loop — use asyncio.run
            pass

        return asyncio.run(_render())
    except ImportError as e:
        return f"<!-- web_engine not available: {e} -->"
    except Exception as e:
        return f"<!-- Failed to render HTML template: {e} -->"


def generate_multi_page_site(site_id: str, template_id: str = None,
                              brand_name: str = "INXOTIVE", industry: str = "general",
                              brand_color: str = "4F46E5",
                              pages: list = None, content_overrides: dict = None) -> dict:
    """Generate multi-page HTML site using web_engine multi_page.py.

    Returns dict with {pages: {slug: html, ...}, page_list: [...], ...}
    """
    try:
        import sys as _sys
        _sys.path.insert(0, str(HOME / "market-api"))
        import asyncio
        from web_engine.multi_page import render_multi_page_site, PAGE_TYPES

        if not pages:
            pages = list(PAGE_TYPES.keys())

        # Convert page names (strings) to page config dicts
        page_configs = []
        for p in pages:
            if isinstance(p, str):
                pt = PAGE_TYPES.get(p, {}).copy()
                page_configs.append({"slug": p, **pt})
            else:
                page_configs.append(p)

        async def _render():
            return await render_multi_page_site(
                template_id=template_id or "landing",
                pages=page_configs,
                brand_name=brand_name,
                industry=industry,
                brand_color=brand_color,
            )

        # Handle both sync and async call contexts
        try:
            asyncio.get_running_loop()
            # Already in async context — run in separate thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, _render())
                result = future.result(timeout=30)
                return {"pages": result, "count": len(result)}
        except RuntimeError:
            # No running loop — use asyncio.run directly
            pass

        result = asyncio.run(_render())
        return {"pages": result, "count": len(result)}
    except ImportError as e:
        return {"error": f"web_engine multi_page not available: {e}", "pages": {}}
    except Exception as e:
        return {"error": f"Failed to generate multi-page: {e}", "pages": {}}


def save_multi_page_site(site_id: str, pages: dict) -> dict:
    """Save generated multi-page HTML files to site directory."""
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return {"error": "Site not found"}

    site_dir = Path(s["directory"])
    if not site_dir.exists():
        return {"error": "Site directory not found"}

    output_dir = site_dir / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for slug, html in pages.items():
        # slug is already a path like "index.html" or "tentang/index.html"
        if slug.endswith(".html"):
            filename = slug
        else:
            filename = "index.html" if slug == "home" else f"{slug}.html"
        filepath = output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(html)
        saved.append({"slug": slug, "file": str(filepath)})

    s["multi_page"] = True
    s["pages"] = list(pages.keys())
    s["updated"] = _now()
    data["sites"][site_id] = s
    save_data(data)

    return {"success": True, "pages": saved, "count": len(saved)}


def get_template(template_id: str) -> dict:
    tpl = TEMPLATE_REGISTRY.get(template_id)
    if not tpl:
        return None
    # HTML templates don't have a dir on disk - rendered by web_engine
    if tpl.get("type") == "html":
        return {"id": template_id, "type": "html", **tpl}
    tpl_dir = TEMPLATES_DIR / tpl["dir"]
    if not tpl_dir.exists():
        return {"id": template_id, "error": "template not found on disk", **tpl}
    # Read the default site.config.js to get the schema
    config_path = tpl_dir / "site.config.js"
    if not config_path.exists():
        config_path = tpl_dir / "src" / "config" / "site.config.js"
    config_sample = ""
    if config_path.exists():
        config_sample = config_path.read_text()[:2000]
    return {
        "id": template_id,
        "label": tpl["label"],
        "description": tpl["description"],
        "default_theme": tpl["default_theme"],
        "themes": tpl["themes"],
        "config_sample": config_sample,
    }


# ════════════════════════════════════════════════════════════════
# SITES
# ════════════════════════════════════════════════════════════════

def list_sites(status_filter: str = None):
    data = load_data()
    sites = []
    for sid, s in data["sites"].items():
        if status_filter and s.get("status") != status_filter:
            continue
        # Get latest deployment status
        deploys = [d for d in data["deployments"].values() if d.get("site_id") == sid]
        latest_deploy = max(deploys, key=lambda d: d.get("created", "")) if deploys else None
        sites.append({
            "id": sid,
            "name": s.get("name", ""),
            "template": s.get("template", ""),
            "theme": s.get("theme", ""),
            "client_id": s.get("client_id", ""),
            "client_name": s.get("client_name", ""),
            "domain": s.get("domain", ""),
            "status": s.get("status", "draft"),
            "vercel_project": s.get("vercel_project", ""),
            "last_deploy": latest_deploy.get("url", "") if latest_deploy else "",
            "last_deploy_status": latest_deploy.get("status", "") if latest_deploy else "",
            "created": s.get("created", ""),
            "updated": s.get("updated", ""),
        })
    return sorted(sites, key=lambda s: s.get("updated", ""), reverse=True)


def get_site(site_id: str) -> dict:
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return None
    # Attach deployments
    deployments = sorted(
        [d for d in data["deployments"].values() if d.get("site_id") == site_id],
        key=lambda d: d.get("created", ""),
        reverse=True,
    )
    # Attach assets
    assets = [a for a in data["assets"].values() if a.get("site_id") == site_id]
    # Read current config from disk (if available)
    config = None
    config_path_str = s.get("config_path", "")
    if config_path_str:
        cp = Path(config_path_str)
        if not cp.exists():
            cp = Path(s.get("directory", "")) / "site.config.js"
        if not cp.exists():
            cp = Path(s.get("directory", "")) / "src" / "config" / "site.config.js"
        if cp.exists():
            import re
            raw = cp.read_text()
            m = re.search(r"export\s+const\s+siteConfig\s*=\s*(\{.*\})\s*;?\s*$", raw, re.DOTALL)
            if m:
                try:
                    config = json.loads(m.group(1))
                except:
                    pass
    return {**s, "id": site_id, "config": config, "deployments": deployments, "assets": assets}


def create_site(data_in: dict) -> dict:
    """Create site from template. For React: copies template dir. For HTML: lightweight record."""
    data = load_data()
    template_id = data_in.get("template", "landing")
    tpl = TEMPLATE_REGISTRY.get(template_id)
    if not tpl:
        return {"error": f"Template '{template_id}' not found", "valid_templates": list(TEMPLATE_REGISTRY.keys())}

    sid = _gen_id()
    site_name = data_in.get("name", f"Site-{sid[:6]}")
    safe_name = site_name.lower().replace(" ", "-").replace("_", "-")[:30]
    site_dir = CLIENTS_DIR / f"site-{safe_name}"

    # Parse config
    config = data_in.get("config", {})
    theme = config.get("theme", data_in.get("theme", tpl["default_theme"]))
    brand_name = config.get("brand", {}).get("name", data_in.get("name", "Nama Bisnis"))

    is_html = tpl.get("type") == "html"

    if not is_html:
        # REACT TEMPLATE: copy dir from disk
        tpl_dir = TEMPLATES_DIR / tpl["dir"]
        if not tpl_dir.exists():
            return {"error": f"Template directory not found on disk: {tpl_dir}"}
        if site_dir.exists():
            shutil.rmtree(site_dir)
        shutil.copytree(tpl_dir, site_dir, ignore=shutil.ignore_patterns("node_modules", "dist", ".git"))

    # Build full site config
    site_config = {
        "theme": theme,
        "brand": {
            "name": brand_name,
            "tagline": config.get("brand", {}).get("tagline", ""),
            "logo": None,
            "badge": config.get("brand", {}).get("badge", f"✦ {brand_name.upper()}"),
            "colors": config.get("brand", {}).get("colors", {}),
        },
        "contact": {
            "whatsapp": config.get("contact", {}).get("whatsapp", ""),
            "phone": config.get("contact", {}).get("phone", ""),
            "email": config.get("contact", {}).get("email", ""),
            "address": config.get("contact", {}).get("address", ""),
            "mapsEmbedUrl": config.get("contact", {}).get("mapsEmbedUrl", ""),
        },
        "hours": config.get("hours", [
            {"day": "Senin – Jumat", "time": "09.00 – 21.00"},
            {"day": "Sabtu", "time": "09.00 – 18.00"},
            {"day": "Minggu", "time": "10.00 – 15.00"},
        ]),
        "stats": config.get("stats", [
            {"value": "3+", "label": "Tahun melayani"},
            {"value": "500+", "label": "Pelanggan puas"},
            {"value": "⭐4.9", "label": "Rating Google"},
        ]),
        "services": config.get("services", []),
        "about": {
            "title": config.get("about", {}).get("title", f"Tentang {brand_name}"),
            "desc": config.get("about", {}).get("desc", ""),
            "highlights": config.get("about", {}).get("highlights", []),
        },
        "features": {
            "booking": config.get("features", {}).get("booking", False),
            "aiChat": config.get("features", {}).get("aiChat", False),
            "search": config.get("features", {}).get("search", False),
            "cms": config.get("features", {}).get("cms", False),
        },
        "testimonials": config.get("testimonials", []),
        "team": config.get("team", []),
        "social": config.get("social", {}),
        "seo": {
            "title": config.get("seo", {}).get("title", f"{brand_name} — INXOTIVE"),
            "description": config.get("seo", {}).get("description", ""),
            "ogImage": "/og.png",
        },
    }

    # ── Determine config path & write ──
    if is_html:
        # HTML templates: write JSON config to a data dir
        site_dir.mkdir(parents=True, exist_ok=True)
        config_path = site_dir / "site-config.json"
        config_path.write_text(json.dumps(site_config, indent=2))
        # Write placeholder index
        (site_dir / "index.html").write_text(f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<title>{site_name} — INXOTIVE</title></head><body>
<!-- INXOTIVE HTML Template: {template_id} — rendered at preview/build time -->
<h1 style="display:none">{site_name}</h1>
</body></html>""")
    else:
        # REACT TEMPLATE: write site.config.js
        config_path = site_dir / "site.config.js"
        if not config_path.exists():
            config_path = site_dir / "src" / "config" / "site.config.js"
        config_path.write_text(f"export const siteConfig = {json.dumps(site_config, indent=2, ensure_ascii=False)};\n")

        # Fix ghost branding
        index_path = site_dir / "index.html"
        if index_path.exists():
            index_html = index_path.read_text()
            index_html = re.sub(r'<title>.*?</title>', f'<title>{site_name} — INXOTIVE</title>', index_html)
            index_html = index_html.replace('lang="en"', 'lang="id"')
            index_path.write_text(index_html)

        pkg_path = site_dir / "package.json"
        if pkg_path.exists():
            try:
                pkg = json.loads(pkg_path.read_text())
                pkg["name"] = safe_name.replace("-", "")
                pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
            except (json.JSONDecodeError, Exception):
                pass

    # ── Record site ──
    client_id = data_in.get("client_id", "")
    client_name = ""
    if client_id and client_id in data["clients"]:
        client_name = data["clients"][client_id].get("name", "")

    site_record = {
        "name": site_name,
        "template": template_id,
        "theme": theme,
        "client_id": client_id,
        "client_name": client_name,
        "domain": data_in.get("domain", ""),
        "directory": str(site_dir),
        "config_path": str(config_path),
        "status": "draft",
        "vercel_project": "",
        "vercel_deploy_url": "",
        "created": _now(),
        "updated": _now(),
    }
    data["sites"][sid] = site_record
    save_data(data)
    return {"id": sid, **site_record}


def update_site_config(site_id: str, config_updates: dict) -> dict:
    """Update site config fields (partial update)."""
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return None

    site_dir = Path(s["directory"])
    if not site_dir.exists():
        return {"error": "Site directory not found"}

    # Try HTML config (JSON) first, then React config (JS module)
    config_path = site_dir / s.get("config_path", "")
    if not config_path.exists():
        config_path = site_dir / "site-config.json"
    if not config_path.exists():
        config_path = site_dir / "site.config.js"
    if not config_path.exists():
        config_path = site_dir / "src" / "config" / "site.config.js"
    if not config_path.exists():
        return {"error": "Config file not found"}

    # Read current config
    is_json_config = config_path.suffix == ".json"
    if is_json_config:
        try:
            current = json.loads(config_path.read_text())
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in config"}
    else:
        current_raw = config_path.read_text()
        import re
        m = re.search(r"export\s+const\s+siteConfig\s*=\s*(\{.*\})\s*;?\s*$", current_raw, re.DOTALL)
        if not m:
            return {"error": "Cannot parse existing config"}
        try:
            current = json.loads(m.group(1))
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in config"}

    # Deep merge updates
    def deep_merge(base, updates):
        for k, v in updates.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                deep_merge(base[k], v)
            elif v is not None:
                base[k] = v
        return base

    current = deep_merge(current, config_updates)

    # Update theme if changed
    if "theme" in config_updates:
        s["theme"] = config_updates["theme"]
    if "brand" in config_updates and "name" in config_updates["brand"]:
        s["name"] = config_updates["brand"]["name"]
    s["updated"] = _now()
    data["sites"][site_id] = s

    # Write updated config
    if is_json_config:
        config_path.write_text(json.dumps(current, indent=2))
    else:
        config_path.write_text(f"export const siteConfig = {json.dumps(current, indent=2, ensure_ascii=False)};\n")

    save_data(data)
    return {"id": site_id, "updated": True, "theme": s["theme"], "name": s["name"]}


def build_site(site_id: str) -> dict:
    """Build site. React: npm build. HTML: render via web_engine."""
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return {"error": "Site not found"}

    site_dir = Path(s["directory"])
    if not site_dir.exists():
        return {"error": "Site directory not found"}

    tpl = TEMPLATE_REGISTRY.get(s["template"], {})

    # ── HTML template: render via web_engine ──
    if tpl.get("type") == "html":
        try:
            html = render_html_site(
                s["template"],
                brand_name=s.get("name", "INXOTIVE"),
                industry=s.get("industry", "general"),
            )
            dist_dir = site_dir / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            (dist_dir / "index.html").write_text(html)
            s["status"] = "built"
            s["updated"] = _now()
            data["sites"][site_id] = s
            save_data(data)
            return {"success": True, "output": f"HTML rendered: {len(html)} chars"}
        except Exception as e:
            return {"success": False, "error": f"HTML render failed: {e}"}

    # ── React template: npm build ──
    node_modules = site_dir / "node_modules"
    if not node_modules.exists():
        tpl_item = TEMPLATE_REGISTRY.get(s["template"])
        if tpl_item:
            tpl_dir_item = TEMPLATES_DIR / tpl_item["dir"]
            if (tpl_dir_item / "node_modules").exists():
                shutil.copytree(str(tpl_dir_item / "node_modules"), str(node_modules), symlinks=True)

    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(site_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            s["status"] = "built"
            s["updated"] = _now()
            data["sites"][site_id] = s
            save_data(data)
            return {"success": True, "output": result.stdout[-500:]}
        else:
            return {"success": False, "error": result.stderr[-500:], "stdout": result.stdout[-500:]}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Build timed out after 120s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def deploy_site(site_id: str) -> dict:
    """Deploy site to Vercel production."""
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return {"error": "Site not found"}

    if not VERCEL_TOKEN:
        return {"error": "VERCEL_TOKEN not set in environment"}

    site_dir = Path(s["directory"])
    if not site_dir.exists():
        return {"error": f"Site directory not found: {s['directory']}"}

    # Step 1: Build if not already built
    dist_dir = site_dir / "dist"
    if not dist_dir.exists():
        build_result = build_site(site_id)
        if not build_result.get("success"):
            return {"error": "Build failed before deploy", "details": build_result.get("error")}

    # Step 2: Find vercel binary
    vercel_bin = str(site_dir / "node_modules" / ".bin" / "vercel")
    if not os.path.exists(vercel_bin):
        # Fallback to template's vercel
        tpl = TEMPLATE_REGISTRY.get(s.get("template"))
        if tpl:
            tpl_vercel = str(TEMPLATES_DIR / tpl["dir"] / "node_modules" / ".bin" / "vercel")
            if os.path.exists(tpl_vercel):
                vercel_bin = tpl_vercel
        if not os.path.exists(vercel_bin):
            return {"error": "vercel CLI not found. Install with: npm install --save-dev vercel"}

    # Step 3: Vercel build (generate .vercel/output)
    try:
        subprocess.run(
            [vercel_bin, "build", "--prod", "--yes",
             "--scope", VERCEL_TEAM, "--token", VERCEL_TOKEN],
            cwd=str(site_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {"error": "Vercel build timed out"}
    except Exception as e:
        return {"error": f"Vercel build error: {e}"}

    # Step 4: Deploy prebuilt
    did = _gen_id()
    try:
        result = subprocess.run(
            [vercel_bin,
             "deploy", "--prebuilt", "--prod", "--yes",
             "--scope", VERCEL_TEAM, "--token", VERCEL_TOKEN],
            cwd=str(site_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )
        deploy_url = result.stdout.strip() or ""
        status = "ready" if result.returncode == 0 else "failed"

        deployment = {
            "id": did,
            "site_id": site_id,
            "vercel_deployment_id": "",
            "status": status,
            "url": deploy_url,
            "commit_msg": f"Deploy {s['name']} from INXOTIVE Builder",
            "created": _now(),
        }
        data["deployments"][did] = deployment

        if status == "ready":
            s["status"] = "deployed"
            s["vercel_deploy_url"] = deploy_url
            # Try to find vercel project id
            proj_file = site_dir / ".vercel" / "project.json"
            if proj_file.exists():
                try:
                    proj = json.loads(proj_file.read_text())
                    s["vercel_project"] = proj.get("projectId", "")
                except:
                    pass
        else:
            s["status"] = "deploy-failed"
            deployment["error"] = result.stderr[-500:]

        s["updated"] = _now()
        data["sites"][site_id] = s
        save_data(data)
        return {"id": did, "url": deploy_url, "status": status, "site_id": site_id}

    except subprocess.TimeoutExpired:
        return {"error": "Deploy timed out"}
    except Exception as e:
        return {"error": f"Deploy error: {e}"}


def set_site_domain(site_id: str, domain: str) -> dict:
    """Assign custom domain to site's Vercel project."""
    data = load_data()
    s = data["sites"].get(site_id)
    if not s:
        return {"error": "Site not found"}
    if not VERCEL_TOKEN:
        return {"error": "VERCEL_TOKEN not set"}

    # Use Vercel API to assign domain
    vercel_project = s.get("vercel_project", "")
    if not vercel_project:
        return {"error": "No Vercel project associated. Deploy first."}

    import httpx as _httpx
    try:
        resp = _httpx.post(
            f"https://api.vercel.com/v9/projects/{vercel_project}/alias?teamId={VERCEL_TEAM}",
            headers={"Authorization": f"Bearer {VERCEL_TOKEN}"},
            json={"domain": domain},
            timeout=30,
        )
        if resp.is_success or "ALIAS_DOMAIN_EXIST" in resp.text:
            s["domain"] = domain
            s["updated"] = _now()
            data["sites"][site_id] = s
            save_data(data)
            return {"success": True, "domain": domain, "message": "Domain assigned"}
        else:
            return {"error": f"API Error: {resp.text}"}
    except Exception as e:
        return {"error": str(e)}


def delete_site(site_id: str) -> bool:
    data = load_data()
    s = data["sites"].pop(site_id, None)
    if not s:
        return False
    # Remove directory ONLY if no other site uses it
    site_dir = Path(s["directory"])
    shared = any(s2.get("directory") == s["directory"] for sid2, s2 in data["sites"].items())
    if site_dir.exists() and not shared:
        shutil.rmtree(site_dir)
    # Remove related
    for did in list(data["deployments"].keys()):
        if data["deployments"][did].get("site_id") == site_id:
            del data["deployments"][did]
    save_data(data)
    return True


# ════════════════════════════════════════════════════════════════
# ASSETS
# ════════════════════════════════════════════════════════════════

def list_assets(site_id: str = None):
    data = load_data()
    assets = []
    for aid, a in data["assets"].items():
        if site_id and a.get("site_id") != site_id:
            continue
        assets.append({"id": aid, **a})
    return sorted(assets, key=lambda a: a.get("uploaded", ""), reverse=True)


def upload_asset(client_id: str, site_id: str, filename: str, file_bytes: bytes, content_type: str = "") -> dict:
    """Save uploaded file and register in data."""
    data = load_data()
    aid = _gen_id()

    # Ensure directory
    site_assets_dir = ASSETS_DIR / site_id / "images"
    site_assets_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    safe_name = f"{aid}-{filename.lower().replace(' ', '-')}"
    file_path = site_assets_dir / safe_name
    file_path.write_bytes(file_bytes)

    # Determine type
    ext = Path(filename).suffix.lower()
    asset_type = "image" if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"] else "document"

    asset = {
        "client_id": client_id,
        "site_id": site_id,
        "filename": filename,
        "stored_as": safe_name,
        "path": str(file_path),
        "url": f"/api/assets/file/{aid}",
        "type": asset_type,
        "size": len(file_bytes),
        "content_type": content_type or "",
        "uploaded": _now(),
    }
    data["assets"][aid] = asset
    save_data(data)
    return {"id": aid, **asset}


def delete_asset(asset_id: str) -> bool:
    data = load_data()
    a = data["assets"].pop(asset_id, None)
    if not a:
        return False
    # Delete file
    asset_path = Path(a.get("path", ""))
    if asset_path.exists():
        asset_path.unlink()
    save_data(data)
    return True


# ════════════════════════════════════════════════════════════════
# CLIENT PORTAL TOKENS
# ════════════════════════════════════════════════════════════════

def generate_portal_token(client_id: str) -> str:
    """Generate a unique token for client portal access."""
    data = load_data()
    token = uuid.uuid4().hex[:32]
    data["portal_tokens"][token] = {
        "client_id": client_id,
        "created": _now(),
        "last_accessed": "",
    }
    save_data(data)
    return token


def verify_portal_token(token: str) -> dict:
    """Verify portal token and return client info."""
    data = load_data()
    entry = data["portal_tokens"].get(token)
    if not entry:
        return None
    cid = entry["client_id"]
    client = data["clients"].get(cid)
    if not client:
        return None
    # Update last accessed
    entry["last_accessed"] = _now()
    data["portal_tokens"][token] = entry
    save_data(data)
    sites = [s for s in data["sites"].values() if s.get("client_id") == cid]
    return {
        "client": {"id": cid, "name": client.get("name", ""), "company": client.get("company", "")},
        "sites": sites,
        "token": token,
    }
