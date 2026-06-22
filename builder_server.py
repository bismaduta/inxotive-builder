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
import json

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
    # Check inxotive-builder first, fallback to market-api
    for p in [Path.home() / "inxotive-builder", Path.home() / "market-api"]:
        path = p / "builder.html"
        if path.exists():
            return HTMLResponse(path.read_text())
    return HTMLResponse("<h1>Builder not found</h1>", status_code=404)


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
    For React templates, reads from dev server or dist.
    For HTML templates, renders via web_engine on-the-fly.
    """
    from builder import get_site, render_html_site, generate_multi_page_site, load_data

    site = get_site(sid)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    template_id = site.get("template", "landing")

    # Check if HTML template (web_engine rendered)
    # We check by looking up the template registry
    from builder import TEMPLATE_REGISTRY
    tpl = TEMPLATE_REGISTRY.get(template_id, {})
    if tpl.get("type") == "html":
        # Render single page
        content_overrides = {}
        config = site.get("config", {})
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

    # React template -- serve dist/index.html or trigger build
    site_dir = Path(site.get("directory", ""))
    if not site_dir.exists():
        return HTMLResponse("<html><body><h2>Site directory not found</h2></body></html>", status_code=404)

    dist_index = site_dir / "dist" / "index.html"
    if dist_index.exists():
        html = dist_index.read_text()
        # Rewrite asset paths to go through builder's static serving
        html = html.replace('src="/assets/', 'src="/site-assets/' + sid + '/assets/')
        html = html.replace('href="/assets/', 'href="/site-assets/' + sid + '/assets/')
        return HTMLResponse(html)

    # Check for multi-page (on non-primary pages)
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
        _sys.path.insert(0, os.path.expanduser("~/market-api"))
        from web_engine.css_framework import ALL_BRANDS
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


@app.get("/api/premium/html/{slug}")
async def api_premium_html(slug: str, template: str = "landing", download: bool = False):
    try:
        _sys.path.insert(0, os.path.expanduser("~/market-api"))
        from web_engine.css_framework import generate_premium_page
        html = generate_premium_page(slug)
        headers = {"X-Content-Type-Options": "nosniff"}
        if download:
            headers["Content-Disposition"] = f'attachment; filename="premium-{slug}.html"'
        return HTMLResponse(content=html, headers=headers)
    except ImportError:
        return HTMLResponse(
            content=f"<html><body style='padding:40px;font-family:sans-serif'><h2>Premium Engine Not Available</h2><p>Run: cd ~/market-api && python3 web_engine/premium_tailor.py</p></body></html>",
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
        _sys.path.insert(0, os.path.expanduser("~/market-api"))
        from web_engine.css_framework import generate_framework
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

    # 1. Generate premium HTML
    try:
        _sys.path.insert(0, os.path.expanduser("~/market-api"))
        from web_engine.css_framework import generate_premium_page
        html = generate_premium_page(slug)
    except ImportError:
        raise HTTPException(status_code=503, detail="Premium engine not available (web_engine.css_framework missing)")
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
