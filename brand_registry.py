"""
INXOTIVE Brand Registry — Single Source of Truth
=================================================
Menggabungkan 3 sumber brand:
1. css_framework.BRAND_PRESETS (13 brand, full design tokens)
2. design_tokens.BRAND_* (10 brand, Brand class)
3. getdesign_brands.GETDESIGN_BRANDS (62 brand, getdesign.md)

Termasuk: archetype mapping, industry mapping, section variants per brand.
"""

from typing import Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path


# ── Core Brand Definition ──
@dataclass
class Brand:
    """Unified brand definition."""
    slug: str
    name: str
    primary: str = "#6366f1"
    secondary: str = "#8b5cf6"
    accent: str = "#f59e0b"
    archetype: str = "corporate"  # bold | warm | corporate | editorial
    industry: str = "general"
    fonts: dict = field(default_factory=lambda: {
        "display": "'Plus Jakarta Sans', sans-serif",
        "body": "'Inter', sans-serif",
        "mono": "'JetBrains Mono', monospace",
    })
    colors: dict = field(default_factory=lambda: {})
    dark_mode: bool = True
    source: str = "builtin"

    def to_css_vars(self) -> str:
        """Generate CSS custom properties string."""
        css = f"""
--brand-primary: {self.primary};
--brand-secondary: {self.secondary};
--brand-accent: {self.accent};
--brand-gradient: linear-gradient(135deg, {self.primary}, {self.accent});
--font-display: {self.fonts['display']};
--font-body: {self.fonts['body']};
--font-mono: {self.fonts['mono']};
"""
        if self.colors:
            for k, v in self.colors.items():
                if k not in ('primary', 'secondary', 'accent'):
                    css += f"--{k}: {v};\n"
        return css


# ── 13 Built-in Brand Presets (combined + enriched) ──
BUILTIN_BRANDS = {
    "inxotive": Brand("inxotive", "INXOTIVE", "#4F46E5", "#6366F1", "#F59E0B", "bold", "tech",
        {"display": "'Clash Display', sans-serif", "body": "'Inter', sans-serif"}),
    "tech": Brand("tech", "TechStart", "#2563EB", "#3B82F6", "#8B5CF6", "bold", "tech"),
    "healthcare": Brand("healthcare", "Healthcare", "#0D9488", "#134B4A", "#F0FDFA", "warm", "healthcare",
        {"display": "'Plus Jakarta Sans', sans-serif", "body": "'Source Sans 3', sans-serif"}),
    "fnb": Brand("fnb", "F&B", "#DC2626", "#EA580C", "#FEF3C7", "warm", "fnb",
        {"display": "'Playfair Display', serif", "body": "'Plus Jakarta Sans', sans-serif"}),
    "luxury": Brand("luxury", "Luxury", "#1A1A2E", "#C9A94E", "#F5F0E8", "editorial", "luxury",
        {"display": "'Playfair Display', serif", "body": "'Cormorant Garamond', serif"}),
    "education": Brand("education", "Edukasi", "#3B82F6", "#1D4ED8", "#EFF6FF", "corporate", "education",
        {"display": "'Plus Jakarta Sans', sans-serif", "body": "'Outfit', sans-serif"}),
    "fashion": Brand("fashion", "Fashion", "#EC4899", "#F43F5E", "#FDF2F8", "editorial", "fashion"),
    "creative": Brand("creative", "Creative", "#EC4899", "#F43F5E", "#FDF2F8", "editorial", "creative",
        {"display": "'Outfit', sans-serif", "body": "'Sora', sans-serif"}),
    "corporate": Brand("corporate", "Corporate", "#1E293B", "#475569", "#F1F5F9", "corporate", "corporate",
        {"display": "'Inter', sans-serif", "body": "'Source Sans 3', sans-serif"}),
    "minimal": Brand("minimal", "Minimal", "#333333", "#666666", "#FAFAFA", "corporate", "general",
        {"display": "'Inter', sans-serif", "body": "'DM Sans', sans-serif"}),
    "nature": Brand("nature", "Nature", "#059669", "#047857", "#ECFDF5", "warm", "wellness",
        {"display": "'Libre Caslon', serif", "body": "'Source Sans 3', sans-serif"}),
    "cyberpunk": Brand("cyberpunk", "Cyberpunk", "#F706CF", "#00F0FF", "#0D0221", "bold", "tech"),
    "fitness": Brand("fitness", "Fitness", "#EF4444", "#F97316", "#FEF2F2", "bold", "fitness",
        {"display": "'Space Grotesk', sans-serif", "body": "'Inter', sans-serif"}),
    "wellness": Brand("wellness", "Wellness Spa", "#8B5CF6", "#A78BFA", "#F5F3FF", "warm", "wellness"),
    "klinik": Brand("klinik", "Klinik", "#0D9488", "#134B4A", "#CCFBF1", "warm", "healthcare"),
    "restaurant": Brand("restaurant", "Restaurant", "#DC2626", "#B91C1C", "#FEE2E2", "warm", "fnb"),
}

