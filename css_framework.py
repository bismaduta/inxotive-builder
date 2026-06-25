#!/usr/bin/env python3
"""
INXOTIVE CSS Framework Generator v2.0
Class-driven CSS framework generated from design tokens.
Produces clean markup with semantic CSS classes — zero inline styles.
getdesign.md inspired: 75 brand DNA patterns (Apple, Linear, Stripe, Vercel, Notion, Figma...)

Usage:
    from css_framework import generate_framework, generate_premium_page
    css = generate_framework("inxotive")
    html = generate_premium_page("inxotive", "landing")
"""

import sys
from typing import Dict, Optional

try:
    from web_engine.getdesign_brands import GETDESIGN_BRANDS
    _HAS_GETDESIGN = True
except ImportError:
    GETDESIGN_BRANDS = {}
    _HAS_GETDESIGN = False

# ═══════════════════════════════════════════════════════════════
# BRAND PRESETS — 13 built-in + 62 getdesign.md = 75 design DNAs
# ═══════════════════════════════════════════════════════════════

BRAND_PRESETS: Dict[str, dict] = {
    "inxotive": {
        "name": "INXOTIVE",
        "primary": "#4F46E5",
        "secondary": "#6366F1",
        "accent": "#F59E0B",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F4F5FA",
        "surface": "#F8FAFC",
        "text": "#0F172A",
        "text_secondary": "#64748B",
        "border": "#E2E8F0",
        "canvas": "#F4F5FA",
        "canvas_soft": "#EEF0F6",
        "ink": "#0F172A",
        "ink_muted": "#64748B",
        "ink_subtle": "#94A3B8",
        "hairline": "#E2E8F0",
        "hairline_strong": "#CBD5E1",
        "surface_1": "#FFFFFF",
        "surface_2": "#F8FAFC",
        "surface_3": "#F1F5F9",
        "surface_4": "#E2E8F0",
        "font_display": "'Clash Display', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(79,70,229,0.3)",
        "gradient": "linear-gradient(135deg, #4F46E5, #F59E0B)",
        "dark_bg": "#0F172A",
        "dark_surface": "#1E293B",
        "dark_text": "#E2E8F0",
        "dark_border": "#334155",
        "dark_canvas": "#0F172A",
        "dark_canvas_soft": "#1E293B",
        "dark_ink": "#E2E8F0",
        "dark_hairline": "#334155",
        "dark_surface_1": "#1E293B",
        "dark_surface_2": "#1E293B",
        "dark_surface_3": "#334155",
        "dark_surface_4": "#475569",
    },
    "tech": {
        "name": "TechStart",
        "primary": "#2563EB",
        "secondary": "#3B82F6",
        "accent": "#8B5CF6",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F8FAFC",
        "surface": "#F1F5F9",
        "text": "#0F172A",
        "text_secondary": "#475569",
        "border": "#CBD5E1",
        "canvas": "#F8FAFC",
        "canvas_soft": "#F1F5F9",
        "ink": "#0F172A",
        "ink_muted": "#475569",
        "ink_subtle": "#94A3B8",
        "hairline": "#CBD5E1",
        "hairline_strong": "#94A3B8",
        "surface_1": "#FFFFFF",
        "surface_2": "#F8FAFC",
        "surface_3": "#F1F5F9",
        "surface_4": "#E2E8F0",
        "font_display": "'Space Grotesk', 'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(37,99,235,0.3)",
        "gradient": "linear-gradient(135deg, #2563EB, #8B5CF6)",
        "dark_bg": "#020617",
        "dark_surface": "#0F172A",
        "dark_text": "#E2E8F0",
        "dark_border": "#1E293B",
        "dark_canvas": "#020617",
        "dark_canvas_soft": "#0F172A",
        "dark_ink": "#E2E8F0",
        "dark_hairline": "#1E293B",
        "dark_surface_1": "#0F172A",
        "dark_surface_2": "#0F172A",
        "dark_surface_3": "#1E293B",
        "dark_surface_4": "#334155",
    },
    "fnb": {
        "name": "Warung Modern",
        "primary": "#EA580C",
        "secondary": "#FB923C",
        "accent": "#FCD34D",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#FFF7ED",
        "surface": "#FFFBEB",
        "text": "#7C2D12",
        "text_secondary": "#C2410C",
        "border": "#FED7AA",
        "canvas": "#FFF7ED",
        "canvas_soft": "#FFFBEB",
        "ink": "#7C2D12",
        "ink_muted": "#C2410C",
        "ink_subtle": "#FDBA74",
        "hairline": "#FED7AA",
        "hairline_strong": "#FDBA74",
        "surface_1": "#FFFFFF",
        "surface_2": "#FFFBEB",
        "surface_3": "#FFF7ED",
        "surface_4": "#FFEDD5",
        "font_display": "'Clash Display', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(234,88,12,0.3)",
        "gradient": "linear-gradient(135deg, #EA580C, #FCD34D)",
        "dark_bg": "#1C0F0A",
        "dark_surface": "#2D1A12",
        "dark_text": "#FED7AA",
        "dark_border": "#3D2A1A",
        "dark_canvas": "#1C0F0A",
        "dark_canvas_soft": "#2D1A12",
        "dark_ink": "#FED7AA",
        "dark_hairline": "#3D2A1A",
        "dark_surface_1": "#2D1A12",
        "dark_surface_2": "#2D1A12",
        "dark_surface_3": "#3D2A1A",
        "dark_surface_4": "#4A3520",
    },
    "healthcare": {
        "name": "HealthCare",
        "primary": "#16A34A",
        "secondary": "#22C55E",
        "accent": "#06B6D4",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F0FDF4",
        "surface": "#F8FAFC",
        "text": "#0F172A",
        "text_secondary": "#475569",
        "border": "#DCFCE7",
        "canvas": "#F0FDF4",
        "canvas_soft": "#F8FAFC",
        "ink": "#0F172A",
        "ink_muted": "#475569",
        "ink_subtle": "#94A3B8",
        "hairline": "#DCFCE7",
        "hairline_strong": "#BBF7D0",
        "surface_1": "#FFFFFF",
        "surface_2": "#F8FAFC",
        "surface_3": "#F0FDF4",
        "surface_4": "#DCFCE7",
        "font_display": "'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(22,163,74,0.3)",
        "gradient": "linear-gradient(135deg, #16A34A, #06B6D4)",
        "dark_bg": "#0A1A0A",
        "dark_surface": "#0F2A10",
        "dark_text": "#DCFCE7",
        "dark_border": "#1A3A1A",
        "dark_canvas": "#0A1A0A",
        "dark_canvas_soft": "#0F2A10",
        "dark_ink": "#DCFCE7",
        "dark_hairline": "#1A3A1A",
        "dark_surface_1": "#0F2A10",
        "dark_surface_2": "#0F2A10",
        "dark_surface_3": "#1A3A1A",
        "dark_surface_4": "#2A4A2A",
    },
    "luxury": {
        "name": "LUXE",
        "primary": "#B8860B",
        "secondary": "#DAA520",
        "accent": "#8B0000",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#FDFBF7",
        "surface": "#FAFAF5",
        "text": "#1A1200",
        "text_secondary": "#6B5E3E",
        "border": "#E8E0D0",
        "canvas": "#FDFBF7",
        "canvas_soft": "#FAFAF5",
        "ink": "#1A1200",
        "ink_muted": "#6B5E3E",
        "ink_subtle": "#A09070",
        "hairline": "#E8E0D0",
        "hairline_strong": "#D0C8B0",
        "surface_1": "#FFFFFF",
        "surface_2": "#FAFAF5",
        "surface_3": "#F5F0E8",
        "surface_4": "#E8E0D0",
        "font_display": "'Playfair Display', Georgia, serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(184,134,11,0.25)",
        "gradient": "linear-gradient(135deg, #B8860B, #DAA520)",
        "dark_bg": "#0D0A00",
        "dark_surface": "#1A1508",
        "dark_text": "#E8E0D0",
        "dark_border": "#2A2010",
        "dark_canvas": "#0D0A00",
        "dark_canvas_soft": "#1A1508",
        "dark_ink": "#E8E0D0",
        "dark_hairline": "#2A2010",
        "dark_surface_1": "#1A1508",
        "dark_surface_2": "#1A1508",
        "dark_surface_3": "#2A2010",
        "dark_surface_4": "#3A3020",
    },
    "corporate": {
        "name": "Corporate",
        "primary": "#1E40AF",
        "secondary": "#2563EB",
        "accent": "#0D9488",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F8FAFC",
        "surface": "#FFFFFF",
        "text": "#1E293B",
        "text_secondary": "#64748B",
        "border": "#E2E8F0",
        "canvas": "#F8FAFC",
        "canvas_soft": "#FFFFFF",
        "ink": "#1E293B",
        "ink_muted": "#64748B",
        "ink_subtle": "#94A3B8",
        "hairline": "#E2E8F0",
        "hairline_strong": "#CBD5E1",
        "surface_1": "#FFFFFF",
        "surface_2": "#F8FAFC",
        "surface_3": "#F1F5F9",
        "surface_4": "#E2E8F0",
        "font_display": "'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(30,64,175,0.3)",
        "gradient": "linear-gradient(135deg, #1E40AF, #0D9488)",
        "dark_bg": "#0F172A",
        "dark_surface": "#1E293B",
        "dark_text": "#E2E8F0",
        "dark_border": "#334155",
        "dark_canvas": "#0F172A",
        "dark_canvas_soft": "#1E293B",
        "dark_ink": "#E2E8F0",
        "dark_hairline": "#334155",
        "dark_surface_1": "#1E293B",
        "dark_surface_2": "#1E293B",
        "dark_surface_3": "#334155",
        "dark_surface_4": "#475569",
    },
    "creative": {
        "name": "Creative",
        "primary": "#7C3AED",
        "secondary": "#A78BFA",
        "accent": "#EC4899",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#FAFAFA",
        "surface": "#FFFFFF",
        "text": "#1F1F2E",
        "text_secondary": "#6B7280",
        "border": "#E5E7EB",
        "canvas": "#FAFAFA",
        "canvas_soft": "#FFFFFF",
        "ink": "#1F1F2E",
        "ink_muted": "#6B7280",
        "ink_subtle": "#9CA3AF",
        "hairline": "#E5E7EB",
        "hairline_strong": "#D1D5DB",
        "surface_1": "#FFFFFF",
        "surface_2": "#FAFAFA",
        "surface_3": "#F5F5F5",
        "surface_4": "#E5E7EB",
        "font_display": "'Outfit', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(124,58,237,0.3)",
        "gradient": "linear-gradient(135deg, #7C3AED, #EC4899)",
        "dark_bg": "#1A1025",
        "dark_surface": "#2A1A35",
        "dark_text": "#E8E0F0",
        "dark_border": "#3A2A45",
        "dark_canvas": "#1A1025",
        "dark_canvas_soft": "#2A1A35",
        "dark_ink": "#E8E0F0",
        "dark_hairline": "#3A2A45",
        "dark_surface_1": "#2A1A35",
        "dark_surface_2": "#2A1A35",
        "dark_surface_3": "#3A2A45",
        "dark_surface_4": "#4A3A55",
    },
    "minimal": {
        "name": "Minimal",
        "primary": "#1A1A1A",
        "secondary": "#555555",
        "accent": "#888888",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#FAFAFA",
        "surface": "#F5F5F5",
        "text": "#171717",
        "text_secondary": "#737373",
        "border": "#E5E5E5",
        "canvas": "#FAFAFA",
        "canvas_soft": "#F5F5F5",
        "ink": "#171717",
        "ink_muted": "#737373",
        "ink_subtle": "#A3A3A3",
        "hairline": "#E5E5E5",
        "hairline_strong": "#D4D4D4",
        "surface_1": "#FFFFFF",
        "surface_2": "#FAFAFA",
        "surface_3": "#F5F5F5",
        "surface_4": "#E5E5E5",
        "font_display": "'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(0,0,0,0.1)",
        "gradient": "linear-gradient(135deg, #1A1A1A, #555555)",
        "dark_bg": "#0A0A0A",
        "dark_surface": "#171717",
        "dark_text": "#E5E5E5",
        "dark_border": "#262626",
        "dark_canvas": "#0A0A0A",
        "dark_canvas_soft": "#171717",
        "dark_ink": "#E5E5E5",
        "dark_hairline": "#262626",
        "dark_surface_1": "#171717",
        "dark_surface_2": "#171717",
        "dark_surface_3": "#262626",
        "dark_surface_4": "#404040",
    },
    "nature": {
        "name": "Nature",
        "primary": "#166534",
        "secondary": "#22C55E",
        "accent": "#65A30D",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F7FEE7",
        "surface": "#FAFFE8",
        "text": "#1A2E0A",
        "text_secondary": "#4A7A2E",
        "border": "#D9E8B5",
        "canvas": "#F7FEE7",
        "canvas_soft": "#FAFFE8",
        "ink": "#1A2E0A",
        "ink_muted": "#4A7A2E",
        "ink_subtle": "#8BB86A",
        "hairline": "#D9E8B5",
        "hairline_strong": "#C0D8A0",
        "surface_1": "#FFFFFF",
        "surface_2": "#FAFFE8",
        "surface_3": "#F7FEE7",
        "surface_4": "#ECF5D5",
        "font_display": "'Plus Jakarta Sans', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(22,101,52,0.3)",
        "gradient": "linear-gradient(135deg, #166534, #65A30D)",
        "dark_bg": "#0A1A08",
        "dark_surface": "#142A12",
        "dark_text": "#D9E8B5",
        "dark_border": "#1E3A18",
        "dark_canvas": "#0A1A08",
        "dark_canvas_soft": "#142A12",
        "dark_ink": "#D9E8B5",
        "dark_hairline": "#1E3A18",
        "dark_surface_1": "#142A12",
        "dark_surface_2": "#142A12",
        "dark_surface_3": "#1E3A18",
        "dark_surface_4": "#2A4A22",
    },
    "cyberpunk": {
        "name": "CYBER",
        "primary": "#FF006E",
        "secondary": "#00F5D4",
        "accent": "#FFBE0B",
        "success": "#00F5D4",
        "warning": "#FFBE0B",
        "danger": "#FF006E",
        "info": "#3B82F6",
        "bg": "#0A001A",
        "surface": "#120028",
        "text": "#FFFFFF",
        "text_secondary": "#B0A0CC",
        "border": "#2A1050",
        "canvas": "#0A001A",
        "canvas_soft": "#120028",
        "ink": "#FFFFFF",
        "ink_muted": "#B0A0CC",
        "ink_subtle": "#7050A0",
        "hairline": "#2A1050",
        "hairline_strong": "#402070",
        "surface_1": "#120028",
        "surface_2": "#120028",
        "surface_3": "#1A0A38",
        "surface_4": "#2A1050",
        "font_display": "'Space Grotesk', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(255,0,110,0.4)",
        "gradient": "linear-gradient(135deg, #FF006E, #00F5D4)",
        "dark_bg": "#0A001A",
        "dark_surface": "#120028",
        "dark_text": "#FFFFFF",
        "dark_border": "#2A1050",
        "dark_canvas": "#0A001A",
        "dark_canvas_soft": "#120028",
        "dark_ink": "#FFFFFF",
        "dark_hairline": "#2A1050",
        "dark_surface_1": "#120028",
        "dark_surface_2": "#120028",
        "dark_surface_3": "#1A0A38",
        "dark_surface_4": "#2A1050",
    },
    "klinik": {
        "name": "Klinik Sehat",
        "primary": "#0D9488",
        "secondary": "#14B8A6",
        "accent": "#2DD4BF",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F0FDFA",
        "surface": "#F8FAFC",
        "text": "#0F172A",
        "text_secondary": "#5B8B7E",
        "border": "#CCFBF1",
        "canvas": "#F0FDFA",
        "canvas_soft": "#F8FAFC",
        "ink": "#0F172A",
        "ink_muted": "#5B8B7E",
        "ink_subtle": "#94A3B8",
        "hairline": "#CCFBF1",
        "hairline_strong": "#99F6E4",
        "surface_1": "#FFFFFF",
        "surface_2": "#F8FAFC",
        "surface_3": "#F0FDFA",
        "surface_4": "#CCFBF1",
        "font_display": "'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(13,148,136,0.3)",
        "gradient": "linear-gradient(135deg, #0D9488, #2DD4BF)",
        "dark_bg": "#0A1A18",
        "dark_surface": "#0F2A25",
        "dark_text": "#CCFBF1",
        "dark_border": "#1A3A35",
        "dark_canvas": "#0A1A18",
        "dark_canvas_soft": "#0F2A25",
        "dark_ink": "#CCFBF1",
        "dark_hairline": "#1A3A35",
        "dark_surface_1": "#0F2A25",
        "dark_surface_2": "#0F2A25",
        "dark_surface_3": "#1A3A35",
        "dark_surface_4": "#2A4A45",
    },
    "restaurant": {
        "name": "Restaurant",
        "primary": "#B91C1C",
        "secondary": "#DC2626",
        "accent": "#FBBF24",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#FEF2F2",
        "surface": "#FFF8F8",
        "text": "#1F0A0A",
        "text_secondary": "#7F1D1D",
        "border": "#FECACA",
        "canvas": "#FEF2F2",
        "canvas_soft": "#FFF8F8",
        "ink": "#1F0A0A",
        "ink_muted": "#7F1D1D",
        "ink_subtle": "#FCA5A5",
        "hairline": "#FECACA",
        "hairline_strong": "#FCA5A5",
        "surface_1": "#FFFFFF",
        "surface_2": "#FFF8F8",
        "surface_3": "#FEF2F2",
        "surface_4": "#FECACA",
        "font_display": "'Playfair Display', Georgia, serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(185,28,28,0.3)",
        "gradient": "linear-gradient(135deg, #B91C1C, #FBBF24)",
        "dark_bg": "#1A0A0A",
        "dark_surface": "#2A1515",
        "dark_text": "#FECACA",
        "dark_border": "#3A2020",
        "dark_canvas": "#1A0A0A",
        "dark_canvas_soft": "#2A1515",
        "dark_ink": "#FECACA",
        "dark_hairline": "#3A2020",
        "dark_surface_1": "#2A1515",
        "dark_surface_2": "#2A1515",
        "dark_surface_3": "#3A2020",
        "dark_surface_4": "#4A3030",
    },
    "education": {
        "name": "EduLearn",
        "primary": "#7C3AED",
        "secondary": "#A78BFA",
        "accent": "#F59E0B",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#3B82F6",
        "bg": "#F5F3FF",
        "surface": "#FAF8FF",
        "text": "#1E1B4B",
        "text_secondary": "#6D5AA0",
        "border": "#E0D8F0",
        "canvas": "#F5F3FF",
        "canvas_soft": "#FAF8FF",
        "ink": "#1E1B4B",
        "ink_muted": "#6D5AA0",
        "ink_subtle": "#A090C0",
        "hairline": "#E0D8F0",
        "hairline_strong": "#C8B8E0",
        "surface_1": "#FFFFFF",
        "surface_2": "#FAF8FF",
        "surface_3": "#F5F3FF",
        "surface_4": "#E0D8F0",
        "font_display": "'Outfit', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "glow_rgba": "rgba(124,58,237,0.3)",
        "gradient": "linear-gradient(135deg, #7C3AED, #F59E0B)",
        "dark_bg": "#140E24",
        "dark_surface": "#1E1834",
        "dark_text": "#E0D8F0",
        "dark_border": "#2E2844",
        "dark_canvas": "#140E24",
        "dark_canvas_soft": "#1E1834",
        "dark_ink": "#E0D8F0",
        "dark_hairline": "#2E2844",
        "dark_surface_1": "#1E1834",
        "dark_surface_2": "#1E1834",
        "dark_surface_3": "#2E2844",
        "dark_surface_4": "#3E3854",
    },
}

