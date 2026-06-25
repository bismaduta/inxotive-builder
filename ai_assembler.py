"""
INXOTIVE Section Assembler
============================
Layer 2: Menerima SectionSpec JSON dari AIOrchestrator, merender tiap section
menggunakan css_framework.py, menggabung dengan CSS framework per brand,
dan menghasilkan halaman HTML lengkap.

Flow:
  spec → generate CSS framework → render each section → wrap page → HTML
"""

import json
from typing import Optional


class SectionAssembler:
    """Assemble section specs into complete HTML pages."""

    def __init__(self):
        self._css_framework = None
        self._brand_data = None

    def _ensure_framework(self):
        """Lazy-load the CSS framework module."""
        if self._css_framework is None:
            import sys
            from pathlib import Path
            # Ensure we can import from inxotive-builder
            sys.path.insert(0, str(Path.home() / "inxotive-builder"))
            from css_framework import (
                generate_framework, generate_navbar,
                generate_premium_page, list_brands
            )
            self._css_framework = {
                "generate": generate_framework,
                "navbar": generate_navbar,
                "page": generate_premium_page,
                "brands": list_brands,
            }

    def render(self, section_type: str, variant: str, content: dict, brand_data: dict) -> str:
        """Render a single section by type.

        Delegates to css_framework's internal renderers, passing content as kwargs.
        Falls back to generate_premium_page sections if direct renderer not found.
        """
        self._ensure_framework()
        primary = brand_data.get("colors", {}).get("primary", "#6366f1")
        accent = brand_data.get("colors", {}).get("accent", "#f59e0b")
        secondary = brand_data.get("colors", {}).get("secondary", "#8b5cf6")

        # Map to css_framework renderers with parameters
        renderers = {
            "hero": self._render_hero,
            "features": self._render_features,
            "stats": self._render_stats,
            "testimonials": self._render_testimonials,
            "cta": self._render_cta,
            "pricing": self._render_pricing,
            "about": self._render_about,
            "team": self._render_team,
            "faq": self._render_faq,
            "contact": self._render_contact,
            "gallery": self._render_gallery,
            "footer": self._render_footer,
        }

        render_fn = renderers.get(section_type)
        if render_fn:
            try:
                return render_fn(variant, content, primary, accent, secondary, brand_data)
            except Exception as e:
                return f"<!-- Error rendering {section_type}: {e} -->"

        return f"<!-- Section {section_type} not implemented yet -->"

    def _hero_content_params(self, c: dict, primary: str) -> dict:
        """Extract and prepare hero content parameters."""
        return {
            "headline": c.get("headline", "Welcome"),
            "tagline": c.get("tagline", "Tagline"),
            "subheadline": c.get("subheadline", ""),
            "cta": c.get("cta_text", "Get Started"),
            "cta_link": c.get("cta_link", "#cta"),
            "secondary_cta": c.get("secondary_text", "Learn More"),
            "secondary_link": c.get("secondary_link", "#features"),
            "trust_stats": c.get("trust_stats", []),
            "image": c.get("image", ""),
            "primary": primary,
        }

    def _render_hero(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        """Render hero section with appropriate variant."""
        name = c.get("headline", "Welcome")
        tagline = c.get("tagline", "")
        sub = c.get("subheadline", "")
        image = c.get("image", "")
        trust = c.get("trust_stats", [])

        if variant == "centered":
            return self._make_section("hero", f"""
  <div class="container container--narrow" style="text-align:center;position:relative;z-index:1">
    <div class="vfx-slide-up">
      <span class="badge" style="display:inline-block;padding:8px 20px;background:var(--brand-primary);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);margin-bottom:var(--space-lg)">{tagline}</span>
      <h1 class="heading-1" style="margin-bottom:var(--space-lg)">{name}</h1>
      <p class="body-text" style="font-size:1.125rem;max-width:600px;margin:0 auto var(--space-xl);color:var(--ink);opacity:0.85">{sub or "Solusi lengkap untuk transformasi digital bisnis Anda."}</p>
      <div class="flex" style="display:flex;gap:var(--space-md);justify-content:center;flex-wrap:wrap">
        <a href="{c.get('cta_link','#cta')}" class="btn-primary">{c.get('cta_text','Mulai Sekarang')}</a>
        <a href="{c.get('secondary_link','#features')}" class="btn-secondary">{c.get('secondary_text','Pelajari')}</a>
      </div>
    </div>
  </div>""")
        elif variant == "gradient":
            return self._make_section("hero", f"""
  <div class="container container--narrow" style="text-align:center;position:relative;z-index:1">
    <div class="vfx-slide-up">
      <span class="badge" style="display:inline-block;padding:8px 20px;background:rgba(255,255,255,0.2);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);margin-bottom:var(--space-lg)">{tagline}</span>
      <h1 class="heading-1" style="color:#fff;margin-bottom:var(--space-lg)">{name}</h1>
      <p class="body-text" style="color:rgba(255,255,255,0.85);max-width:600px;margin:0 auto var(--space-xl)">{sub or "Platform all-in-one untuk bisnis Anda."}</p>
      <div class="flex" style="display:flex;gap:var(--space-md);justify-content:center;flex-wrap:wrap">
        <a href="{c.get('cta_link','#cta')}" style="display:inline-flex;padding:16px 36px;background:#fff;color:var(--brand-primary);border-radius:var(--radius-full);font-weight:600">{c.get('cta_text','Mulai')}</a>
        <a href="{c.get('secondary_link','#features')}" style="display:inline-flex;padding:16px 36px;border:2px solid rgba(255,255,255,0.3);color:#fff;border-radius:var(--radius-full)">{c.get('secondary_text','Pelajari')}</a>
      </div>
    </div>
  </div>""", extra_class="section--dark")
        else:
            # Default: split
            trust_html = ""
            if trust:
                items = "".join(f'<div><strong class="heading-4" style="color:var(--brand-primary)">{t["number"]}</strong><p class="text-small" style="color:var(--ink);opacity:0.75">{t["label"]}</p></div>' for t in trust[:3])
                trust_html = f'<div class="flex" style="display:flex;gap:var(--space-lg);margin-top:var(--space-xxl);padding-top:var(--space-lg);border-top:1px solid var(--hairline)">{items}</div>'

            img_html = ""
            if image:
                img_html = f'<div style="width:100%;height:100%;background:var(--surface-2);background-image:url({image});background-size:cover;background-position:center"></div>'
            else:
                img_html = '<div style="padding:40px;min-height:320px;display:flex;flex-direction:column;gap:16px;background:var(--surface-1)"><div style="height:48px;width:60%;background:var(--brand-gradient);opacity:0.15;border-radius:var(--radius-md)"></div><div style="height:16px;width:90%;background:var(--surface-3);border-radius:var(--radius-sm)"></div><div style="flex:1;min-height:80px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px"><div style="background:linear-gradient(180deg, var(--brand-primary)00, var(--brand-primary)20);border-radius:var(--radius-md);border:1px solid var(--hairline)"></div><div style="background:linear-gradient(180deg, var(--brand-secondary)00, var(--brand-secondary)15);border-radius:var(--radius-md);margin-top:16px"></div><div style="background:linear-gradient(180deg, var(--brand-accent)00, var(--brand-accent)15);border-radius:var(--radius-md)"></div></div></div>'

            return self._make_section("hero", f"""
  <div class="container">
    <div class="hero-split" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center;min-height:80vh">
      <div class="vfx-slide-up">
        <span class="badge" style="display:inline-block;padding:6px 16px;background:var(--brand-primary);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);margin-bottom:var(--space-lg)">{tagline}</span>
        <h1 class="heading-1" style="margin-bottom:var(--space-lg)">{name}</h1>
        <p class="body-text" style="font-size:1.125rem;margin-bottom:var(--space-xl);max-width:520px;color:var(--ink);opacity:0.85">{sub or "Platform all-in-one untuk mengelola dan mengembangkan bisnis Anda."}</p>
        <div class="flex" style="display:flex;gap:var(--space-md);flex-wrap:wrap">
          <a href="{c.get('cta_link','#cta')}" class="btn-primary">{c.get('cta_text','Mulai Gratis')}</a>
          <a href="{c.get('secondary_link','#features')}" class="btn-secondary">{c.get('secondary_text','Tonton Demo')}</a>
        </div>
        {trust_html}
      </div>
      <div class="hero-mockup vfx-float" style="background:var(--surface-2);border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-xl);border:1px solid var(--hairline)">
        <div class="mockup-bar" style="display:flex;align-items:center;gap:6px;padding:12px 16px;background:var(--surface-3);border-bottom:1px solid var(--hairline)">
          <span style="width:10px;height:10px;border-radius:50%;background:#EF4444"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#F59E0B"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#22C55E"></span>
        </div>
        {img_html}
      </div>
    </div>
  </div>""")

    def _render_features(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "Fitur")
        subtitle = c.get("subtitle", "")

        if not items:
            return ""

        cards = "\n".join(
            f'<div class="glass-card-solid card-feature hover-lift stagger-{(i%5)+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);text-align:center">'
            f'<div style="width:40px;height:40px;margin-bottom:var(--space-md);font-size:2rem">{item.get("icon","🚀")}</div>'
            f'<h3 class="heading-4" style="margin-bottom:var(--space-sm)">{item.get("title","")}</h3>'
            f'<p class="body-text text-small" style="color:var(--ink);opacity:0.75">{item.get("desc","")}</p></div>'
            for i, item in enumerate(items)
        )

        return self._make_section("features", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:600;text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">{title}</span>
      <h2 class="section__heading">{subtitle or "Semua yang Anda Butuhkan"}</h2>
    </div>
    <div class="grid-3" style="gap:var(--space-lg)">{cards}</div>
  </div>""")

    def _render_stats(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        if not items:
            return ""
        stats = "\n".join(
            f'<div class="stat-item vfx-fade-in-up stagger-{(i%4)+1}"><div class="heading-1" style="color:#fff;font-weight:800">{s["number"]}</div><p style="color:rgba(255,255,255,0.8);font-size:var(--text-body)">{s["label"]}</p></div>'
            for i, s in enumerate(items)
        )
        return self._make_section("stats", f"""
  <div class="container">
    <div class="grid-4" style="gap:var(--space-xl)">{stats}</div>
  </div>""", extra_class="section--accent")

    def _render_testimonials(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "Testimoni")
        subtitle = c.get("subtitle", "")
        if not items:
            return ""
        cards = "\n".join(
            f'<div class="glass-card-solid hover-lift stagger-{(i%3)+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);position:relative">'
            f'<div style="font-size:3rem;color:var(--brand-primary);opacity:0.2;position:absolute;top:16px;right:20px;font-family:serif;line-height:1">"</div>'
            f'<p class="body-text" style="margin-bottom:var(--space-lg);font-style:italic;position:relative;z-index:1">"{t.get("text","")}"</p>'
            f'<div class="flex" style="display:flex;align-items:center;gap:var(--space-md)">'
            f'<div style="width:44px;height:44px;border-radius:50%;background:var(--brand-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700">{t.get("name","?")[0]}</div>'
            f'<div><strong style="font-size:var(--text-small)">{t.get("name","")}</strong><p class="text-xs text-muted">{t.get("role","")}</p></div></div></div>'
            for i, t in enumerate(items)
        )
        return self._make_section("testimonials", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle or "Apa kata mereka"}</p>
    </div>
    <div class="grid-3" style="gap:var(--space-lg)">{cards}</div>
  </div>""")

    def _render_cta(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        title = c.get("title", "Siap Memulai?")
        subtitle = c.get("subtitle", "")
        btn_text = c.get("button_text", "Hubungi Kami")
        btn_link = c.get("button_link", "#contact")
        sec_text = c.get("secondary_text", "Lihat Pricing")
        sec_link = c.get("secondary_link", "#pricing")

        return self._make_section("cta", f"""
  <div class="container container--narrow" style="position:relative;z-index:1;text-align:center">
    <div class="vfx-scale-in">
      <h2 class="heading-2" style="color:#fff;margin-bottom:var(--space-md)">{title}</h2>
      <p class="body-text" style="color:rgba(255,255,255,0.85);margin-bottom:var(--space-xl);font-size:1.125rem">{subtitle or "Gabung dengan ratusan bisnis yang sudah bertransformasi digital."}</p>
      <div class="flex" style="display:flex;gap:var(--space-md);justify-content:center;flex-wrap:wrap">
        <a href="{btn_link}" style="display:inline-flex;padding:16px 36px;background:#fff;color:var(--brand-primary);border-radius:var(--radius-full);font-weight:600;box-shadow:var(--shadow-lg)">{btn_text}</a>
        <a href="{sec_link}" style="display:inline-flex;padding:16px 36px;border:2px solid rgba(255,255,255,0.3);color:#fff;border-radius:var(--radius-full)">{sec_text}</a>
      </div>
    </div>
  </div>""", extra_class="cta-gradient")

    def _render_pricing(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "Pricing")
        subtitle = c.get("subtitle", "")
        if not items:
            return ""
        cards = ""
        for i, plan in enumerate(items):
            popular = plan.get("popular", False)
            features_html = "\n".join(
                f'<li style="display:flex;align-items:center;gap:var(--space-sm);padding:8px 0"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{"var(--brand-primary)" if not popular else "#fff"}" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>{f}</li>'
                for f in plan.get("features", [])
            )
            popular_class = "transform:scale(1.05);border:2px solid var(--brand-primary);position:relative" if popular else ""
            popular_badge = '<div style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--brand-primary);color:#fff;padding:4px 16px;border-radius:var(--radius-full);font-size:var(--text-xs);font-weight:600">POPULER</div>' if popular else ""
            btn_class = "background:var(--brand-gradient);color:#fff" if popular else "border:1px solid var(--hairline)"
            cards += f'<div class="glass-card-solid hover-lift stagger-{i+1}" style="padding:var(--space-xxl);border-radius:var(--radius-lg);text-align:center;{popular_class}">{popular_badge}<h3 class="heading-3" style="margin-bottom:var(--space-sm)">{plan.get("name","")}</h3><p class="text-small text-muted" style="margin-bottom:var(--space-lg)">{plan.get("desc","")}</p><div class="heading-2" style="margin-bottom:var(--space-lg)">{plan.get("price","")}<span class="text-small text-muted">{plan.get("period","")}</span></div><ul style="text-align:left;margin-bottom:var(--space-xl)">{features_html}</ul><a href="{c.get("button_link","#cta")}" style="display:block;padding:14px 0;border-radius:var(--radius-full);font-weight:600;{btn_class}">{plan.get("cta","Pilih")}</a></div>'

        return self._make_section("pricing", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle or "Pilih paket yang sesuai"}</p>
    </div>
    <div class="grid-3" style="gap:var(--space-lg);align-items:start">{cards}</div>
  </div>""")

    def _render_about(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        title = c.get("title", "Tentang Kami")
        body = c.get("body", "")
        body2 = c.get("body2", "")
        image = c.get("image", "")
        stats = c.get("stats", [])

        stats_html = ""
        if stats:
            stats_html = '<div class="flex" style="display:flex;gap:var(--space-xl);flex-wrap:wrap">' + \
                "".join(f'<div><strong class="heading-3" style="color:var(--brand-primary)">{s["number"]}</strong><p class="text-small text-muted">{s["label"]}</p></div>' for s in stats) + '</div>'

        img_html = f'<div style="width:100%;height:100%;background-image:url({image});background-size:cover;background-position:center"></div>' if image else '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:24px;width:100%"><div style="height:120px;background:var(--brand-primary);opacity:0.15;border-radius:var(--radius-md)"></div><div style="height:120px;background:var(--brand-accent);opacity:0.15;border-radius:var(--radius-md);margin-top:30px"></div><div style="height:80px;background:var(--brand-secondary);opacity:0.12;border-radius:var(--radius-md);grid-column:1/-1"></div></div>'

        return self._make_section("about", f"""
  <div class="container">
    <div class="about-split" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center">
      <div class="vfx-slide-up">
        <h2 class="heading-2" style="margin-bottom:var(--space-lg)">{title}</h2>
        <p class="body-text" style="margin-bottom:var(--space-md)">{body}</p>
        {f'<p class="body-text text-muted" style="margin-bottom:var(--space-xl)">{body2}</p>' if body2 else ''}
        {stats_html}
      </div>
      <div class="about-image vfx-float" style="background:var(--surface-3);border-radius:var(--radius-lg);height:400px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:var(--shadow-lg)">
        {img_html}
      </div>
    </div>
  </div>""")

    def _render_team(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "Tim Kami")
        subtitle = c.get("subtitle", "")
        if not items:
            return ""
        cards = "\n".join(
            f'<div class="glass-card-solid hover-lift stagger-{(i%4)+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);text-align:center">'
            f'<div style="width:80px;height:80px;border-radius:50%;background:var(--brand-gradient);margin:0 auto var(--space-md);display:flex;align-items:center;justify-content:center;font-size:2rem;color:#fff;font-weight:700">{m.get("name","?")[0]}</div>'
            f'<h4 class="heading-4" style="margin-bottom:var(--space-xs)">{m.get("name","")}</h4>'
            f'<p class="text-small" style="color:var(--brand-primary);margin-bottom:var(--space-sm)">{m.get("role","")}</p>'
            f'<p class="text-xs text-muted">{m.get("desc","")}</p></div>'
            for i, m in enumerate(items)
        )
        return self._make_section("team", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle or "Tim ahli di balik kesuksesan"}</p>
    </div>
    <div class="grid-4" style="gap:var(--space-lg)">{cards}</div>
  </div>""")

    def _render_faq(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "FAQ")
        subtitle = c.get("subtitle", "")
        if not items:
            return ""
        faqs = "\n".join(
            f'<details class="glass-card-solid" style="padding:var(--space-lg);border-radius:var(--radius-md);margin-bottom:var(--space-sm);cursor:pointer">'
            f'<summary style="font-weight:600;font-size:var(--text-body);display:flex;align-items:center;justify-content:space-between">'
            f'{faq.get("question","")}<span style="font-size:1.2rem;transition:transform var(--anim-duration-normal)">▼</span></summary>'
            f'<p class="body-text text-muted" style="margin-top:var(--space-md)">{faq.get("answer","")}</p></details>'
            for faq in items
        )
        return self._make_section("faq", f"""
  <div class="container container--narrow">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle or "Pertanyaan umum"}</p>
    </div>
    {faqs}
  </div>""")

    def _render_contact(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        title = c.get("title", "Kontak")
        subtitle = c.get("subtitle", "Hubungi Kami")
        email = c.get("email", "hello@inxotive.com")
        phone = c.get("phone", "")
        address = c.get("address", "")
        whatsapp = c.get("whatsapp", "")

        info_items = f'<div><strong style="font-size:var(--text-body)">Email</strong><p class="text-muted text-small">{email}</p></div>'
        if phone:
            info_items += f'<div><strong style="font-size:var(--text-body)">Telepon</strong><p class="text-muted text-small">{phone}</p></div>'
        if address:
            info_items += f'<div><strong style="font-size:var(--text-body)">Alamat</strong><p class="text-muted text-small">{address}</p></div>'
        if whatsapp:
            info_items += f'<div><strong style="font-size:var(--text-body)">WhatsApp</strong><p class="text-muted text-small"><a href="https://wa.me/{whatsapp}" target="_blank">{whatsapp}</a></p></div>'

        return self._make_section("contact", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle}</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);max-width:900px;margin:0 auto">
      <div class="glass-card-solid" style="padding:var(--space-xl);border-radius:var(--radius-lg);display:flex;flex-direction:column;gap:var(--space-lg)">
        {info_items}
      </div>
      <form class="glass-card-solid" style="padding:var(--space-xl);border-radius:var(--radius-lg);display:flex;flex-direction:column;gap:var(--space-md)">
        <input placeholder="Nama" style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-1)">
        <input placeholder="Email" type="email" style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-1)">
        <textarea placeholder="Pesan" rows="4" style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-1);resize:vertical"></textarea>
        <button style="padding:14px;background:var(--brand-gradient);color:#fff;border:none;border-radius:var(--radius-full);font-weight:600;cursor:pointer">Kirim Pesan</button>
      </form>
    </div>
  </div>""")

    def _render_gallery(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        items = c.get("items", [])
        title = c.get("title", "Portfolio")
        subtitle = c.get("subtitle", "")
        if not items:
            return ""
        grid_items = "\n".join(
            f'<div style="overflow:hidden;border-radius:var(--radius-lg);aspect-ratio:4/3;background:var(--surface-2);position:relative;cursor:pointer;transition:transform var(--anim-duration-normal)">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(0,0,0,0.4));z-index:1"></div>'
            f'<div style="position:absolute;bottom:0;left:0;right:0;padding:var(--space-lg);z-index:2;color:#fff">'
            f'<strong>{item.get("title","Project")}</strong><p class="text-xs" style="opacity:0.7">{item.get("category","")}</p></div>'
            f'<div style="width:100%;height:100%;background:linear-gradient(135deg,var(--brand-primary),var(--brand-accent));opacity:0.12"></div></div>'
            for item in items
        )
        return self._make_section("gallery", f"""
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">{title}</h2>
      <p class="section__subheading">{subtitle or "Karya terbaik kami"}</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--space-lg)">
      {grid_items}
    </div>
  </div>""")

    def _render_footer(self, variant: str, c: dict, primary: str, accent: str, secondary: str, brand: dict) -> str:
        brand_name = c.get("brand", "INXOTIVE")
        desc = c.get("description", "Building digital future")
        email = c.get("email", "")
        social = c.get("social", {})
        social_html = ""
        if social:
            links = []
            if social.get("instagram"):
                links.append(f'<a href="{social["instagram"]}" target="_blank" style="color:var(--ink-muted);text-decoration:none">Instagram</a>')
            if social.get("youtube"):
                links.append(f'<a href="{social["youtube"]}" target="_blank" style="color:var(--ink-muted);text-decoration:none">YouTube</a>')
            if links:
                social_html = '<div style="display:flex;gap:var(--space-md);margin-top:var(--space-md)">' + "".join(links) + '</div>'

        return f"""<footer class="section section--dark" role="contentinfo" style="padding:var(--space-xxl) 0 var(--space-lg)">
  <div class="container">
    <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:var(--space-xxl);margin-bottom:var(--space-xxl)">
      <div><h3 class="heading-4" style="color:#fff;margin-bottom:var(--space-md)">{brand_name}</h3><p class="text-small" style="color:rgba(255,255,255,0.7);max-width:280px">{desc}</p>{social_html}</div>
      <div><h4 class="text-small" style="color:#fff;margin-bottom:var(--space-md);font-weight:600">Layanan</h4><div style="display:flex;flex-direction:column;gap:var(--space-sm)"><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">Web Design</a><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">AI Automation</a><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">SEO</a></div></div>
      <div><h4 class="text-small" style="color:#fff;margin-bottom:var(--space-md);font-weight:600">Perusahaan</h4><div style="display:flex;flex-direction:column;gap:var(--space-sm)"><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">Tentang</a><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">Karir</a><a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">Blog</a></div></div>
      <div><h4 class="text-small" style="color:#fff;margin-bottom:var(--space-md);font-weight:600">Kontak</h4><div style="display:flex;flex-direction:column;gap:var(--space-sm)">{f'<a href="mailto:{email}" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:var(--text-small)">{email}</a>' if email else ''}</div></div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.1);padding-top:var(--space-lg);text-align:center;color:rgba(255,255,255,0.4);font-size:var(--text-xs)">
      &copy; 2026 {brand_name}. All rights reserved.
    </div>
  </div>
