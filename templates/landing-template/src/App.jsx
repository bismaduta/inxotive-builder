import React, { useState, useEffect, useRef } from "react";
import { siteConfig as C } from "./config/site.config.js";
import { resolveTheme, themeList } from "./config/themes/index.js";

const T = resolveTheme(C);
const cl = T.colors;
const r = T.radius;

function useReveal() {
  const ref = useRef(null);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(([e]) => e.isIntersecting && setShown(true), { threshold: 0.15 });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  return [ref, shown];
}

function Reveal({ children, delay = 0 }) {
  const [ref, shown] = useReveal();
  return (
    <div ref={ref} style={{ opacity: shown ? 1 : 0, transform: shown ? "translateY(0)" : "translateY(28px)", transition: `opacity 0.7s ease ${delay}s, transform 0.7s ease ${delay}s` }}>
      {children}
    </div>
  );
}

function ContactForm({ theme }) {
  const c = theme.colors;
  const rd = theme.radius;
  const [data, setData] = useState({ nama: "", telp: "", pesan: "" });
  const [sent, setSent] = useState(false);
  const inp = { width: "100%", padding: "15px 18px", borderRadius: rd.card, border: `1.5px solid ${c.primary}22`, fontSize: 15, fontFamily: "inherit", background: "#fff", outline: "none", color: c.text };

  if (sent) return (
    <div style={{ background: "#fff", borderRadius: rd.card, padding: 50, boxShadow: theme.shadow, textAlign: "center" }}>
      <div style={{ fontSize: 48, marginBottom: 16 }}>✓</div>
      <h3 style={{ fontFamily: `'${theme.fonts.heading}',serif`, fontSize: 24, fontWeight: 600, color: c.primary, marginBottom: 10 }}>Terima kasih, {data.nama || "Sahabat"}!</h3>
      <p style={{ opacity: .7 }}>Kami akan menghubungi {data.telp || "Anda"} segera.</p>
      <button onClick={() => { setSent(false); setData({ nama: "", telp: "", pesan: "" }); }}
        style={{ marginTop: 24, background: "none", border: `1.5px solid ${c.primary}`, color: c.primary, padding: "12px 26px", borderRadius: rd.pill, fontWeight: 600, fontFamily: "inherit", cursor: "pointer" }}>
        Kirim lagi
      </button>
    </div>
  );

  return (
    <div style={{ background: "#fff", borderRadius: rd.card, padding: "40px 36px", boxShadow: theme.shadow, textAlign: "left" }}>
      <div style={{ display: "grid", gap: 16 }}>
        <input style={inp} placeholder="Nama lengkap" value={data.nama} onChange={e => setData({ ...data, nama: e.target.value })} />
        <input style={inp} placeholder="No. WhatsApp" value={data.telp} onChange={e => setData({ ...data, telp: e.target.value })} />
        <textarea style={{ ...inp, minHeight: 100, resize: "vertical" }} placeholder="Pesan (opsional)" value={data.pesan} onChange={e => setData({ ...data, pesan: e.target.value })} />
        <button onClick={() => data.nama && data.telp ? setSent(true) : alert("Mohon isi nama & nomor WA")}
          style={{ background: c.primary, color: "#fff", border: "none", padding: 16, borderRadius: rd.card, fontSize: 16, fontWeight: 600, fontFamily: "inherit", cursor: "pointer", boxShadow: theme.shadow }}>
          Kirim Pesan
        </button>
      </div>
    </div>
  );
}

