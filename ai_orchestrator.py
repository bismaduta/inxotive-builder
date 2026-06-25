"""
INXOTIVE AI Design Orchestrator
=================================
Layer 1: Menerima prompt user + upload + opsi, menghubungi AI model (9Router > Ollama VPS),
menghasilkan structured JSON spec yang siap di-assemble oleh SectionAssembler.

Flow:
  prompt → design_intel recommendations → LLM call → validate → return spec

Combo model:
  Primary: 9Router (Gemini Flash, Nemotron, Claude, DeepSeek)
  Fallback: Ollama VPS qwen2.5:7b (100.78.79.60:11434)
"""

import json, re, os
from typing import Optional

# ── SECTION SCHEMA — parameter definitions per section type ──
SECTION_SCHEMA = {
    "hero": {
        "variants": ["split", "centered", "gradient", "full-bleed", "video"],
        "default_variant": "split",
        "params": {
            "headline": {"type": "string", "default": "Welcome"},
            "tagline": {"type": "string", "default": "Tagline"},
            "subheadline": {"type": "string", "default": ""},
            "cta_text": {"type": "string", "default": "Get Started"},
            "cta_link": {"type": "string", "default": "#cta"},
            "secondary_text": {"type": "string", "default": "Learn More"},
            "secondary_link": {"type": "string", "default": "#features"},
            "image": {"type": "string", "default": ""},
            "trust_stats": {
                "type": "array",
                "items": {"type": "object", "props": {"number": "string", "label": "string"}},
                "default": [
                    {"number": "500+", "label": "Users"},
                    {"number": "99.9%", "label": "Uptime"},
                    {"number": "4.9★", "label": "Rating"}
                ]
            }
        }
    },
    "features": {
        "variants": ["grid-3", "grid-4", "zigzag", "showcase", "icon-grid"],
        "default_variant": "grid-3",
        "params": {
            "title": {"type": "string", "default": "Features"},
            "subtitle": {"type": "string", "default": "What we offer"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"icon": "string", "title": "string", "desc": "string"}},
                "default": [
                    {"icon": "🚀", "title": "Fast Performance", "desc": "Lightning speed"},
                    {"icon": "🔒", "title": "Secure", "desc": "End-to-end encryption"},
                    {"icon": "🎨", "title": "Modern Design", "desc": "Beautiful UI/UX"}
                ]
            }
        }
    },
    "stats": {
        "variants": ["default", "grid-4"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "By the Numbers"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"number": "string", "label": "string"}},
                "default": [
                    {"number": "500+", "label": "Clients"},
                    {"number": "99.9%", "label": "Uptime"},
                    {"number": "50K+", "label": "Hours"},
                    {"number": "15+", "label": "Years"}
                ]
            }
        }
    },
    "testimonials": {
        "variants": ["default", "carousel", "grid"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Testimonials"},
            "subtitle": {"type": "string", "default": "What people say"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"name": "string", "role": "string", "text": "string", "avatar": "string"}},
                "default": [
                    {"name": "Client", "role": "CEO", "text": "Great service!", "avatar": ""}
                ]
            }
        }
    },
    "pricing": {
        "variants": ["default", "compact", "side-by-side"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Pricing"},
            "subtitle": {"type": "string", "default": "Choose your plan"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {
                    "name": "string", "price": "string", "period": "string",
                    "desc": "string", "features": {"type": "array", "items": "string"},
                    "popular": "bool", "cta": "string"
                }},
                "default": [
                    {"name": "Starter", "price": "Rp 1.5jt", "period": "/project", "desc": "For beginners",
                     "features": ["1 Website", "5 Pages", "SSL Free"], "popular": False, "cta": "Choose"},
                    {"name": "Professional", "price": "Rp 3.5jt", "period": "/project", "desc": "For growing",
                     "features": ["10 Websites", "Unlimited Pages", "SSL + CDN"], "popular": True, "cta": "Choose"},
                    {"name": "Enterprise", "price": "Rp 7.5jt", "period": "/project", "desc": "For large",
                     "features": ["Unlimited", "Custom Features", "Dedicated"], "popular": False, "cta": "Contact"}
                ]
            }
        }
    },
    "about": {
        "variants": ["standard", "right-image", "split"],
        "default_variant": "standard",
        "params": {
            "title": {"type": "string", "default": "About Us"},
            "body": {"type": "string", "default": "Our story..."},
            "body2": {"type": "string", "default": ""},
            "image": {"type": "string", "default": ""},
            "stats": {
                "type": "array",
                "items": {"type": "object", "props": {"number": "string", "label": "string"}},
                "default": [
                    {"number": "5+", "label": "Years"},
                    {"number": "500+", "label": "Projects"}
                ]
            }
        }
    },
    "team": {
        "variants": ["default", "grid"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Our Team"},
            "subtitle": {"type": "string", "default": "Meet the experts"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"name": "string", "role": "string", "desc": "string", "avatar": "string"}},
                "default": [
                    {"name": "Bisma", "role": "CEO", "desc": "Visionary", "avatar": ""}
                ]
            }
        }
    },
    "faq": {
        "variants": ["default"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "FAQ"},
            "subtitle": {"type": "string", "default": "Common questions"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"question": "string", "answer": "string"}},
                "default": [
                    {"question": "How does it work?", "answer": "It's simple..."}
                ]
            }
        }
    },
    "cta": {
        "variants": ["default", "compact", "newsletter"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Ready to Start?"},
            "subtitle": {"type": "string", "default": "Join us today"},
            "button_text": {"type": "string", "default": "Contact Us"},
            "button_link": {"type": "string", "default": "#contact"},
            "secondary_text": {"type": "string", "default": "Learn More"},
            "secondary_link": {"type": "string", "default": "#features"}
        }
    },
    "contact": {
        "variants": ["default"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Contact Us"},
            "subtitle": {"type": "string", "default": "Get in touch"},
            "email": {"type": "string", "default": "hello@inxotive.com"},
            "phone": {"type": "string", "default": "+62 812 3456 7890"},
            "address": {"type": "string", "default": "Jakarta, Indonesia"},
            "whatsapp": {"type": "string", "default": "6281234567890"}
        }
    },
    "gallery": {
        "variants": ["default", "masonry", "grid"],
        "default_variant": "default",
        "params": {
            "title": {"type": "string", "default": "Our Work"},
            "subtitle": {"type": "string", "default": "Recent projects"},
            "items": {
                "type": "array",
                "items": {"type": "object", "props": {"title": "string", "category": "string", "image": "string"}},
                "default": [
                    {"title": "Project 1", "category": "Web", "image": ""}
                ]
            }
        }
    },
    "footer": {
        "variants": ["default", "compact"],
        "default_variant": "default",
        "params": {
            "brand": {"type": "string", "default": "INXOTIVE"},
            "description": {"type": "string", "default": "Building digital future"},
            "email": {"type": "string", "default": "hello@inxotive.com"},
            "social": {
                "type": "object",
                "props": {"instagram": "string", "youtube": "string"},
                "default": {"instagram": "#", "youtube": "#"}
            }
        }
    },
    "divider": {
        "variants": ["wave", "default"],
        "default_variant": "wave",
        "params": {}
    }
}