</footer>"""

    def _make_section(self, section_type: str, inner_html: str, extra_class: str = "") -> str:
        """Wrap inner HTML in a standard section container."""
        section_class = f"section section--{section_type} section--reveal"
        if extra_class:
            section_class += f" {extra_class}"
        return f'<section class="{section_class}" role="region" aria-label="{section_type}">\n{inner_html}\n</section>'

    def assemble(self, spec: dict, brand_name: Optional[str] = None) -> str:
        """Assemble complete HTML page from spec.

        Args:
            spec: Dict with "brand", "sections" (array of {type, variant, content}), "colors", "fonts"
            brand_name: Override brand name (falls back to spec["brand"])

        Returns:
            Complete HTML page as string
        """
        self._ensure_framework()
        brand = brand_name or spec.get("brand", "inxotive")

        try:
            css = self._css_framework["generate"](brand)
        except Exception:
            css = ""

        # Get brand colors for renderers
        brand_data = {"colors": spec.get("colors", {}), "fonts": spec.get("fonts", {})}

        # Render each section
        sections_html = []
        for sec in spec.get("sections", []):
            html = self.render(
                sec.get("type", ""),
                sec.get("variant", ""),
                sec.get("content", {}),
                brand_data
            )
            sections_html.append(html)

        all_sections = "\n".join(sections_html)

        fonts = spec.get("fonts", {})
        heading_font = fonts.get("heading", "Plus Jakarta Sans") if fonts else "Plus Jakarta Sans"
        body_font = fonts.get("body", "Inter") if fonts else "Inter"

        html = f"""<!DOCTYPE html>
<html lang="id" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{spec.get("title", "INXOTIVE Design")}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={heading_font.replace(' ', '+')}:wght@400;500;600;700;800&family={body_font.replace(' ', '+')}:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="page-wrapper" style="font-family:'{body_font}',sans-serif">
{all_sections}
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  // IntersectionObserver for scroll animations
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }}
    }});
  }}, {{ threshold: 0.1 }});
  document.querySelectorAll('.section--reveal').forEach(el => observer.observe(el));
}});
</script>
</body>
</html>"""
        return html


def assemble(spec: dict, brand_name: Optional[str] = None) -> str:
    """Convenience function: assemble spec into HTML."""
    assembler = SectionAssembler()
    return assembler.assemble(spec, brand_name)