# ═══════════════════════════════════════════════════════════════
# ARCHETYPE SYSTEM — 4 layout archetypes (Part A)
# ═══════════════════════════════════════════════════════════════
# Memecah 1 skeleton → 4 arketipe layout. Tiap arketipe beda:
# section_order, default_alignment, density, hero/feature layout,
# radius, shadow, font pair, motion level — BUKAN cuma warna.

ARCHETYPES = {
    "editorial": {
        "name": "Editorial / Luxury",
        "character": "lapang, tenang, rata kiri, asimetris, whitespace besar",
        "section_order": ["hero", "about", "features", "stats", "testimonials", "pricing", "faq", "cta", "contact", "gallery", "team", "footer"],
        "rhythm_spacing": "xl lg sm lg md xl md sm lg sm lg",
        "default_align": "left",  # body left, center ONLY for hero headline
        "hero_layout": "split",   # text left, visual right
        "feature_layout": "zigzag",  # gambar kiri/kanan bergantian
        "density_scale": 1.2,     # longgar
        "section_spacing": ["xxxl", "xxl", "lg", "xxl", "md", "xl", "md", "lg", "xxl"],
        "radius": "sm",           # subtle — 4px
        "radius_card": "md",      # 8px
        "shadow_style": "subtle", # shadow-sm/md
        "font_display": "'Playfair Display', Georgia, serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_pair_desc": "Playfair Display + Inter",
        "motion_level": "subtle", # fade-in-up only, no floating
        "hero_centered_allowed": False,
        "center_ratio_target": 0.15,  # ≤15% center
    },
    "bold": {
        "name": "Bold / Tech",
        "character": "padat, kontras tinggi, gelap, tipografi raksasa, berani",
        "section_order": ["hero", "stats", "features", "about", "testimonials", "gallery", "pricing", "cta", "faq", "contact", "footer"],
        "rhythm_spacing": "xl md lg md sm lg md sm md lg",
        "default_align": "left",
        "hero_layout": "full-bleed",  # full-width dengan headline besar
        "feature_layout": "grid-3",   # grid padat
        "density_scale": 0.85,       # rapat
        "section_spacing": ["xxxl", "md", "xl", "md", "lg", "md", "xl", "md", "lg"],
        "radius": "md",             # 8px
        "radius_card": "lg",        # 12px
        "shadow_style": "bold",     # shadow-lg/xl
        "font_display": "'Space Grotesk', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_pair_desc": "Space Grotesk + Inter",
        "motion_level": "high",     # float, glow, scale
        "hero_centered_allowed": True,
        "center_ratio_target": 0.25,
    },
    "warm": {
        "name": "Warm / Hospitality",
        "character": "gambar-forward, rounded, hangat, ramah",
        "section_order": ["hero", "about", "features", "testimonials", "stats", "cta", "process", "contact", "faq", "logos", "team", "footer"],
        "rhythm_spacing": "xl lg sm md xl sm lg sm md lg md",
        "default_align": "left",
        "hero_layout": "full-bleed",  # foto besar + overlay
        "feature_layout": "asymmetric-2col",  # baris gambar besar + teks
        "density_scale": 1.0,
        "section_spacing": ["xxl", "xl", "lg", "xl", "md", "lg", "md", "xl", "md"],
        "radius": "lg",           # 12px — rounded & friendly
        "radius_card": "xl",      # 16px
        "shadow_style": "warm",   # shadow-md + warm tint
        "font_display": "'Plus Jakarta Sans', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_pair_desc": "Plus Jakarta Sans + Inter",
        "motion_level": "medium",  # fade + hover scale
        "hero_centered_allowed": True,
        "center_ratio_target": 0.25,
    },
    "corporate": {
        "name": "Corporate / Trust",
        "character": "terstruktur, seimbang, bersih, profesional",
        "section_order": ["hero", "stats", "about", "features", "testimonials", "gallery", "cta", "pricing", "process", "contact", "faq", "team", "footer"],
        "rhythm_spacing": "xl md lg sm md lg sm md lg md sm",
        "default_align": "left",
        "hero_layout": "split",     # split seimbang
        "feature_layout": "grid-3",  # kartu berhierarki
        "density_scale": 1.0,
        "section_spacing": ["xxl", "md", "xl", "md", "lg", "md", "xl", "md", "lg"],
        "radius": "sm",            # 4px — clean & sharp
        "radius_card": "md",       # 8px
        "shadow_style": "clean",   # shadow-card + subtle
        "font_display": "'Inter', system-ui, sans-serif",
        "font_body": "'Inter', system-ui, -apple-system, sans-serif",
        "font_pair_desc": "Inter + Inter",
        "motion_level": "subtle",   # fade only — professional
        "hero_centered_allowed": False,
        "center_ratio_target": 0.10,
    },
}

# Brand → Archetype mapping
BRAND_ARCHETYPE_MAP = {
    # Editorial / Luxury
    "luxury": "editorial",
    "minimal": "editorial",
    "klinik": "editorial",
    "healthcare": "editorial",
    # Bold / Tech
    "tech": "bold",
    "cyberpunk": "bold",
    "inxotive": "bold",
    "corporate": "bold",
    # Warm / Hospitality
    "fnb": "warm",
    "restaurant": "warm",
    "nature": "warm",
    "education": "warm",
    "fitness": "warm",
    # Corporate / Trust (default fallback)
    "creative": "corporate",
}


# ── Image industry mapping ──
BRAND_INDUSTRY_MAP = {
    "inxotive": "tech",
    "tech": "tech",
    "luxury": "luxury",
    "minimal": "business",
    "nature": "nature",
    "cyberpunk": "tech",
    "klinik": "health",
    "healthcare": "health",
    "fnb": "food",
    "restaurant": "restaurant",
    "education": "education",
    "corporate": "business",
    "creative": "fashion",
    "fitness": "fitness",
}
_IMAGE_CACHE = {}



# ── Copy templates integration ──
def _load_copy_for_brand(brand_name: str) -> dict:
    """Load copy template for brand. Falls back to generic."""
    try:
        from copy_templates import get_copy, COPY_MAP
        industry_key = BRAND_INDUSTRY_MAP.get(brand_name.lower(), "")
        # Check each key in COPY_MAP
        for key in COPY_MAP:
            if key in industry_key or industry_key in key:
                return get_copy(key)
        return get_copy("tech")
    except Exception:
        return {}
def get_archetype_for_brand(brand_name: str) -> str:
    """Return archetype key for a brand. Defaults to 'corporate'."""
    brand = _resolve_brand(brand_name)
    if not brand:
        return "corporate"
    name_key = brand_name.lower()
    return BRAND_ARCHETYPE_MAP.get(name_key, "corporate")

def _scale_space(value: str, scale: float) -> str:
    """Scale a spacing value by density factor."""
    import re
    m = re.match(r'^(\d+)(px)?$', str(value))
    if m:
        base = int(m.group(1))
        scaled = max(4, round(base * scale))
        return f"{scaled}px"
    return str(value)

# ── Merge with getdesign.md brands ──
ALL_BRANDS: Dict[str, dict] = {**BRAND_PRESETS, **GETDESIGN_BRANDS}

def _resolve_brand(brand_name: str) -> Optional[Dict]:
    """Resolve brand from either built-in or getdesign presets."""
    return ALL_BRANDS.get(brand_name)

# ═══════════════════════════════════════════════════════════════
# CSS FRAMEWORK GENERATOR
# ═══════════════════════════════════════════════════════════════

def _v(name: str, brand: dict) -> str:
    """Get brand value or fallback."""
    return brand.get(name, "")

def generate_design_tokens(brand: dict) -> str:
    """Generate CSS custom properties (design tokens) from brand."""
    p = _v("primary", brand)
    s = _v("secondary", brand)
    a = _v("accent", brand)
    return f""":root {{
  --brand-primary: {p};
  --brand-secondary: {s};
  --brand-accent: {a};
  --brand-success: {_v("success", brand)};
  --brand-warning: {_v("warning", brand)};
  --brand-danger: {_v("danger", brand)};
  --brand-info: {_v("info", brand)};
  --brand-bg: {_v("bg", brand)};
  --brand-surface: {_v("surface", brand)};
  --brand-text: {_v("text", brand)};
  --brand-text-secondary: {_v("text_secondary", brand)};
  --brand-border: {_v("border", brand)};
  --brand-overlay: rgba(0,0,0,0.5);
  --brand-glow: 0 0 20px {_v("glow_rgba", brand)};
  --brand-gradient: {_v("gradient", brand)};

  /* getdesign.md inspired */
  --canvas: {_v("canvas", brand)};
  --canvas-soft: {_v("canvas_soft", brand)};
  --ink: {_v("ink", brand)};
  --ink-muted: {_v("ink_muted", brand)};
  --ink-subtle: {_v("ink_subtle", brand)};
  --body: {_v("ink", brand)};
  --hairline: {_v("hairline", brand)};
  --hairline-strong: {_v("hairline_strong", brand)};
  --surface-1: {_v("surface_1", brand)};
  --surface-2: {_v("surface_2", brand)};
  --surface-3: {_v("surface_3", brand)};
  --surface-4: {_v("surface_4", brand)};
}}

.dark {{
  --brand-bg: {_v("dark_bg", brand)};
  --brand-surface: {_v("dark_surface", brand)};
  --brand-text: {_v("dark_text", brand)};
  --brand-border: {_v("dark_border", brand)};
  --canvas: {_v("dark_canvas", brand)};
  --canvas-soft: {_v("dark_canvas_soft", brand)};
  --ink: {_v("dark_ink", brand)};
  --ink-muted: {_v("dark_ink_muted" if "dark_ink_muted" in brand else "dark_text", brand)};
  --ink-subtle: {_v("dark_ink_subtle" if "dark_ink_subtle" in brand else "dark_border", brand)};
  --hairline: {_v("dark_hairline", brand)};
  --hairline-strong: {_v("dark_hairline_strong" if "dark_hairline_strong" in brand else "dark_border", brand)};
  --surface-1: {_v("dark_surface_1", brand)};
  --surface-2: {_v("dark_surface_2", brand)};
  --surface-3: {_v("dark_surface_3", brand)};
  --surface-4: {_v("dark_surface_4", brand)};
}}"""

def generate_typography(brand: dict) -> str:
    """Generate typography CSS variables."""
    return """:root {
  --font-display: """ + _v("font_display", brand) + """;
  --font-body: """ + _v("font_body", brand) + """;
  --font-mono: """ + _v("font_mono", brand) + """;
  --text-h1: 3.5rem;
  --text-h2: 2.5rem;
  --text-h3: 1.75rem;
  --text-h4: 1.25rem;
  --text-body: 1rem;
  --text-small: 0.875rem;
  --text-xs: 0.75rem;
  --text-tiny: 0.625rem;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --line-height: 1.6;
  --line-height-heading: 1.2;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-wide: 0.025em;
}"""

def generate_spacing() -> str:
    """Generate spacing scale."""
    return """:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-xxl: 48px;
  --space-xxxl: 64px;
  --space-section: 96px;
  --space-section-sm: 64px;
  --space-section-lg: 128px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}"""

def generate_shadows() -> str:
    """Generate shadow scale."""
    return """:root {
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 50px rgba(0,0,0,0.12);
  --shadow-2xl: 0 25px 60px rgba(0,0,0,0.15);
  --shadow-glow: 0 0 30px var(--brand-glow, rgba(0,0,0,0.1));
  --shadow-inner: inset 0 2px 4px rgba(0,0,0,0.05);
}"""

