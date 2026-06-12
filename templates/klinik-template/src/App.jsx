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
  const [data, setData] = useState({ nama: "", telp: "", layanan: C.services[0]?.title || "", pesan: "" });
  const [sent, setSent] = useState(false);
  const inp = { width: "100%", padding: "15px 18px", borderRadius: rd.card, border: `1.5px solid ${c.primary}22`, fontSize: 15, fontFamily: "inherit", background: "#fff", outline: "none", color: c.text };

  if (sent) return (
    <div style={{ background: "#fff", borderRadius: rd.card, padding: 50, boxShadow: theme.shadow, textAlign: "center" }}>
      <div style={{ fontSize: 48, marginBottom: 16 }}>✓</div>
      <h3 style={{ fontFamily: `'${theme.fonts.heading}',serif`, fontSize: 26, fontWeight: 600, color: c.primary, marginBottom: 10 }}>Terima kasih, {data.nama || "Sahabat Sehat"}!</h3>
      <p style={{ opacity: .7 }}>Tim kami akan segera menghubungi nomor {data.telp || "Anda"}.</p>
      <button onClick={() => { setSent(false); setData({ nama: "", telp: "", layanan: C.services[0]?.title || "", pesan: "" }); }}
        style={{ marginTop: 24, background: "none", border: `1.5px solid ${c.primary}`, color: c.primary, padding: "12px 26px", borderRadius: rd.pill, fontWeight: 600, fontFamily: "inherit", cursor: "pointer" }}>
        Buat janji lain
      </button>
    </div>
  );

  return (
    <div style={{ background: "#fff", borderRadius: rd.card, padding: "40px 36px", boxShadow: theme.shadow, textAlign: "left" }}>
      <div style={{ display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <input style={inp} placeholder="Nama lengkap" value={data.nama} onChange={e => setData({ ...data, nama: e.target.value })} />
          <input style={inp} placeholder="No. WhatsApp" value={data.telp} onChange={e => setData({ ...data, telp: e.target.value })} />
        </div>
        <select style={inp} value={data.layanan} onChange={e => setData({ ...data, layanan: e.target.value })}>
          {C.services.map(s => <option key={s.title}>{s.title}</option>)}
        </select>
        <textarea style={{ ...inp, minHeight: 100, resize: "vertical" }} placeholder="Keluhan atau catatan (opsional)" value={data.pesan} onChange={e => setData({ ...data, pesan: e.target.value })} />
        <button onClick={() => data.nama && data.telp ? setSent(true) : alert("Mohon isi nama & nomor WhatsApp")}
          style={{ background: c.primary, color: "#fff", border: "none", padding: 16, borderRadius: rd.card, fontSize: 16, fontWeight: 600, fontFamily: "inherit", cursor: "pointer", boxShadow: theme.shadow }}>
          Kirim Permintaan Janji
        </button>
      </div>
    </div>
  );
}

// Komponen preview satu DNA — dipakai di /dna-preview
function DnaCard({ theme }) {
  const c = theme.colors;
  const rd = theme.radius;
  return (
    <div style={{ border: `1px solid ${c.mist}`, borderRadius: rd.card, overflow: "hidden", fontFamily: `'${theme.fonts.body}',sans-serif` }}>
      <style>{`@import url('${theme.fonts.embedUrl}');`}</style>
      {/* Mini hero */}
      <div style={{ background: `linear-gradient(135deg,${c.bg},${c.mist})`, padding: "32px 28px" }}>
        <div style={{ display: "inline-block", padding: "6px 14px", borderRadius: rd.pill, background: "#fff", color: c.primary, fontSize: 11, fontWeight: 700, letterSpacing: 1, marginBottom: 14 }}>
          {theme.label.toUpperCase()}
        </div>
        <h3 style={{ fontFamily: `'${theme.fonts.heading}',serif`, fontSize: 26, fontWeight: 700, color: c.text, marginBottom: 10, lineHeight: 1.2 }}>
          {C.brand.tagline}
        </h3>
        <p style={{ fontSize: 13, color: c.primary, fontWeight: 300, marginBottom: 18 }}>{C.seo.description}</p>
        <div style={{ display: "flex", gap: 10 }}>
          <div style={{ background: c.primary, color: "#fff", padding: "10px 20px", borderRadius: rd.button, fontSize: 13, fontWeight: 600 }}>Buat Janji →</div>
          <div style={{ background: "#fff", color: c.text, padding: "10px 20px", borderRadius: rd.button, fontSize: 13, fontWeight: 600, border: `1px solid ${c.mist}` }}>Lihat Layanan</div>
        </div>
      </div>
      {/* Mini services */}
      <div style={{ padding: "20px 28px", background: "#fff", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
        {C.services.slice(0, 3).map(s => (
          <div key={s.title} style={{ background: c.bg, borderRadius: rd.card, padding: "14px 12px", boxShadow: theme.shadow }}>
            <div style={{ fontSize: 20, marginBottom: 6 }}>{s.icon}</div>
            <div style={{ fontSize: 11, fontWeight: 600, color: c.text }}>{s.title}</div>
          </div>
        ))}
      </div>
      {/* Color swatches */}
      <div style={{ padding: "12px 28px 20px", background: "#fff", display: "flex", gap: 8, alignItems: "center" }}>
        {[c.primary, c.secondary, c.accent, c.bg, c.mist].map((col, i) => (
          <div key={i} title={col} style={{ width: 22, height: 22, borderRadius: "50%", background: col, border: "1px solid rgba(0,0,0,.1)" }} />
        ))}
        <span style={{ fontSize: 11, color: "#999", marginLeft: 6 }}>{theme.fonts.heading} · {theme.fonts.body}</span>
      </div>
    </div>
  );
}

// Route /dna-preview — hanya muncul di dev
function DnaPreview() {
  return (
    <div style={{ fontFamily: "system-ui,sans-serif", padding: "40px 24px", maxWidth: 1200, margin: "0 auto" }}>
      <div style={{ marginBottom: 40 }}>
        <h1 style={{ fontSize: 32, fontWeight: 800, marginBottom: 8 }}>🎨 DNA Preview</h1>
        <p style={{ color: "#666" }}>Semua 5 Design DNA ditampilkan untuk alat closing klien. Route ini hanya aktif saat <code>npm run dev</code>.</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(340px,1fr))", gap: 32 }}>
        {themeList.map(theme => <DnaCard key={theme.name} theme={theme} />)}
      </div>
      <div style={{ marginTop: 32, padding: "20px 24px", background: "#f8f8f8", borderRadius: 12, fontSize: 13, color: "#555" }}>
        <strong>Cara pakai:</strong> Tunjukkan halaman ini saat meeting klien. Setelah klien pilih DNA, ubah <code>theme</code> di <code>site.config.js</code> menjadi nama DNA yang dipilih.
      </div>
    </div>
  );
}

export default function App() {
  const isDnaPreview = typeof window !== "undefined" && window.location.pathname === "/dna-preview";
  if (isDnaPreview) return <DnaPreview />;

  const [navSolid, setNavSolid] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => {
    const fn = () => setNavSolid(window.scrollY > 40);
    window.addEventListener("scroll", fn);
    return () => window.removeEventListener("scroll", fn);
  }, []);
  const scrollTo = id => { setMenuOpen(false); document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); };

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

      {/* NAV */}
      <nav style={{ position: "fixed", top: 0, left: 0, right: 0, zIndex: 50, padding: navSolid ? "14px 0" : "22px 0", background: navSolid ? "rgba(255,255,255,.94)" : "transparent", backdropFilter: navSolid ? "blur(10px)" : "none", boxShadow: navSolid ? T.shadow : "none", transition: "all .4s ease" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", padding: "0 24px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 38, height: 38, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", color: "#fff", fontSize: 20 }}>✚</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 21 }}>{C.brand.name}</span>
          </div>
          <div className="desktop-nav" style={{ display: "flex", alignItems: "center", gap: 24 }}>
            {["Layanan", "Tentang", "Jadwal", "Kontak"].map(m => (
              <span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 15, fontWeight: 500, cursor: "pointer" }}>{m}</span>
            ))}
            {C.features.booking && (
              <button className="btn" onClick={() => scrollTo("kontak")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "10px 20px", borderRadius: r.pill, fontSize: 14, fontWeight: 600, fontFamily: "inherit" }}>Buat Janji Temu</button>
            )}
          </div>
          <button className="hamburger" onClick={() => setMenuOpen(o => !o)} style={{ display: "none", background: "none", border: "none", cursor: "pointer", fontSize: 26, color: navSolid ? cl.text : "#fff", padding: 4 }}>{menuOpen ? "✕" : "☰"}</button>
        </div>
        {menuOpen && (
          <div style={{ background: "rgba(255,255,255,.97)", backdropFilter: "blur(10px)", padding: "20px 24px 28px", display: "flex", flexDirection: "column", gap: 16, borderTop: `1px solid ${cl.mist}` }}>
            {["Layanan", "Tentang", "Jadwal", "Kontak"].map(m => (
              <span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 16, fontWeight: 500, cursor: "pointer", padding: "8px 0", borderBottom: `1px solid ${cl.mist}` }}>{m}</span>
            ))}
            {C.features.booking && (
              <button className="btn" onClick={() => scrollTo("kontak")} style={{ background: cl.primary, color: "#fff", border: "none", padding: 14, borderRadius: r.card, fontSize: 15, fontWeight: 600, fontFamily: "inherit", marginTop: 4 }}>Buat Janji Temu</button>
            )}
          </div>
        )}
      </nav>

      {/* HERO */}
      <header style={{ position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", background: `linear-gradient(135deg,${cl.bg},${cl.mist})`, overflow: "hidden" }}>
        <div style={{ position: "absolute", top: "12%", right: "-6%", width: 420, height: 420, borderRadius: "50%", background: `radial-gradient(circle,${cl.primary}22,transparent 70%)`, animation: "floaty 7s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "8%", left: "-4%", width: 300, height: 300, borderRadius: "50%", background: `radial-gradient(circle,${cl.accent}22,transparent 70%)`, animation: "floaty 9s ease-in-out infinite" }} />
        <div style={{ maxWidth: 1180, margin: "0 auto", padding: "120px 24px 60px", position: "relative", zIndex: 2 }}>
          <Reveal><span style={{ display: "inline-block", padding: "8px 18px", borderRadius: r.pill, background: "#fff", color: cl.primary, fontSize: 13, fontWeight: 600, letterSpacing: 1, marginBottom: 28, boxShadow: T.shadow }}>{C.brand.badge}</span></Reveal>
          <Reveal delay={0.1}><h1 className="display" style={{ fontSize: "clamp(38px,6vw,66px)", fontWeight: 700, lineHeight: 1.05, maxWidth: 720, marginBottom: 24 }}>{C.brand.tagline}</h1></Reveal>
          <Reveal delay={0.2}><p style={{ fontSize: 19, lineHeight: 1.6, color: cl.primary, maxWidth: 540, marginBottom: 36, fontWeight: 300 }}>{C.seo.description}</p></Reveal>
          <Reveal delay={0.3}>
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              {C.features.booking && <button className="btn" onClick={() => scrollTo("kontak")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "16px 32px", borderRadius: r.pill, fontSize: 16, fontWeight: 600, fontFamily: "inherit", boxShadow: T.shadow }}>Buat Janji Temu →</button>}
              <button className="btn" onClick={() => scrollTo("layanan")} style={{ background: "#fff", color: cl.text, border: `1.5px solid ${cl.text}22`, padding: "16px 32px", borderRadius: r.pill, fontSize: 16, fontWeight: 600, fontFamily: "inherit" }}>Lihat Layanan</button>
            </div>
          </Reveal>
          <Reveal delay={0.4}>
            <div style={{ display: "flex", gap: 40, marginTop: 64, flexWrap: "wrap" }}>
              {C.stats.map(s => (
                <div key={s.label}>
                  <div className="display" style={{ fontSize: 36, fontWeight: 700, color: cl.primary }}>{s.value}</div>
                  <div style={{ fontSize: 14, opacity: .6 }}>{s.label}</div>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </header>

      {/* LAYANAN */}
      <section id="layanan" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto" }}>
        <Reveal>
          <div style={{ textAlign: "center", marginBottom: 60 }}>
            <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>LAYANAN KAMI</span>
            <h2 className="display" style={{ fontSize: "clamp(30px,4vw,44px)", fontWeight: 700, marginTop: 12 }}>Perawatan lengkap satu atap</h2>
          </div>
        </Reveal>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(280px,1fr))", gap: 26 }}>
          {C.services.map((s, i) => (
            <Reveal key={s.title} delay={i * 0.08}>
              <div className="lift" style={{ background: cl.bg, borderRadius: r.card, padding: "34px 30px", border: `1px solid ${cl.mist}` }}>
                <div style={{ width: 58, height: 58, borderRadius: r.card, background: "#fff", display: "grid", placeItems: "center", fontSize: 28, marginBottom: 20, boxShadow: T.shadow }}>{s.icon}</div>
                <h3 className="display" style={{ fontSize: 21, fontWeight: 600, marginBottom: 10 }}>{s.title}</h3>
                <p style={{ fontSize: 15, lineHeight: 1.6, opacity: .7, fontWeight: 300 }}>{s.desc}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* TENTANG */}
      <section id="tentang" style={{ background: cl.secondary, color: "#fff", padding: "100px 24px" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: 60, alignItems: "center" }}>
          <Reveal>
            <div>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>TENTANG KAMI</span>
              <h2 className="display" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, margin: "14px 0 24px", lineHeight: 1.15 }}>{C.about.title}</h2>
              <p style={{ fontSize: 16, lineHeight: 1.7, opacity: .8, fontWeight: 300 }}>{C.about.desc}</p>
            </div>
          </Reveal>
          <Reveal delay={0.2}>
            <div style={{ display: "grid", gap: 18 }}>
              {C.about.highlights.map((h, i) => (
                <div key={i} style={{ display: "flex", gap: 16, background: "rgba(255,255,255,.05)", padding: "20px 22px", borderRadius: r.card }}>
                  <div style={{ color: cl.accent, fontSize: 22 }}>✓</div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>{h.title}</div>
                    <div style={{ fontSize: 14, opacity: .65, fontWeight: 300 }}>{h.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </section>

      {/* JADWAL */}
      <section id="jadwal" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: 50, alignItems: "center" }}>
          <Reveal>
            <div>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>JADWAL BUKA</span>
              <h2 className="display" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, margin: "14px 0 28px" }}>Kami siap kapan Anda butuh</h2>
              {C.hours.map((h, i) => (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "18px 4px", borderBottom: `1px solid ${cl.mist}` }}>
                  <span style={{ fontWeight: 500 }}>{h.day}</span>
                  <span style={{ color: cl.primary, fontWeight: 600 }}>{h.time}</span>
                </div>
              ))}
              {C.contact.address && <p style={{ marginTop: 20, fontSize: 14, opacity: .6 }}>📍 {C.contact.address}</p>}
            </div>
          </Reveal>
          <Reveal delay={0.15}>
            <div style={{ background: `linear-gradient(135deg,${cl.primary},${cl.secondary})`, borderRadius: r.card, padding: 44, color: "#fff" }}>
              <div style={{ fontSize: 40, marginBottom: 16 }}>🚑</div>
              <h3 className="display" style={{ fontSize: 26, fontWeight: 600, marginBottom: 12 }}>Layanan Darurat</h3>
              <p style={{ fontSize: 15, lineHeight: 1.6, opacity: .85, marginBottom: 24, fontWeight: 300 }}>Untuk kondisi darurat di luar jam buka, hubungi nomor darurat kami.</p>
              <div style={{ background: "rgba(255,255,255,.12)", borderRadius: r.card, padding: "16px 20px", fontSize: 20, fontWeight: 600 }}>📞 {C.contact.phone}</div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* KONTAK */}
      {C.features.booking && (
        <section id="kontak" style={{ background: cl.mist, padding: "100px 24px" }}>
          <div style={{ maxWidth: 720, margin: "0 auto", textAlign: "center" }}>
            <Reveal>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>BUAT JANJI</span>
              <h2 className="display" style={{ fontSize: "clamp(30px,4.5vw,46px)", fontWeight: 700, margin: "14px 0 18px" }}>Jadwalkan kunjungan Anda</h2>
              <p style={{ fontSize: 17, color: cl.primary, marginBottom: 40, fontWeight: 300 }}>Isi data di bawah, tim kami akan menghubungi Anda untuk konfirmasi.</p>
            </Reveal>
            <Reveal delay={0.15}><ContactForm theme={T} /></Reveal>
          </div>
        </section>
      )}

      {/* FOOTER */}
      <footer style={{ background: cl.secondary, color: "#fff", padding: "50px 24px 34px" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", display: "flex", flexWrap: "wrap", gap: 30, justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 34, height: 34, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", fontSize: 18 }}>✚</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 19 }}>{C.brand.name}</span>
          </div>
          <div style={{ fontSize: 13, opacity: .5 }}>Website oleh <strong style={{ color: cl.accent }}>INXOTIVE</strong></div>
        </div>
      </footer>
    </div>
  );
}