# ── Brand DNA mapping ──
BRAND_DESCRIPTIONS = {
    "inxotive": {"label": "INXOTIVE", "archetype": "bold", "vibe": "Modern tech", "colors": ["#6366f1", "#8b5cf6", "#f59e0b"]},
    "healthcare": {"label": "Healthcare", "archetype": "warm", "vibe": "Clean professional", "colors": ["#0D9488", "#134B4A", "#F0FDFA"]},
    "fnb": {"label": "F&B", "archetype": "warm", "vibe": "Warm appetizing", "colors": ["#DC2626", "#EA580C", "#FEF3C7"]},
    "luxury": {"label": "Luxury", "archetype": "editorial", "vibe": "Elegant premium", "colors": ["#1A1A2E", "#C9A94E", "#F5F0E8"]},
    "tech": {"label": "Technology", "archetype": "bold", "vibe": "Modern startup", "colors": ["#2563EB", "#7C3AED", "#F8FAFC"]},
    "corporate": {"label": "Corporate", "archetype": "corporate", "vibe": "Professional B2B", "colors": ["#1E293B", "#475569", "#F1F5F9"]},
    "creative": {"label": "Creative", "archetype": "editorial", "vibe": "Artistic bold", "colors": ["#EC4899", "#F43F5E", "#FDF2F8"]},
    "nature": {"label": "Nature", "archetype": "warm", "vibe": "Organic earthy", "colors": ["#059669", "#047857", "#ECFDF5"]},
    "education": {"label": "Education", "archetype": "corporate", "vibe": "Trustworthy", "colors": ["#3B82F6", "#1D4ED8", "#EFF6FF"]},
    "minimal": {"label": "Minimal", "archetype": "corporate", "vibe": "Clean simple", "colors": ["#333333", "#666666", "#FAFAFA"]},
    "cyberpunk": {"label": "Cyberpunk", "archetype": "bold", "vibe": "Dark edgy", "colors": ["#F706CF", "#00F0FF", "#0D0221"]},
    "fitness": {"label": "Fitness", "archetype": "bold", "vibe": "Energetic", "colors": ["#EF4444", "#F97316", "#FEF2F2"]},
    "wellness": {"label": "Wellness", "archetype": "warm", "vibe": "Calm peaceful", "colors": ["#8B5CF6", "#A78BFA", "#F5F3FF"]},
}