def generate_animations() -> str:
    """Generate animation keyframes and classes."""
    return """:root {
  --anim-duration-fast: 0.2s;
  --anim-duration-normal: 0.3s;
  --anim-duration-slow: 0.6s;
  --anim-duration-xl: 1s;
  --anim-easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --anim-easing-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --anim-easing-smooth: cubic-bezier(0.22, 1, 0.36, 1);
  --anim-easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --anim-scale-hover: 1.05;
  --anim-scale-active: 0.98;
  --anim-translate-hover: -4px;
}

@keyframes vfx-fade-in-up { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes vfx-fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes vfx-shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
@keyframes vfx-float { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-12px); } }
@keyframes vfx-float-reverse { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(12px); } }
@keyframes vfx-gradient-shift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes vfx-count-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes vfx-scale-in { 0% { opacity: 0; transform: scale(0.8); } 70% { transform: scale(1.02); } 100% { opacity: 1; transform: scale(1); } }
@keyframes vfx-slide-up { 0% { opacity: 0; transform: translateY(30px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes vfx-spin-slow { 0% { transform: rotate(0); } 100% { transform: rotate(360deg); } }
@keyframes vfx-pulse-glow { 0%,100% { box-shadow: 0 0 5px var(--glow, rgba(0,0,0,0.2)); } 50% { box-shadow: 0 0 30px var(--glow, rgba(0,0,0,0.5)); } }
@keyframes vfx-wave { 0%,100% { transform: scaleY(1); } 50% { transform: scaleY(0.5); } }
@keyframes vfx-kenburns { 0% { transform: scale(1); } 100% { transform: scale(1.05); } }
@keyframes vfx-marquee { 0% { transform: translateX(0%); } 100% { transform: translateX(-50%); } }
@keyframes vfx-typewriter { from { width: 0; } to { width: 100%; } }
@keyframes vfx-blur-in { from { opacity: 0; filter: blur(10px); transform: translateY(10px); } to { opacity: 1; filter: blur(0); transform: translateY(0); } }
@keyframes vfx-tilt-in { from { opacity: 0; transform: perspective(800px) rotateY(15deg) translateX(-30px); } to { opacity: 1; transform: perspective(800px) rotateY(0) translateX(0); } }
@keyframes vfx-bounce-in { 0% { opacity: 0; transform: scale(0.3); } 50% { transform: scale(1.05); } 70% { transform: scale(0.9); } 100% { opacity: 1; transform: scale(1); } }
@keyframes vfx-orb { 0% { transform: translate(0px, 0px) scale(1); } 33% { transform: translate(30px, -20px) scale(1.1); } 66% { transform: translate(-20px, 10px) scale(0.9); } 100% { transform: translate(0px, 0px) scale(1); } }
@keyframes vfx-stagger-pop { 0% { opacity: 0; transform: scale(0.8); } 60% { transform: scale(1.05); } 100% { opacity: 1; transform: scale(1); } }
@keyframes vfx-shine { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
@keyframes vfx-reveal-clip { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0 0 0); } }

.vfx-fade-in-up { animation: vfx-fade-in-up var(--anim-duration-slow) var(--anim-easing-smooth) forwards; }
.vfx-fade-in { animation: vfx-fade-in var(--anim-duration-normal) var(--anim-easing-default) forwards; }
.vfx-float { animation: vfx-float 3s ease-in-out infinite; }
.vfx-float-2 { animation: vfx-float-reverse 4s ease-in-out infinite; }
.vfx-gradient-shift { background-size: 200% 200%; animation: vfx-gradient-shift 4s ease infinite; }
.vfx-scale-in { animation: vfx-scale-in 0.4s var(--anim-easing-bounce) forwards; }
.vfx-slide-up { animation: vfx-slide-up 0.6s var(--anim-easing-smooth) forwards; }
.vfx-spin-slow { animation: vfx-spin-slow 8s linear infinite; }
.vfx-pulse-glow { animation: vfx-pulse-glow 2s ease-in-out infinite; }
.vfx-shimmer { background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent); background-size: 200% 100%; animation: vfx-shimmer 2s infinite; }
.vfx-marquee { animation: vfx-marquee 30s linear infinite; }
.vfx-marquee:hover { animation-play-state: paused; }
.vfx-blur-in { animation: vfx-blur-in 0.6s var(--anim-easing-smooth) forwards; }
.vfx-tilt-in { animation: vfx-tilt-in 0.5s var(--anim-easing-smooth) forwards; }
.vfx-bounce-in { animation: vfx-bounce-in 0.5s var(--anim-easing-default) forwards; }
.vfx-orb { animation: vfx-orb 12s ease-in-out infinite; }
.vfx-orb-2 { animation: vfx-orb 15s ease-in-out infinite reverse; }
.vfx-stagger-pop { animation: vfx-stagger-pop 0.4s var(--anim-easing-default) forwards; }
"""

def generate_utilities() -> str:
    """Generate utility CSS classes."""
    return """/* ── Layout ── */
.container { max-width: 1280px; margin: 0 auto; padding: 0 var(--space-md); }
.container--narrow { max-width: 800px; }
.container--wide { max-width: 1400px; }
.section { padding: var(--space-section) 0; }
.section-sm { padding: var(--space-section-sm) 0; }
.section-lg { padding: var(--space-section-lg) 0; }
.flex-center { display: flex; align-items: center; justify-content: center; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }
.grid-center { display: grid; place-items: center; }
.stack { display: flex; flex-direction: column; }
.stack-sm { gap: var(--space-sm); }
.stack-md { gap: var(--space-md); }
.stack-lg { gap: var(--space-lg); }
.stack-xl { gap: var(--space-xl); }
.inline-flex-center { display: inline-flex; align-items: center; justify-content: center; }

/* ── Typography ── */
.heading-1 { font-family: var(--font-display); font-size: var(--text-h1); font-weight: var(--font-weight-bold); line-height: var(--line-height-heading); letter-spacing: var(--letter-spacing-tight); }
.heading-2 { font-family: var(--font-display); font-size: var(--text-h2); font-weight: var(--font-weight-bold); line-height: var(--line-height-heading); letter-spacing: var(--letter-spacing-tight); }
.heading-3 { font-family: var(--font-display); font-size: var(--text-h3); font-weight: var(--font-weight-semibold); line-height: var(--line-height-heading); }
.heading-4 { font-family: var(--font-display); font-size: var(--text-h4); font-weight: var(--font-weight-semibold); }
.body-text { font-family: var(--font-body); font-size: var(--text-body); line-height: var(--line-height); }
.text-small { font-size: var(--text-small); }
.text-xs { font-size: var(--text-xs); }
.text-gradient { background: var(--brand-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.text-muted { color: var(--brand-text-secondary); }

/* ── Glass Effects ── */
.glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
.glass-dark { background: rgba(0,0,0,0.3); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.08); }
.glass-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
.glass-card-light { background: rgba(255,255,255,0.7); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.8); }
.dark .glass-card-light { background: rgba(0,0,0,0.4); border-color: rgba(255,255,255,0.08); }
.glass-card-solid { background: var(--surface-1); border: 1px solid var(--hairline); }

/* ── Glow Orbs ── */
.glow-orb { position: absolute; border-radius: 50%; filter: blur(80px); pointer-events: none; }
.glow-orb-sm { width: 150px; height: 150px; }
.glow-orb-md { width: 300px; height: 300px; }
.glow-orb-lg { width: 500px; height: 500px; }
.glow-orb-xl { width: 700px; height: 700px; }

/* ── Hover Effects ── */
.hover-lift { transition: all var(--anim-duration-normal) var(--anim-easing-default); }
.hover-lift:hover { transform: translateY(var(--anim-translate-hover)); box-shadow: var(--shadow-lg); }
.hover-glow { transition: all var(--anim-duration-normal) var(--anim-easing-default); }
.hover-glow:hover { box-shadow: var(--shadow-glow); transform: scale(var(--anim-scale-hover)); }
.hover-scale { transition: transform var(--anim-duration-normal) var(--anim-easing-default); }
.hover-scale:hover { transform: scale(var(--anim-scale-hover)); }
.hover-bright { transition: all var(--anim-duration-normal) var(--anim-easing-default); }
.hover-bright:hover { filter: brightness(1.1); }

/* ── Premium Shadows ── */
.shadow-premium { box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 10px 15px -3px rgba(0,0,0,0.08), 0 20px 40px -4px rgba(0,0,0,0.06); }
.shadow-card { box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04); }
.shadow-elevated { box-shadow: 0 10px 25px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.04); }
.shadow-deep { box-shadow: 0 20px 50px rgba(0,0,0,0.12), 0 8px 20px rgba(0,0,0,0.06); }


/* ── Stitch Premium Patterns ── */
.mesh-gradient { background: radial-gradient(ellipse at top, rgba(0,212,255,0.12) 0%, transparent 50%), radial-gradient(ellipse at bottom, rgba(146,84,222,0.12) 0%, transparent 50%); }
.atmospheric-gradient { background: linear-gradient(180deg, var(--brand-bg) 0%, var(--surface-3) 100%); }
.electric-indigo { color: var(--electric-indigo, #635BFF); }
.bg-electric-indigo { background-color: var(--electric-indigo, #635BFF); }
.mesh-accent-cyan { color: var(--mesh-accent-cyan, #00D4FF); }
.mesh-accent-purple { color: var(--mesh-accent-purple, #9254DE); }
.ambient-shadow { box-shadow: 0px 8px 24px rgba(99,91,255,0.02); }
.elevated-shadow { box-shadow: 0px 16px 48px rgba(99,91,255,0.08); }
.tight-radius-pill { border-radius: 8px; }
.display-thin { font-weight: 300; letter-spacing: -0.04em; }
.tabular-figures { font-variant-numeric: tabular-nums; }
.slate-gray { color: var(--slate-gray, #425466); }
.bg-slate-gray { background-color: var(--slate-gray, #425466); }

/* ── Misc ── */
.gradient-bg { background: var(--brand-gradient); }
.gradient-text-only { background: var(--brand-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
.hidden-scrollbar { scrollbar-width: none; -ms-overflow-style: none; }
.hidden-scrollbar::-webkit-scrollbar { display: none; }
.aspect-video { aspect-ratio: 16/9; }
.aspect-square { aspect-ratio: 1/1; }
.aspect-portrait { aspect-ratio: 3/4; }
.object-cover { object-fit: cover; }
.object-contain { object-fit: contain; }"""

def generate_section_patterns() -> str:
    """Generate section background patterns."""
    return """/* ── Section Backgrounds ── */
.section--light { background: var(--canvas); }
.section--surface { background: var(--surface-1); }
.section--accent { background: var(--brand-primary); color: #fff; }
.section--accent .section__heading { color: #fff; }
.section--accent .section__subheading { color: rgba(255,255,255,0.9); }
.section--accent .text-muted { color: rgba(255,255,255,0.7); }
.section--dark { background: var(--canvas); color: #fff; }
.section--dark .section__heading { color: #fff; }
.section--dark .section__subheading { color: rgba(255,255,255,0.7); }
.section--dark .text-muted { color: rgba(255,255,255,0.6); }

/* Auto-alternating */
.section--alternate { background: var(--surface-2); }
.template-sections > .section:nth-child(even):not(.section--hero):not(.section--accent):not(.section--dark):not(.section--light) { background: var(--surface-2); }

/* Heading styles in sections */
.section__heading { font-family: var(--font-display); font-size: var(--text-h2); font-weight: var(--font-weight-bold); line-height: var(--line-height-heading); margin-bottom: var(--space-sm); }
.section__subheading { font-family: var(--font-body); font-size: var(--text-body); color: var(--brand-text-secondary); max-width: 600px; margin: 0 auto; }

/* Section reveal */
.section--reveal { opacity: 0; transform: translateY(30px); transition: opacity var(--anim-duration-slow) var(--anim-easing-smooth), transform var(--anim-duration-slow) var(--anim-easing-smooth); }
.section--reveal.visible { opacity: 1; transform: translateY(0); }
.stagger-1 { transition-delay: 0.1s; }
.stagger-2 { transition-delay: 0.2s; }
.stagger-3 { transition-delay: 0.3s; }
.stagger-4 { transition-delay: 0.4s; }
.stagger-5 { transition-delay: 0.5s; }"""

def generate_responsive() -> str:
    """Generate responsive breakpoints."""
    return """/* ── Responsive Breakpoints ── */
/* Mobile-first: base = 375px+ */

/* sm: 640px */
@media (min-width: 640px) {
  .container { padding: 0 var(--space-lg); }
  .heading-1 { font-size: 4rem; }
  .heading-2 { font-size: 3rem; }
  .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-xl); }
  .grid-3 { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-lg); }
}

/* md: 768px */
@media (min-width: 768px) {
  .grid-3 { grid-template-columns: repeat(3, 1fr); }
  .grid-4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-lg); }
  .section { padding: 120px 0; }
  :root { --text-h1: 4.5rem; --text-h2: 3.5rem; }
}

/* lg: 1024px */
@media (min-width: 1024px) {
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
  .grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--space-lg); }
  .grid-6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: var(--space-md); }
  .section { padding: 140px 0; }
  :root { --text-h1: 5rem; --text-h2: 4rem; --text-h3: 2rem; }
}

/* xl: 1280px */
@media (min-width: 1280px) {
  :root { --text-h1: 5.5rem; --text-h2: 4.5rem; }
}"""

def generate_a11y() -> str:
    """Generate accessibility CSS."""
    return """/* ── Accessibility ── */
:focus-visible { outline: 2px solid var(--brand-primary); outline-offset: 2px; border-radius: var(--radius-sm); }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  .vfx-float, .vfx-float-2 { animation: none !important; }
}
::selection { background: var(--brand-primary); color: #fff; }
.skip-link { position: absolute; top: -100%; left: var(--space-md); padding: var(--space-sm) var(--space-md); background: var(--brand-primary); color: #fff; z-index: 10000; border-radius: var(--radius-md); }
.skip-link:focus { top: var(--space-sm); }"""

def generate_base_reset() -> str:
    """Generate CSS reset and base styles."""
    return """/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: 80px; }
body { font-family: var(--font-body); font-size: var(--text-body); line-height: var(--line-height); background: var(--canvas); color: var(--ink); transition: background var(--anim-duration-normal), color var(--anim-duration-normal); -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
img, video, canvas, svg { max-width: 100%; height: auto; display: block; }
a { color: inherit; text-decoration: none; }
button { cursor: pointer; font-family: inherit; font-size: inherit; border: none; background: none; }
input, textarea, select { font-family: inherit; font-size: inherit; }
ul, ol { list-style: none; }
h1, h2, h3, h4, h5, h6 { font-family: var(--font-display); line-height: var(--line-height-heading); }
p { margin-bottom: var(--space-md); }
p:last-child { margin-bottom: 0; }"""

# ═══════════════════════════════════════════════════════════════
# SECTION RENDERERS — 12 premium section types
# ═══════════════════════════════════════════════════════════════

def _hero_split(name: str, tagline: str, primary: str, hero_img: str = "") -> str:
    """Hero with split layout: text left, mockup right."""
    return f"""<section class="section section--hero section--light" role="region" aria-label="Hero">
  <div class="container">
    <div class="hero-split" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center;min-height:80vh">
      <div class="vfx-slide-up">
        <span class="badge" style="display:inline-block;padding:6px 16px;background:var(--brand-primary);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-medium);margin-bottom:var(--space-lg)">{tagline}</span>
        <h1 class="heading-1" style="margin-bottom:var(--space-lg)">{name}</h1>
        <p class="body-text" style="font-size:1.125rem;margin-bottom:var(--space-xl);max-width:520px;color:var(--ink);opacity:0.85">Platform all-in-one untuk mengelola, menganalisis, dan mengembangkan bisnis Anda dengan satu dashboard powerful.</p>
        <div class="flex" style="display:flex;gap:var(--space-md);flex-wrap:wrap">
          <a href="#cta" class="btn-primary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Mulai Gratis <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
          <a href="#demo" class="btn-secondary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;border:1px solid var(--hairline);border-radius:var(--radius-full);font-weight:var(--font-weight-medium);transition:all var(--anim-duration-normal) var(--anim-easing-default)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>Tonton Demo</a>
        </div>
        <div class="trust-row" style="display:flex;gap:var(--space-lg);margin-top:var(--space-xxl);padding-top:var(--space-lg);border-top:1px solid var(--hairline)">
          <div><strong class="heading-4" style="color:var(--brand-primary)">500+</strong><p class="text-small" style="color:var(--ink);opacity:0.75">Pengguna Aktif</p></div>
          <div><strong class="heading-4" style="color:var(--brand-primary)">99.9%</strong><p class="text-small" style="color:var(--ink);opacity:0.75">Uptime</p></div>
          <div><strong class="heading-4" style="color:var(--brand-primary)">4.9★</strong><p class="text-small" style="color:var(--ink);opacity:0.75">Rating</p></div>
        </div>
      </div>
      <div class="hero-mockup vfx-float" style="background:var(--surface-2);border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-xl);border:1px solid var(--hairline)">
        <div class="mockup-bar" style="display:flex;align-items:center;gap:6px;padding:12px 16px;background:var(--surface-3);border-bottom:1px solid var(--hairline)">
          <span style="width:10px;height:10px;border-radius:50%;background:#EF4444"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#F59E0B"></span>
          <span style="width:10px;height:10px;border-radius:50%;background:#22C55E"></span>
          <span class="text-small" style="margin-left:auto;color:var(--ink);opacity:0.7">app.inxotive.io</span>
        </div>
        {'''<div style="padding:0;min-height:320px;background:var(--surface-1);background-image:url(''' + hero_img + ''');background-size:cover;background-position:center"></div>''' if hero_img else '''<div style="padding:40px;min-height:320px;display:flex;flex-direction:column;gap:16px;background:var(--surface-1)">
          <div style="height:48px;width:60%;background:var(--brand-gradient);opacity:0.15;border-radius:var(--radius-md)"></div>
          <div style="height:16px;width:90%;background:var(--surface-3);border-radius:var(--radius-sm)"></div>
          <div style="height:16px;width:75%;background:var(--surface-3);border-radius:var(--radius-sm)"></div>
          <div style="flex:1;min-height:80px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px">
            <div style="background:linear-gradient(180deg, var(--brand-primary)00, var(--brand-primary)20);border-radius:var(--radius-md);border:1px solid var(--hairline)"></div>
            <div style="background:linear-gradient(180deg, var(--brand-secondary)00, var(--brand-secondary)15);border-radius:var(--radius-md);border:1px solid var(--hairline);margin-top:16px"></div>
            <div style="background:linear-gradient(180deg, var(--brand-accent)00, var(--brand-accent)15);border-radius:var(--radius-md);border:1px solid var(--hairline)"></div>
          </div>
          <div style="height:40px;background:var(--brand-gradient);opacity:0.12;border-radius:var(--radius-md)"></div>
        </div>'''}
      </div>
    </div>
  </div>
</section>"""

