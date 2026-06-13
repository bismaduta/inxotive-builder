"""
INXOTIVE Web Builder Server
============================
Standalone FastAPI server on port 7777.
Builder + Client Portal.
"""

import sys, os
from pathlib import Path

sys.path.insert(0, str(Path.home() / "market-api"))

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
)

app = FastAPI(title="INXOTIVE Builder", version="1.0")


# ── HTML Pages ──

@app.get("/", response_class=HTMLResponse)
async def builder_root():
    path = Path.home() / "market-api" / "builder.html"
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
    return result, 201


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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)