# ── Industry detection ──
INDUSTRY_KEYWORDS = {
    "healthcare": ["klinik", "dokter", "hospital", "medical", "health", "sehat", "rumah sakit"],
    "fnb": ["restoran", "makanan", "cafe", "kafe", "food", "restaurant", "kuliner", "minuman"],
    "tech": ["teknologi", "startup", "saas", "software", "app", "tech", "digital", "ai"],
    "luxury": ["luxury", "mewah", "premium", "eksklusif", "high-end"],
    "education": ["sekolah", "course", "learning", "belajar", "education", "kursus"],
    "fashion": ["fashion", "pakaian", "clothing", "style", "baju"],
    "fitness": ["fitness", "gym", "olahraga", "sport", "yoga"],
    "wellness": ["spa", "wellness", "salon", "beauty", "kecantikan"],
    "corporate": ["perusahaan", "corporate", "company", "bisnis", "business"],
    "creative": ["creative", "kreatif", "art", "seni", "design", "desain", "agency"],
}

# ── Section selection by industry ──
INDUSTRY_SECTIONS = {
    "healthcare": ["hero", "about", "features", "stats", "testimonials", "faq", "cta", "contact", "footer"],
    "fnb": ["hero", "features", "gallery", "testimonials", "pricing", "cta", "contact", "footer"],
    "tech": ["hero", "features", "stats", "testimonials", "pricing", "faq", "cta", "contact", "footer"],
    "luxury": ["hero", "gallery", "features", "testimonials", "pricing", "cta", "contact", "footer"],
    "education": ["hero", "features", "stats", "testimonials", "team", "faq", "cta", "contact", "footer"],
    "fashion": ["hero", "gallery", "features", "testimonials", "pricing", "about", "cta", "contact", "footer"],
    "fitness": ["hero", "features", "stats", "testimonials", "pricing", "team", "cta", "contact", "footer"],
    "wellness": ["hero", "features", "gallery", "testimonials", "pricing", "cta", "contact", "footer"],
    "corporate": ["hero", "about", "features", "stats", "testimonials", "pricing", "team", "cta", "contact", "footer"],
    "creative": ["hero", "gallery", "features", "testimonials", "team", "cta", "contact", "footer"],
}