function DnaCard({ theme }) {
  const c = theme.colors; const rd = theme.radius;
  return (
    <div style={{ border: `1px solid ${c.mist}`, borderRadius: rd.card, overflow: "hidden", fontFamily: `'${theme.fonts.body}',sans-serif` }}>
      <style>{`@import url('${theme.fonts.embedUrl}');`}</style>
      <div style={{ background: `linear-gradient(135deg,${c.bg},${c.mist})`, padding: "32px 28px" }}>
        <div style={{ display: "inline-block", padding: "6px 14px", borderRadius: rd.pill, background: "#fff", color: c.primary, fontSize: 11, fontWeight: 700, letterSpacing: 1, marginBottom: 14 }}>{theme.label.toUpperCase()}</div>
        <h3 style={{ fontFamily: `'${theme.fonts.heading}',serif`, fontSize: 26, fontWeight: 700, color: c.text, marginBottom: 10, lineHeight: 1.2 }}>{C.brand.tagline}</h3>
        <p style={{ fontSize: 13, color: c.primary, fontWeight: 300, marginBottom: 18 }}>{C.seo.description}</p>
        <div style={{ display: "flex", gap: 10 }}>
          <div style={{ background: c.primary, color: "#fff", padding: "10px 20px", borderRadius: rd.button, fontSize: 13, fontWeight: 600 }}>Pesan →</div>
          <div style={{ background: "#fff", color: c.text, padding: "10px 20px", borderRadius: rd.button, fontSize: 13, fontWeight: 600, border: `1px solid ${c.mist}` }}>Lihat Layanan</div>
        </div>
      </div>
      <div style={{ padding: "12px 28px 20px", background: "#fff", display: "flex", gap: 8, alignItems: "center" }}>
        {[c.primary, c.secondary, c.accent, c.bg, c.mist].map((col, i) => (
          <div key={i} title={col} style={{ width: 22, height: 22, borderRadius: "50%", background: col, border: "1px solid rgba(0,0,0,.1)" }} />
        ))}
        <span style={{ fontSize: 11, color: "#999", marginLeft: 6 }}>{theme.fonts.heading} · {theme.fonts.body}</span>
      </div>
    </div>
  );
}

function DnaPreview() {
  return (
    <div style={{ fontFamily: "system-ui,sans-serif", padding: "40px 24px", maxWidth: 1200, margin: "0 auto" }}>
      <div style={{ marginBottom: 40 }}><h1 style={{ fontSize: 32, fontWeight: 800, marginBottom: 8 }}>🎨 DNA Preview</h1><p style={{ color: "#666" }}>Alat closing klien — route hanya aktif saat dev.</p></div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(340px,1fr))", gap: 32 }}>{themeList.map(t => <DnaCard key={t.name} theme={t} />)}</div>
    </div>
  );
}

