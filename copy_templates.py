"""
COPY TEMPLATES — 3 industri (F&B, Tech, Health/Beauty)
Pakai ini untuk generate konten real, bukan placeholder generik.
"""

# ═══════════════════════════════════════════════
# F&B — RESTORAN / KAFE / KULINER
# ═══════════════════════════════════════════════

FNB = {
    "brand_tone": "hangat, menggugah selera, personal, otentik",
    "hero": {
        "eyebrow": "Warung & Resto Online",
        "headline": "Pesanan Masuk.{br}Dapur Jalan.{br}Rejeki Ngalir.",
        "subtext": "Bikin warung atau restoran kamu bisa dipesan online dalam 15 menit. Digital tanpa ribet — tinggal terima order, kami urus sisanya.",
        "cta": "Bikin Online Sekarang",
        "cta_alt": "Lihat Contoh Menu",
    },
    "stats": [
        ("500+", "Warung Online"),
        ("15Mnt", "Setup Cepat"),
        ("99.9%", "Uptime Order"),
        ("4.9★", "Rating Pelanggan"),
    ],
    "features": {
        "heading": "Ngurus Warung Digital,{br}Semudah Masak Air.",
        "subtext": "Tools khusus untuk pegusaha F&B. Dari menu digital sampai laporan keuangan.",
        "items": [
            {"icon": "svg-menu", "title": "Menu Digital", "desc": "Katalog menu dengan foto, harga, dan opsi custom. Update kapan aja, cetak ulang nol rupiah."},
            {"icon": "svg-order", "title": "Order Masuk Otomatis", "desc": "Setiap pesanan langsung ke dapur. No missed call, no salah catat. Riwayat order rapi."},
            {"icon": "svg-payment", "title": "Bayar di Tempat & Online", "desc": "QRIS, transfer, atau bayar langsung. Semua nyambung, rekap otomatis tiap hari."},
            {"icon": "svg-report", "title": "Laporan Harian", "desc": "Penjualan hari ini, menu terlaris, stok hampir habis. Semua dalam satu dashboard."},
            {"icon": "svg-promo", "title": "Promo & Diskon", "desc": "Bikin promo dalam 2 klik. Happy hour, diskon menu, atau paket hemat — atur sendiri."},
            {"icon": "svg-delivery", "title": "Antar Sendiri atau Gojek", "desc": "Integrasi kurir internal + Gojek/Grab. Pelanggan lihat estimasi sampai."},
        ],
    },
    "about": {
        "heading": "Dari Dapur Kecil,{br}Kami Bikin Sistem Besar.",
        "body": "Kami mulai dari ngobrol sama pemilik warung dan resto di 5 kota. Keluhan mereka selalu sama: \"susah urus online sendiri, makan waktu, capek.\" Makanya kami bikin platform yang sesederhana masak air — tinggal colok, nyala, jalan. Sekarang 500+ pegusaha F&B udah pakai. Dari angkringan sampai restoran.",
    },
    "testimonial": {
        "name": "Bu Sari",
        "role": "Pemilik Warung Sari Rasa, Yogyakarta",
        "text": "Dulu setiap order WA saya tulis manual. Sering salah, pelanggan komplain. Sekarang semua otomatis, saya tinggal masak. Pesanan naik 2 kali lipat.",
    },
    "pricing_tiers": [
        {"name": "Pemula", "price": "Rp 99rb", "period": "/bln", "desc": "Coba dulu, nggak pakai ribet.", "features": ["1 Outlet", "Menu Digital 30 Item", "Order WA", "Laporan Harian"], "popular": False},
        {"name": "Laris", "price": "Rp 299rb", "period": "/bln", "desc": "Paling laku buat yang udah mulai rame.", "features": ["3 Outlet", "Menu Digital Unlimited", "Order WA + App", "Pembayaran Online", "Promo & Diskon"], "popular": True},
        {"name": "Korporasi", "price": "Rp 799rb", "period": "/bln", "desc": "Buat bisnis yang udah gede dan punya tim.", "features": ["10 Outlet", "Menu Digital Unlimited", "Multi-Order Channel", "Laporan Keuangan", "Integrasi Gojek/Grab", "Dedicated CS"], "popular": False},
    ],
    "faq": [
        ("Apakah saya perlu punya HP mahal?", "Cukup HP Android 4GB RAM. Web app — nggak perlu install apa-apa."),
        ("Saya nggak paham teknologi, susah nggak?", "Lebih mudah dari bikin kopi. Kami bantu setup 15 menit via telepon."),
        ("Kalau pelanggan bayar online, uangnya kapan masuk?", "Masuk otomatis ke rekening kamu dalam 1-2 hari kerja. Transparan."),
        ("Bisa dipasang di lebih dari satu outlet?", "Bisa. Semua outlet terpantau dalam satu dashboard. Cocok buat franchise."),
    ],
    "cta": {
        "heading": "Mulai Online Hari Ini,{br}Besok Pesanan Masuk.",
        "subtext": "15 menit setup. Gratis 7 hari pertama. Nggak cocok? Batal kapan aja.",
        "button": "Bikin Online Gratis",
    },
    "contact_whatsapp": "62811-9988-7766",
    "footer_tagline": "Online itu gampang, tinggal sentuh.",
}