# Default sections for unknown industries
DEFAULT_SECTIONS = ["hero", "features", "stats", "testimonials", "cta", "contact", "footer"]


class AIOrchestrator:
    """AI Design Orchestrator — connects prompt → structured section spec."""

    def __init__(self):
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt with all available brands, sections, and output format."""
        brands_list = "\n".join([f'  - {k}: {v["label"]} ({v["archetype"]}, {v["vibe"]}, colors: {", ".join(v["colors"])})' for k, v in BRAND_DESCRIPTIONS.items()])
        sections_list = "\n".join([f'  - {k}: variants={v["variants"]}, params={list(v["params"].keys())}' for k, v in SECTION_SCHEMA.items()])

        return f"""You are INXOTIVE AI Design Orchestrator. Your job: turn user descriptions into structured JSON website specs.

AVAILABLE BRANDS (choose one):
{brands_list}

AVAILABLE SECTIONS (choose from these types):
{sections_list}

OUTPUT RULES:
- Respond ONLY with valid JSON, no markdown, no explanation
- Choose sections appropriate for the industry
- Set brand to the closest matching brand DNA
- Fill content fields with professional copy matching the brand tone
- Include ALL sections that make sense for this type of business
- Use Indonesian language for copy if the prompt is in Indonesian
- Make the design choices (brand, sections, variants) based on the prompt description

OUTPUT JSON FORMAT:
{{
  "brand": "brand_name",
  "sections": [
    {{
      "type": "section_type",
      "variant": "variant_name",
      "content": {{
        "field1": "value1",
        ...
      }}
    }}
  ]
}}

IMPORTANT: Respond ONLY with JSON, no other text."""

    def detect_industry(self, prompt: str) -> str:
        """Detect industry from prompt keywords."""
        prompt_lower = prompt.lower()
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                return industry
        return "tech"

    def select_sections(self, industry: str) -> list:
        """Choose appropriate sections for the industry."""
        return INDUSTRY_SECTIONS.get(industry, DEFAULT_SECTIONS)

    def validate_spec(self, spec: dict) -> dict:
        """Validate and fix the spec against schemas."""
        if not spec or "sections" not in spec:
            return spec

        for sec in spec["sections"]:
            stype = sec.get("type", "")
            schema = SECTION_SCHEMA.get(stype)
            if not schema:
                continue
            # Set default variant if invalid
            if sec.get("variant") not in schema["variants"]:
                sec["variant"] = schema["default_variant"]
            # Fill in missing content with defaults
            content = sec.get("content", {})
            for param, config in schema["params"].items():
                if param not in content or content[param] is None:
                    content[param] = config["default"]
            sec["content"] = content

        return spec

    async def generate_spec(self, prompt: str, model: str = "9router-gemini-flash",
                            industry: Optional[str] = None) -> dict:
        """Generate spec from prompt using the appropriate AI model.

        Args:
            prompt: User's design description
            model: Model ID (9router-*, local-*, api-*)
            industry: Optional forced industry override

        Returns:
            dict: Complete section spec ready for assembly
        """
        detected_industry = industry or self.detect_industry(prompt)
        suggested_sections = self.select_sections(detected_industry)

        # Try design_intel.py if available
        try:
            from design_intel import suggest_palette, suggest_font
            palette = suggest_palette(detected_industry, None)
            font = suggest_font(detected_industry, None)
        except ImportError:
            palette = None
            font = None

        # Build the prompt with context
        full_prompt = f"""User request: {prompt}

This is a website for {detected_industry} industry.
Suggested sections: {', '.join(suggested_sections)}