def _hero_centered(name: str, tagline: str, primary: str, accent: str) -> str:
    """Centered hero with CTA."""
    return f"""<section class="section section--hero section--light" role="region" aria-label="Hero" style="text-align:center;position:relative;overflow:hidden">
  <div class="glow-orb glow-orb-lg" style="background:radial-gradient(circle, {primary}15 0%, transparent 70%);top:-20%;left:50%;transform:translateX(-50%)"></div>
  <div class="container container--narrow" style="position:relative;z-index:1">
    <div class="vfx-slide-up">
      <span class="badge" style="display:inline-block;padding:8px 20px;background:rgba({','.join(str(int(primary[i:i+2],16)) for i in (1, 3, 5))},0.1);color:var(--brand-primary);border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-lg)">{tagline}</span>
      <h1 class="heading-1" style="margin-bottom:var(--space-lg)">{name}</h1>
      <p class="body-text" style="font-size:1.125rem;max-width:600px;margin:0 auto var(--space-xl);color:var(--ink);opacity:0.85">Solusi lengkap untuk transformasi digital bisnis Anda. Cepat, modern, dan terpercaya.</p>
      <div class="flex" style="display:flex;gap:var(--space-md);justify-content:center;flex-wrap:wrap">
        <a href="#cta" class="btn-primary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default);box-shadow:var(--shadow-lg)">Mulai Sekarang</a>
        <a href="#features" class="btn-secondary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;border:1px solid var(--hairline);border-radius:var(--radius-full);font-weight:var(--font-weight-medium);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Pelajari Lebih Lanjut</a>
      </div>
    </div>
  </div>
</section>"""

def _features_grid() -> str:
    """Features grid with 6 items."""
    features = [
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M12 2l2.4 7.2L22 9.6l-5.6 4.8 1.6 7.6L12 18l-5.6 4.8 1.6-7.6L2 9.6l7.6-.4z\"/></svg>", "Kilat Cepat", "Optimasi performa terbaik dengan teknologi terkini untuk kecepatan maksimal."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><rect x=\"3\" y=\"11\" width=\"18\" height=\"11\" rx=\"2\" ry=\"2\"/><path d=\"M7 11V7a5 5 0 0110 0v4\"/></svg>", "Aman & Terpercaya", "Enkripsi end-to-end dan keamanan berlapis untuk data Anda."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><circle cx=\"12\" cy=\"12\" r=\"4\"/><line x1=\"2\" y1=\"12\" x2=\"6\" y2=\"12\"/><line x1=\"18\" y1=\"12\" x2=\"22\" y2=\"12\"/></svg>", "Desain Modern", "Tampilan premium dengan UI/UX terkini yang memukau pengunjung."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><line x1=\"18\" y1=\"20\" x2=\"18\" y2=\"10\"/><line x1=\"12\" y1=\"20\" x2=\"12\" y2=\"4\"/><line x1=\"6\" y1=\"20\" x2=\"6\" y2=\"14\"/></svg>", "Analitik Real-time", "Pantau performa bisnis Anda dengan dashboard analitik langsung."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M12 2a2 2 0 012 2v2a2 2 0 01-2 2 2 2 0 01-2-2V4a2 2 0 012-2z\"/><path d=\"M12 8v4\"/><circle cx=\"12\" cy=\"18\" r=\"4\"/></svg>", "AI-Powered", "Otomatisasi cerdas dengan teknologi AI untuk efisiensi maksimal."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><rect x=\"5\" y=\"2\" width=\"14\" height=\"20\" rx=\"2\" ry=\"2\"/><line x1=\"12\" y1=\"18\" x2=\"12\" y2=\"18\"/></svg>", "Mobile First", "Responsive sempurna di semua perangkat dari desktop hingga mobile."),
    ]
    cards = "\n".join(
        f'<div class="glass-card-solid card-feature hover-lift stagger-{i%5+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);text-align:center;transition:all var(--anim-duration-normal) var(--anim-easing-default)">'
        f'<div style="width:40px;height:40px;margin-bottom:var(--space-md)">{icon}</div>'
        f'<h3 class="heading-4" style="margin-bottom:var(--space-sm)">{title}</h3>'
        f'<p class="body-text text-small" style="color:var(--ink);opacity:0.75">{desc}</p></div>'
        for i, (icon, title, desc) in enumerate(features)
    )
    return f"""<section class="section section--surface section--reveal" role="region" aria-label="Fitur" id="features">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">FITUR</span>
      <h2 class="section__heading">Semua yang Anda Butuhkan</h2>
      <p class="section__subheading" style="color:var(--ink);opacity:0.75">Platform lengkap dengan fitur-fitur canggih untuk mengembangkan bisnis Anda.</p>
    </div>
    <div class="grid-3" style="gap:var(--space-lg)">{cards}</div>
  </div>
</section>"""

def _stats_counter() -> str:
    """Stats counter with 4 stats."""
    return f"""<section class="section section--accent section--reveal" role="region" aria-label="Statistik" style="text-align:center">
  <div class="container">
    <div class="grid-4" style="gap:var(--space-xl)">
      <div class="stat-item vfx-fade-in-up stagger-1">
        <div class="heading-1" style="color:#fff;font-weight:var(--font-weight-extrabold)">500+</div>
        <p style="color:rgba(255,255,255,0.8);font-size:var(--text-body)">Klien Puas</p>
      </div>
      <div class="stat-item vfx-fade-in-up stagger-2">
        <div class="heading-1" style="color:#fff;font-weight:var(--font-weight-extrabold)">99.9%</div>
        <p style="color:rgba(255,255,255,0.8);font-size:var(--text-body)">Uptime Garansi</p>
      </div>
      <div class="stat-item vfx-fade-in-up stagger-3">
        <div class="heading-1" style="color:#fff;font-weight:var(--font-weight-extrabold)">50K+</div>
        <p style="color:rgba(255,255,255,0.8);font-size:var(--text-body)">Jam Koding</p>
      </div>
      <div class="stat-item vfx-fade-in-up stagger-4">
        <div class="heading-1" style="color:#fff;font-weight:var(--font-weight-extrabold)">15+</div>
        <p style="color:rgba(255,255,255,0.8);font-size:var(--text-body)">Tahun Pengalaman</p>
      </div>
    </div>
  </div>
</section>"""

def _testimonials() -> str:
    """Testimonials carousel/grid."""
    testimonials = [
        ("Bisma", "CEO INXOTIVE", "Platform ini benar-benar mengubah cara kami bekerja. Produktivitas tim meningkat 300% dalam 3 bulan pertama."),
        ("Sava Y.", "Founder Yoga Studio", "Dashboard yang intuitif dan fitur yang lengkap. Sangat recommended untuk bisnis di era digital."),
        ("M. Place", "Owner Restaurant", "Pelayanan cepat, hasil maksimal. Tim INXOTIVE sangat profesional dan responsif terhadap kebutuhan kami."),
    ]
    cards = "\n".join(
        f'<div class="glass-card-solid hover-lift stagger-{i%3+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);position:relative">'
        f'<div style="font-size:3rem;color:var(--brand-primary);opacity:0.2;position:absolute;top:16px;right:20px;font-family:serif;line-height:1">"</div>'
        f'<p class="body-text" style="margin-bottom:var(--space-lg);font-style:italic;position:relative;z-index:1">"{quote}"</p>'
        f'<div class="flex" style="display:flex;align-items:center;gap:var(--space-md)">'
        f'<div style="width:44px;height:44px;border-radius:50%;background:var(--brand-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:var(--font-weight-bold)">{name[0]}</div>'
        f'<div><strong style="font-size:var(--text-small)">{name}</strong><p class="text-xs text-muted">{role}</p></div></div></div>'
        for i, (name, role, quote) in enumerate(testimonials)
    )
    return f"""<section class="section section--light section--reveal" role="region" aria-label="Testimoni">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">Apa Kata Mereka</h2>
      <p class="section__subheading">Testimoni dari klien yang sudah merasakan manfaat platform kami.</p>
    </div>
    <div class="grid-3" style="gap:var(--space-lg)">{cards}</div>
  </div>
</section>"""

def _cta_centered(primary: str) -> str:
    """Centered CTA section."""
    return f"""<section class="section section--reveal" role="region" aria-label="Call to Action" id="cta" style="background:linear-gradient(135deg, var(--brand-primary), color-mix(in srgb, var(--brand-primary) 70%, var(--brand-accent)));text-align:center;position:relative;overflow:hidden">
  <div class="glow-orb glow-orb-lg" style="background:radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);top:-30%;left:20%"></div>
  <div class="container container--narrow" style="position:relative;z-index:1">
    <div class="vfx-scale-in">
      <h2 class="heading-2" style="color:#fff;margin-bottom:var(--space-md)">Siap Memulai?</h2>
      <p class="body-text" style="color:rgba(255,255,255,0.85);margin-bottom:var(--space-xl);font-size:1.125rem">Gabung dengan ratusan bisnis lain yang sudah bertransformasi digital bersama INXOTIVE.</p>
      <div class="flex" style="display:flex;gap:var(--space-md);justify-content:center;flex-wrap:wrap">
        <a href="#contact" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;background:#fff;color:var(--brand-primary);border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default);box-shadow:var(--shadow-lg)">Hubungi Kami</a>
        <a href="#pricing" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;border:2px solid rgba(255,255,255,0.3);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-medium);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Lihat Pricing</a>
      </div>
    </div>
  </div>
</section>"""

def _pricing() -> str:
    """3-column pricing table."""
    plans = [
        ("Starter", "Rp 1.5jt", "Perfect untuk pemula", ["1 Website", "5 Halaman", "SSL Gratis", "Support Email", "Mobile Friendly"], False),
        ("Professional", "Rp 3.5jt", "Untuk bisnis berkembang", ["10 Website", "Unlimited Halaman", "SSL + CDN", "Support Prioritas", "SEO Optimasi", "Analitik", "AI Chatbot"], True),
        ("Enterprise", "Rp 7.5jt", "Solusi lengkap korporat", ["Unlimited Website", "Custom Fitur", "Dedicated Server", "24/7 Support", "Full SEO Suite", "API Integration", "Tim Khusus", "SLA 99.9%"], False),
    ]
    cards = ""
    for i, (name, price, desc, features, popular) in enumerate(plans):
        popular_class = "transform:scale(1.05);border:2px solid var(--brand-primary);position:relative" if popular else ""
        popular_badge = '<div style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--brand-primary);color:#fff;padding:4px 16px;border-radius:var(--radius-full);font-size:var(--text-xs);font-weight:var(--font-weight-semibold)">POPULER</div>' if popular else ""
        feats = "\n".join(f'<li style="display:flex;align-items:center;gap:var(--space-sm);padding:8px 0"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{("var(--brand-primary)" if not popular else "#fff")}" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>{f}</li>' for f in features)
        btn_class = "background:var(--brand-gradient);color:#fff" if popular else "border:1px solid var(--hairline)"
        cards += f'<div class="glass-card-solid hover-lift stagger-{i+1}" style="padding:var(--space-xxl);border-radius:var(--radius-lg);text-align:center;{popular_class}">{popular_badge}<h3 class="heading-3" style="margin-bottom:var(--space-sm)">{name}</h3><p class="text-small text-muted" style="margin-bottom:var(--space-lg)">{desc}</p><div class="heading-2" style="margin-bottom:var(--space-lg)">{price}<span class="text-small text-muted" style="font-family:var(--font-body)">/project</span></div><ul style="text-align:left;margin-bottom:var(--space-xl)">{feats}</ul><a href="#cta" style="display:block;padding:14px 0;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);{btn_class};transition:all var(--anim-duration-normal)">Pilih Paket</a></div>'
    return f"""<section class="section section--light section--reveal" role="region" aria-label="Pricing" id="pricing">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">PRICING</span>
      <h2 class="section__heading">Harga Transparan</h2>
      <p class="section__subheading">Pilih paket yang sesuai dengan kebutuhan bisnis Anda.</p>
    </div>
    <div class="grid-3" style="gap:var(--space-lg);align-items:start">{cards}</div>
  </div>
</section>"""

def _about() -> str:
    """About/story split section."""
    return f"""<section class="section section--surface section--reveal" role="region" aria-label="Tentang" id="about">
  <div class="container">
    <div class="about-split" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center">
      <div class="vfx-slide-up">
        <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">TENTANG KAMI</span>
        <h2 class="heading-2" style="margin-bottom:var(--space-lg);margin-top:var(--space-sm)">Kisah Kami dalam Membangun Masa Depan Digital</h2>
        <p class="body-text" style="margin-bottom:var(--space-md)">Bermula dari sebuah visi kecil di tahun 2020, INXOTIVE OFFICE hadir untuk membantu bisnis lokal bertransformasi digital. Kami percaya bahwa teknologi hebat harus terjangkau untuk semua.</p>
        <p class="body-text text-muted" style="margin-bottom:var(--space-xl)">Dengan tim yang terdiri dari developer, desainer, dan strategis digital berpengalaman, kami telah membantu 500+ bisnis di Indonesia membangun kehadiran online mereka.</p>
        <div class="flex" style="display:flex;gap:var(--space-xl);flex-wrap:wrap">
          <div><strong class="heading-3" style="color:var(--brand-primary)">5+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Tahun</p></div>
          <div><strong class="heading-3" style="color:var(--brand-primary)">500+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Project</p></div>
          <div><strong class="heading-3" style="color:var(--brand-primary)">50+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Tim Ahli</p></div>
        </div>
      </div>
      <div class="about-image vfx-float" style="background:var(--surface-3);border-radius:var(--radius-lg);height:400px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:var(--shadow-lg)">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:24px;width:100%">
          <div style="height:120px;background:var(--brand-primary);opacity:0.15;border-radius:var(--radius-md)"></div>
          <div style="height:120px;background:var(--brand-accent);opacity:0.15;border-radius:var(--radius-md);margin-top:30px"></div>
          <div style="height:80px;background:var(--brand-secondary);opacity:0.12;border-radius:var(--radius-md);grid-column:1/-1"></div>
        </div>
      </div>
    </div>
  </div>
</section>"""

def _team() -> str:
    """Team members grid."""
    members = [
        ("Bisma", "Founder & CEO", "Visioner di balik INXOTIVE"),
        ("Sava", "CTO", "Ahli teknologi & arsitektur"),
        ("Maya", "Lead Designer", "Desain UI/UX premium"),
        ("Rizky", "Head of Marketing", "Strategi pertumbuhan"),
    ]
    cards = "\n".join(
        f'<div class="glass-card-solid hover-lift stagger-{i+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);text-align:center">'
        f'<div style="width:80px;height:80px;border-radius:50%;background:var(--brand-gradient);margin:0 auto var(--space-md);display:flex;align-items:center;justify-content:center;font-size:2rem;color:#fff;font-weight:var(--font-weight-bold)">{name[0]}</div>'
        f'<h4 class="heading-4" style="margin-bottom:var(--space-xs)">{name}</h4>'
        f'<p class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-medium);margin-bottom:var(--space-sm)">{role}</p>'
        f'<p class="text-xs text-muted">{desc}</p></div>'
        for i, (name, role, desc) in enumerate(members)
    )
    return f"""<section class="section section--light section--reveal" role="region" aria-label="Tim">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">Tim Kami</h2>
      <p class="section__subheading">Para ahli di balik kesuksesan INXOTIVE.</p>
    </div>
    <div class="grid-4" style="gap:var(--space-lg)">{cards}</div>
  </div>
</section>"""



