# Backlog Rekayasa Perangkat Lunak (ENGINEERING_BACKLOG)

Versi: 1.1 (Revisi MVP)
Proyek: PRAKIRA
Status: Perencanaan Sprints (MVP)
Pemilik: Chief Technical Project Manager (TPM)

---

## Ringkasan Backlog
- **Total Sprints:** 14 Sprints
- **Total Tasks (MVP):** 61 Tasks
- **Tugas Kritis (P0):** ~45 Tasks
- **Definisi Selesai MVP:** Aplikasi dapat di-deploy secara lokal menggunakan Docker Compose dan secara remote menggunakan PaaS (Render/Railway), dengan Cloudflare, PostgreSQL, Redis, dan Firebase. Aplikasi memiliki backend FastAPI dan Flutter app fungsional yang dapat menerima push notification saat sensor simulasi atau API BMKG mendeteksi banjir.

---

## Sprint 1: Fondasi Backend
**Epic Utama:** Backend Foundation

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-101 | Inisialisasi Repositori | Membuat repositori Git dan aturan cabang. | P0 | 1 | 2h | - | Repo Git | Aturan aktif |
| T-102 | Buat Proyek FastAPI | Setup kerangka dasar FastAPI. | P0 | 2 | 4h | T-101 | Aplikasi FastAPI | App berjalan lokal |
| T-103 | Setup Struktur Proyek | Membuat folder src, tests, docs. | P0 | 1 | 2h | T-102 | Folder terstruktur | Sesuai pedoman |
| T-104 | Setup Configuration Loader | Membaca variabel lingkungan (.env). | P0 | 2 | 4h | T-103 | Config Loader | Variabel termuat |
| T-105 | Setup Environment Validation | Validasi env vars menggunakan Pydantic. | P0 | 2 | 4h | T-104 | Pydantic Settings | Error jika env salah |
| T-106 | Setup Logger Terstruktur | Konfigurasi JSON logger untuk aplikasi. | P0 | 2 | 4h | T-103 | Logger Module | Log tercetak JSON |
| T-107 | Setup Health, Liveness, Readiness | Endpoint GET /health, /ready, /live. | P0 | 1 | 3h | T-102 | Endpoint API | Mengembalikan HTTP 200 |
| T-108 | Setup Dependency Injection | Konfigurasi DI kontainer / FastAPI Depends. | P0 | 2 | 4h | T-102 | DI Container | Bisa injeksi DB |
| T-109 | Setup Global Exception Handler | Menangkap unhandled exception & format JSON. | P0 | 2 | 4h | T-102 | Error Middleware | Respon HTTP 500 rapi |
| T-110 | Setup Base Middleware & Router | CORS, base API versioning (v1). | P0 | 2 | 4h | T-102 | Router API | Route v1 aktif |
| T-111 | Setup Base Testing | Konfigurasi Pytest & coverage. | P0 | 2 | 4h | T-102 | Pytest Suite | Bisa run pytest |
| T-112 | Setup Docker & Compose | Dockerfile dan docker-compose.yml untuk lokal. | P0 | 3 | 6h | T-102 | Docker Config | Bisa docker compose up |
| T-113 | Setup README | Dokumentasi cara menjalankan aplikasi. | P0 | 1 | 2h | T-101 | README.md | Instruksi lengkap |

## Sprint 2: Basis Data
**Epic Utama:** Manajemen Data

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-201 | Provisioning PostgreSQL & PostGIS | Setup DB lokal via Docker Compose. | P0 | 2 | 4h | T-112 | Lokal DB | Koneksi via psql |
| T-202 | Integrasi ORM (SQLAlchemy) | Koneksi backend ke database. | P0 | 3 | 6h | T-201 | Koneksi DB | Bisa read/write DB |
| T-203 | Setup Migrasi (Alembic) | Alat manajemen versi skema basis data. | P0 | 2 | 4h | T-202 | Alembic Config | Migrasi kosong berjalan |
| T-204 | Skema Tabel Geografi | Model Area, Watershed, River sesuai DATABASE_DESIGN. | P0 | 3 | 8h | T-203 | Model ORM | Tabel terbuat |
| T-205 | Skema Tabel Observasi | Model time-series cuaca & sungai. | P0 | 3 | 8h | T-204 | Model ORM | Tabel time-series siap |
| T-206 | Skema Tabel Prediksi | Model penyimpanan hasil prediksi. | P0 | 2 | 4h | T-204 | Model ORM | Tabel prediksi siap |
| T-207 | Provisioning Redis Lokal | Setup Redis di Docker Compose. | P0 | 1 | 2h | T-112 | Redis lokal | Koneksi Redis sukses |