Generate JSON spec for this website."""

        # Call appropriate model
        if model.startswith("local-"):
            spec = await self._call_ollama(full_prompt)
        else:
            spec = await self._call_9router(full_prompt, model)

        if not spec:
            spec = self._fallback_spec(prompt, detected_industry, suggested_sections)

        # Apply design_intel recommendations
        if palette and not spec.get("colors"):
            spec["colors"] = {"primary": palette["primary"], "secondary": palette.get("secondary", palette["primary"]), "accent": palette.get("accent", "#f59e0b")}
        if font and not spec.get("fonts"):
            spec["fonts"] = {"heading": font.get("heading", "Inter"), "body": font.get("body", "Inter")}

        return self.validate_spec(spec)

    def _fallback_spec(self, prompt: str, industry: str, sections: list) -> dict:
        """Generate spec without LLM — keyword-based fallback."""
        # Choose brand
        brand = "inxotive"
        for brand_key, desc in BRAND_DESCRIPTIONS.items():
            if industry in brand_key:
                brand = brand_key
                break
        # Map industry to brand
        industry_brand_map = {
            "healthcare": "healthcare", "fnb": "fnb", "tech": "tech",
            "luxury": "luxury", "education": "education", "fashion": "creative",
            "fitness": "fitness", "wellness": "wellness", "corporate": "corporate",
            "creative": "creative"
        }
        brand = industry_brand_map.get(industry, brand)

        # Extract site name from prompt
        name = prompt.split()[:5]
        name = " ".join(name).title()[:40]

        # Build sections with defaults
        result_sections = []
        for sec_type in sections:
            schema = SECTION_SCHEMA.get(sec_type)
            if not schema:
                continue
            params = {}
            for param, config in schema["params"].items():
                params[param] = config["default"]
            result_sections.append({
                "type": sec_type,
                "variant": schema["default_variant"],
                "content": params
            })

        # Override hero with name from prompt
        for sec in result_sections:
            if sec["type"] == "hero":
                sec["content"]["headline"] = name
            if sec["type"] == "footer":
                sec["content"]["brand"] = name

        return {"brand": brand, "sections": result_sections}

    async def _call_9router(self, prompt: str, model: str) -> Optional[dict]:
        """Call 9Router API."""
        import httpx
        api_key = os.environ.get("NINE_ROUTER_API_KEY", "")
        if not api_key:
            return None

        model_map = {
            "9router-gemini-flash": "google/gemini-2.0-flash-001",
            "9router-nemotron": "nvidia/llama-nemotron-3-ultra",
            "9router-claude": "anthropic/claude-haiku-4-5",
            "9router-deepseek": "deepseek/deepseek-v4",
        }
        api_model = model_map.get(model, "google/gemini-2.0-flash-001")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    "https://9router.com/v1/chat/completions",
                    json={
                        "model": api_model,
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000
                    },
                    headers={"Authorization": f"Bearer {api_key}"}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return self._extract_json(content)
        except Exception:
            return None

    async def _call_ollama(self, prompt: str) -> Optional[dict]:
        """Call Ollama VPS (fallback)."""
        import httpx
        endpoints = ["http://100.78.79.60:11434", "http://localhost:11434"]

        for endpoint in endpoints:
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.post(f"{endpoint}/api/chat", json={
                        "model": "qwen2.5:7b",
                        "messages": [
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "stream": False,
                        "options": {"temperature": 0.2}
                    })
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data["message"]["content"]
                        return self._extract_json(content)
            except Exception:
                continue
        return None

    def _extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from LLM response."""
        # Try direct parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        # Try extracting from code block
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        # Try finding JSON object
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return None


# Convenience function
async def orchestrate(prompt: str, model: str = "9router-gemini-flash", industry: Optional[str] = None) -> dict:
    """One-shot: prompt → section spec ready for assembly."""
    orchestrator = AIOrchestrator()
    return await orchestrator.generate_spec(prompt, model, industry)