# ── Archetype definitions with section order, spacing, defaults ──
ARCHETYPES = {
    "editorial": {
        "name": "Editorial / Luxury",
        "section_order": ["hero", "about", "features", "stats", "testimonials", "pricing", "faq", "cta", "contact", "gallery", "team", "footer"],
        "default_align": "left",
        "hero_layout": "split",
        "feature_layout": "zigzag",
        "density_scale": 1.2,
        "radius": "sm",
        "radius_card": "md",
        "shadow_style": "subtle",
        "motion_level": "subtle",
        "font_pair": "Playfair Display + Inter",
    },
    "bold": {
        "name": "Bold / Tech",
        "section_order": ["hero", "stats", "features", "about", "testimonials", "gallery", "pricing", "cta", "faq", "contact", "footer"],
        "default_align": "center",
        "hero_layout": "centered",
        "feature_layout": "grid-3",
        "density_scale": 0.85,
        "radius": "md",
        "radius_card": "lg",
        "shadow_style": "bold",
        "motion_level": "high",
        "font_pair": "Space Grotesk + Inter",
    },
    "warm": {
        "name": "Warm / Organic",
        "section_order": ["hero", "about", "features", "stats", "testimonials", "pricing", "faq", "cta", "contact", "footer"],
        "default_align": "left",
        "hero_layout": "split",
        "feature_layout": "showcase",
        "density_scale": 1.0,
        "radius": "lg",
        "radius_card": "xl",
        "shadow_style": "warm",
        "motion_level": "medium",
        "font_pair": "Playfair Display + Jakarta Sans",
    },
    "corporate": {
        "name": "Corporate / Trust",
        "section_order": ["hero", "about", "features", "stats", "testimonials", "team", "pricing", "cta", "faq", "contact", "footer"],
        "default_align": "center",
        "hero_layout": "split",
        "feature_layout": "grid-3",
        "density_scale": 1.0,
        "radius": "sm",
        "radius_card": "md",
        "shadow_style": "subtle",
        "motion_level": "low",
        "font_pair": "Inter + Source Sans 3",
    },
}

# ── Section variants available per type ──
SECTION_VARIANTS = {
    "hero": ["split", "centered", "gradient", "full-bleed", "video"],
    "features": ["grid-3", "grid-4", "zigzag", "showcase", "icon-grid"],
    "stats": ["default", "grid-4"],
    "testimonials": ["default", "carousel", "grid"],
    "pricing": ["default", "compact", "side-by-side"],
    "about": ["standard", "right-image", "split"],
    "team": ["default", "grid"],
    "faq": ["default"],
    "cta": ["default", "compact", "newsletter"],
    "contact": ["default"],
    "gallery": ["default", "masonry", "grid"],
    "footer": ["default", "compact"],
    "divider": ["wave", "default"],
}