## Sprint 3: Autentikasi
**Epic Utama:** Keamanan & Akses

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-301 | Skema Tabel Pengguna | Membuat tabel Users & Preferences. | P0 | 2 | 4h | T-204 | Model ORM | Tabel pengguna siap |
| T-302 | Setup Firebase Auth | Konfigurasi Firebase Project untuk otentikasi MVP. | P0 | 2 | 4h | - | Firebase Project | API Key Firebase siap |
| T-303 | Middleware Autentikasi | Verifikasi token JWT Firebase di FastAPI. | P0 | 3 | 8h | T-302 | Middleware Auth | Token tertolak jika invalid |
| T-304 | Endpoint Profil & Registrasi | API sinkronisasi Firebase UID dan profil. | P0 | 3 | 8h | T-303 | Endpoint API | Pengguna tersimpan di DB |
| T-305 | Pengaturan Preferences | API CRUD preferensi notifikasi. | P1 | 2 | 6h | T-304 | Endpoint API | Preferensi tersimpan |
| T-306 | Unit Test Auth | Test untuk fungsi otentikasi. | P0 | 2 | 6h | T-304 | Test Suite | Coverage lengkap |

## Sprint 4: Pengumpul Cuaca
**Epic Utama:** Integrasi Eksternal

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-401 | Modul HTTP Client | Klien asinkron (httpx) untuk API eksternal. | P0 | 2 | 6h | T-102 | HTTP Client | Bisa melakukan GET |
| T-402 | Klien API BMKG | Integrasi prakiraan cuaca via HTTP. | P0 | 3 | 8h | T-401 | Modul BMKG | Bisa menarik data |
| T-403 | Penyimpanan Cuaca | Simpan data ke DB. | P0 | 3 | 8h | T-402 | Fungsi Repositori | Data cuaca tersimpan |
| T-404 | Background Task Cuaca | Setup worker ringan (Celery/APScheduler) lokal. | P0 | 3 | 8h | T-207 | Worker Task | Berjalan otomatis |
| T-405 | Publish Event Cuaca | Pancarkan event menggunakan Redis pub/sub. | P0 | 2 | 4h | T-404 | Redis Event | Event tercetak |

## Sprint 5: Pengumpul Sungai
**Epic Utama:** Integrasi Eksternal

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-501 | Klien API Sungai | Tarik data TMA dari sensor sungai. | P0 | 3 | 8h | T-401 | Modul TMA | Data TMA didapat |
| T-502 | Penyimpanan TMA | Simpan observasi sungai ke DB. | P0 | 2 | 4h | T-501 | Fungsi Repositori | TMA tersimpan |
| T-503 | Kalkulasi Debit (Q) | Rumus hitung estimasi debit. | P1 | 3 | 8h | T-502 | Fungsi Logika | Debit dihitung |
| T-504 | Worker Polling Sungai | Job cron untuk cek TMA secara berkala. | P0 | 2 | 4h | T-404 | Worker Task | Polling aktif |
| T-505 | Pemetaan Awal DAS | Seed data Kali Serua & Tangsel ke DB. | P1 | 1 | 3h | T-204 | Seed Script | Data DAS ada |

## Sprint 6: Pengumpul Radar & Satelit (MVP)
**Epic Utama:** Integrasi Lanjutan

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-601 | Klien Citra Radar | Unduh gambar radar terbaru. | P1 | 3 | 8h | T-401 | Modul Radar | Gambar radar terunduh |
| T-602 | Ekstraksi Sederhana Radar | Ubah warna piksel ke estimasi hujan. | P1 | 4 | 12h | T-601 | Image Processor | Nilai intensitas didapat |
| T-603 | Klien Citra Satelit | Unduh satelit inframerah (opsional MVP). | P2 | 2 | 6h | T-401 | Modul Satelit | Gambar satelit siap |
| T-604 | Worker Radar | Job periodik untuk radar. | P1 | 2 | 4h | T-404 | Worker Task | Radar diproses otomatis |