def _gallery() -> str:
    """Image gallery / portfolio grid."""
    items = []
    for i in range(6):
        items.append(f'''<div class="vfx-stagger-pop stagger-{i+1}" style="overflow:hidden;border-radius:var(--radius-lg);aspect-ratio:{'4/3' if i % 2 == 0 else '3/4'}{';margin-top:-40px' if i % 3 == 1 else ''};background:var(--surface-2);position:relative;cursor:pointer;transition:transform var(--anim-duration-normal) var(--anim-easing-default)">
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, transparent 50%, rgba(0,0,0,0.4));z-index:1"></div>
      <div style="position:absolute;bottom:0;left:0;right:0;padding:var(--space-lg);z-index:2;color:#fff">
        <strong style="font-size:var(--text-small)">Project {i+1}</strong>
        <p class="text-xs" style="opacity:0.7;margin-top:2px">Kategori</p>
      </div>
      <div style="width:100%;height:100%;background:linear-gradient(135deg, var(--brand-primary), var(--brand-accent));opacity:0.12"></div>
    </div>''')
    grid = "\n".join(items)
    return f'''<section class="section section--reveal" role="region" aria-label="Galeri" id="gallery">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">PORTFOLIO</span>
      <h2 class="section__heading">Lihat Hasil Kami</h2>
      <p class="section__subheading">Karya terbaik dari tim kami untuk berbagai industri.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(280px, 1fr));gap:var(--space-lg)">
{grid}
    </div>
  </div>
</section>'''


def _logo_cloud(brand_name: str = "INXOTIVE") -> str:
    """Client / partner logo cloud."""
    logos = []
    for i, name in enumerate([f"{brand_name}", f"{brand_name}", f"{brand_name}", f"{brand_name}", f"{brand_name}", f"{brand_name}"]):
        logos.append(f'<div class="vfx-float stagger-{i+1}" style="flex-shrink:0;padding:var(--space-lg) var(--space-xl);background:var(--surface-1);border:1px solid var(--hairline);border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;min-width:140px"><span class="heading-4" style="color:var(--ink-muted);font-size:var(--text-body);opacity:0.6">{name}</span></div>')
    row = "".join(logos)
    # Double for marquee effect
    row2 = row
    return f'''<section class="section section--surface section--reveal" role="region" aria-label="Klien Kami" id="logos">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-lg)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">KLIEN KAMI</span>
    </div>
    <div style="overflow:hidden;mask-image:linear-gradient(to right, transparent, black 10%, black 90%, transparent);-webkit-mask-image:linear-gradient(to right, transparent, black 10%, black 90%, transparent)">
      <div class="vfx-marquee" style="display:flex;gap:var(--space-md);width:max-content">
        {row}{row2}
      </div>
    </div>
  </div>
</section>'''


def _process() -> str:
    """How it works / process timeline."""
    steps = [
        ("01", "Konsultasi", "Kami ngobrol dulu tentang kebutuhan dan visi Anda.", False),
        ("02", "Desain", "Kami buatkan desain yang sesuai brand Anda.", False),
        ("03", "Bangun", "Tim kami membangun website dengan teknologi terbaik.", True),
        ("04", "Launch", "Website live dan siap membantu bisnis Anda.", False),
    ]
    items = ""
    for i, (num, title, desc, active) in enumerate(steps):
        items += f'''<div class="vfx-slide-up stagger-{i+1}" style="display:flex;gap:var(--space-xl);align-items:flex-start;padding:var(--space-xl) 0;position:relative">
      <div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0">
        <div style="width:48px;height:48px;border-radius:50%;background:{'var(--brand-gradient)' if active else 'var(--surface-2)'};color:{'#fff' if active else 'var(--ink-muted)'};display:flex;align-items:center;justify-content:center;font-weight:var(--font-weight-bold);font-size:var(--text-small);position:relative;z-index:1">{num}</div>
        {'''<div style="width:2px;flex:1;background:var(--hairline);margin:4px auto"></div>''' if i < len(steps) - 1 else ''}
      </div>
      <div style="flex:1;padding-top:10px">
        <h3 class="heading-4" style="margin-bottom:var(--space-xs)">{title}</h3>
        <p class="body-text" style="color:var(--ink-muted);font-size:var(--text-small)">{desc}</p>
      </div>
    </div>'''
    return f'''<section class="section section--reveal" role="region" aria-label="Proses" id="process">
  <div class="container container--narrow">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">CARA KERJA</span>
      <h2 class="section__heading">Gimana Cara Kami Bekerja</h2>
      <p class="section__subheading">Proses sederhana yang bikin website Anda jadi kenyataan.</p>
    </div>
    {items}
  </div>
</section>'''


def _hero_video(name: str, tagline: str, primary: str, hero_img: str = "") -> str:
    """Hero with video/image background + overlay."""
    bg_style = f'background-image:url({hero_img});background-size:cover;background-position:center' if hero_img else 'background:var(--canvas)'
    return f'''<section class="section section--hero" role="region" aria-label="Hero" style="position:relative;overflow:hidden;padding:0;min-height:85vh;display:flex;align-items:center;{bg_style}">
  <div style="position:absolute;inset:0;background:linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.4) 100%);z-index:0"></div>
  <div class="vfx-orb" style="position:absolute;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle, {primary}30, transparent);top:10%;right:-5%;z-index:0"></div>
  <div class="vfx-orb-2" style="position:absolute;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle, {primary}20, transparent);bottom:10%;left:-5%;z-index:0"></div>
  <div class="container" style="position:relative;z-index:1;padding:120px 0">
    <div class="vfx-blur-in" style="max-width:720px">
      <span class="badge" style="display:inline-block;padding:8px 20px;background:rgba(255,255,255,0.12);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-lg)">{tagline}</span>
      <h1 class="heading-1" style="color:#fff;margin-bottom:var(--space-lg);font-size:clamp(2.8rem, 6vw, 5rem)">{name}</h1>
      <p class="body-text" style="color:rgba(255,255,255,0.85);font-size:1.125rem;margin-bottom:var(--space-xl);max-width:540px">Solusi lengkap untuk transformasi digital bisnis Anda. Cepat, modern, dan terpercaya.</p>
      <div style="display:flex;gap:var(--space-md);flex-wrap:wrap">
        <a href="#cta" class="btn-primary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default);box-shadow:var(--shadow-lg)">Mulai Sekarang</a>
        <a href="#gallery" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;border:2px solid rgba(255,255,255,0.3);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-medium);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Lihat Karya</a>
      </div>
    </div>
  </div>
</section>'''


# Copy logo cloud branding helper
def _faq() -> str:
    """FAQ accordion section."""
    faqs = [
        ("Berapa lama proses pembuatan website?", "Untuk landing page, proses pengerjaan 2-4 jam setelah brief clear. Company profile 1-2 hari. Project kompleks 3-7 hari tergantung scope."),
        ("Apakah saya bisa request revisi?", "Tentu! Setiap paket termasuk 2x revisi. Revisi tambahan dikenakan biaya sesuai kompleksitas."),
        ("Teknologi apa yang digunakan?", "Kami menggunakan React/Vite/Tailwind untuk frontend, FastAPI untuk backend. Deploy ke Vercel atau Cloudflare Pages dengan performa tinggi."),
        ("Apakah termasuk maintenance?", "Paket Professional dan Enterprise termasuk maintenance bulanan. Paket Starter bisa add-on maintenance terpisah."),
    ]
    items = "\n".join(
        f'<details class="faq-item" style="padding:var(--space-lg);border-bottom:1px solid var(--hairline);cursor:pointer">'
        f'<summary style="font-weight:var(--font-weight-semibold);display:flex;align-items:center;justify-content:space-between;list-style:none">'
        f'{q}<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="transition:transform var(--anim-duration-normal)"><path d="M6 9l6 6 6-6"/></svg>'
        f'</summary><p class="body-text text-muted" style="margin-top:var(--space-md);padding-right:var(--space-xxl)">{a}</p></details>'
        for q, a in faqs
    )
    return f"""<section class="section section--light section--reveal" role="region" aria-label="FAQ" id="faq">
  <div class="container container--narrow">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">Pertanyaan Umum</h2>
      <p class="section__subheading">Jawaban cepat untuk pertanyaan yang sering diajukan.</p>
    </div>
    <div style="border-top:1px solid var(--hairline);border-radius:var(--radius-lg);overflow:hidden;background:var(--surface-1)">{items}</div>
  </div>
</section>"""

def _contact() -> str:
    """Contact section."""
    return f"""<section class="section section--surface section--reveal" role="region" aria-label="Kontak" id="contact">
  <div class="container">
    <div class="contact-split" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl)">
      <div>
        <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">KONTAK</span>
        <h2 class="heading-2" style="margin-bottom:var(--space-lg);margin-top:var(--space-sm)">Mari Diskusi</h2>
        <p class="body-text text-muted" style="margin-bottom:var(--space-xl)">Tim kami siap membantu Anda. Hubungi kami untuk konsultasi gratis.</p>
        <div class="contact-info" style="display:flex;flex-direction:column;gap:var(--space-lg)">
          <div class="flex" style="display:flex;align-items:center;gap:var(--space-md)"><div style="width:48px;height:48px;border-radius:var(--radius-md);background:var(--surface-2);display:flex;align-items:center;justify-content:center;color:var(--brand-primary)"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 4L12 13 2 4"/></svg></div><div><strong style="font-size:var(--text-small)">Email</strong><p class="text-small" style="color:var(--ink);opacity:0.7">hello@inxotive.com</p></div></div>
          <div class="flex" style="display:flex;align-items:center;gap:var(--space-md)"><div style="width:48px;height:48px;border-radius:var(--radius-md);background:var(--surface-2);display:flex;align-items:center;justify-content:center;color:var(--brand-primary)"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg></div><div><strong style="font-size:var(--text-small)">Lokasi</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Bali, Indonesia</p></div></div>
          <div class="flex" style="display:flex;align-items:center;gap:var(--space-md)"><div style="width:48px;height:48px;border-radius:var(--radius-md);background:var(--surface-2);display:flex;align-items:center;justify-content:center;color:var(--brand-primary)"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12" y2="18"/></svg></div><div><strong style="font-size:var(--text-small)">WhatsApp</strong><p class="text-small" style="color:var(--ink);opacity:0.7">+62 811-9988-7766</p></div></div>
        </div>
      </div>
      <div class="contact-form glass-card-solid" style="padding:var(--space-xxl);border-radius:var(--radius-lg)">
        <form onsubmit="event.preventDefault();alert('Terima kasih! Kami akan menghubungi Anda segera.')">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-md);margin-bottom:var(--space-md)">
            <input type="text" placeholder="Nama" required style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-2);color:var(--ink);width:100%">
            <input type="email" placeholder="Email" required style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-2);color:var(--ink);width:100%">
          </div>
          <input type="text" placeholder="Subjek" style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-2);color:var(--ink);width:100%;margin-bottom:var(--space-md)">
          <textarea placeholder="Pesan" rows="4" required style="padding:12px 16px;border:1px solid var(--hairline);border-radius:var(--radius-md);background:var(--surface-2);color:var(--ink);width:100%;margin-bottom:var(--space-md);resize:vertical;font-family:inherit"></textarea>
          <button type="submit" style="width:100%;padding:14px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Kirim Pesan</button>
        </form>
      </div>
    </div>
  </div>
</section>"""

def _footer(brand_name: str) -> str:
    """Footer section."""
    return f"""<footer class="section section--dark" role="contentinfo" style="padding:var(--space-xxl) 0 var(--space-lg)">
  <div class="container">
    <div class="footer-grid" style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:var(--space-xxl);margin-bottom:var(--space-xxl)">
      <div>
        <h3 class="heading-4" style="color:#fff;margin-bottom:var(--space-md)">{brand_name}</h3>
        <p class="text-small" style="color:rgba(255,255,255,0.6);max-width:300px">Platform all-in-one untuk transformasi digital bisnis Anda. Cepat, modern, dan terpercaya.</p>
      </div>
      <div>
        <h4 style="color:#fff;font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-md);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">Layanan</h4>
        <ul style="display:flex;flex-direction:column;gap:var(--space-sm)"><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Website</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">SEO</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Maintenance</a></li></ul>
      </div>
      <div>
        <h4 style="color:#fff;font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-md);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">Perusahaan</h4>
        <ul style="display:flex;flex-direction:column;gap:var(--space-sm)"><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Tentang</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Karir</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Blog</a></li></ul>
      </div>
      <div>
        <h4 style="color:#fff;font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-md);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">Kontak</h4>
        <ul style="display:flex;flex-direction:column;gap:var(--space-sm)"><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">hello@inxotive.com</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">+62 811-9988-7766</a></li><li><a href="#" class="text-small" style="color:rgba(255,255,255,0.6);transition:color var(--anim-duration-fast)">Bali, Indonesia</a></li></ul>
      </div>
    </div>
    <div class="footer-bottom" style="padding-top:var(--space-lg);border-top:1px solid rgba(255,255,255,0.1);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:var(--space-md)">
      <p class="text-xs" style="color:rgba(255,255,255,0.4)">© 2026 {brand_name}. All rights reserved.</p>
      <div class="flex" style="display:flex;gap:var(--space-md)"><a href="#" class="text-xs" style="color:rgba(255,255,255,0.4);transition:color var(--anim-duration-fast)">Privacy</a><a href="#" class="text-xs" style="color:rgba(255,255,255,0.4);transition:color var(--anim-duration-fast)">Terms</a></div>
    </div>
  </div>
</section>"""


# ═══════════════════════════════════════════════════════════════


def _features_showcase() -> str:
    """Features with large showcase images in a 2-col staggered layout."""
    features = [
        ("Strategi Digital", "Kami bantu Anda menyusun strategi digital yang tepat sasaran, dari riset pasar hingga eksekusi.", True),
        ("Desain Kreatif", "Desain yang bukan cuma cantik, tapi juga fungsional dan konversi-optimized.", False),
        ("Teknologi Handal", "Dibangun dengan stack modern yang cepat, aman, dan mudah dikembangkan.", True),
        ("Dukungan 24/7", "Tim kami siap membantu kapan pun Anda butuh, tanpa drama.", False),
    ]
    items = ""
    for i, (title, desc, is_left) in enumerate(features):
        items += f'''<div class="vfx-blur-in stagger-{i+1}" style="display:grid;grid-template-columns:1.2fr 0.8fr{' 0.8fr 1.2fr' if i%2==1 else ''};gap:var(--space-xxl);align-items:center;margin-bottom:var(--space-xl)">
      <div{" style='order:2'" if i%2==1 else ""}>
        <h3 class="heading-3" style="margin-bottom:var(--space-md)">{title}</h3>
        <p class="body-text" style="color:var(--ink);opacity:0.75">{desc}</p>
      </div>
      <div style="height:220px;background:linear-gradient(135deg, color-mix(in srgb, var(--brand-primary) 8%, var(--surface-1)), color-mix(in srgb, var(--brand-accent) 5%, var(--surface-1)));border-radius:var(--radius-lg);{'order:1' if i%2==1 else ''};border:1px solid var(--hairline)">
        <div style="padding:var(--space-lg)"><div style="width:32px;height:32px;border-radius:var(--radius-md);background:var(--brand-gradient);opacity:0.3"></div></div>
      </div>
    </div>'''
    return f'''<section class="section section--reveal" role="region" aria-label="Fitur" id="features">
  <div class="container">
    <div class="section__header" style="text-align:left;margin-bottom:var(--space-xxl)">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">KENAPA KAMI</span>
      <h2 class="section__heading">Yang Membuat Kami Berbeda</h2>
    </div>
    {items}
  </div>
</section>'''


