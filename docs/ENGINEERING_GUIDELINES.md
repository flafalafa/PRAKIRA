# Pedoman Rekayasa Perangkat Lunak (ENGINEERING_GUIDELINES)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Standar Rekayasa  
Pemilik: Chief Software Engineering Manager  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan standar rekayasa, alur kerja pengembangan, ekspektasi pengkodean, serta aturan pengujian dan dokumentasi untuk platform PRAKIRA.

Pedoman ini **wajib** dipatuhi oleh setiap Insinyur Perangkat Lunak (Software Engineer) maupun Agen AI yang berkontribusi pada repositori ini. Tujuannya adalah untuk menjamin kualitas perangkat lunak berskala *enterprise* yang konsisten, aman, dan mudah dipelihara meskipun tim terus berkembang.

---

## 2. Prinsip Rekayasa (Engineering Principles)

* **Utamakan Dokumentasi (Documentation First):** Jangan menulis kode sebelum spesifikasi disepakati. Dokumentasi adalah sumber kebenaran (*single source of truth*).
* **Utamakan API (API First):** Rancang antarmuka kontrak (API) secara ketat sebelum membangun logika *backend* maupun *frontend*.
* **Utamakan Keamanan (Security First):** Jangan pernah menaruh *secrets* dalam kode, selalu asumsikan data masuk (*input*) itu berbahaya, dan terapkan asas hak istimewa terkecil (*least privilege*).
* **Utamakan Pengujian (Test First):** Jika memungkinkan (TDD), tulis kasus uji sebelum fungsi dibuat untuk menjamin perilaku kode.
* **Observabilitas (Observability):** Setiap komponen yang dibangun harus memancarkan log terstruktur, metrik, dan mendukung pelacakan.
* **Kesederhanaan (Simplicity):** Hindari abstraksi yang terlalu dini atau kompleksitas kode yang tidak perlu (KISS - *Keep It Simple, Stupid*).
* **Kemudahan Pemeliharaan (Maintainability):** Tulis kode untuk dibaca oleh manusia lain di masa depan, bukan hanya untuk dipahami oleh komputer.
* **Skalabilitas (Scalability):** Rancang komponen agar bekerja tanpa hambatan saat memproses 10 ribu titik data vs 1 titik data.

---

## 3. Struktur Proyek (Project Structure)

Repositori PRAKIRA terorganisasi ke dalam direktori fungsional yang ketat:

* `docs/`: (Hanya-baca selama implementasi). Berisi spesifikasi arsitektur, basis data, dan aturan mesin. Hanya boleh diubah saat merancang arsitektur.
* `research/`: Laporan penelitian awal (historis banjir, analisis sungai).
* `src/` (atau `app/`, `lib/`): Berisi *source code* murni, terbagi menjadi subdirektori berdasarkan layanan atau modul.
* `tests/`: Kumpulan skrip pengujian unit dan integrasi.
* `infra/`: Konfigurasi *Infrastructure-as-Code* (Terraform, k8s manifests, docker).

---

## 4. Alur Kerja Pengembangan (Development Workflow)

Setiap pengembangan fitur wajib mengikuti alur yang ketat. **Tidak ada implementasi yang boleh melewatkan tahap spesifikasi.**

**Riset (Research)**
↓
**Spesifikasi (Specification)** - Tulis atau perbarui *Markdown*
↓
**Tinjauan Arsitektur (Architecture Review)**
↓
**Implementasi (Implementation)** - Menulis kode sumber
↓
**Pengujian (Testing)**
↓
**Tinjauan Kode (Code Review)**
↓
**Pembaruan Dokumentasi (Documentation Update)**
↓
**Penggabungan (Merge)**

---

## 5. Strategi Git (Git Strategy)

* **Penamaan Cabang (Branch Naming):** 
  * `feature/[nama-fitur]`
  * `bugfix/[isu-yang-diperbaiki]`
  * `hotfix/[perbaikan-darurat-produksi]`
* **Konvensi Pesan Commit (Commit Messages):** Gunakan standar *Conventional Commits* (contoh: `feat: add rainfall prediction rule`, `fix: resolve db connection leak`).
* **Syarat Pull Request (PR):** Harus ditautkan ke tiket/isu terkait. PR tidak boleh memuat ratusan berkas jika bisa dipecah.
* **Strategi Penggabungan (Merge Strategy):** Menggunakan *Squash and Merge* untuk menjaga riwayat *commit* di cabang utama (`main`) tetap rapi.
* **Tag Rilis (Release Tags):** Menggunakan *Semantic Versioning* (contoh: `v1.2.0`).

---

## 6. Standar Pengkodean (Coding Standards)

Panduan ini bersifat agnostik-bahasa:

* **Penamaan (Naming Conventions):** Gunakan *camelCase* untuk variabel/fungsi, *PascalCase* untuk Kelas/Antarmuka, dan *UPPER_SNAKE_CASE* untuk konstanta/variabel lingkungan. Konsisten di seluruh repositori.
* **Penanganan Kesalahan (Error Handling):** Tangkap pengecualian (*exceptions*) secara eksplisit. Jangan pernah "menelan" *error* secara diam-diam (*silent catch*).
* **Pencatatan (Logging):** Gunakan level log dengan benar (`DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`). Jangan melog PII (Data Identitas Pribadi).
* **Konfigurasi (Configuration):** Tidak ada *hardcoding*. Semua parameter harus diakses melalui *Environment Variables* (.env).
* **Manajemen Ketergantungan (Dependency Management):** Kunci (*lock*) semua versi *library* pendukung untuk mencegah pembaruan tak terduga yang merusak kompatibilitas.
* **Komentar (Comments):** Komentari MENGAPA (*WHY*) Anda melakukan sesuatu yang rumit, bukan APA (*WHAT*) yang dilakukan kode (kode harus cukup jelas untuk menjelaskan *WHAT*).
* **Keterbacaan (Code Readability):** Satu fungsi, satu tanggung jawab (*Single Responsibility Principle*). Jaga agar fungsi tetap pendek.

---

## 7. Aturan Dokumentasi (Documentation Rules)

Setiap fitur besar yang diselesaikan harus menyertakan pembaruan pada dokumentasi (di folder `docs/`). Pembaruan wajib mencakup:

* Dampak spesifikasi sistem
* Dampak arsitektur (jika ada *service* baru)
* Perubahan kontrak API (jika skema *request/response* berubah)
* Perubahan skema Basis Data
* Catatan Rilis (*Release notes*)

---

## 8. Standar Pengujian (Testing Standards)

* **Unit Testing:** Menguji satu fungsi atau kelas terisolasi (*Mock/Stub* semua dependensi luar). Cakupan target: >80%.
* **Integration Testing:** Menguji interaksi antara beberapa komponen internal (misal: Layanan ke Basis Data lokal).
* **API Testing:** Memvalidasi *endpoint* HTTP merespons dengan status, *header*, dan JSON yang benar.
* **Performance Testing:** Memastikan *endpoint* prediksi merespons dalam <200ms di bawah beban sedang.
* **Regression Testing:** Menguji ulang fungsionalitas lama untuk menjamin kode baru tidak merusak sistem yang sudah jalan.
* **Manual Testing:** Uji UI/UX dasar oleh pengembang sebelum meminta tinjauan (*Code Review*).
* **Acceptance Testing:** Divalidasi oleh Pemilik Produk (*Product Owner*) berdasarkan kriteria awal.

---

## 9. Daftar Periksa Tinjauan Kode (Code Review Checklist)

Setiap PR harus melewati tinjauan berdasarkan daftar ini:

- [ ] **Arsitektur:** Sesuai dengan batasan lapisan (*layer boundaries*) sistem.
- [ ] **Keamanan:** Bebas dari injeksi (SQL/XSS), otorisasi tepat, tidak ada kata sandi tersimpan.
- [ ] **Kinerja (Performance):** Tidak ada kueri basis data N+1, kerumitan algoritma optimal.
- [ ] **Kemudahan Pemeliharaan:** Kode bersih (*clean code*), variabel deskriptif, metode singkat.
- [ ] **Pengujian (Testing):** Kasus uji ditambahkan untuk semua tepi-kasus (*edge-cases*) kritis.
- [ ] **Dokumentasi:** *Docblocks* diperbarui, berkas *markdown* diperbarui jika skema berubah.
- [ ] **Kompatibilitas Mundur (Backward Compatibility):** Perubahan API tidak akan merusak aplikasi klien versi lama.

---

## 10. Definisi Selesai (Definition of Done - DoD)

Sebuah tugas (isu/tiket) baru dianggap SELESAI (*DONE*) jika dan hanya jika:

* Kode sumber telah diimplementasikan sepenuhnya.
* Pengujian unit dan integrasi berhasil lewat dengan sukses (di *CI/CD pipeline* lokal/remote).
* Dokumentasi proyek (`docs/`) telah disinkronkan dengan pembaruan kode.
* Kontrak dan dokumentasi API (misalnya OpenAPI/Swagger) telah diperbarui.
* Lolos daftar periksa tinjauan kode (*Code Review Checklist*) oleh setidaknya 1 insinyur senior.
* Tidak ditemukan isu/hambatan keamanan dan kinerja tingkat kritis (*Zero Critical Issues*).
