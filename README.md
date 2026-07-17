<div align="center">

<!-- Animasi Teks -->
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Space+Grotesk&weight=700&size=32&pause=1000&color=B9A6FF&center=true&vCenter=true&width=600&lines=AI+Data+Analyst+Agent;Auto-EDA+%2B+Data+Cleaning;Powered+by+Groq+%26+LangChain)](https://git.io/typing-svg)

**Asisten Cerdas untuk Eksplorasi, Visualisasi, dan Pembersihan Data Otomatis.**

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6600?style=for-the-badge&logo=groq&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</div>

---

##  Daftar Isi
- [Tentang Proyek](#-tentang-proyek)
- [Fitur Unggulan](#-fitur-unggulan)
- [Demo](#-demo)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Instalasi](#-instalasi--setup-lokal)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Direktori](#-struktur-direktori)
- [Screenshot](#-screenshot)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)
- [Author](#-author)

---

##  Tentang Proyek
**AI Data Analyst** adalah aplikasi web interaktif yang memungkinkan Anda "berbicara" langsung dengan dataset (CSV) Anda. Dibangun dengan antarmuka *Glassmorphism* modern, aplikasi ini memanfaatkan kekuatan **Groq (Llama-3)** dan **LangChain** untuk menganalisis data, membuat visualisasi, hingga membersihkan data secara otomatis tanpa Anda perlu menulis satu baris kode pun.

###  Masalah yang Dipecahkan
- **Data Cleaning Membosankan** → Otomatisasi pembersihan data dengan perintah sederhana
- **Visualisasi Memakan Waktu** → Grafik instan hanya dengan chat
- **Analisis Data Sulit** → AI membantu interpretasi data secara natural language
- **Kurangnya Konteks** → AI mengingat riwayat chat untuk analisis yang lebih dalam

---

##  Fitur Unggulan

| Fitur | Deskripsi |
|-------|-----------|
| 🧠 **Chat Memory** | AI mengingat percakapan sebelumnya untuk analisis kontekstual |
| 🧹 **Auto-Cleaning** | Hapus missing values, duplikat, atau kolom tertentu dengan perintah |
| 📥 **Download CSV** | Unduh hasil data yang sudah dibersihkan langsung |
| 🔮 **Auto-EDA** | Ringkasan data otomatis begitu file diunggah |
| 📊 **Smart Charts** | Pembuatan grafik otomatis (bar, line, scatter, histogram) |
| 🎨 **Glassmorphism UI** | Tampilan modern dengan dark mode elegan |
| 💬 **Natural Language** | Interaksi dengan bahasa sehari-hari |
| ⚡ **Real-time Processing** | Analisis cepat dengan Groq API |

---

##  Teknologi yang Digunakan

### Core Framework
- **Python 3.9+** — Bahasa pemrograman utama
- **Streamlit** — Framework web untuk dashboard interaktif

### AI & NLP
- **LangChain** — Framework untuk aplikasi LLM
- **Groq API** — Inference engine untuk Llama-3
- **Llama-3-70B** — Model bahasa besar untuk analisis

### Data Processing
- **Pandas** — Manipulasi dan analisis data
- **NumPy** — Komputasi numerik
- **Matplotlib** — Visualisasi data dasar
- **Seaborn** — Visualisasi statistik

### Utilities
- **Python-dotenv** — Manajemen environment variables
- **UUID** — Identifikasi unik untuk session
- **Base64** — Enkoding untuk download file

---

##  Instalasi & Setup Lokal

### Persyaratan Sistem
- Python 3.9 atau lebih baru
- Pip (Python package manager)
- Groq API Key ([Dapatkan di sini](https://console.groq.com/))

### Langkah Instalasi

**1. Clone Repositori**
```bash
git clone https://github.com/dimssrmdn01/data-agent.git
cd data-agent
```

**2. Buat Virtual Environment (Direkomendasikan)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup Environment Variables**
```bash
# Buat file .env
echo "GROQ_API_KEY=your_api_key_here" > .env
```

**5. Jalankan Aplikasi**
```bash
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501` secara otomatis.

---

##  Cara Penggunaan

### 1. Persiapan Awal
- Buka aplikasi di browser (`http://localhost:8501`)
- Masukkan Groq API Key di sidebar kiri
- API Key bisa didapat dari [console.groq.com](https://console.groq.com/)

### 2. Upload Dataset
- Klik tombol **"📤 Upload CSV"**
- Pilih file CSV dari komputer Anda
- Tunggu hingga AI memberikan ringkasan otomatis (Auto-EDA)
- Dataset akan ditampilkan dalam bentuk tabel interaktif

### 3. Mulai Menganalisis
Berikan perintah dalam bahasa Indonesia atau Inggris, contoh:
- "Tampilkan statistik deskriptif dari kolom 'harga'"
- "Buat visualisasi sebaran data usia customer"
- "Hapus baris yang memiliki nilai kosong"
- "Buang kolom 'alamat' dari dataset"
- "Tampilkan 5 data teratas"
- "Analisis korelasi antar variabel numerik"

### 4. Download Hasil
Setelah data cleaning, tombol **"📥 Download CSV"** akan muncul. Klik untuk mengunduh hasil pembersihan data — file akan terdownload dengan nama `cleaned_dataset.csv`.

###  Contoh Interaksi
```
User: "Tampilkan 5 data teratas"
AI: Menampilkan head dari dataset dengan 5 baris pertama...

User: "Buat histogram untuk kolom 'umur'"
AI: [Menampilkan histogram interaktif]

User: "Hapus baris yang nilai 'harga'-nya kosong"
AI: [Membersihkan data] Data siap diunduh!
```

---

##  Struktur Direktori

```
data-agent/
│
├── app.py                 # Aplikasi utama Streamlit
├── core_agent.py           # Konfigurasi AI & LangChain
├── requirements.txt        # Dependensi Python
├── README.md                # Dokumentasi (file ini)
├── LICENSE                  # Lisensi MIT
│
├── .streamlit/              # Konfigurasi Streamlit
│   └── config.toml
│
└── assets/                  # Asset visual (logo, icons, dll)
    ├── data_agent_logo.png
    └── groq_icon.png
```

### Penjelasan File

| File | Fungsi |
|------|--------|
| `app.py` | Mengatur UI, session state, chat interface, dan logika visualisasi |
| `core_agent.py` | Menginisialisasi Groq LLM, prompt templates, dan memory management |
| `requirements.txt` | Semua package Python yang dibutuhkan |
| `.streamlit/config.toml` | Custom theme dan konfigurasi Streamlit |

---

##  Screenshot
Screenshot akan segera ditambahkan.

---

##  Kontribusi
Kontribusi sangat diterima! Berikut cara berkontribusi:

** Melaporkan Bug**
- Buka issue dengan label `bug`
- Deskripsikan bug secara detail
- Sertakan langkah-langkah untuk reproduksi
- Lampirkan screenshot jika memungkinkan

** Saran Fitur**
- Buka issue dengan label `enhancement`
- Jelaskan fitur yang diinginkan
- Berikan use case atau contoh penggunaan

** Pull Request**
1. Fork repositori
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

** Panduan Coding**
- Ikuti PEP 8 style guide
- Tambahkan docstring untuk fungsi
- Test perubahan sebelum commit
- Update README jika diperlukan

---

##  Lisensi
Didistribusikan di bawah **MIT License**. Lihat file `LICENSE` untuk informasi lebih lanjut.

```
MIT License

Copyright (c) 2024 Dimas Arya Ramadhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

##  Acknowledgements
- [Groq](https://groq.com/) - Platform AI yang powerful
- [LangChain](https://www.langchain.com/) - Framework LLM yang fleksibel
- [Streamlit](https://streamlit.io/) - Framework web yang memudahkan
- Llama-3 - Model AI yang luar biasa

##  Roadmap
- [ ] Integrasi dengan database SQL
- [ ] Support file Excel (.xlsx)
- [ ] Export report dalam PDF
- [ ] Advanced visualisasi dengan Plotly
- [ ] Machine Learning prediction
- [ ] Multi-file analysis
- [ ] Real-time data streaming
- [ ] Deployment di cloud (Streamlit Cloud, HuggingFace)

##  Author
**Dimas Arya Ramadhan**
Dibuat dengan ❤️ oleh Dimas Arya Ramadhan
