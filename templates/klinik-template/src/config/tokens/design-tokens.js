// ============================================================
// DESIGN TOKEN SYSTEM — INXOTIVE v2
// Master token file — semua nilai desain terpusat di sini
// ============================================================

// ─── 1. COLOR PRIMITIVES ─────────────────────────────────────
export const primitives = {
  white: "#FFFFFF",
  black: "#000000",
  transparent: "transparent",
  current: "currentColor",

  neutral: {
    50: "#FAFAFA", 100: "#F5F5F5", 200: "#E5E5E5",
    300: "#D4D4D4", 400: "#A3A3A3", 500: "#737373",
    600: "#525252", 700: "#404040", 800: "#262626",
    900: "#171717", 950: "#0A0A0A",
  },

  warmNeutral: {
    50: "#FDFBF7", 100: "#F9F5ED", 200: "#F0E8D8",
    300: "#E4D7BE", 400: "#D4C2A3", 500: "#BFA785",
    600: "#A68B66", 700: "#8A704C", 800: "#6F5838",
    900: "#564228", 950: "#3C2D1A",
  },

  gold: {
    50: "#FDF8E8", 100: "#F9EDC5", 200: "#F3DF9E",
    300: "#EDCF72", 400: "#E8C04F", 500: "#D4A843",
    600: "#B8965A", 700: "#A07D42", 800: "#866830",
    900: "#523F15", 950: "#382B0C",
  },

  oxblood: {
    50: "#FDF2F2", 100: "#F9E0E0", 200: "#F0C2C2",
    300: "#E39D9D", 400: "#D17474", 500: "#B84D4D",
    600: "#9A3636", 700: "#7F2A2A", 800: "#671F1F",
    900: "#4D1616", 950: "#2E0A0A",
  },

  teal: {
    50: "#F0FDFA", 100: "#CCFBF1", 200: "#99F6E4",
    300: "#5EEAD4", 400: "#2DD4BF", 500: "#14B8A6",
    600: "#0D9488", 700: "#0F766E", 800: "#115E59",
    900: "#134E4A", 950: "#042F2E",
  },
};

// ─── 2. TYPOGRAPHY ──────────────────────────────────────────
export const typography = {
  fonts: {
    display: "'Instrument Serif', serif",
    heading: "'Fraunces', serif",
    body: "'Geist', sans-serif",
    alt: "'DM Sans', sans-serif",
    mono: "'JetBrains Mono', monospace",
  },

  scale: {
    display: { size: "clamp(3.5rem,8vw,7rem)", lineHeight: 0.95, letterSpacing: "-0.03em", weight: 400 },
    h1:      { size: "clamp(2.5rem,5vw,4rem)", lineHeight: 1.05, letterSpacing: "-0.02em", weight: 600 },
    h2:      { size: "clamp(2rem,4vw,3rem)",   lineHeight: 1.15, letterSpacing: "-0.015em", weight: 600 },
    h3:      { size: "clamp(1.5rem,3vw,2rem)", lineHeight: 1.25, letterSpacing: "-0.01em", weight: 500 },
    h4:      { size: "clamp(1.25rem,2vw,1.5rem)", lineHeight: 1.3, letterSpacing: "0", weight: 500 },
    body:    { size: "1rem", lineHeight: 1.6, letterSpacing: "0", weight: 400 },
    bodyLg:  { size: "1.125rem", lineHeight: 1.65, letterSpacing: "0", weight: 400 },
    bodySm:  { size: "0.875rem", lineHeight: 1.5, letterSpacing: "0", weight: 400 },
    caption: { size: "0.75rem", lineHeight: 1.4, letterSpacing: "0.01em", weight: 400 },
    overline: { size: "0.7rem", lineHeight: 1, letterSpacing: "0.1em", weight: 600, textTransform: "uppercase" },
  },

  weights: {
    thin: 100, light: 300, regular: 400, medium: 500,
    semibold: 600, bold: 700, black: 900,
  },
};

// ─── 3. SPACING (4px base) ──────────────────────────────────
export const spacing = {
  0: "0px", px: "1px", 0.5: "0.125rem", 1: "0.25rem",
  1.5: "0.375rem", 2: "0.5rem", 2.5: "0.625rem", 3: "0.75rem",
  3.5: "0.875rem", 4: "1rem", 5: "1.25rem", 6: "1.5rem",
  7: "1.75rem", 8: "2rem", 9: "2.25rem", 10: "2.5rem",
  11: "2.75rem", 12: "3rem", 14: "3.5rem", 16: "4rem",
  20: "5rem", 24: "6rem", 28: "7rem", 32: "8rem",
  36: "9rem", 40: "10rem",
};

// ─── 4. BREAKPOINTS ─────────────────────────────────────────
export const breakpoints = {
  sm: "640px", md: "768px", lg: "1024px", xl: "1280px", "2xl": "1536px",
};

// ─── 5. SHADOWS ─────────────────────────────────────────────
export const shadows = {
  none: "none",
  sm: "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
  md: "0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04)",
  lg: "0 10px 15px rgba(0,0,0,0.06), 0 4px 6px rgba(0,0,0,0.04)",
  xl: "0 20px 25px rgba(0,0,0,0.08), 0 8px 10px rgba(0,0,0,0.04)",
  glow: "0 0 20px rgba(232,192,79,0.15)",
  glowStrong: "0 0 30px rgba(232,192,79,0.25)",
};

// ─── 6. ANIMATION ───────────────────────────────────────────
export const animation = {
  duration: { fast: "150ms", normal: "300ms", slow: "500ms", slower: "800ms", glacial: "1200ms" },
  easing: {
    out: "cubic-bezier(0.16,1,0.3,1)",
    inOut: "cubic-bezier(0.65,0,0.35,1)",
    spring: "cubic-bezier(0.34,1.56,0.64,1)",
    smooth: "cubic-bezier(0.2,0,0,1)",
    linear: "linear",
  },
  delay: { none: "0ms", short: "100ms", medium: "250ms", long: "500ms", stagger: "60ms" },
};

// ─── 7. BORDER RADIUS ───────────────────────────────────────
export const borderRadius = {
  none: "0px", sm: "4px", md: "8px", lg: "12px", xl: "16px", "2xl": "20px", full: "9999px",
};

// ─── 8. BREAKPOINT QUERY HELPER ─────────────────────────────
export const mq = {
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
};