export default function App() {
  if (typeof window !== "undefined" && window.location.pathname === "/dna-preview") return <DnaPreview />;

  const [navSolid, setNavSolid] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => { const fn = () => setNavSolid(window.scrollY > 40); window.addEventListener("scroll", fn); return () => window.removeEventListener("scroll", fn); }, []);
  const scrollTo = id => { setMenuOpen(false); document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); };
  const waUrl = `https://wa.me/${C.contact.whatsapp}?text=Halo ${C.brand.name}, saya ingin tahu lebih lanjut`;

  return (
    <div style={{ fontFamily: `'${T.fonts.body}',sans-serif`, color: cl.text, background: "#fff" }}>
      <style>{`
        @import url('${T.fonts.embedUrl}');
        *{margin:0;padding:0;box-sizing:border-box;}html{scroll-behavior:smooth;}
        .display{font-family:'${T.fonts.heading}',serif;}
        .lift{transition:transform .35s ease,box-shadow .35s ease;}
        .lift:hover{transform:translateY(-6px);box-shadow:${T.shadow};}
        .btn{transition:all .3s ease;cursor:pointer;}
        .btn:hover{transform:translateY(-2px);}
        @keyframes floaty{0%,100%{transform:translateY(0);}50%{transform:translateY(-12px);}}
        @media(max-width:768px){.desktop-nav{display:none!important;}.hamburger{display:block!important;}}
      `}</style>

      <nav style={{ position: "fixed", top: 0, left: 0, right: 0, zIndex: 50, padding: navSolid ? "14px 0" : "22px 0", background: navSolid ? "rgba(255,255,255,.94)" : "transparent", backdropFilter: navSolid ? "blur(10px)" : "none", boxShadow: navSolid ? T.shadow : "none", transition: "all .4s ease" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 38, height: 38, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", color: "#fff", fontSize: 18, fontWeight: 700 }}>{C.brand.logo || "✦"}</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 20 }}>{C.brand.name}</span>
          </div>
          <div className="desktop-nav" style={{ display: "flex", alignItems: "center", gap: 24, color: navSolid ? cl.text : "rgba(255,255,255,.9)" }}>
            {["Layanan", "Tentang", "Kontak"].map(m => (<span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 14, fontWeight: 500, cursor: "pointer" }}>{m}</span>))}
            <a href={waUrl} target="_blank" rel="noreferrer" className="btn" style={{ background: cl.primary, color: "#fff", padding: "10px 20px", borderRadius: r.pill, fontSize: 14, fontWeight: 600, textDecoration: "none", display: "inline-block" }}>WhatsApp</a>
          </div>
          <button className="hamburger" onClick={() => setMenuOpen(o => !o)} style={{ display: "none", background: "none", border: "none", cursor: "pointer", fontSize: 26, color: navSolid ? cl.text : "#fff", padding: 4 }}>{menuOpen ? "✕" : "☰"}</button>
        </div>
        {menuOpen && (
          <div style={{ background: "rgba(255,255,255,.97)", backdropFilter: "blur(10px)", padding: "20px 24px 28px", display: "flex", flexDirection: "column", gap: 16, borderTop: `1px solid ${cl.mist}` }}>
            {["Layanan", "Tentang", "Kontak"].map(m => (<span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 16, fontWeight: 500, cursor: "pointer", padding: "8px 0", borderBottom: `1px solid ${cl.mist}` }}>{m}</span>))}
            <a href={waUrl} target="_blank" rel="noreferrer" className="btn" style={{ background: cl.primary, color: "#fff", padding: 14, borderRadius: r.card, fontSize: 15, fontWeight: 600, textAlign: "center", marginTop: 4, textDecoration: "none" }}>Hubungi WhatsApp</a>
          </div>
        )}
      </nav>

      <header style={{ position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", background: `linear-gradient(135deg,${cl.bg},${cl.mist})`, overflow: "hidden" }}>
        <div style={{ position: "absolute", top: "12%", right: "-6%", width: 420, height: 420, borderRadius: "50%", background: `radial-gradient(circle,${cl.primary}22,transparent 70%)`, animation: "floaty 7s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "8%", left: "-4%", width: 300, height: 300, borderRadius: "50%", background: `radial-gradient(circle,${cl.accent}22,transparent 70%)`, animation: "floaty 9s ease-in-out infinite" }} />
        <div style={{ maxWidth: 1180, margin: "0 auto", padding: "120px 24px 60px", position: "relative", zIndex: 2 }}>
          <Reveal><span style={{ display: "inline-block", padding: "8px 18px", borderRadius: r.pill, background: "#fff", color: cl.primary, fontSize: 13, fontWeight: 600, letterSpacing: 1, marginBottom: 28, boxShadow: T.shadow }}>{C.brand.badge}</span></Reveal>
          {/* FIX: Siklus 3 -- H1=800 heading hierarchy */}
          <Reveal delay={0.1}><h1 className="display" style={{ fontSize: "clamp(38px,6vw,66px)", fontWeight: 800, lineHeight: 1.05, maxWidth: 720, marginBottom: 24 }}>{C.brand.tagline}</h1></Reveal>
          <Reveal delay={0.2}><p style={{ fontSize: 19, lineHeight: 1.6, color: cl.primary, maxWidth: 540, marginBottom: 36, fontWeight: 300 }}>{C.seo.description}</p></Reveal>
          <Reveal delay={0.3}>
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              <a href={waUrl} target="_blank" rel="noreferrer" className="btn" style={{ background: cl.primary, color: "#fff", padding: "16px 32px", borderRadius: r.pill, fontSize: 16, fontWeight: 600, fontFamily: "inherit", boxShadow: T.shadow, textDecoration: "none" }}>Hubungi Kami →</a>
              <button className="btn" onClick={() => scrollTo("layanan")} style={{ background: "#fff", color: cl.text, border: `1.5px solid ${cl.text}22`, padding: "16px 32px", borderRadius: r.pill, fontSize: 16, fontWeight: 600, fontFamily: "inherit" }}>Lihat Layanan</button>
            </div>
          </Reveal>
          <Reveal delay={0.4}>
            <div style={{ display: "flex", gap: 40, marginTop: 64, flexWrap: "wrap" }}>
              {C.stats.map(s => (<div key={s.label}><div className="display" style={{ fontSize: 36, fontWeight: 700, color: cl.primary }}>{s.value}</div><div style={{ fontSize: 14, opacity: .6 }}>{s.label}</div></div>))}
            </div>
          </Reveal>
        </div>
      </header>

      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="layanan" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto", scrollMarginTop: 90 }}>
        <Reveal><div style={{ textAlign: "center", marginBottom: 60 }}><span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>LAYANAN KAMI</span><h2 className="display" style={{ fontSize: "clamp(30px,4vw,44px)", fontWeight: 700, marginTop: 12 }}>Apa yang kami tawarkan</h2></div></Reveal>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))", gap: 26 }}>
          {C.services.map((s, i) => (
            <Reveal key={s.title} delay={i * 0.08}>
              <div className="lift" style={{ background: cl.bg, borderRadius: r.card, padding: "34px 30px", border: `1px solid ${cl.mist}` }}>
                <div style={{ width: 58, height: 58, borderRadius: r.card, background: "#fff", display: "grid", placeItems: "center", fontSize: 28, marginBottom: 20, boxShadow: T.shadow }}>{s.icon}</div>
                <h3 className="display" style={{ fontSize: 20, fontWeight: 600, marginBottom: 10 }}>{s.title}</h3>
                <p style={{ fontSize: 14, lineHeight: 1.6, opacity: .7, fontWeight: 300 }}>{s.desc}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="tentang" style={{ background: cl.secondary, color: "#fff", padding: "100px 24px", scrollMarginTop: 90 }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: 60, alignItems: "center" }}>
          <Reveal><div><span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>TENTANG KAMI</span><h2 className="display" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, margin: "14px 0 24px", lineHeight: 1.15 }}>{C.about.title}</h2><p style={{ fontSize: 16, lineHeight: 1.7, opacity: .8, fontWeight: 300 }}>{C.about.desc}</p></div></Reveal>
          <Reveal delay={0.2}><div style={{ display: "grid", gap: 18 }}>{C.about.highlights.map((h, i) => (<div key={i} style={{ display: "flex", gap: 16, background: "rgba(255,255,255,.05)", padding: "20px 22px", borderRadius: r.card }}><div style={{ color: cl.accent, fontSize: 22 }}>✓</div><div><div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>{h.title}</div><div style={{ fontSize: 14, opacity: .65, fontWeight: 300 }}>{h.desc}</div></div></div>))}</div></Reveal>
        </div>
      </section>

      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="kontak" style={{ background: cl.mist, padding: "100px 24px", scrollMarginTop: 90 }}>
        <div style={{ maxWidth: 720, margin: "0 auto", textAlign: "center" }}>
          <Reveal><span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>KONTAK</span><h2 className="display" style={{ fontSize: "clamp(28px,4.5vw,46px)", fontWeight: 700, margin: "14px 0 18px" }}>{C.seo.description}</h2></Reveal>
          <Reveal delay={0.15}><ContactForm theme={T} /></Reveal>
        </div>
      </section>

      <footer style={{ background: cl.secondary, color: "#fff", padding: "44px 24px 30px" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", display: "flex", flexWrap: "wrap", gap: 20, justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 34, height: 34, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", fontSize: 16 }}>✦</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 18 }}>{C.brand.name}</span>
          </div>
          <div style={{ fontSize: 12, opacity: .4 }}>Speculative Demo — INXOTIVE</div>
        </div>
      </footer>
    </div>
  );
}