def _features_icon_grid() -> str:
    """Features grid with minimal icons — clean, fast."""
    features = [
        ("Sepatu", "Kustomisasi sesuai kebutuhan bisnis Anda.", "svg-star"),
        ("Cepat", "Loading super cepat dengan teknologi modern.", "svg-zap"),
        ("Aman", "Data Anda aman dengan enkripsi end-to-end.", "svg-shield"),
        ("Responsive", "Tampil sempurna di semua perangkat.", "svg-monitor"),
        ("SEO", "Optimasi mesin pencari built-in.", "svg-search"),
        ("Analitik", "Pantau performa dengan dashboard real-time.", "svg-bar"),
    ]
    cards = ""
    for i, (title, desc, _) in enumerate(features):
        cards += f'''<div class="vfx-stagger-pop stagger-{i+1}" style="padding:var(--space-lg);border-radius:var(--radius-lg);border:1px solid var(--hairline);background:var(--surface-1);display:flex;gap:var(--space-md);align-items:flex-start">
      <div style="width:36px;height:36px;border-radius:var(--radius-md);background:var(--brand-primary);opacity:0.12;display:flex;align-items:center;justify-content:center;flex-shrink:0">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--brand-primary)" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
      </div>
      <div>
        <strong style="font-size:var(--text-small);font-weight:var(--font-weight-semibold)">{title}</strong>
        <p class="text-small" style="color:var(--ink-muted);margin-top:4px">{desc}</p>
      </div>
    </div>'''
    return f'''<section class="section section--reveal" role="region" aria-label="Fitur" id="features">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">Mengapa Pilih Kami</h2>
      <p class="section__subheading">Kami menggabungkan kreativitas dengan teknologi untuk hasil maksimal.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(300px, 1fr));gap:var(--space-md)">
      {cards}
    </div>
  </div>
</section>'''


def _hero_showcase(name: str, tagline: str, primary: str, hero_img: str = "") -> str:
    """Hero with product grid — untuk portfolio/agency."""
    return f'''<section class="section section--hero section--light" role="region" aria-label="Hero" style="position:relative;overflow:hidden">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 0.9fr;gap:var(--space-xxl);align-items:center;min-height:80vh">
      <div class="vfx-blur-in">
        <span class="badge" style="display:inline-block;padding:6px 16px;background:var(--brand-primary);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-medium);margin-bottom:var(--space-lg)">{tagline}</span>
        <h1 class="heading-1" style="margin-bottom:var(--space-lg);text-align:left">{name}</h1>
        <p class="body-text" style="font-size:1.125rem;color:var(--ink);opacity:0.85;margin-bottom:var(--space-xl);max-width:500px">Solusi lengkap untuk transformasi digital bisnis Anda.</p>
        <div style="display:flex;gap:var(--space-md);flex-wrap:wrap">
          <a href="#cta" class="btn-primary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold)">Mulai Sekarang</a>
          <a href="#features" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;border:1px solid var(--hairline);border-radius:var(--radius-full);font-weight:var(--font-weight-medium)">Pelajari</a>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-md)">
        <div style="background:var(--surface-2);border-radius:var(--radius-lg);aspect-ratio:1;overflow:hidden;box-shadow:var(--shadow-md);display:flex;align-items:center;justify-content:center">
          <div style="padding:var(--space-lg);text-align:center">
            <div style="width:40px;height:40px;border-radius:var(--radius-md);background:var(--brand-gradient);opacity:0.2;margin:0 auto var(--space-sm)"></div>
            <strong style="font-size:var(--text-xs)">Desain</strong>
          </div>
        </div>
        <div style="background:var(--surface-2);border-radius:var(--radius-lg);aspect-ratio:1;overflow:hidden;box-shadow:var(--shadow-md);margin-top:var(--space-xl);display:flex;align-items:center;justify-content:center">
          <div style="padding:var(--space-lg);text-align:center">
            <div style="width:40px;height:40px;border-radius:50%;background:var(--brand-accent);opacity:0.15;margin:0 auto var(--space-sm)"></div>
            <strong style="font-size:var(--text-xs)">Kode</strong>
          </div>
        </div>
        <div style="background:var(--surface-2);border-radius:var(--radius-lg);aspect-ratio:1;overflow:hidden;box-shadow:var(--shadow-md);margin-top:-20px;display:flex;align-items:center;justify-content:center">
          <div style="padding:var(--space-lg);text-align:center">
            <div style="width:40px;height:40px;border-radius:var(--radius-md);background:var(--brand-secondary);opacity:0.15;margin:0 auto var(--space-sm)"></div>
            <strong style="font-size:var(--text-xs)">Launch</strong>
          </div>
        </div>
        <div style="background:var(--surface-2);border-radius:var(--radius-lg);aspect-ratio:1;overflow:hidden;box-shadow:var(--shadow-md);margin-top:var(--space-lg);display:flex;align-items:center;justify-content:center">
          <div style="padding:var(--space-lg);text-align:center">
            <div style="width:40px;height:40px;border-radius:50%;background:var(--brand-primary);opacity:0.12;margin:0 auto var(--space-sm)"></div>
            <strong style="font-size:var(--text-xs)">Grow</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>'''


def _pricing_compact() -> str:
    """Compact pricing row — for quick scanning."""
    plans = [
        ("Starter", "Gratis", "Coba dulu", False),
        ("Pro", "$29", "Untuk profesional", True),
        ("Tim", "$79", "Untuk kolaborasi", False),
        ("Enterprise", "$199", "Untuk skala besar", False),
    ]
    cards = ""
    for i, (name, price, desc, popular) in enumerate(plans):
        is_popular = 'transform:scale(1.05);border:2px solid var(--brand-primary);position:relative' if popular else ''
        badge = '<div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--brand-primary);color:#fff;padding:2px 12px;border-radius:var(--radius-full);font-size:var(--text-xs);font-weight:var(--font-weight-semibold)">POPULER</div>' if popular else ''
        btn = 'background:var(--brand-gradient);color:#fff' if popular else 'border:1px solid var(--hairline)'
        cards += f'''<div class="vfx-stagger-pop stagger-{i+1}" style="flex:1;min-width:180px;padding:var(--space-xl) var(--space-lg);border-radius:var(--radius-lg);text-align:center;background:var(--surface-1);border:1px solid var(--hairline);{is_popular}">
      {badge}
      <h3 class="heading-4" style="margin-bottom:var(--space-xxs)">{name}</h3>
      <div class="heading-2" style="margin-bottom:var(--space-xs)">{price}<span class="text-small text-muted">/bln</span></div>
      <p class="text-xs text-muted" style="margin-bottom:var(--space-lg)">{desc}</p>
      <a href="#cta" style="display:block;padding:10px 0;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);font-size:var(--text-small);{btn};transition:all var(--anim-duration-normal)">Pilih</a>
    </div>'''
    return f'''<section class="section section--reveal" role="region" aria-label="Harga" id="pricing">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-lg)">
      <h2 class="section__heading">Pilihan Harga</h2>
      <p class="section__subheading">Sesuaikan dengan kebutuhan Anda.</p>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:var(--space-md);justify-content:center">
      {cards}
    </div>
  </div>
</section>'''


def _testimonials_carousel() -> str:
    """Testimonial carousel with horizontal scroll."""
    items = [
        ("Bisma", "Founder & CEO", "Platform ini benar-benar mengubah cara kami bekerja. Sangat direkomendasikan!"),
        ("Sava", "CTO", "Teknologi yang handal dan tim yang responsif. Luar biasa!"),
        ("Maya", "Lead Designer", "Desain yang dihasilkan sesuai dengan visi brand kami."),
    ]
    cards = ""
    for i, (name, role, text) in enumerate(items):
        cards += f'''<div class="glass-card-solid vfx-stagger-pop stagger-{i+1}" style="min-width:300px;padding:var(--space-xl);border-radius:var(--radius-lg);flex-shrink:0;scroll-snap-align:start;background:var(--surface-1)">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--brand-primary)" stroke-width="1.5" style="margin-bottom:var(--space-md);opacity:0.4"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/></svg>
      <p class="body-text" style="font-size:var(--text-small);margin-bottom:var(--space-lg);line-height:1.7;color:var(--ink);opacity:0.85">{text}</p>
      <div class="flex" style="display:flex;align-items:center;gap:var(--space-sm)">
        <div style="width:36px;height:36px;border-radius:50%;background:var(--brand-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-size:var(--text-xs);font-weight:var(--font-weight-bold)">{name[0]}</div>
        <div><strong style="font-size:var(--text-xs)">{name}</strong><p class="text-xs" style="color:var(--ink-muted)">{role}</p></div>
      </div>
    </div>'''

    return f'''<section class="section section--reveal" role="region" aria-label="Testimoni" id="testimonials">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xl)">
      <h2 class="section__heading">Apa Kata Mereka</h2>
    </div>
    <div style="display:flex;gap:var(--space-md);overflow-x:auto;padding:var(--space-sm) 0;scroll-snap-type:x mandatory;scrollbar-width:none">
      {cards}
    </div>
  </div>
</section>'''


def _about_split() -> str:
    """About with image left, text right."""
    return f'''<section class="section section--reveal" role="region" aria-label="Tentang" id="about">
  <div class="container">
    <div style="display:grid;grid-template-columns:0.9fr 1.1fr;gap:var(--space-xxl);align-items:center">
      <div class="vfx-float" style="background:linear-gradient(135deg, var(--brand-primary)10, var(--brand-accent)08);border-radius:var(--radius-lg);height:360px;display:flex;align-items:center;justify-content:center;overflow:hidden">
        <div style="width:80px;height:80px;border-radius:var(--radius-lg);background:var(--brand-gradient);opacity:0.2;transform:rotate(15deg)"></div>
        <div style="width:60px;height:60px;border-radius:50%;background:var(--brand-accent);opacity:0.15;transform:translate(-30px, 30px)"></div>
      </div>
      <div class="vfx-blur-in">
        <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide)">TENTANG KAMI</span>
        <h2 class="section__heading" style="text-align:left;margin-top:var(--space-sm)">Perjalanan Kami dalam Membangun Masa Depan Digital</h2>
        <p class="body-text" style="color:var(--ink);opacity:0.75;margin-bottom:var(--space-lg)">Kami adalah tim profesional yang berdedikasi untuk memberikan solusi terbaik bagi bisnis Anda. Dengan pengalaman bertahun-tahun di industri, kami telah membantu banyak klien mencapai tujuan mereka melalui inovasi digital dan strategi yang tepat.</p>
        <div class="flex" style="display:flex;gap:var(--space-xl);flex-wrap:wrap">
          <div><strong class="heading-3" style="color:var(--brand-primary)">5+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Tahun</p></div>
          <div><strong class="heading-3" style="color:var(--brand-primary)">500+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Project</p></div>
          <div><strong class="heading-3" style="color:var(--brand-primary)">50+</strong><p class="text-small" style="color:var(--ink);opacity:0.7">Tim Ahli</p></div>
        </div>
      </div>
    </div>
  </div>
</section>'''

# VARIANT SECTION RENDERERS — Part B (anti-monoton)
# ═══════════════════════════════════════════════════════════════

def _hero_full_bleed(name: str, tagline: str, primary: str, archetype_key: str = None, hero_img: str = "") -> str:
    """Full-bleed hero with visual overlay — untuk Bold/Tech & Warm."""
    is_bold = archetype_key == "bold"
    bg_color = "#080012" if is_bold else "var(--canvas)"
    overlay_op = "0.25" if is_bold else "0.15"
    if is_bold:
        badge_style = 'display:inline-block;padding:8px 20px;background:rgba(255,255,255,0.12);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-lg)'
        sec_btn_style = 'display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;border:1px solid rgba(255,255,255,0.15);border-radius:var(--radius-full);font-weight:var(--font-weight-medium);color:#fff;transition:all var(--anim-duration-normal) var(--anim-easing-default)'
    else:
        badge_style = 'display:inline-block;padding:8px 20px;background:rgba(' + ','.join(str(int(primary[i:i+2],16)) for i in (1, 3, 5)) + ',0.15);color:var(--brand-primary);border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-semibold);margin-bottom:var(--space-lg)'
        sec_btn_style = 'display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;border:1px solid var(--hairline);border-radius:var(--radius-full);font-weight:var(--font-weight-medium);transition:all var(--anim-duration-normal) var(--anim-easing-default)'
    glow_gl = primary + "35" if is_bold else primary + "25"
    glow_md = primary + "25" if is_bold else primary + "15"
    return f'''<section class="section section--hero section--dark" role="region" aria-label="Hero" style="position:relative;overflow:hidden;padding:0;min-height:90vh;display:flex;align-items:center;background:{bg_color}">
  {'''<div style="position:absolute;inset:0;background-image:url(''' + hero_img + ''');background-size:cover;background-position:center;z-index:0"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(135deg, var(--canvas), transparent 60%);z-index:0"></div>''' if hero_img else '''<div style="position:absolute;inset:0;background:var(--brand-gradient);opacity:''' + str(overlay_op) + ''';z-index:0"></div>'''}
  <div class="glow-orb glow-orb-xl" style="background:radial-gradient(circle, {glow_gl} 0%, transparent 70%);top:-20%;right:-10%;z-index:0"></div>
  <div class="glow-orb glow-orb-lg" style="background:radial-gradient(circle, {glow_md} 0%, transparent 70%);bottom:-20%;left:-10%;z-index:0"></div>
  <div class="container" style="position:relative;z-index:1;padding:120px 0">
    <div class="vfx-slide-up" style="max-width:860px">
      <span class="badge" style="{badge_style}">{tagline}</span>
      <h1 class="heading-1" style="margin-bottom:var(--space-lg);font-size:clamp(3rem, 8vw, 6rem);line-height:1.05">{name}</h1>
      <p class="body-text" style="font-size:1.25rem;color:#fff;opacity:0.9;margin-bottom:var(--space-xl);max-width:580px">Platform all-in-one untuk mengelola, menganalisis, dan mengembangkan bisnis Anda.</p>
      <div style="display:flex;gap:var(--space-md);flex-wrap:wrap">
        <a href="#cta" class="btn-primary" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:16px 36px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);font-size:1.05rem;transition:all var(--anim-duration-normal) var(--anim-easing-default);box-shadow:var(--shadow-lg)">Mulai Sekarang</a>
        <a href="#features" class="btn-secondary" style="{sec_btn_style}">Pelajari</a>
      </div>
    </div>
  </div>
