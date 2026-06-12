export const siteConfig = {
  theme: "clinical-trust",
  brand: {
    name: "Klinik Sehat Sentosa",
    tagline: "Kesehatan keluarga Anda, prioritas kami.",
    logo: null,
    badge: "✚ KLINIK KELUARGA TEPERCAYA",
    // colors opsional — isi hanya jika ingin override warna dari theme DNA
    colors: {},
  },
  // fonts diatur oleh theme DNA — tidak perlu diisi di sini
  contact: {
    whatsapp: "6281234567890",
    phone: "0800-1234-5678",
    email: "",
    address: "Jl. Melati No. 12, Kota Anda",
    mapsEmbedUrl: "",
  },
  hours: [
    { day: "Senin – Jumat", time: "08.00 – 21.00" },
    { day: "Sabtu", time: "08.00 – 18.00" },
    { day: "Minggu & Libur", time: "09.00 – 15.00" },
  ],
  stats: [
    { value: "15+", label: "Tahun melayani" },
    { value: "8", label: "Dokter & apoteker" },
    { value: "12rb+", label: "Pasien terlayani" },
  ],
  services: [
    { icon: "🩺", title: "Pemeriksaan Umum", desc: "Konsultasi dokter umum untuk keluhan harian dan cek kesehatan." },
    { icon: "💊", title: "Apotek & Konsultasi Obat", desc: "Apoteker siap membantu penggunaan obat yang tepat dan aman." },
    { icon: "🧪", title: "Laboratorium", desc: "Pemeriksaan darah, gula, kolesterol, dan paket cek kesehatan." },
    { icon: "💉", title: "Imunisasi & Vaksin", desc: "Vaksinasi anak dan dewasa sesuai jadwal yang direkomendasikan." },
    { icon: "🤰", title: "KIA & Kandungan", desc: "Pemeriksaan ibu hamil, KB, dan kesehatan ibu serta anak." },
    { icon: "🦷", title: "Gigi & Mulut", desc: "Perawatan gigi rutin, pembersihan karang, dan konsultasi gigi." },
  ],
  about: {
    title: "Dirawat dengan hati, ditangani dengan hati",
    desc: "Klinik Sehat Sentosa hadir untuk menjadi tempat keluarga Anda merasa aman. Tim dokter dan apoteker kami berkomitmen memberikan pelayanan yang ramah, jujur, dan berbasis bukti.",
    highlights: [
      { title: "Tenaga profesional bersertifikat", desc: "Dokter & apoteker berlisensi resmi" },
      { title: "Apoteker siap konsultasi", desc: "Penggunaan obat yang aman & rasional" },
      { title: "Suasana nyaman & bersih", desc: "Ruang tunggu yang menenangkan" },
      { title: "Harga transparan", desc: "Tidak ada biaya tersembunyi" },
    ],
  },
  seo: {
    title: "Klinik Sehat Sentosa — Klinik Keluarga Tepercaya",
    description: "Pelayanan medis menyeluruh dengan dokter dan apoteker berpengalaman.",
    ogImage: "/og.png",
  },
  features: {
    booking: true,
    aiChat: false,
    search: false,
    cms: false,
  },
};
