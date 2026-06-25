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

const alurPemeriksaan = [
  { icon: "🏥", title: "Datang & Daftar", desc: "Kunjungi laboratorium kami langsung. Pendaftaran cepat tanpa antre panjang." },
  { icon: "💉", title: "Ambil Sampel", desc: "Tenaga medis profesional mengambil sampel darah/urin dengan alat steril sekali pakai." },
  { icon: "📱", title: "Hasil via WhatsApp", desc: "Hasil pemeriksaan dikirim langsung ke WhatsApp Anda dalam 1×24 jam." },
];

const team = [
  { name: "dr. Ni Made Sari, Sp.PK", role: "Dokter Penanggung Jawab" },
  { name: "Aan Putra, A.Md.A.K", role: "Analis Kesehatan" },
  { name: "Dewi Lestari, A.Md.Keb", role: "Petugas Pengambilan Sampel" },
];

const waUrl = `https://wa.me/${C.contact.whatsapp}?text=Halo ${C.brand.name}, saya ingin konsultasi hasil lab`;

// Komponen preview DNA (sama dengan template lain)
function DnaCard({ theme }) {
  const c = theme.colors;
  const rd = theme.radius;
  return (
    <div style={{ border: `1px solid ${c.mist}`, borderRadius: rd.card, overflow: "hidden", fontFamily: `'${theme.fonts.body}',sans-serif` }}>
      <style>{`@import url('${theme.fonts.embedUrl}');`}</style>
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
      <div style={{ padding: "20px 28px", background: "#fff", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
        {C.services.slice(0, 3).map(s => (
          <div key={s.title} style={{ background: c.bg, borderRadius: rd.card, padding: "14px 12px", boxShadow: theme.shadow }}>
            <div style={{ fontSize: 20, marginBottom: 6 }}>{s.icon}</div>
            <div style={{ fontSize: 11, fontWeight: 600, color: c.text }}>{s.title}</div>
          </div>
        ))}
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
      <div style={{ marginBottom: 40 }}>
        <h1 style={{ fontSize: 32, fontWeight: 800, marginBottom: 8 }}>🎨 DNA Preview</h1>
        <p style={{ color: "#666" }}>Semua 5 Design DNA — alat closing klien. Route hanya aktif saat dev.</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(340px,1fr))", gap: 32 }}>
        {themeList.map(theme => <DnaCard key={theme.name} theme={theme} />)}
      </div>
      <div style={{ marginTop: 32, padding: "20px 24px", background: "#f8f8f8", borderRadius: 12, fontSize: 13, color: "#555" }}>
        <strong>Cara pakai:</strong> Tunjukkan saat meeting klien. Setelah pilih DNA, ubah <code>theme</code> di <code>site.config.js</code>.
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
            <div style={{ width: 38, height: 38, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", color: "#fff", fontSize: 20, fontWeight: 700, fontFamily: `'${T.fonts.heading}',serif` }}>🔬</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 20 }}>{C.brand.name}</span>
          </div>
          <div className="desktop-nav" style={{ display: "flex", alignItems: "center", gap: 24 }}>
            {["Pemeriksaan", "Alur", "Tentang", "Hasil", "Kontak"].map(m => (
              <span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 14, fontWeight: 500, cursor: "pointer" }}>{m}</span>
            ))}
            <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "10px 20px", borderRadius: r.button, fontSize: 14, fontWeight: 600, fontFamily: "inherit" }}>Hubungi Lab</button>
          </div>
          <button className="hamburger" onClick={() => setMenuOpen(o => !o)} style={{ display: "none", background: "none", border: "none", cursor: "pointer", fontSize: 26, color: navSolid ? cl.text : "#fff", padding: 4 }}>{menuOpen ? "✕" : "☰"}</button>
        </div>
        {menuOpen && (
          <div style={{ background: "rgba(255,255,255,.97)", backdropFilter: "blur(10px)", padding: "20px 24px 28px", display: "flex", flexDirection: "column", gap: 16, borderTop: `1px solid ${cl.mist}` }}>
            {["Pemeriksaan", "Alur", "Tentang", "Hasil", "Kontak"].map(m => (
              <span key={m} onClick={() => scrollTo(m.toLowerCase())} style={{ fontSize: 16, fontWeight: 500, cursor: "pointer", padding: "8px 0", borderBottom: `1px solid ${cl.mist}` }}>{m}</span>
            ))}
            <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: cl.primary, color: "#fff", border: "none", padding: 14, borderRadius: r.card, fontSize: 15, fontWeight: 600, fontFamily: "inherit", marginTop: 4 }}>Hubungi Lab</button>
          </div>
        )}
      </nav>

      {/* HERO */}
      <header style={{ position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", background: `linear-gradient(135deg,${cl.bg},${cl.mist})`, overflow: "hidden" }}>
        <div style={{ position: "absolute", top: "12%", right: "-6%", width: 420, height: 420, borderRadius: "50%", background: `radial-gradient(circle,${cl.primary}22,transparent 70%)`, animation: "floaty 7s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "8%", left: "-4%", width: 300, height: 300, borderRadius: "50%", background: `radial-gradient(circle,${cl.accent}22,transparent 70%)`, animation: "floaty 9s ease-in-out infinite" }} />
        <div style={{ maxWidth: 1180, margin: "0 auto", padding: "120px 24px 60px", position: "relative", zIndex: 2 }}>
          <Reveal><span style={{ display: "inline-block", padding: "8px 18px", borderRadius: r.pill, background: "#fff", color: cl.primary, fontSize: 13, fontWeight: 600, letterSpacing: 1, marginBottom: 28, boxShadow: T.shadow }}>{C.brand.badge}</span></Reveal>
          {/* FIX: Siklus 3 -- H1=800 heading hierarchy */}
          <Reveal delay={0.1}><h1 className="display" style={{ fontSize: "clamp(38px,6vw,66px)", fontWeight: 800, lineHeight: 1.05, maxWidth: 720, marginBottom: 24, color: cl.text }}>{C.brand.tagline}</h1></Reveal>
          <Reveal delay={0.2}><p style={{ fontSize: 19, lineHeight: 1.6, color: cl.primary, maxWidth: 540, marginBottom: 36, fontWeight: 300 }}>{C.seo.description}</p></Reveal>
          <Reveal delay={0.3}>
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              <button className="btn" onClick={() => scrollTo("pemeriksaan")} style={{ background: cl.primary, color: "#fff", border: "none", padding: "16px 32px", borderRadius: r.button, fontSize: 16, fontWeight: 600, fontFamily: "inherit", boxShadow: T.shadow }}>Lihat Pemeriksaan →</button>
              <button className="btn" onClick={() => window.open(waUrl, "_blank")} style={{ background: "rgba(255,255,255,.08)", color: cl.text, border: `1.5px solid ${cl.text}22`, padding: "16px 32px", borderRadius: r.button, fontSize: 16, fontWeight: 600, fontFamily: "inherit" }}>Hubungi via WhatsApp</button>
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

      {/* PEMERIKSAAN */}
      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="pemeriksaan" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto", scrollMarginTop: 90 }}>
        <Reveal>
          <div style={{ textAlign: "center", marginBottom: 60 }}>
            <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>LAYANAN PEMERIKSAAN</span>
            <h2 className="display" style={{ fontSize: "clamp(30px,4vw,44px)", fontWeight: 700, marginTop: 12 }}>Pemeriksaan lengkap untuk Anda</h2>
            <p style={{ fontSize: 16, color: cl.text, marginTop: 12, fontWeight: 300, opacity: .7 }}>Semua pemeriksaan dilakukan dengan alat modern dan hasil akurat</p>
          </div>
        </Reveal>
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

      {/* ALUR PEMERIKSAAN */}
      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="alur" style={{ background: cl.secondary, color: "#fff", padding: "100px 24px", scrollMarginTop: 90 }}>
        <div style={{ maxWidth: 1180, margin: "0 auto" }}>
          <Reveal>
            <div style={{ textAlign: "center", marginBottom: 60 }}>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>ALUR PEMERIKSAAN</span>
              <h2 className="display" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, margin: "12px 0 14px" }}>Cara kerja kami</h2>
              <p style={{ fontSize: 16, opacity: .7, fontWeight: 300 }}>Tiga langkah mudah — dari pendaftaran hingga hasil di tangan Anda</p>
            </div>
          </Reveal>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))", gap: 30 }}>
            {alurPemeriksaan.map((a, i) => (
              <Reveal key={a.title} delay={i * 0.15}>
                <div style={{ textAlign: "center", padding: "40px 28px", position: "relative" }}>
                  <div style={{ width: 80, height: 80, borderRadius: "50%", background: `linear-gradient(135deg,${cl.accent}33,${cl.primary}33)`, display: "grid", placeItems: "center", fontSize: 40, margin: "0 auto 24px", border: `2px solid ${cl.accent}44` }}>{a.icon}</div>
                  <div style={{ position: "absolute", top: 20, left: "50%", transform: "translateX(-50%)", background: cl.accent, color: cl.text, width: 28, height: 28, borderRadius: "50%", display: "grid", placeItems: "center", fontSize: 13, fontWeight: 800 }}>{i + 1}</div>
                  <h3 className="display" style={{ fontSize: 20, fontWeight: 600, marginBottom: 12 }}>{a.title}</h3>
                  <p style={{ fontSize: 14, opacity: .7, lineHeight: 1.6, fontWeight: 300 }}>{a.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* TENTANG */}
      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="tentang" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto", scrollMarginTop: 90 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: 60, alignItems: "start" }}>
          <Reveal>
            <div>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>TENTANG KAMI</span>
              <h2 className="display" style={{ fontSize: "clamp(28px,4vw,42px)", fontWeight: 700, margin: "14px 0 24px", lineHeight: 1.15 }}>{C.about.title}</h2>
              <p style={{ fontSize: 16, lineHeight: 1.7, color: cl.text, fontWeight: 300, opacity: .8 }}>{C.about.desc}</p>
            </div>
          </Reveal>
          <Reveal delay={0.15}>
            <div style={{ display: "grid", gap: 14 }}>
              {C.about.highlights.map((h, i) => (
                <div key={i} style={{ display: "flex", gap: 16, background: cl.bg, padding: "18px 22px", borderRadius: r.card, border: `1px solid ${cl.mist}` }}>
                  <div style={{ color: cl.accent, fontSize: 20, flexShrink: 0 }}>✓</div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 3 }}>{h.title}</div>
                    <div style={{ fontSize: 13, opacity: .65, fontWeight: 300 }}>{h.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
        {/* Team */}
        <Reveal>
          <div style={{ marginTop: 60, textAlign: "center" }}>
            <h3 className="display" style={{ fontSize: 26, fontWeight: 700, marginBottom: 30, color: cl.text }}>Tim Analis Kami</h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(200px,1fr))", gap: 20 }}>
              {team.map(t => (
                <div key={t.name} style={{ background: cl.bg, borderRadius: r.card, padding: "28px 20px", border: `1px solid ${cl.mist}` }}>
                  <div style={{ width: 56, height: 56, borderRadius: "50%", background: `linear-gradient(135deg,${cl.primary},${cl.accent})`, display: "grid", placeItems: "center", fontSize: 24, color: "#fff", margin: "0 auto 14px" }}>{t.name[0]}</div>
                  <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>{t.name}</div>
                  <div style={{ fontSize: 12, opacity: .6, fontWeight: 300 }}>{t.role}</div>
                </div>
              ))}
            </div>
          </div>
        </Reveal>
      </section>

      {/* HASIL ONLINE */}
      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="hasil" style={{ background: cl.mist, padding: "100px 24px", scrollMarginTop: 90 }}>
        <div style={{ maxWidth: 720, margin: "0 auto", textAlign: "center" }}>
          <Reveal>
            <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>HASIL ONLINE</span>
            <h2 className="display" style={{ fontSize: "clamp(28px,4.5vw,42px)", fontWeight: 700, margin: "14px 0 18px" }}>Cek hasil pemeriksaan Anda secara online</h2>
            <p style={{ fontSize: 16, color: cl.text, marginBottom: 36, fontWeight: 300, opacity: .7 }}>Fitur ini akan segera hadir. Saat ini, hasil pemeriksaan dikirim via WhatsApp langsung ke HP Anda.</p>
          </Reveal>
          <Reveal delay={0.15}>
            <div style={{ background: "#fff", borderRadius: r.card, padding: "48px 32px", boxShadow: T.shadow, border: `2px dashed ${cl.mist}` }}>
              <div style={{ fontSize: 64, marginBottom: 20 }}>🔄</div>
              <h3 className="display" style={{ fontSize: 22, fontWeight: 600, marginBottom: 12 }}>Segera Hadir</h3>
              <p style={{ fontSize: 14, color: cl.text, marginBottom: 24, fontWeight: 300, opacity: .7 }}>Sistem hasil online sedang dalam pengembangan. Anda akan bisa melihat riwayat hasil pemeriksaan kapan saja.</p>
              <div style={{ display: "inline-flex", alignItems: "center", gap: 12, background: cl.bg, borderRadius: r.pill, padding: "16px 24px" }}>
                <span style={{ fontSize: 20 }}>📱</span>
                <span style={{ fontSize: 15, fontWeight: 500 }}>Sementara, hasil dikirim via WhatsApp dalam 1×24 jam</span>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* JADWAL & KONTAK */}
      {/* FIX: Siklus 3 -- scroll-margin-top for sticky header */}
      <section id="kontak" style={{ padding: "100px 24px", maxWidth: 1180, margin: "0 auto", scrollMarginTop: 90 }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: 40, alignItems: "start" }}>
          <Reveal>
            <div>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>JADWAL BUKA</span>
              <h2 className="display" style={{ fontSize: "clamp(26px,3.5vw,38px)", fontWeight: 700, margin: "12px 0 24px" }}>Kunjungi laboratorium kami</h2>
              {C.hours.map((h, i) => (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "14px 4px", borderBottom: `1px solid ${cl.mist}` }}>
                  <span style={{ fontWeight: 500 }}>{h.day}</span>
                  <span style={{ color: cl.primary, fontWeight: 600 }}>{h.time}</span>
                </div>
              ))}
              {C.contact.address && <p style={{ marginTop: 16, fontSize: 14, opacity: .6 }}>📍 {C.contact.address}</p>}
            </div>
          </Reveal>
          <Reveal delay={0.15}>
            <div style={{ background: cl.bg, borderRadius: r.card, padding: 36, border: `1px solid ${cl.mist}` }}>
              <span style={{ color: cl.accent, fontWeight: 600, fontSize: 14, letterSpacing: 2 }}>HUBUNGI KAMI</span>
              <h3 className="display" style={{ fontSize: 24, fontWeight: 700, margin: "12px 0 8px" }}>Ada pertanyaan?</h3>
              <p style={{ fontSize: 14, opacity: .7, fontWeight: 300, marginBottom: 24 }}>Tim kami siap membantu — konsultasi gratis, hasil via WhatsApp.</p>
              <a href={waUrl} target="_blank" rel="noreferrer" style={{ display: "block", background: cl.primary, color: "#fff", textAlign: "center", padding: "16px", borderRadius: r.button, fontSize: 16, fontWeight: 600, textDecoration: "none", boxShadow: T.shadow, marginBottom: 12 }}>
                💬 Chat WhatsApp Sekarang
              </a>
              {C.contact.email && (
                <a href={`mailto:${C.contact.email}`} style={{ display: "block", background: "#fff", color: cl.text, textAlign: "center", padding: "14px", borderRadius: r.button, fontSize: 14, fontWeight: 500, textDecoration: "none", border: `1px solid ${cl.mist}` }}>
                  📧 {C.contact.email}
                </a>
              )}
            </div>
          </Reveal>
        </div>
      </section>

      {/* FOOTER */}
      <footer style={{ background: cl.secondary, color: "#fff", padding: "44px 24px 30px" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto", display: "flex", flexWrap: "wrap", gap: 20, justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 34, height: 34, borderRadius: r.card, background: cl.primary, display: "grid", placeItems: "center", fontSize: 16, fontWeight: 700 }}>🔬</div>
            <span className="display" style={{ fontWeight: 700, fontSize: 18 }}>{C.brand.name}</span>
          </div>
          <div style={{ fontSize: 12, opacity: .4 }}>Website oleh <strong style={{ color: cl.accent }}>INXOTIVE</strong></div>
        </div>
      </footer>
    </div>
  );
}