## Sprint 7: Mesin Hidrologi
**Epic Utama:** Pemrosesan Logika

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-701 | Event Subscriber | Konsumsi event Redis cuaca & sungai. | P0 | 2 | 6h | T-405 | Redis Consumer | Event terbaca |
| T-702 | Akumulasi Hujan | Hitung agregasi hujan (1h, 3h, 24h). | P0 | 3 | 8h | T-701 | Fungsi Logika | Akumulasi benar |
| T-703 | Indeks Hujan Pendahulu | Estimasi kejenuhan tanah. | P0 | 3 | 8h | T-702 | Fungsi Logika | Indeks dihitung |
| T-704 | Deteksi Backwater Dasar | Status peringatan backwater (air balik). | P1 | 3 | 8h | T-503 | Fungsi Logika | Deteksi berfungsi |

## Sprint 8: Mesin Keputusan
**Epic Utama:** Logika Prediksi

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-801 | Evaluasi Aturan Status Risiko | Logika SAFE hingga EMERGENCY. | P0 | 4 | 12h | T-701 | Fungsi Keputusan | Status berganti sesuai kondisi |
| T-802 | Kalkulasi ETA | Hitung estimasi waktu tiba banjir. | P0 | 4 | 12h | T-801 | Fungsi ETA | Menit didapat |
| T-803 | Kalkulasi Keparahan & Penjelasan | Generate skor keparahan dan string alasan. | P0 | 3 | 8h | T-801 | Fungsi Explainability | Alasan jelas |
| T-804 | Penyimpanan Prediksi | Simpan hasil putusan ke tabel Prediksi. | P0 | 2 | 4h | T-801 | Fungsi DB | Data prediksi tersimpan |
| T-805 | Publish Prediksi | Pancarkan event PredictionGenerated. | P0 | 1 | 2h | T-804 | Redis Event | Event dipancarkan |

## Sprint 9: Sistem Notifikasi
**Epic Utama:** Peringatan

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-901 | Subscriber Prediksi | Dengarkan event prediksi. | P0 | 2 | 4h | T-805 | Redis Consumer | Event prediksi masuk |
| T-902 | Pengiriman Push Notification | Kirim via Firebase Admin SDK. | P0 | 4 | 12h | T-901 | FCM Sender | Push diterima HP |
| T-903 | Deduplikasi & Debounce Notifikasi | Jangan kirim spam berulang. | P0 | 2 | 6h | T-902 | Logika Filter | 1 notif per jam per user |
| T-904 | Log Pengiriman | Simpan histori notifikasi pengguna. | P1 | 2 | 4h | T-902 | Fungsi DB | Log tersimpan |

## Sprint 10: Backend API
**Epic Utama:** Penyajian

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-1001 | Endpoint Prediksi Saat Ini | GET /api/v1/predictions/current | P0 | 2 | 6h | T-804 | Router Endpoint | Data JSON keluar |
| T-1002 | Endpoint Area & Peta | GET /api/v1/areas (GeoJSON). | P0 | 3 | 8h | T-204 | Router Endpoint | Data peta tersedia |
| T-1003 | Endpoint Grafik Cuaca | Data time-series untuk frontend. | P1 | 2 | 6h | T-205 | Router Endpoint | Array chart data |
| T-1004 | Endpoint Riwayat Banjir | GET /api/v1/history. | P1 | 2 | 4h | T-206 | Router Endpoint | Paginasi jalan |
| T-1005 | API Caching Middleware | Cache Redis untuk GET API. | P1 | 2 | 4h | T-207 | Middleware | Cache Hit berjalan |

## Sprint 11: Flutter Foundation
**Epic Utama:** Frontend

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-1101 | Init Project & Tema | Flutter, Riverpod, GoRouter, PRAKIRA theme. | P0 | 2 | 6h | - | Flutter Repo | UI dasar jalan |
| T-1102 | Integrasi Auth & Firebase | Login/Google Sign In di UI. | P0 | 4 | 12h | T-302 | Auth Flow | Login sukses |
| T-1103 | Navigasi Bawah & Routing | Shell Route untuk Home, Map, dll. | P0 | 1 | 3h | T-1101 | Nav UI | Bisa pindah tab |
| T-1104 | HTTP Client & Interceptor | Dio + JWT injeksi. | P0 | 2 | 4h | T-1102 | Dio Client | Koneksi ke backend |
| T-1105 | Setup Flutter Push Notif | Terima FCM push di background. | P0 | 3 | 8h | T-902 | FCM Handler | Notif tampil |