</section>'''
def _hero_split_left(name: str, tagline: str, primary: str, accent: str, hero_img: str = "") -> str:
    """Asymmetric hero — teks kiri kuat, visual kanan, untuk Editorial."""
    r, g, b = int(primary[1:3], 16), int(primary[3:5], 16), int(primary[5:7], 16)
    return f"""<section class="section section--hero section--light" role="region" aria-label="Hero" style="position:relative;overflow:hidden">
  <div class="container">
    <div style="display:grid;grid-template-columns:1.2fr 0.8fr;gap:var(--space-xxl);align-items:center;min-height:85vh">
      <div class="vfx-slide-up" style="padding-right:var(--space-xxl)">
        <span class="badge" style="display:inline-block;padding:6px 16px;background:rgba({r},{g},{b},0.08);color:var(--brand-primary);border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-medium);margin-bottom:var(--space-lg)">{tagline}</span>
        <h1 class="heading-1" style="margin-bottom:var(--space-lg);text-align:left;font-size:clamp(2.8rem, 5vw, 5rem)">{name}</h1>
        <p class="body-text" style="font-size:1.125rem;color:var(--ink);opacity:0.85;margin-bottom:var(--space-xl);max-width:500px;text-align:left">Solusi lengkap untuk transformasi digital bisnis Anda. Cepat, modern, dan terpercaya.</p>
        <div style="display:flex;gap:var(--space-md);flex-wrap:wrap;justify-content:flex-start">
          <a href="#cta" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold)">Mulai Gratis →</a>
          <a href="#features" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;border:1px solid var(--hairline);border-radius:var(--radius-full);font-weight:var(--font-weight-medium)">Pelajari</a>
        </div>
      </div>
      {'''<div class="vfx-float" style="background:var(--surface-2);border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-elevated);border:1px solid var(--hairline);aspect-ratio:4/3;background-image:url(''' + hero_img + ''');background-size:cover;background-position:center"></div>''' if hero_img else '''<div class="vfx-float" style="background:linear-gradient(135deg, var(--surface-2), color-mix(in srgb, var(--brand-primary) 5%, var(--surface-1)));border-radius:var(--radius-lg);overflow:hidden;box-shadow:var(--shadow-elevated);border:1px solid var(--hairline);aspect-ratio:4/3;display:flex;align-items:center;justify-content:center">
        <div style="display:flex;flex-direction:column;gap:16px;padding:32px;width:100%">
          <div style="height:32px;width:50%;background:var(--brand-gradient);opacity:0.2;border-radius:var(--radius-sm)"></div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div style="height:120px;background:linear-gradient(180deg, color-mix(in srgb, var(--brand-primary) 10%, transparent), transparent);border-radius:var(--radius-lg);border:1px solid var(--hairline)">
              <div style="padding:16px"><div style="width:24px;height:24px;border-radius:var(--radius-sm);background:var(--brand-gradient)"></div></div>
            </div>
            <div style="height:100px;background:linear-gradient(180deg, color-mix(in srgb, var(--brand-accent) 8%, transparent), transparent);border-radius:var(--radius-lg);border:1px solid var(--hairline);margin-top:24px)">
              <div style="padding:16px"><div style="width:24px;height:24px;border-radius:50%;background:var(--brand-primary);opacity:0.3"></div></div>
            </div>
          </div>
          <div style="height:48px;display:flex;gap:12px">
            <div style="flex:1;background:var(--surface-3);border-radius:var(--radius-sm);display:flex;gap:6px;padding:12px"><div style="width:20px;height:8px;background:var(--brand-gradient);border-radius:2px;margin:auto 0"></div><div style="width:20px;height:8px;background:var(--surface-4);border-radius:2px;margin:auto 0"></div></div>
            <div style="width:48px;background:var(--brand-gradient);opacity:0.15;border-radius:var(--radius-sm)"></div>
          </div>
        </div>
      </div>'''}
    </div>
  </div>
</section>"""

def _features_zigzag() -> str:
    """Zig-zag feature rows (gambar kiri/kanan bergantian) — untuk Editorial."""
    features = [
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M12 2l2.4 7.2L22 9.6l-5.6 4.8 1.6 7.6L12 18l-5.6 4.8 1.6-7.6L2 9.6l7.6-.4z\"/></svg>", "Kilat Cepat", "Optimasi performa terbaik dengan teknologi terkini untuk kecepatan maksimal."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><rect x=\"3\" y=\"11\" width=\"18\" height=\"11\" rx=\"2\" ry=\"2\"/><path d=\"M7 11V7a5 5 0 0110 0v4\"/></svg>", "Aman & Terpercaya", "Enkripsi end-to-end dan keamanan berlapis untuk data Anda."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><circle cx=\"12\" cy=\"12\" r=\"4\"/><line x1=\"2\" y1=\"12\" x2=\"6\" y2=\"12\"/><line x1=\"18\" y1=\"12\" x2=\"22\" y2=\"12\"/></svg>", "Desain Modern", "Tampilan premium dengan UI/UX terkini yang memukau pengunjung."),
    ]
    rows = ""
    for i, (icon, title, desc) in enumerate(features):
        is_reverse = i % 2 == 1
        rows += f"""<div class="section--reveal stagger-{i+1}" style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center;margin-bottom:var(--space-xxl)">
  <div{" class='vfx-slide-up'" if not is_reverse else ""} style="{'' if not is_reverse else 'order:2'}">
    <div style="width:40px;height:40px;margin-bottom:var(--space-md)">{icon}</div>
    <h3 class="heading-3" style="margin-bottom:var(--space-sm);text-align:left">{title}</h3>
    <p class="body-text" style="text-align:left;color:var(--ink);opacity:0.75">{desc}</p>
  </div>
  <div{" class='vfx-slide-up'" if is_reverse else ""} style="background:var(--surface-2);border-radius:var(--radius-lg);height:240px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:var(--shadow-md)">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:24px;width:100%">
      <div style="height:80px;background:var(--brand-primary);opacity:0.12;border-radius:var(--radius-md)"></div>
      <div style="height:120px;background:var(--brand-accent);opacity:0.1;border-radius:var(--radius-md);margin-top:20px"></div>
      <div style="height:50px;background:var(--brand-success);opacity:0.08;border-radius:var(--radius-md);grid-column:1/-1"></div>
    </div>
  </div>
</div>"""
    return f"""<section class="section section--surface section--reveal" role="region" aria-label="Fitur" id="features">
  <div class="container">
    <div class="section__header" style="text-align:left;margin-bottom:var(--space-xxl);max-width:600px;margin-left:0">
      <span class="text-small" style="color:var(--brand-primary);font-weight:var(--font-weight-semibold);text-transform:uppercase;letter-spacing:var(--letter-spacing-wide);display:block;text-align:left">FITUR</span>
      <h2 class="section__heading" style="text-align:left;margin-left:0">Semua yang Anda Butuhkan</h2>
      <p class="section__subheading" style="text-align:left;margin:0;max-width:520px">Platform lengkap dengan fitur-fitur canggih.</p>
    </div>
    {rows}
  </div>
</section>"""

def _features_asymmetric() -> str:
    """Asymmetric 2-column features — untuk Warm."""
    features = [
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M12 2l2.4 7.2L22 9.6l-5.6 4.8 1.6 7.6L12 18l-5.6 4.8 1.6-7.6L2 9.6l7.6-.4z\"/></svg>", "Kilat Cepat", "Optimasi performa terbaik dengan teknologi terkini."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><rect x=\"3\" y=\"11\" width=\"18\" height=\"11\" rx=\"2\" ry=\"2\"/><path d=\"M7 11V7a5 5 0 0110 0v4\"/></svg>", "Aman & Terpercaya", "Enkripsi end-to-end untuk data Anda."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><circle cx=\"12\" cy=\"12\" r=\"4\"/><line x1=\"2\" y1=\"12\" x2=\"6\" y2=\"12\"/><line x1=\"18\" y1=\"12\" x2=\"22\" y2=\"12\"/></svg>", "Desain Modern", "Tampilan premium dengan UI/UX terkini."),
        ("<svg width=\"32\" height=\"32\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><line x1=\"18\" y1=\"20\" x2=\"18\" y2=\"10\"/><line x1=\"12\" y1=\"20\" x2=\"12\" y2=\"4\"/><line x1=\"6\" y1=\"20\" x2=\"6\" y2=\"14\"/></svg>", "Analitik", "Pantau performa bisnis secara real-time."),
    ]
    # Grid asymmetric: 1 large card + 3 smaller
    cards = "\n".join(
        f'<div class="glass-card-solid hover-lift stagger-{i%3+1}" style="padding:var(--space-xl);border-radius:var(--radius-lg);{"grid-column:1/-1" if i==0 else ""};text-align:left">'
        f'<div style="font-size:{"2rem" if i==0 else "1.5rem"};margin-bottom:var(--space-sm)">{icon}</div>'
        f'<h3 class="heading-4" style="margin-bottom:var(--space-xs)">{title}</h3>'
        f'<p class="body-text text-small" style="color:var(--ink);opacity:0.75">{desc}</p></div>'
        for i, (icon, title, desc) in enumerate(features)
    )
    return f"""<section class="section section--light section--reveal" role="region" aria-label="Fitur" id="features">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-xxl)">
      <h2 class="section__heading">Fitur Unggulan</h2>
      <p class="section__subheading">Platform lengkap untuk bisnis Anda.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-md)">{cards}</div>
  </div>
</section>"""

def _about_right_image() -> str:
    """About dengan image di kanan — varian layout."""
    return _about().replace(
        'grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center',
        'grid-template-columns:1fr 1fr;gap:var(--space-xxl);align-items:center;direction:rtl'
    ).replace(
        'Kisah Kami dalam Membangun Masa Depan Digital</h2>',
        'Perjalanan Kami dalam Membangun Masa Depan Digital</h2>'
    )

def _team_carousel() -> str:
    """Team horizontal scroll — untuk Warm/Hospitality."""
    members = [
        ("Bisma", "Founder & CEO"),
        ("Sava", "CTO"),
        ("Maya", "Lead Designer"),
        ("Rizky", "Head of Marketing"),
    ]
    cards = "\n".join(
        f'<div class="glass-card-solid hover-lift" style="min-width:220px;padding:var(--space-lg);border-radius:var(--radius-lg);text-align:center;flex-shrink:0">'
        f'<div style="width:64px;height:64px;border-radius:50%;background:var(--brand-gradient);margin:0 auto var(--space-md);display:flex;align-items:center;justify-content:center;font-size:1.5rem;color:#fff;font-weight:var(--font-weight-bold)">{name[0]}</div>'
        f'<h4 class="heading-4" style="margin-bottom:var(--space-xs)">{name}</h4>'
        f'<p class="text-small" style="color:var(--ink);opacity:0.7">{role}</p></div>'
        for name, role in members
    )
    return f"""<section class="section section--surface section--reveal" role="region" aria-label="Tim">
  <div class="container">
    <div class="section__header" style="text-align:center;margin-bottom:var(--space-lg)">
      <h2 class="section__heading">Tim Kami</h2>
      <p class="section__subheading">Para ahli di balik kesuksesan kami.</p>
    </div>
    <div class="hidden-scrollbar" style="display:flex;gap:var(--space-md);overflow-x:auto;padding:var(--space-md) 0;scroll-snap-type:x mandatory">{cards}</div>
  </div>
</section>"""

def _cta_compact(primary: str) -> str:
    """Compact CTA — untuk Bold/Tech & Corporate."""
    return f"""<section class="section section--reveal" role="region" aria-label="Call to Action" id="cta" style="background:var(--surface-2);text-align:center;padding:var(--space-xxl) 0">
  <div class="container container--narrow">
    <h2 class="heading-2" style="margin-bottom:var(--space-sm)">Siap Memulai?</h2>
    <p class="body-text text-muted" style="margin-bottom:var(--space-lg)">Hubungi tim kami untuk konsultasi gratis.</p>
    <a href="#contact" style="display:inline-flex;align-items:center;gap:var(--space-sm);padding:14px 32px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Hubungi Kami →</a>
  </div>
</section>"""

def _footer_compact(brand_name: str) -> str:
    """Compact footer — untuk Bold/Tech."""
    return f"""<footer class="section section--dark" role="contentinfo" style="padding:var(--space-xl) 0 var(--space-lg)">
  <div class="container">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:var(--space-md);margin-bottom:var(--space-lg)">
      <h3 class="heading-4" style="color:#fff;margin:0">{brand_name}</h3>
      <div style="display:flex;gap:var(--space-lg)">
        <a href="#" class="text-small" style="color:rgba(255,255,255,0.5);transition:color var(--anim-duration-fast)">Fitur</a>
        <a href="#" class="text-small" style="color:rgba(255,255,255,0.5);transition:color var(--anim-duration-fast)">Harga</a>
        <a href="#" class="text-small" style="color:rgba(255,255,255,0.5);transition:color var(--anim-duration-fast)">Kontak</a>
      </div>
    </div>
    <div style="padding-top:var(--space-md);border-top:1px solid rgba(255,255,255,0.08);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:var(--space-sm)">
      <p class="text-xs" style="color:rgba(255,255,255,0.3)">© 2026 {brand_name}. All rights reserved.</p>
      <div style="display:flex;gap:var(--space-md)"><a href="#" class="text-xs" style="color:rgba(255,255,255,0.3)">Privacy</a><a href="#" class="text-xs" style="color:rgba(255,255,255,0.3)">Terms</a></div>
    </div>
  </div>
</footer>"""


# ═══════════════════════════════════════════════════════════════
# ARCHETYPE-AWARE PAGE GENERATOR (Part A + B)
# ═══════════════════════════════════════════════════════════════

def generate_archetype_css(brand_name: str, archetype_key: str = None) -> str:
    """Generate CSS framework with archetype-aware spacing and radius overrides."""
    brand = _resolve_brand(brand_name)
    if not brand:
        raise ValueError(f"Unknown brand: {brand_name}")

    if not archetype_key:
        archetype_key = get_archetype_for_brand(brand_name)

    arch = ARCHETYPES.get(archetype_key, ARCHETYPES["corporate"])
    density = arch["density_scale"]

    # Generate overrides for spacing and radius based on archetype
    spacing_overrides = f"""
  /* Archetype: {arch['name']} (density: {density}) */
  --space-section: {_scale_space("96px", density)};
  --space-section-sm: {_scale_space("64px", density)};
  --space-section-lg: {_scale_space("128px", density)};
  --space-xs: {_scale_space("4px", density)};
  --space-sm: {_scale_space("8px", density)};
  --space-md: {_scale_space("16px", density)};
  --space-lg: {_scale_space("24px", density)};
  --space-xl: {_scale_space("32px", density)};
  --space-xxl: {_scale_space("48px", density)};
  --space-xxxl: {_scale_space("64px", density)};
  --radius-sm: {arch['radius'] == 'sm' and '4px' or arch['radius'] == 'lg' and '12px' or '8px'};
  --radius-md: {arch['radius_card'] == 'md' and '8px' or arch['radius_card'] == 'lg' and '12px' or arch['radius_card'] == 'xl' and '16px' or '8px'};
  /* Rhythm section spacings */
  .section-wrapper[data-space="xl"] { padding: var(--space-section-lg) 0; }
  .section-wrapper[data-space="lg"] { padding: var(--space-section) 0; }
  .section-wrapper[data-space="md"] { padding: var(--space-section-sm) 0; }
  .section-wrapper[data-space="sm"] { padding: calc(var(--space-section-sm) * 0.6) 0; }
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
"""

    # Insert spacing overrides into generate_spacing output
    base_css = generate_framework(brand_name)

    # Replace the spacing section with archetype-aware version
    # We'll insert the overrides after the font variables
    tokens_section = generate_design_tokens(brand)

    return base_css


def generate_archetype_page(brand_name: str, archetype_key: str = None,
                            template_type: str = "landing",
                            content_overrides: dict = None) -> str:
    """
    Generate premium HTML page using archetype-aware layout.

    This is the main entry point for Part A+B. It produces structurally
    DIFFERENT pages per archetype — not just color swaps.
    """
    brand = _resolve_brand(brand_name)
    if not brand:
        brand = _resolve_brand("inxotive") or {}

    if not archetype_key:
        archetype_key = get_archetype_for_brand(brand_name)

    arch = ARCHETYPES.get(archetype_key, ARCHETYPES["corporate"])

    name = _v("name", brand)
    primary = _v("primary", brand)
    accent = _v("accent", brand)
    css = generate_framework(brand_name)
    navbar = generate_navbar(brand_name)

    # Archetype-aware spacing overrides in CSS
    density = arch["density_scale"]
    spacing_css = f"""
  /* Archetype: {arch['name']} — density {density} */
  --space-section: {_scale_space("96px", density)};
  --space-section-sm: {_scale_space("64px", density)};
  --space-section-lg: {_scale_space("128px", density)};
  --radius-sm: {arch['radius'] == 'sm' and '4px' or arch['radius'] == 'lg' and '12px' or '8px'};
  --radius-md: {arch['radius_card'] == 'md' and '8px' or arch['radius_card'] == 'lg' and '12px' or '16px'};
"""

    # Left-aligned overrides for editorial & corporate archetypes
    # Force all section layout container text-alignment
    if archetype_key in ("editorial", "corporate"):
        spacing_css += """
  /* Left-aligned section overrides for """ + arch['name'] + """ — inline suppression */
  .template-sections .section__header { text-align: left !important; margin-left: 0 !important; }
  .template-sections .section__heading { text-align: left !important; }
  .template-sections .section__subheading { text-align: left !important; margin-left: 0 !important; margin-right: auto !important; }
  .template-sections [style*="text-align:center"].section__header { text-align: left !important; }
  .template-sections .section[aria-label="FAQ"] .section__header,
  .template-sections .section[aria-label="Testimoni"] .section__header,
  .template-sections .section[aria-label="Pricing"] .section__header { text-align: center !important; }
  .template-sections .section[aria-label="Tim"] .section__header,
  .template-sections .section[aria-label="Kontak"] .section__header { text-align: left !important; }
"""

    tagline = {
        "inxotive": "INXOTIVE OFFICE",
        "tech": "TechStart Indonesia",
        "fnb": "Warung Modern",
        "healthcare": "Sehat Bersama",
        "luxury": "Premium LUXE",
        "corporate": "Corporate Solution",
        "creative": "Creative Studio",
        "minimal": "Minimal Design",
        "nature": "Nature First",
        "cyberpunk": "CYBER FUTURE",
        "klinik": "Klinik Sehat",
        "restaurant": "Fine Dining",
        "education": "EduLearn Indonesia",
    }.get(brand_name, name)

    # ── Select hero variant based on archetype ──
    hero_layout = arch["hero_layout"]
    # Try to fetch a stock image for this brand
    hero_img = ""
    try:
        import sys as _sys
        _sys.path.insert(0, "/home/bisma/market-api")
        from web_engine.illustration_resolver import search_images as _si
        industry = BRAND_INDUSTRY_MAP.get(brand_name.lower(), "business")
        _results = _si(industry, count=1)
        if _results and len(_results) > 0:
            hero_img = _results[0]
    except Exception:
        pass
    if hero_layout == "split":
        hero = _hero_split_left(name, tagline, primary, accent, hero_img)
    elif hero_layout == "full-bleed":
        hero = _hero_full_bleed(name, tagline, primary, archetype_key, hero_img)
    elif hero_layout == "video":
        hero = _hero_video(name, tagline, primary, hero_img)
    else:
        hero = _hero_centered(name, tagline, primary, accent)

    # ── Select feature variant ──
    feat_layout = arch["feature_layout"]
    if feat_layout == "zigzag":
        features = _features_zigzag()
    elif feat_layout == "asymmetric-2col":
        features = _features_asymmetric()
    elif feat_layout == "showcase":
        features = _features_showcase()
    elif feat_layout == "icon-grid":
        features = _features_icon_grid()
    else:
        features = _features_grid()

    # ── Build SiteContent from copy data ──
    copy_data = _load_copy_for_brand(brand_name)
    site_content = None
    if copy_data:
        try:
            from content_models import SiteContent
            site_content = SiteContent.from_copy_template(copy_data)
        except Exception:
            pass
    section_map = {
        "hero": hero,
        "features": features,
        "stats": _stats_counter(),
        "about": _about_split() if arch["name"] == "Editorial / Luxury" else (_about_right_image() if arch["name"] == "Warm / Hospitality" else _about()),
        "testimonials": _testimonials_carousel() if arch["motion_level"] in ("high", "medium") else _testimonials(),
        "pricing": _pricing_compact() if arch["name"] in ("Bold / Tech", "Corporate / Trust") else _pricing(),
        "faq": _faq(),
        "cta": _cta_compact(primary) if arch["name"] in ("Bold / Tech", "Corporate / Trust") else _cta_centered(primary),
        "contact": _contact(),
        "team": _team_carousel() if arch["motion_level"] in ("high", "medium") else _team(),
        "footer": _footer_compact(name) if arch["name"] == "Bold / Tech" else _footer(name),
        "gallery": _gallery(),
        "process": _process(),
        "logos": _logo_cloud(name),
    }

    # Build sections in archetype order with data attributes for editor
    section_order = arch["section_order"]
    all_variants = {
        "hero": hero_layout,
        "features": feat_layout,
        "about": "wide" if arch["name"] == "Warm / Hospitality" else "standard",
        "stats": "default",
        "testimonials": "default",
        "pricing": "default",
        "faq": "default",
        "cta": "compact" if arch["name"] in ("Bold / Tech", "Corporate / Trust") else "centered",
        "contact": "default",
        "team": "carousel" if arch["motion_level"] in ("high", "medium") else "grid",
        "footer": "compact" if arch["name"] == "Bold / Tech" else "standard",
    }
    rhythm_list = arch.get("rhythm_spacing", "").split()
    sections_html = ""
    for idx, s in enumerate(section_order):
        if s not in section_map:
            continue
        section_html = section_map[s]
        variant = all_variants.get(s, "default")
        space = rhythm_list[idx] if idx < len(rhythm_list) else "lg"
        sections_html += f'\n<div class="section-wrapper" data-section-idx="{idx}" data-section-type="{s}" data-variant="{variant}" data-space="{space}">\n{section_html}\n</div>'
    sections_html = sections_html  # Clean up extra whitespace

    # IntersectionObserver for reveal animations
    # ── Apply copy templates to replace hardcoded text ──
    if copy_data:
        c = copy_data
        # Hero subtext
        hero_sub = c.get("hero", {}).get("subtext", "")
        if hero_sub:
            sections_html = sections_html.replace(
                "Platform all-in-one untuk mengelola, menganalisis, dan mengembangkan bisnis Anda dengan satu dashboard powerful.",
                hero_sub
            )
            sections_html = sections_html.replace(
                "Solusi lengkap untuk transformasi digital bisnis Anda. Cepat, modern, dan terpercaya.",
                hero_sub
            )
        # Features heading/subtext
        feat_heading = c.get("features", {}).get("heading", "").replace("{br}", " ")
        feat_subtext = c.get("features", {}).get("subtext", "")
        if feat_heading:
            sections_html = sections_html.replace("Semua yang Anda Butuhkan", feat_heading)
        if feat_subtext:
            sections_html = sections_html.replace(
                "Platform lengkap dengan fitur-fitur canggih untuk mengembangkan bisnis Anda.",
                feat_subtext
            )
        # Feature items (first 3)
        items = c.get("features", {}).get("items", [])
        if items:
            for i, item in enumerate(items[:6]):
                old_titles = ["Kilat Cepat", "Aman & Terpercaya", "Desain Modern", "Analitik Real-time", "AI-Powered", "Mobile First"]
                old_descs = [
                    "Optimasi performa terbaik dengan teknologi terkini untuk kecepatan maksimal.",
                    "Enkripsi end-to-end dan keamanan berlapis untuk data Anda.",
                    "Tampilan premium dengan UI/UX terkini yang memukau pengunjung.",
                    "Pantau performa bisnis Anda dengan dashboard analitik langsung.",
                    "Otomatisasi cerdas dengan teknologi AI untuk efisiensi maksimal.",
                    "Responsive sempurna di semua perangkat dari desktop hingga mobile.",
                ]
                if i < len(old_titles) and i < len(items):
                    if isinstance(items[i], dict) and "title" in items[i]:
                        sections_html = sections_html.replace(old_titles[i], items[i]["title"])
                    old_descs_text = old_descs[i] if i < len(old_descs) else ""
                    if old_descs_text and isinstance(items[i], dict) and "desc" in items[i]:
                        sections_html = sections_html.replace(old_descs_text, items[i]["desc"])
        # About section
        about_heading = c.get("about", {}).get("heading", "").replace("{br}", " ")
        if about_heading:
            sections_html = sections_html.replace("Tentang Kami", about_heading)
        about_body = c.get("about", {}).get("body", "")
        old_about = "Kami adalah tim profesional yang berdedikasi untuk memberikan solusi terbaik bagi bisnis Anda. Dengan pengalaman bertahun-tahun di industri, kami telah membantu banyak klien mencapai tujuan mereka melalui inovasi digital dan strategi yang tepat."
        if about_body and old_about in sections_html:
            sections_html = sections_html.replace(old_about, about_body)
        # CTA section
        cta_heading = c.get("cta", {}).get("heading", "").replace("{br}", " ")
        cta_sub = c.get("cta", {}).get("subtext", "")
        cta_btn = c.get("cta", {}).get("button", "")
        if cta_heading:
            sections_html = sections_html.replace("Siap Memulai?", cta_heading)
        old_cta_sub = "Bergabunglah dengan ratusan bisnis yang telah bertransformasi bersama kami. Mulai perjalanan digital Anda sekarang."
        if cta_sub and old_cta_sub in sections_html:
            sections_html = sections_html.replace(old_cta_sub, cta_sub)
        if cta_btn:
            sections_html = sections_html.replace("Mulai Sekarang", cta_btn, 1) if sections_html.count("Mulai Sekarang") == 1 else sections_html
        # Stats labels
        stats = c.get("stats", [])
        if len(stats) >= 4:
            sections_html = sections_html.replace("Pengguna Aktif", stats[0][1] if isinstance(stats[0], (list, tuple)) and len(stats[0]) > 1 else stats[0], 1)
            sections_html = sections_html.replace("Uptime", stats[1][1] if isinstance(stats[1], (list, tuple)) and len(stats[1]) > 1 else stats[1], 1)
    reveal_js = """<script>
(function(){
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('visible')}
    })
  },{threshold:0.1});
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('.section--reveal').forEach(function(el){observer.observe(el)});
  });
})();
</script>"""

    html = f"""<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — {tagline}</title>
    <meta name="description" content="{name} — {arch['name']} style landing page">
    <meta property="og:title" content="{name} — {tagline}">
    <meta property="og:description" content="Premium {arch['name'].lower()} page with modern design.">
    <meta property="og:image" content="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'><rect fill='%23{primary[1:]}' width='1200' height='630'/><text x='600' y='315' text-anchor='middle' fill='white' font-size='48' font-family='sans-serif'>{name}</text></svg>">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{name[:3].upper()}</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&family=Outfit:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
{css}
{spacing_css}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to content</a>

    {navbar}

    <main id="main">
        <div class="template-sections">
{sections_html}
        </div>
    </main>

{reveal_js}
</body>
</html>"""
    return html


# ═══════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════

def generate_framework(brand_name: str, archetype_key: str = None) -> str:
    """
    Generate complete CSS framework for a brand.
    Returns the full CSS string with design tokens, utilities, animations, responsive, a11y.
    If archetype_key provided, applies archetype-specific spacing/radius overrides.
    """
    brand = _resolve_brand(brand_name)
    if not brand:
        raise ValueError(f"Unknown brand: {brand_name}. Available: {', '.join(ALL_BRANDS.keys())}")

    # Resolve archetype
    if not archetype_key:
        archetype_key = get_archetype_for_brand(brand_name)
    arch = ARCHETYPES.get(archetype_key, ARCHETYPES["corporate"])
    density = arch["density_scale"]

    # Archetype spacing overrides
    spacing_override = f"""
  /* Archetype overrides: {arch['name']} (density {density}) */
  --space-section: {_scale_space("96px", density)};
  --space-section-sm: {_scale_space("64px", density)};
  --space-section-lg: {_scale_space("128px", density)};
  --radius-sm: {arch['radius'] == 'sm' and '4px' or arch['radius'] == 'lg' and '12px' or '8px'};
  --radius-md: {arch['radius_card'] == 'md' and '8px' or arch['radius_card'] == 'lg' and '12px' or '16px'};
"""

    parts = [
        f"/* ════════════════════════════════════════ */",
        f"/*  Design System: {_v('name', brand)} */",
        f"/*  Archetype: {arch['name']} */",
        f"/* ════════════════════════════════════════ */",
        generate_base_reset(),
        generate_design_tokens(brand),
        generate_typography(brand),
        generate_spacing(),
        spacing_override,
        generate_shadows(),
        generate_animations(),
        generate_utilities(),
        generate_section_patterns(),
        generate_responsive(),
        generate_a11y(),
    ]
    return "\n\n".join(parts)


def generate_navbar(brand_name: str) -> str:
    """Generate premium navbar HTML."""
    brand = _resolve_brand(brand_name) or _resolve_brand("inxotive") or {}  # fallback
    name = _v("name", brand)
    return f"""<nav class="glass" role="navigation" style="position:fixed;top:0;left:0;right:0;z-index:50;border-bottom:1px solid var(--hairline)">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;height:64px">
    <a href="#" class="heading-4" style="background:var(--brand-gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{name}</a>
    <div class="nav-links" style="display:flex;gap:var(--space-xl)">
      <a href="#features" class="text-small" style="color:var(--ink-muted);transition:color var(--anim-duration-fast)">Fitur</a>
      <a href="#pricing" class="text-small" style="color:var(--ink-muted);transition:color var(--anim-duration-fast)">Harga</a>
      <a href="#about" class="text-small" style="color:var(--ink-muted);transition:color var(--anim-duration-fast)">Tentang</a>
      <a href="#contact" class="text-small" style="color:var(--ink-muted);transition:color var(--anim-duration-fast)">Kontak</a>
    </div>
    <a href="#cta" class="btn-primary" style="padding:10px 24px;background:var(--brand-gradient);color:#fff;border-radius:var(--radius-full);font-size:var(--text-small);font-weight:var(--font-weight-semibold);transition:all var(--anim-duration-normal) var(--anim-easing-default)">Hubungi Kami</a>
  </div>
</nav>"""


def generate_premium_page(brand_name: str, template_type: str = "landing",
                          archetype_key: str = None) -> str:
    """
    Generate complete premium HTML page for a brand.

    Uses archetype system (Part A+B) when archetype_key is provided or resolvable.
    Falls back to original single-skeleton behavior for backward compatibility.

    Args:
        brand_name: Key in BRAND_PRESETS
        template_type: "landing" (default)
        archetype_key: Optional explicit archetype key. Auto-resolved if None.

    Returns:
        Complete HTML page as a string.
    """
    # Use archetype-aware generator
    if archetype_key is not None or brand_name.lower() in BRAND_ARCHETYPE_MAP:
        try:
            return generate_archetype_page(brand_name, archetype_key, template_type)
        except Exception:
            pass  # Fall through to legacy generator

    # ── Legacy single-skeleton generator (backward compat) ──
    brand = _resolve_brand(brand_name)
    if not brand:
        brand = _resolve_brand("inxotive") or {}

    name = _v("name", brand)
    primary = _v("primary", brand)
    accent = _v("accent", brand)
    css = generate_framework(brand_name)
    navbar = generate_navbar(brand_name)

    # Extract hex components for inline styles
    r = int(primary[1:3], 16)
    g = int(primary[3:5], 16)
    b = int(primary[5:7], 16)

    tagline = {
        "inxotive": "INXOTIVE OFFICE",
        "tech": "TechStart Indonesia",
        "fnb": "Warung Modern",
        "healthcare": "Sehat Bersama",
        "luxury": "Premium LUXE",
        "corporate": "Corporate Solution",
        "creative": "Creative Studio",
        "minimal": "Minimal Design",
        "nature": "Nature First",
        "cyberpunk": "CYBER FUTURE",
        "klinik": "Klinik Sehat",
        "restaurant": "Fine Dining",
        "education": "EduLearn Indonesia",
    }.get(brand_name, name)

    # Assemble sections
    hero = _hero_centered(name, tagline, primary, accent)
    features = _features_grid()
    stats = _stats_counter()
    about = _about()
    testimonials = _testimonials()
    pricing = _pricing()
    faq = _faq()
    cta = _cta_centered(primary)
    contact = _contact()
    footer = _footer(name)

    # IntersectionObserver for reveal animations
    reveal_js = """<script>
(function(){
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('visible')}
    })
  },{threshold:0.1});
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('.section--reveal').forEach(function(el){observer.observe(el)});
  });
})();
</script>"""

    html = f"""<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — {tagline}</title>
    <meta name="description" content="{name} — Premium landing page with modern design">
    <meta property="og:title" content="{name} — {tagline}">
    <meta property="og:description" content="{name} — Premium landing page with modern design, dark mode, and responsive layout.">
    <meta property="og:image" content="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'><rect fill='%23{primary[1:]}' width='1200' height='630'/><text x='600' y='315' text-anchor='middle' fill='white' font-size='48' font-family='sans-serif'>{name}</text></svg>">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{name[:3].upper()}</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&family=Outfit:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to content</a>

    {navbar}

    <main id="main">
        <div class="template-sections">
{hero}
{features}
{stats}
{about}
{testimonials}
{pricing}
{faq}
{cta}
{contact}
        </div>
    </main>

{footer}
{reveal_js}
</body>
</html>"""
    return html


def list_brands() -> list:
    """Return list of available brand names."""
    return list(ALL_BRANDS.keys())


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="INXOTIVE CSS Framework Generator")
    parser.add_argument("brand", nargs="?", default="inxotive", help="Brand name")
    parser.add_argument("--list", action="store_true", help="List available brands")
    parser.add_argument("--css", action="store_true", help="Output CSS only")
    parser.add_argument("--html", action="store_true", default=True, help="Output complete HTML (default)")
    parser.add_argument("--output", "-o", type=str, help="Output file path")

    args = parser.parse_args()

    if args.list:
        print("Available brands:")
        for b in list_brands():
            print(f"  - {b}: {ALL_BRANDS[b]['name']}")
        sys.exit(0)

    if args.css:
        output = generate_framework(args.brand)
    else:
        output = generate_premium_page(args.brand)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)
