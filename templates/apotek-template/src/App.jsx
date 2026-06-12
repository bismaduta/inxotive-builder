import React, { useState, useEffect, useRef } from "react";
import { siteConfig as C } from "./config/site.config.js";
import { resolveTheme } from "./config/themes/index.js";

const T = resolveTheme(C);
const cl = T.colors;
const r = T.radius;

function useReveal() {
  const ref = useRef(null);
  const [s, set] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const o = new IntersectionObserver(([e]) => e.isIntersecting && set(true), { threshold: 0.15 });
    o.observe(ref.current);
    return () => o.disconnect();
  }, []);
  return [ref, s];
}

function R({ children, d = 0 }) {
  const [ref, s] = useReveal();
  return (
    <div ref={ref} style={{ opacity: s ? 1 : 0, transform: s ? "translateY(0)" : "translateY(24px)", transition: `opacity .6s ease ${d}s,transform .6s ease ${d}s` }}>
      {children}
    </div>
  );
}

export default function App() {
  const [nav, setNav] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => {
    const f = () => setNav(window.scrollY > 40);
    window.addEventListener("scroll", f);
    return () => window.removeEventListener("scroll", f);
  }, []);
  const go = id => { setMenuOpen(false); document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); };

  const waUrl = `https://wa.me/${C.contact.whatsapp}?text=Halo ${C.brand.name}, saya ingin pesan obat`;

  return (
    <div style={{ fontFamily: `'${T.fonts.body}',sans-serif`, color: cl.text, background: "#fff" }}>
      <style>{`
        @import url('${T.fonts.embedUrl}');
        *{margin:0;padding:0;box-sizing:border-box;}html{scroll-behavior:smooth;}
        .dp{font-family:'${T.fonts.heading}',serif;}
        .lift{transition:transform .3s,box-shadow .3s;}
        .lift:hover{transform:translateY(-5px);box-shadow:${T.shadow};}
        .btn{transition:all .3s;cursor:pointer;}
        .btn:hover{transform:translateY(-2px);}
        @keyframes bob{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
        @media(max-width:768px){.desktop-nav{display:none!important;}.hamburger{display:block!important;}}
      `}</style>

      {/* NAV */}
      <nav style={{ position: "fixed", top: 0, left: 0, right: 0, zIndex: 50, padding: nav ? "12px 0" : "20px 0", background: nav ? `rgba(253,246,238,.95)` : "transparent", backdropFilter: nav ? "blur(10px)" : "none", boxShadow: nav ? `0 2px 20px ${cl.secondary}14` : "none", transition: "all .4s" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 38, height: 38, borderRadius: 12, background: cl.primary, display: "grid", placeItems: "center", fontSize: 20 }}>⚕</div>
            <span className="dp" style={{ fontWeight: 700, fontSize: 20, color: cl.secondary }}>{C.brand.name}</span>
          </div>
          <div className="desktop-nav" style={{ display: "flex", alignItems: "center", gap: 24 }}>
            {["Produk", "Tentang", "Kontak"].map(m => (
              <span key={m} onClick={() => go(m.toLowerCase())} style={{ fontSize: 15, fontWeight: 500, cursor: "pointer", color: cl.secondary }}>{m}</span>
            ))}
            <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "10px 20px", borderRadius: 30, fontSize: 14, fontWeight: 600, fontFamily: "inherit" }}>WhatsApp</button>
          </div>
          <button className="hamburger" onClick={() => setMenuOpen(o => !o)} style={{ display: "none", background: "none", border: "none", cursor: "pointer", fontSize: 26, color: nav ? cl.secondary : cl.primary, padding: 4 }}>{menuOpen ? "✕" : "☰"}</button>
        </div>
        {menuOpen && (
          <div style={{ background: `rgba(253,246,238,.97)`, backdropFilter: "blur(10px)", padding: "20px 24px 28px", display: "flex", flexDirection: "column", gap: 16, borderTop: `1px solid ${cl.sand}` }}>
            {["Produk", "Tentang", "Kontak"].map(m => (
              <span key={m} onClick={() => go(m.toLowerCase())} style={{ fontSize: 16, fontWeight: 500, cursor: "pointer", padding: "8px 0", borderBottom: `1px solid ${cl.sand}` }}>{m}</span>
            ))}
            <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: cl.primary, color: "#fff", border: "none", padding: 14, borderRadius: 14, fontSize: 15, fontWeight: 600, fontFamily: "inherit", marginTop: 4 }}>WhatsApp Sekarang</button>
          </div>
        )}
      </nav>

      {/* HERO */}
      <header style={{ minHeight: "100vh", display: "flex", alignItems: "center", background: `linear-gradient(135deg,${cl.bg},${cl.sand})`, position: "relative", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: "10%", right: "-5%", width: 380, height: 380, borderRadius: "50%", background: `radial-gradient(${cl.primary}18,transparent 70%)`, animation: "bob 8s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "5%", left: "-3%", width: 260, height: 260, borderRadius: "50%", background: `radial-gradient(${cl.accent}18,transparent 70%)`, animation: "bob 10s ease-in-out infinite" }} />
        <div style={{ maxWidth: 1100, margin: "0 auto", padding: "120px 24px 60px", position: "relative", zIndex: 2 }}>
          <R><span style={{ display: "inline-block", padding: "8px 18px", borderRadius: 30, background: "#fff", color: cl.primary, fontSize: 13, fontWeight: 600, letterSpacing: 1, marginBottom: 24, boxShadow: `0 4px 14px ${cl.secondary}14` }}>{C.brand.badge}</span></R>
          <R d={.1}><h1 className="dp" style={{ fontSize: "clamp(36px,5.5vw,62px)", fontWeight: 700, lineHeight: 1.1, maxWidth: 680, marginBottom: 20 }}>{C.brand.tagline}</h1></R>
          <R d={.2}><p style={{ fontSize: 18, lineHeight: 1.65, color: cl.primary, maxWidth: 520, marginBottom: 32, fontWeight: 300 }}>{C.seo.description}</p></R>
          <R d={.3}>
            <div style={{ display: "flex", gap: 14, flexWrap: "wrap" }}>
              <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "15px 30px", borderRadius: 30, fontSize: 16, fontWeight: 600, fontFamily: "inherit", boxShadow: `0 10px 28px ${cl.primary}44` }}>Pesan via WhatsApp →</button>
              <button className="btn" onClick={() => go("produk")} style={{ background: "#fff", color: cl.secondary, border: `1.5px solid ${cl.secondary}22`, padding: "15px 30px", borderRadius: 30, fontSize: 16, fontWeight: 600, fontFamily: "inherit" }}>Lihat Produk</button>
            </div>
          </R>
          <R d={.4}>
            <div style={{ display: "flex", gap: 36, marginTop: 56, flexWrap: "wrap" }}>
              {C.stats.map(s => (
                <div key={s.label}>
                  <div className="dp" style={{ fontSize: 34, fontWeight: 700, color: cl.primary }}>{s.value}</div>
                  <div style={{ fontSize: 13, opacity: .6 }}>{s.label}</div>
                </div>
              ))}
            </div>
          </R>
        </div>
      </header>

      {/* PRODUK */}
      <section id="produk" style={{ padding: "90px 24px", maxWidth: 1100, margin: "0 auto" }}>
        <R>
          <div style={{ textAlign: "center", marginBottom: 56 }}>
            <span style={{ color: cl.accent, fontWeight: 600, fontSize: 13, letterSpacing: 2 }}>LAYANAN & PRODUK</span>
            <h2 className="dp" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, marginTop: 10 }}>Semua kebutuhan kesehatan Anda</h2>
          </div>
        </R>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(270px,1fr))", gap: 24 }}>
          {C.services.map((p, i) => (
            <R key={p.title} d={i * .07}>
              <div className="lift" style={{ background: cl.bg, borderRadius: 20, padding: "30px 26px", border: `1px solid ${cl.sand}` }}>
                <div style={{ width: 54, height: 54, borderRadius: 14, background: "#fff", display: "grid", placeItems: "center", fontSize: 26, marginBottom: 18, boxShadow: `0 4px 12px ${cl.secondary}0f` }}>{p.icon}</div>
                <h3 className="dp" style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>{p.title}</h3>
                <p style={{ fontSize: 14, lineHeight: 1.6, opacity: .7, fontWeight: 300 }}>{p.desc}</p>
              </div>
            </R>
          ))}
        </div>
      </section>

      {/* TENTANG */}
      <section id="tentang" style={{ background: cl.secondary, color: "#fff", padding: "90px 24px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: 56, alignItems: "center" }}>
          <R>
            <div>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 13, letterSpacing: 2 }}>TENTANG KAMI</span>
              <h2 className="dp" style={{ fontSize: "clamp(26px,4vw,40px)", fontWeight: 700, margin: "12px 0 20px", lineHeight: 1.2 }}>{C.about.title}</h2>
              <p style={{ fontSize: 15, lineHeight: 1.7, opacity: .8, fontWeight: 300 }}>{C.about.desc}</p>
            </div>
          </R>
          <R d={.15}>
            <div style={{ display: "grid", gap: 16 }}>
              {C.about.highlights.map((h, i) => (
                <div key={i} style={{ display: "flex", gap: 14, background: "rgba(255,255,255,.05)", padding: "18px 20px", borderRadius: 14 }}>
                  <div style={{ color: cl.accent, fontSize: 20 }}>✓</div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 3 }}>{h.title}</div>
                    <div style={{ fontSize: 13, opacity: .6, fontWeight: 300 }}>{h.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </R>
        </div>
      </section>

      {/* KONTAK */}
      <section id="kontak" style={{ background: cl.bg, padding: "90px 24px" }}>
        <div style={{ maxWidth: 680, margin: "0 auto", textAlign: "center" }}>
          <R>
            <span style={{ color: cl.accent, fontWeight: 600, fontSize: 13, letterSpacing: 2 }}>HUBUNGI KAMI</span>
            <h2 className="dp" style={{ fontSize: "clamp(28px,4vw,44px)", fontWeight: 700, margin: "12px 0 14px" }}>Pesan obat atau konsultasi sekarang</h2>
            <p style={{ fontSize: 16, color: cl.primary, marginBottom: 36, fontWeight: 300 }}>Hubungi kami via WhatsApp atau kunjungi apotek kami langsung.</p>
          </R>
          <R d={.1}>
            <div style={{ display: "grid", gap: 16 }}>
              <a href={waUrl} target="_blank" rel="noreferrer" style={{ display: "block", background: cl.green, color: "#fff", padding: "18px", borderRadius: 16, fontSize: 17, fontWeight: 600, fontFamily: "inherit", textDecoration: "none", boxShadow: `0 10px 28px ${cl.green}44` }}>
                💬 Chat WhatsApp Sekarang
              </a>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                <div style={{ background: "#fff", borderRadius: 16, padding: "22px", boxShadow: `0 4px 16px ${cl.secondary}0f` }}>
                  <div style={{ fontSize: 24, marginBottom: 8 }}>📍</div>
                  <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>Alamat</div>
                  <div style={{ fontSize: 13, opacity: .65, fontWeight: 300 }}>{C.contact.address}</div>
                </div>
                <div style={{ background: "#fff", borderRadius: 16, padding: "22px", boxShadow: `0 4px 16px ${cl.secondary}0f` }}>
                  <div style={{ fontSize: 24, marginBottom: 8 }}>🕐</div>
                  <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>Jam Buka</div>
                  <div style={{ fontSize: 13, opacity: .65, fontWeight: 300 }}>{C.hours.map(h => `${h.day}: ${h.time}`).join(" · ")}</div>
                </div>
              </div>
            </div>
          </R>
        </div>
      </section>

      {/* FOOTER */}
      <footer style={{ background: cl.secondary, color: "#fff", padding: "40px 24px 28px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto", display: "flex", flexWrap: "wrap", gap: 24, justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 32, height: 32, borderRadius: 10, background: cl.primary, display: "grid", placeItems: "center", fontSize: 17 }}>⚕</div>
            <span className="dp" style={{ fontWeight: 700, fontSize: 18 }}>{C.brand.name}</span>
          </div>
          <div style={{ fontSize: 13, opacity: .5 }}>Website oleh <strong style={{ color: cl.accent }}>INXOTIVE</strong></div>
        </div>
      </footer>
    </div>
  );
}