# ═══════════════════════════════════════════════
# TECH / SaaS — STARTUP / APLIKASI / AGENCY
# ═══════════════════════════════════════════════

TECH = {
    "brand_tone": "cepat, inovatif, langsung ke inti, clean",
    "hero": {
        "eyebrow": "Build Faster, Ship Smarter",
        "headline": "Dari Ide ke Produk.{br}3 Minggu,{br}Bukan 3 Bulan.",
        "subtext": "Platform all-in-one buat founder dan tim product. Dari MVP sampai scale — tanpa drama tech stack dan meeting nggak jelas.",
        "cta": "Mulai Gratis",
        "cta_alt": "Lihat Demo",
    },
    "stats": [
        ("200+", "Produk Diluncurkan"),
        ("3×", "Lebih Cepat"),
        ("87%", "Tim Puas"),
        ("4.8★", "Rating"),
    ],
    "features": {
        "heading": "Yang Kamu Butuh{br}Buat Ship Cepat.",
        "subtext": "Toolkit untuk founder, product manager, dan developer yang ingin bergerak cepat tanpa patah arang.",
        "items": [
            {"icon": "svg-template", "title": "Pre-built Templates", "desc": "Bukan boilerplate biasa. Template siap pakai untuk SaaS, marketplace, landing page — dengan best practice udah terpasang."},
            {"icon": "svg-api", "title": "API-First Architecture", "desc": "Semua modul terhubung via REST API. Frontend pisah dari backend. Scale horizontal tanpa rewrite."},
            {"icon": "svg-deploy", "title": "One-Click Deploy", "desc": "Dari lokal ke production dalam 1 klik. Auto SSL, auto scaling, monitoring built-in. No DevOps team needed."},
            {"icon": "svg-analytics", "title": "Real-time Analytics", "desc": "User behavior, conversion funnel, revenue tracking — semua real-time, bukan laporan kemarin sore."},
            {"icon": "svg-ai", "title": "AI-Ready Stack", "desc": "Embed AI agent, RAG pipeline, atau chatbot dalam hitungan jam. Infrastructure udah siap, tinggal tulis prompt."},
            {"icon": "svg-collab", "title": "Async Collaboration", "desc": "Tim bisa kerja async — dokumentasi otomatis, feedback terstruktur, decision log. Rapat mingguan? Nggak perlu."},
        ],
    },
    "about": {
        "heading": "Kami Founder Juga.{br}Makanya Kami Bikin Ini.",
        "body": "Kami bertiga founder yang capek lihat tim product habis 3 bulan cuma setup infrastructure, meetings, dan rewrite. Produknya belum launch, semangat udah habis. Jadi kami bikin platform yang ngasih kamu superpower untuk ship produk dalam minggu, bukan bulan. Dan kami pake sendiri tiap hari.",
    },
    "testimonial": {
        "name": "Andi Pratama",
        "role": "Founder, TechStart.id",
        "text": "MVP pertama kami selesai dalam 3 minggu. Sebelumnya, saya estimasi 3 bulan. Ini bukan tool — ini cheat code buat founder.",
    },
    "pricing_tiers": [
        {"name": "Starter", "price": "Free", "period": "", "desc": "Coba dulu, lihat sendiri.", "features": ["1 Product", "3 Templates", "Basic Analytics", "Community Support"], "popular": False},
        {"name": "Pro", "price": "$29", "period": "/bln", "desc": "Buat yang udah siap scale.", "features": ["5 Products", "All Templates", "Advanced Analytics", "API Access", "Priority Support", "AI Pipeline Ready"], "popular": True},
        {"name": "Enterprise", "price": "$99", "period": "/bln", "desc": "Buat tim yang butuh full power.", "features": ["Unlimited Products", "Custom Templates", "Custom Analytics", "Full API + Webhooks", "Dedicated Success Manager", "SLA 99.99%"], "popular": False},
    ],
    "faq": [
        ("Apakah perlu bisa coding?", "Minimal HTML/CSS untuk landing page. Untuk produk kompleks, kami siapkan template yang tinggal diisi konten."),
        ("Kalau scale gede, apa perlu migrasi?", "Nggak. Infrastruktur kami udah horizontal scale. Dari 100 user ke 1 juta user — platform yang sama, nggak perlu rewrite."),
        ("Bagaimana dengan keamanan data?", "Encrypted at rest dan in transit. Semua data di AWS Singapore. Sertifikasi ISO 27001 dalam proses."),
        ("Bisa custom domain sendiri?", "Support custom domain dari paket Pro. Setup 5 menit via DNS, auto SSL dari Cloudflare."),
    ],
    "cta": {
        "heading": "Berhenti Meeting.{br}Mulai Ship.",
        "subtext": "Gratis 30 hari. Nggak perlu kartu kredit. Kalau cocok, lanjut. Kalau nggak, data kamu tetap bisa di-export.",
        "button": "Mulai Gratis",
    },
    "contact_whatsapp": "62811-9988-7767",
    "footer_tagline": "Ship fast. Stay sane.",
}


