# INXOTIVE Web Agency Builder

> Dashboard, Editor, Client Portal, and Vercel Deploy pipeline for INXOTIVE OFFICE.

**Live:** `http://localhost:7777` (server) · **Source:** `~/inxotive-builder/`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              TIER 1: AGENCY DASHBOARD                    │
│           (Bisma's Command Center — builder.html)        │
│                                                          │
│  Clients → Builder → Deploy → Monitor → Assets → Domain │
└────────────────────────┬────────────────────────────────┘
                         │ API (FastAPI :7777)
┌────────────────────────▼────────────────────────────────┐
│              TIER 2: CLIENT PORTAL                       │
│        (Per-client — /portal/{token})                    │
│                                                          │
│  My Site → Edit Content → Gallery → Requests → Stats    │
└──────────┬─────────────────────────────────────────────-─┘
           │
           ▼
    Template Engine (config-driven)
    Vercel Deploy / CLI
```

## Files

| File | Lines | Role |
|------|-------|------|
| `builder_server.py` | ~400 | FastAPI server (port 7777), all API endpoints |
| `builder.py` | ~777 | Core engine: data layer, template ops, Vercel deploy |
| `builder.html` | ~1506 | Agency dashboard frontend (6 pages) |
| `client-portal.html` | — | Client portal frontend (token-based) |
| `templates/` | 4 dirs | Website templates: klinik, apotek, lab, landing |

## Pages (Agency Dashboard)

1. **🏗️ Sites** — Grid view + stats + filter + deploy 1-klik
2. **🎨 Editor** — Form config (brand, kontak, services, jam, stats, about, SEO), theme picker (6 DNA)
3. **📋 Clients** — Table + stats + pipeline stage, generate portal link
4. **🚀 Deploy** — Ready-to-deploy list + deployment history
5. **🖼️ Assets** — Upload zone per site, drag & drop
6. **⚙️ Settings** — Theme toggle, default template

## API Endpoints

### Clients
```
GET    /api/clients          → list + pipeline stats
POST   /api/clients          → create client
GET    /api/clients/{id}     → detail + sites + activity
PUT    /api/clients/{id}     → update
DELETE /api/clients/{id}     → archive
```

### Sites
```
GET    /api/sites            → list all (dengan status)
POST   /api/sites            → create from template (copy + config)
GET    /api/sites/{id}       → full config JSON + meta
PUT    /api/sites/{id}/config → update config (partial)
POST   /api/sites/{id}/build → npm build
POST   /api/sites/{id}/deploy → Vercel deploy
POST   /api/sites/{id}/domain → custom domain
DELETE /api/sites/{id}       → remove
```

### Assets, Portal, Stats
```
GET/POST/DELETE /api/assets
POST   /api/portal/token     → generate client token
GET    /api/portal/verify/{token}
POST   /api/portal/request   → change request → Discord
GET    /api/stats            → quick overview stats
GET/POST /api/preview/{id}   → live preview (build + serve)
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/bismaduta/inxotive-builder.git
cd inxotive-builder

# 2. Install Python deps
pip install -r requirements.txt

# 3. Set env vars (optional)
export VERCEL_TOKEN="your_vercel_token"
export DISCORD_WEBHOOK="your_discord_webhook_url"

# 4. Run
python builder_server.py
# → http://localhost:7777
```

## Templates

4 config-driven templates with 6 theme variants each:

| Template | Default Theme | For |
|----------|--------------|-----|
| `klinik` | clinical-trust | Klinik, RS, puskesmas |
| `apotek` | fresh-apotek | Apotek, toko obat |
| `lab` | precision-lab | Lab diagnostik |
| `landing` | warm-family | Landing page umum, restoran, jasa |

Themes: clinical-trust, warm-family, precision-lab, heritage-care, fresh-apotek, premium-resto

## Data Storage

- `~/.agency_data.json` — semua data (clients, sites, deployments, assets, tokens)
- `~/client-assets/{site_id}/` — uploaded files
- Template source: `~/templates/` (symlinked from `templates/` dir in this repo)

## Systemd Service

```ini
[Unit]
Description=INXOTIVE Web Builder
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/bisma/inxotive-builder
ExecStart=/usr/bin/python3 -m uvicorn builder_server:app --host 0.0.0.0 --port 7777
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

## Tech Stack

- **Backend:** Python · FastAPI · Uvicorn
- **Frontend:** Vanilla JS · Tailwind CSS · Font Awesome 6
- **Templates:** React 18 · Vite · TailwindCSS
- **Deploy:** Vercel CLI / API
- **Storage:** JSON file → SQLite (future)

---

📦 **INXOTIVE OFFICE** — bismaduta
