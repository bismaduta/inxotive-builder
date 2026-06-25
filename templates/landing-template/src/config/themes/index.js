import clinicalTrust from "./clinical-trust.js";
import warmFamily from "./warm-family.js";
import precisionLab from "./precision-lab.js";
import heritageCare from "./heritage-care.js";
import freshApotek from "./fresh-apotek.js";
import premiumResto from "./premium-resto.js";
import premiumInxotive from "./premium-inxotive.js";

export const themes = {
  "clinical-trust": clinicalTrust,
  "warm-family": warmFamily,
  "precision-lab": precisionLab,
  "heritage-care": heritageCare,
  "fresh-apotek": freshApotek,
  "premium-resto": premiumResto,
  "premium-inxotive": premiumInxotive,
};

export function resolveTheme(siteConfig) {
  const base = themes[siteConfig.theme] || themes["clinical-trust"];
  // brand.colors di config bisa override warna DNA
  return {
    ...base,
    colors: { ...base.colors, ...siteConfig.brand?.colors },
  };
}

export const themeList = Object.values(themes);
