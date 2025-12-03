# 📞 Dashboard Call Center 112 - Surabaya

Dashboard interaktif untuk menganalisis data laporan Call Center 112 dengan fokus pada Statistika Sains Data dan Analisis Kebijakan.

## 🎯 Fitur Utama

- **📊 Overview**: KPI dan metrik kinerja utama
- **📈 Distribusi & Perbandingan**: Analisis kategori laporan 2024 vs 2025
- **📉 Tren Waktu**: Pola temporal bulanan dengan heatmap
- **🎯 Validitas Data**: Analisis laporan valid vs tidak valid
- **💡 Insight & Rekomendasi**: Rekomendasi kebijakan berbasis data

## 🚀 Cara Menggunakan

1. **Upload Data**: Upload file Excel tahun 2024 dan 2025 di sidebar
2. **Filter Data**: Pilih tahun, kategori, dan validitas sesuai kebutuhan
3. **Eksplorasi**: Jelajahi 5 tab berbeda untuk insight mendalam
4. **Export**: Download hasil analisis dalam format CSV

## 📋 Struktur Data yang Dibutuhkan

File Excel harus memiliki kolom minimal:
- `waktu lapor` - Timestamp laporan
- `tipe laporan` - Jenis laporan (Emergency, Information, Prank, Ghost, dll)
- `kategori` - Kategori detail laporan
- `sub kategori 1` - Sub kategori (opsional)

## 🔧 Teknologi

- **Streamlit** - Framework web app
- **Pandas** - Data processing
- **Plotly** - Visualisasi interaktif
- **NumPy** - Komputasi numerik

## 📚 Konteks Akademik

Dashboard ini dibuat untuk mata kuliah:
- **Statistika Sains Data**
- **Analisis Kebijakan**

Fokus pada analisis distribusi, tren temporal, dan rekomendasi kebijakan berbasis data empiris.

## 👨‍💻 Pengembangan

Dikembangkan sebagai bagian dari tugas akhir mata kuliah dengan fokus pada:
- Data cleaning & preprocessing
- Statistical analysis
- Data visualization
- Policy recommendation

## 📄 Lisensi

Untuk keperluan akademik dan edukasi.

---

**Catatan**: Data yang digunakan adalah data laporan Call Center 112 Kota Surabaya tahun 2024-2025.