## Sprint 12: Antarmuka Dasbor
**Epic Utama:** Frontend Utama

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-1201 | UI Dasbor Utama | Konsumsi API prediksi, tampilkan status RISIKO. | P0 | 4 | 12h | T-1001 | Home Screen | Warna status berubah |
| T-1202 | UI Penjelasan & ETA | Tampilkan widget ETA dan reason prediksi. | P0 | 2 | 6h | T-1201 | Info Widget | Penjelasan terlihat |
| T-1203 | Grafik Hujan/Sungai | Gunakan fl_chart untuk tren. | P1 | 3 | 8h | T-1003 | Chart UI | Grafik interaktif |
| T-1204 | Selector Area | Pilih area pantauan (dropdown). | P1 | 2 | 4h | T-1002 | Dropdown UI | Bisa pindah area |

## Sprint 13: Peta & Laporan
**Epic Utama:** Frontend Lanjutan

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-1301 | Mapbox/Google Maps | Tampilkan peta dengan overlay GeoJSON kawasan rawan. | P0 | 4 | 12h | T-1002 | Map Screen | Peta merender |
| T-1302 | UI Form Laporan Warga | Form input lapor banjir & lokasi. | P1 | 2 | 6h | T-1103 | Report Form | Input jalan |
| T-1303 | Upload Foto Laporan | Kompres gambar & upload. | P1 | 3 | 8h | T-1302 | Upload Logic | Gambar terkirim |
| T-1304 | UI Riwayat & Kotak Masuk | Daftar notifikasi & arsip. | P1 | 2 | 6h | T-1004 | List Screen | Data historis muncul |

## Sprint 14: Deployment MVP
**Epic Utama:** Rilis Skala Kecil

| ID | Judul Tugas | Deskripsi Singkat | Pri | SP | Est. | Dep. | *Deliverable* | *Definition of Done (DoD)* |
|---|---|---|---|---|---|---|---|---|
| T-1401 | Deployment Render/Railway | Deploy PostgreSQL, Redis, FastAPI ke Render/Railway. | P0 | 4 | 12h | T-112 | URL API Live | Backend online |
| T-1402 | Konfigurasi Domain & Cloudflare | SSL & DNS untuk API. | P0 | 1 | 2h | T-1401 | Cloudflare DNS | API diakses via HTTPS |
| T-1403 | Load Testing Sederhana | JMeter/Locust test ke Render API. | P1 | 2 | 4h | T-1401 | Test Report | Tahan beban wajar |
| T-1404 | Build APK/AAB Flutter | Kompilasi aplikasi Android & iOS. | P0 | 2 | 6h | T-1201 | Binary File | APK terbuat |
| T-1405 | Rilis Alpha | Distribusi internal APK via Firebase App Distribution. | P0 | 2 | 4h | T-1404 | Alpha Release | Dapat diunduh tester |

## Infrastruktur Masa Depan & Fitur Skala Nasional (Future Release)
Tugas-tugas arsitektur *enterprise* berikut sengaja dikecualikan dari Sprint MVP agar tim dapat bergerak cepat (*fast iteration*), dan baru akan dieksekusi saat PRAKIRA berekspansi ke tahap operasional berskala nasional.

| ID | Judul Tugas Masa Depan | Deskripsi |
|---|---|---|
| T-F01 | Migrasi Kubernetes (GKE/EKS) | Pindah dari PaaS ke Kubernetes mandiri untuk skala besar. |
| T-F02 | Multi-Region Deployment | Redundansi antar benua/datacenter. |
| T-F03 | Integrasi Terraform Penuh | IaC untuk seluruh infrastruktur produksi. |
| T-F04 | Migrasi Redis ke Apache Kafka | Broker pesan skala nasional. |
| T-F05 | Disaster Recovery & Backup Lintas Cloud | Replikasi data otomatis ke penyedia cloud lain. |
| T-F06 | Service Mesh (Istio) | Manajemen jaringan dan mtls antar layanan microservice. |
| T-F07 | Machine Learning Pipeline (MLOps) | Prediksi menggunakan AI (tensorflow/pytorch) selain aturan manual. |
