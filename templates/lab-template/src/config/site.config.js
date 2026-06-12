export const siteConfig = {
  theme: "precision-lab",
  brand: {
    name: "Lab Prima Diagnostika",
    tagline: "Hasil akurat, layanan cepat.",
    logo: null,
    badge: "🧪 LAB DIAGNOSTIK TEPERCAYA",
    colors: {},
  },
  contact: {
    whatsapp: "6281234567890",
    phone: "",
    email: "",
    address: "Jl. Raya Kesehatan No. 10, Denpasar, Bali",
    mapsEmbedUrl: "",
  },
  hours: [
    { day: "Senin – Sabtu", time: "07.00 – 20.00" },
    { day: "Minggu", time: "08.00 – 14.00" },
  ],
  stats: [
    { value: "8+", label: "Tahun melayani" },
    { value: "10rb+", label: "Pasien terlayani" },
    { value: "1×24 jam", label: "Hasil keluar" },
  ],
  services: [
    { icon: "🩸", title: "Darah Lengkap", desc: "Pemeriksaan hemoglobin, leukosit, trombosit, dan hitung jenis darah secara menyeluruh." },
    { icon: "🧬", title: "Kimia Darah", desc: "Gula darah, kolesterol total, trigliserida, SGOT, SGPT, kreatinin, dan asam urat." },
    { icon: "🧪", title: "Urin Lengkap", desc: "Pemeriksaan fisik, kimia, dan sedimen urin untuk deteksi gangguan saluran kemih." },
    { icon: "💉", title: "HbA1c", desc: "Pemantauan gula darah rata-rata 3 bulan terakhir — penting untuk kontrol diabetes." },
    { icon: "🔬", title: "Rapid Test", desc: "HIV, HBsAg, dengue NS1, rapid test COVID-19 — hasil cepat dalam 15–30 menit." },
    { icon: "📋", title: "Paket Cek Kesehatan", desc: "Paket komprehensif untuk check-up rutin: darah lengkap + kimia darah + urin." },
  ],
  about: {
    title: "Laboratorium dengan standar terbaik di Bali",
    desc: "Didirikan pada tahun 2018, Lab Prima Diagnostika berkomitmen menyediakan layanan pemeriksaan laboratorium yang akurat, cepat, dan terjangkau. Seluruh pemeriksaan dilakukan oleh tenaga teknis medis bersertifikat dengan peralatan terkini.",
    highlights: [
      { title: "Peralatan modern & terkalibrasi", desc: "Menggunakan teknologi terbaru untuk hasil yang akurat" },
      { title: "Tenaga teknis bersertifikat", desc: "Dikelola oleh ahli teknologi medis berlisensi" },
      { title: "Hasil cepat & akurat", desc: "Pemeriksaan rutin keluar dalam 1×24 jam" },
      { title: "Antar hasil via WhatsApp", desc: "Hasil dikirim langsung ke HP Anda — tidak perlu ke lab lagi" },
    ],
  },
  features: {
    booking: false,
    whatsappOrder: true,
    aiChat: false,
    search: false,
    cms: false,
  },
  seo: {
    title: "Lab Prima Diagnostika — Laboratorium Kesehatan Terpercaya di Bali",
    description: "Pemeriksaan laboratorium akurat: darah lengkap, kimia darah, urin, HbA1c, rapid test.",
    ogImage: "/og.png",
  },
};
