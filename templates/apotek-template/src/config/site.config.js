export const siteConfig = {
  theme: "fresh-apotek",
  brand: {
    name: "Apotek Sari Sehat",
    tagline: "Kesehatan Anda, tanggung jawab kami.",
    logo: null,
    badge: "⚕ APOTEK KELUARGA TEPERCAYA SEJAK 2009",
    // colors opsional — isi hanya jika ingin override warna dari theme DNA
    colors: {},
  },
  // fonts diatur oleh theme DNA
  contact: {
    whatsapp: "6281234567890",
    phone: "",
    email: "",
    address: "Jl. Melati No. 5, Kota Anda",
    mapsEmbedUrl: "",
  },
  hours: [
    { day: "Senin – Sabtu", time: "08.00 – 21.00" },
    { day: "Minggu", time: "09.00 – 18.00" },
  ],
  stats: [
    { value: "15+", label: "Tahun berpengalaman" },
    { value: "5rb+", label: "Pelanggan setia" },
    { value: "1-2 jam", label: "Antar obat ke rumah" },
  ],
  services: [
    { icon: "💊", title: "Obat Resep", desc: "Layani resep dokter dengan teliti. Apoteker kami pastikan dosis dan interaksi obat aman." },
    { icon: "🌿", title: "Obat Herbal", desc: "Pilihan herbal berkualitas tersertifikasi BPOM untuk melengkapi gaya hidup sehat Anda." },
    { icon: "🧴", title: "Skincare & Vitamin", desc: "Produk perawatan kulit dan suplemen pilihan untuk kesehatan dari dalam dan luar." },
    { icon: "👶", title: "Kesehatan Bayi", desc: "Perlengkapan dan nutrisi bayi dari brand tepercaya dengan panduan apoteker." },
    { icon: "🩺", title: "Alat Kesehatan", desc: "Tensimeter, termometer, nebulizer, dan alat kesehatan rumahan lainnya." },
    { icon: "🚗", title: "Antar Obat", desc: "Layanan antar obat ke rumah Anda. Pesan via WhatsApp, kami antarkan dalam 1-2 jam." },
  ],
  about: {
    title: "Apotek keluarga yang sudah dipercaya lebih dari 15 tahun",
    desc: "Berdiri sejak 2009, Apotek Sari Sehat hadir untuk memastikan setiap keluarga mendapat obat yang tepat, aman, dan dengan harga terjangkau. Kami bukan sekadar apotek — kami adalah mitra kesehatan keluarga Anda.",
    highlights: [
      { title: "Konsultasi obat GRATIS", desc: "Apoteker siap membantu kapan saja" },
      { title: "Obat dijamin asli & BPOM", desc: "Tidak ada produk palsu atau kadaluarsa" },
      { title: "Harga bersaing", desc: "Cocok untuk semua kalangan keluarga" },
      { title: "Antar ke rumah", desc: "Pesan WhatsApp, terima di depan pintu" },
    ],
  },
  seo: {
    title: "Apotek Sari Sehat — Apotek Keluarga Tepercaya",
    description: "Apotek keluarga dengan konsultasi gratis, antar obat, dan produk BPOM terjamin.",
    ogImage: "/og.png",
  },
  features: {
    booking: false,
    whatsappOrder: true,
    aiChat: false,
    search: false,
    cms: false,
  },
};