# ═══════════════════════════════════════════════
# HEALTH / BEAUTY — KLINIK / SPA / DOKTER
# ═══════════════════════════════════════════════

HEALTH = {
    "brand_tone": "tenang, profesional, terpercaya, hangat",
    "hero": {
        "eyebrow": "Klinik & Perawatan Online",
        "headline": "Janji Temu{br}Tanpa Antri.{br}Tanpa Ribet.",
        "subtext": "Booking online untuk klinik, spa, dan perawatan. Pasien dapat kepastian jadwal, Anda dapat pasien yang tepat waktu.",
        "cta": "Coba Gratis 7 Hari",
        "cta_alt": "Lihat Demo",
    },
    "stats": [
        ("300+", "Klinik & Spa"),
        ("5.000+", "Pasien per Bulan"),
        ("92%", "Tepat Waktu"),
        ("4.9★", "Rating Pasien"),
    ],
    "features": {
        "heading": "Urusan Booking,{br}Kami yang Atur.",
        "subtext": "Tools khusus untuk klinik, spa, dan praktik mandiri. Kurangi no-show, naikkan kapasitas perawatan.",
        "items": [
            {"icon": "svg-cal", "title": "Booking Online 24/7", "desc": "Pasien booking dari HP mereka — lihat slot kosong, pilih terapis, konfirmasi otomatis. No missed call."},
            {"icon": "svg-remind", "title": "Auto Reminder", "desc": "SMS + WhatsApp reminder otomatis H-1 dan H-1 jam. No-show turun 72%. Gak perlu telepon satu-satu."},
            {"icon": "svg-med", "title": "Rekam Medis Digital", "desc": "Riwayat perawatan, alergi, catatan dokter — semua digital. Bisa diakses kapan aja dari mana aja."},
            {"icon": "svg-pay", "title": "Pembayaran & Deposit", "desc": "Pasien bisa bayar deposit online. No-show minimal karena ada komitmen. Refund otomatis kalau cancel H+1."},
            {"icon": "svg-staff", "title": "Manajemen Staff & Jadwal", "desc": "Atur jadwal dokter/terapis per shift. Lihat siapa available sekarang dengan 1 klik."},
            {"icon": "svg-analytics-h", "title": "Laporan Bisnis", "desc": "Pasien per hari, revenue, treatment terlaris, rate okupasi. Semua dalam grafik yang bisa kamu pahami."},
        ],
    },
    "about": {
        "heading": "Pasien Tenang,{br}Praktik Jalan Terus.",
        "body": "Kami bangun platform ini setelah ngobrol sama 50+ pemilik klinik dan spa. Masalah nomor satu? Bukan alat medis — tapi manajemen jadwal yang masih manual, pasien no-show, dan administrasi yang makan waktu. Makanya kami bikin sistem booking yang bikin pasien senang dan praktik Anda jalan terus. Tanpa ribet administrasi.",
    },
    "testimonial": {
        "name": "dr. Maya Savitri",
        "role": "Pemilik Klinik Sehat, Denpasar",
        "text": "No-show turun dari 30% ke 5%. Pasien seneng bisa booking dari rumah. Saya seneng praktik lebih teratur. Win-win.",
    },
    "pricing_tiers": [
        {"name": "Praktik", "price": "Rp 199rb", "period": "/bln", "desc": "Untuk praktik mandiri / perorangan.", "features": ["1 Dokter", "Booking Online", "Auto Reminder WA", "Rekam Medis Digital"], "popular": False},
        {"name": "Klinik", "price": "Rp 499rb", "period": "/bln", "desc": "Paling recommended untuk klinik & spa.", "features": ["5 Dokter/Terapis", "Booking + Jadwal Shift", "Reminder WA + SMS", "Rekam Medis Lengkap", "Deposit Online", "Laporan Bisnis"], "popular": True},
        {"name": "Group", "price": "Rp 1.2jt", "period": "/bln", "desc": "Untuk grup klinik atau franchise spa.", "features": ["Unlimited Tenaga Medis", "Multi-Cabang Dashboard", "Central + Lokal Booking", "Full Laporan Konsolidasi", "Dedicated CS", "Integrasi BPJS/KIS"], "popular": False},
    ],
    "faq": [
        ("Apakah data pasien aman?", "Kami terapkan enkripsi end-to-end. Semua data kesehatan sesuai standar kerahasiaan medis. Server di Indonesia."),
        ("Bisa integrasi dengan BPJS?", "Untuk paket Group, sudah support format BPJS. Tinggal sinkronisasi data."),
        ("Kalau pasien tidak datang setelah booking?", "Deposit online mengurangi no-show drastis. Reminder otomatis H-1, H-1 jam. Kalau tetap no-show, deposit bisa dipotong."),
        ("Buat spa juga bisa?", "Bisa. Fitur booking terapis, pilih treatment, dan durasi perawatan sudah support."),
    ],
    "cta": {
        "heading": "Booking Online Hari Ini,{br}Pasien Datang Besok.",
        "subtext": "Gratis 7 hari pertama. Setup 30 menit via telepon. Data aman, pasien senang, praktik naik kelas.",
        "button": "Coba Gratis",
    },
    "contact_whatsapp": "62811-9988-7768",
    "footer_tagline": "Pasien senang, praktik naik kelas.",
}

# ═══════════════════════════════════════════════
# MAP — hubungkan industri ke set copy
# ═══════════════════════════════════════════════
COPY_MAP = {
    "fnb": FNB,
    "restaurant": FNB,
    "food": FNB,
    "tech": TECH,
    "saas": TECH,
    "startup": TECH,
    "health": HEALTH,
    "healthcare": HEALTH,
    "beauty": HEALTH,
    "klinik": HEALTH,
    "spa": HEALTH,
}

def get_copy(industry: str) -> dict:
    """Get copy template for an industry."""
    industry = industry.lower().strip()
    for key, data in COPY_MAP.items():
        if key in industry or industry in key:
            return data
    return TECH  # default


def format_section(html_template: str, copy: dict, section_name: str) -> str:
    """Apply copy to HTML template."""
    # This would be called by the HTML generator
    section = copy.get(section_name, {})
    return html_template.replace(f"{{copy.{section_name}.heading}}", section.get("heading", "")) \
                       .replace(f"{{copy.{section_name}.subtext}}", section.get("subtext", ""))
