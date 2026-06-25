"""
CONTENT MODELS — Content-first architecture for INXOTIVE Builder.
Each client's data is represented as JSON, separate from layout.
The same layout can be reused with different content.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class HeroContent:
    eyebrow: str = ""
    headline: str = ""
    subtext: str = ""
    cta: str = "Mulai Sekarang"
    cta_link: str = "#cta"
    cta_alt: str = "Pelajari"
    cta_alt_link: str = "#features"

@dataclass
class FeatureItem:
    title: str = ""
    desc: str = ""
    icon: str = "star"

@dataclass
class FeaturesContent:
    heading: str = ""
    subtext: str = ""
    items: List[FeatureItem] = field(default_factory=list)

@dataclass
class StatItem:
    number: str = ""
    label: str = ""

@dataclass
class AboutContent:
    heading: str = ""
    body: str = ""
    stats: List[StatItem] = field(default_factory=list)

@dataclass
class TestimonialItem:
    name: str = ""
    role: str = ""
    text: str = ""
    avatar: str = ""

@dataclass
class PricingTier:
    name: str = ""
    price: str = ""
    period: str = ""
    desc: str = ""
    features: List[str] = field(default_factory=list)
    popular: bool = False

@dataclass
class CTAContent:
    heading: str = ""
    subtext: str = ""
    button: str = ""

@dataclass
class SiteContent:
    brand: str = ""
    tagline: str = ""
    hero: HeroContent = field(default_factory=HeroContent)
    features: FeaturesContent = field(default_factory=FeaturesContent)
    stats: List[StatItem] = field(default_factory=list)
    about: AboutContent = field(default_factory=AboutContent)
    testimonials: List[TestimonialItem] = field(default_factory=list)
    pricing: List[PricingTier] = field(default_factory=list)
    cta: CTAContent = field(default_factory=CTAContent)

    def to_dict(self) -> dict:
        """Serialize to dict for JSON."""
        import json
        return json.loads(json.dumps(self, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o)))

    @staticmethod
    def from_copy_template(copy: dict) -> 'SiteContent':
        """Build SiteContent from copy_templates format."""
        sc = SiteContent()
        hero = copy.get("hero", {})
        sc.hero = HeroContent(
            eyebrow=hero.get("eyebrow", ""),
            headline=hero.get("headline", ""),
            subtext=hero.get("subtext", ""),
            cta=hero.get("cta", "Mulai Sekarang"),
        )
        feat = copy.get("features", {})
        items = [FeatureItem(title=i.get("title",""), desc=i.get("desc","")) for i in feat.get("items", [])]
        sc.features = FeaturesContent(
            heading=feat.get("heading",""),
            subtext=feat.get("subtext",""),
            items=items,
        )
        stats = copy.get("stats", [])
        sc.stats = [StatItem(number=s[0], label=s[1]) for s in stats]
        about = copy.get("about", {})
        sc.about = AboutContent(heading=about.get("heading",""), body=about.get("body",""))
        testi = copy.get("testimonial", {})
        sc.testimonials = [TestimonialItem(name=testi.get("name",""), role=testi.get("role",""), text=testi.get("text",""))]
        tiers = copy.get("pricing_tiers", [])
        sc.pricing = [PricingTier(name=t["name"], price=t["price"], period=t.get("period",""), desc=t.get("desc",""), features=t.get("features",[]), popular=t.get("popular",False)) for t in tiers]
        cta = copy.get("cta", {})
        sc.cta = CTAContent(heading=cta.get("heading",""), subtext=cta.get("subtext",""), button=cta.get("button",""))
        return sc


def content_to_json(content: SiteContent) -> str:
    """Serialize SiteContent to JSON for storage/API."""
    import json
    return json.dumps(content.to_dict(), indent=2)


def json_to_content(data: dict) -> SiteContent:
    """Deserialize JSON to SiteContent."""
    sc = SiteContent()
    h = data.get("hero", {})
    sc.hero = HeroContent(**h)
    f = data.get("features", {})
    items = [FeatureItem(**i) for i in f.get("items", [])]
    sc.features = FeaturesContent(heading=f.get("heading",""), subtext=f.get("subtext",""), items=items)
    sc.stats = [StatItem(**s) for s in data.get("stats", [])]
    a = data.get("about", {})
    sc.about = AboutContent(heading=a.get("heading",""), body=a.get("body",""))
    sc.testimonials = [TestimonialItem(**t) for t in data.get("testimonials", [])]
    sc.pricing = [PricingTier(**p) for p in data.get("pricing", [])]
    c = data.get("cta", {})
    sc.cta = CTAContent(**c)
    return sc


if __name__ == "__main__":
    from copy_templates import get_copy

    # Demo: convert F&B copy to SiteContent
    copy = get_copy("fnb")
    sc = SiteContent.from_copy_template(copy)
    print("=== SITE CONTENT (F&B) ===")
    print(f"Brand: {copy.get('brand_tone', '')}")
    print(f"Hero: {sc.hero.headline[:50]}")
    print(f"Features: {len(sc.features.items)} items")
    print(f"Pricing: {len(sc.pricing)} tiers")
    print(f"\nJSON preview:")
    print(content_to_json(sc)[:300] + "...")