# ── Registry ──
class BrandRegistry:
    """Unified brand registry — single source of truth."""

    def __init__(self):
        self._brands: dict[str, Brand] = {}
        self._load_builtin()
        self._try_load_getdesign()

    def _load_builtin(self):
        for slug, brand in BUILTIN_BRANDS.items():
            self._brands[slug] = brand

    def _try_load_getdesign(self):
        """Try to load 62 getdesign brands if available.
        Graceful fallback if file doesn't exist (e.g. VPS without market-api)."""
        try:
            import sys
            for p in [
                str(Path.home() / "inxotive-builder"),
                str(Path("/opt/inxotive/builder")),
                str(Path("/opt/market-api")),
            ]:
                if Path(p).exists():
                    sys.path.insert(0, p)
            from getdesign_brands import GETDESIGN_BRANDS
            for slug, data in GETDESIGN_BRANDS.items():
                if slug not in self._brands:
                    primary = data.get("primary", data.get("colors", {}).get("primary", "#6366f1"))
                    secondary = data.get("secondary", data.get("colors", {}).get("secondary", "#8b5cf6"))
                    accent = data.get("accent", data.get("colors", {}).get("accent", "#f59e0b"))
                    self._brands[slug] = Brand(
                        slug=slug,
                        name=data.get("name", slug.title()),
                        primary=primary,
                        secondary=secondary,
                        accent=accent,
                        archetype=self._get_archetype(slug),
                        source="getdesign"
                    )
        except (ImportError, KeyError):
            pass

    def _get_archetype(self, slug: str) -> str:
        """Determine archetype from slug."""
        slug_lower = slug.lower()
        if any(w in slug_lower for w in ['luxury', 'premium', 'editorial', 'fashion', 'creative', 'apple', 'nike', 'figma']):
            return "editorial"
        if any(w in slug_lower for w in ['tech', 'startup', 'bold', 'cyber', 'saas', 'ai', 'cloud', 'space', 'vercel', 'stripe', 'linear']):
            return "bold"
        if any(w in slug_lower for w in ['warm', 'organic', 'nature', 'food', 'restaurant', 'health', 'wellness', 'spa', 'garden']):
            return "warm"
        return "corporate"

    def get(self, slug: str) -> Optional[Brand]:
        """Get brand by slug."""
        return self._brands.get(slug)

    def list_brands(self) -> list[dict]:
        """List all brands with metadata."""
        return [{
            "slug": slug,
            "name": brand.name,
            "primary": brand.primary,
            "secondary": brand.secondary,
            "accent": brand.accent,
            "archetype": brand.archetype,
            "industry": brand.industry,
            "source": brand.source,
        } for slug, brand in self._brands.items()]

    def get_archetype(self, slug: str) -> str:
        """Get archetype for a brand."""
        brand = self._brands.get(slug)
        return brand.archetype if brand else "corporate"

    def get_archetype_config(self, slug: str) -> dict:
        """Get full archetype configuration."""
        archetype_key = self.get_archetype(slug)
        return ARCHETYPES.get(archetype_key, ARCHETYPES["corporate"])

    def get_colors(self, slug: str) -> dict:
        """Get brand colors."""
        brand = self._brands.get(slug)
        if not brand:
            return {"primary": "#6366f1", "secondary": "#8b5cf6", "accent": "#f59e0b"}
        return {"primary": brand.primary, "secondary": brand.secondary, "accent": brand.accent}

    def get_section_variants(self, section_type: str) -> list:
        """Get available variants for a section type."""
        return SECTION_VARIANTS.get(section_type, ["default"])

    def __len__(self):
        return len(self._brands)


# ── Global singleton ──
_registry: Optional[BrandRegistry] = None

def get_registry() -> BrandRegistry:
    global _registry
    if _registry is None:
        _registry = BrandRegistry()
    return _registry

# ── Convenience functions (matching old API) ──
def list_brands() -> list[dict]:
    return get_registry().list_brands()

def resolve_brand(slug: str) -> Optional[Brand]:
    return get_registry().get(slug)

def get_archetype(slug: str) -> str:
    return get_registry().get_archetype(slug)

def get_archetype_config(slug: str) -> dict:
    return get_registry().get_archetype_config(slug)

def get_section_variants(section_type: str) -> list:
    return SECTION_VARIANTS.get(section_type, ["default"])
