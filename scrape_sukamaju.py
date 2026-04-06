import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://sukamaju.desagarut.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FILE = "hasil_scraping_sukamaju.txt"

def scrape():
    lines = []

    def log(text=""):
        print(text)
        lines.append(text)

    log("="*60)
    log("SCRAPING WEBSITE DESA SUKAMAJU — ANALISIS SISTEM ORGANISASI")
    log(f"URL    : {BASE_URL}")
    log(f"Waktu  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("="*60)

    res = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "lxml")

    # 1. METADATA
    log("\n📋 1. METADATA")
    log("-"*40)
    for tag in soup.find_all("meta"):
        name = tag.get("name") or tag.get("property")
        content = tag.get("content")
        if name and content:
            log(f"  [{name}] → {content}")

    # Generator / platform
    generator = soup.find("meta", {"name": "generator"})
    if generator:
        log(f"  [Platform] → {generator.get('content')}")

    # 2. TAXONOMY & NAVIGATION SYSTEM
    log("\n🗂️  2. TAXONOMY & NAVIGATION SYSTEM")
    log("-"*40)
    seen = set()
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if (text and href.startswith("https://sukamaju.desagarut.com")
                and text not in seen and len(text) > 1):
            seen.add(text)
            log(f"  {text} → {href}")

    # 3. CONTROLLED VOCABULARY
    log("\n🏷️  3. CONTROLLED VOCABULARY")
    log("-"*40)
    log("  Kategori Artikel:")
    for a in soup.find_all("a", href=True):
        if "/kategori/" in a["href"] or "/artikel/kategori" in a["href"]:
            text = a.get_text(strip=True)
            if text:
                log(f"  → {text} ({a['href']})")

    log("  Kategori Menu Statistik:")
    for a in soup.find_all("a", href=True):
        if "/data-statistik/" in a["href"]:
            text = a.get_text(strip=True)
            if text:
                log(f"  → {text}")

    # 4. SEARCH FUNCTIONALITY
    log("\n🔍 4. SEARCH FUNCTIONALITY")
    log("-"*40)
    search = (soup.find("input", {"type": "search"})
              or soup.find("input", {"name": "s"})
              or soup.find("form", {"method": "get"}))
    if search:
        log(f"  Search/Form ditemukan: {search}")
    else:
        log("  Tidak ditemukan fitur pencarian konvensional")
        log("  → Website menggunakan sistem navigasi berbasis menu kategori")

    # 5. SITE MAP
    log("\n🗺️  5. SITE MAP")
    log("-"*40)
    log("  Struktur halaman berdasarkan navigasi:")
    nav_structure = {
        "Profil Desa": ["Visi dan Misi", "Sejarah Desa", "Kondisi Geografis"],
        "Pemerintahan": ["SOTK", "Pemerintah Desa", "BPD", "PKK"],
        "Potensi Desa": ["Lapak", "Galeri", "Pengaduan", "Pembangunan"],
        "Data Statistik": ["Vaksinasi", "Populasi", "Agama", "Pekerjaan",
                           "Pendidikan", "Jenis Kelamin", "Status Perkawinan",
                           "Golongan Darah", "Disabilitas", "Rentang Umur"],
        "Status Desa": ["IDM 2021", "IDM 2022", "IDM 2023", "IDM 2024", "SDGs"],
        "Regulasi": ["Produk Hukum", "Informasi Publik"],
        "Bantuan": ["Bantuan Penduduk", "Bantuan Keluarga"],
    }
    for parent, children in nav_structure.items():
        log(f"  ├── {parent}")
        for child in children:
            log(f"  │   └── {child}")

    # Simpan ke file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n✅ Hasil disimpan ke: {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape()
