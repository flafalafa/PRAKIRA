# Komponen Sistem (SYSTEM_COMPONENTS)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Arsitektur Komponen  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan komponen-komponen perangkat lunak utama dari PRAKIRA beserta tanggung jawabnya.

Setiap komponen harus tetap modular, dapat diuji secara independen (*independently testable*), dan dapat diskalakan (*scalable*).

---

## 2. Arsitektur Inti (Core Architecture)

Penyedia Eksternal (*External Providers*)
↓
Lapisan Pengumpul (*Collector Layer*)
↓
Lapisan Pemrosesan (*Processing Layer*)
↓
Lapisan Prediksi (*Prediction Layer*)
↓
Lapisan Layanan (*Service Layer*)
↓
Lapisan Presentasi (*Presentation Layer*)

---

## 3. Komponen-Komponen (Components)

### API Gateway
Tanggung jawab:
* Autentikasi
* Perutean (*Routing*)
* Pembatasan laju (*Rate limiting*)
* Pembuatan versi (*Versioning*)
* Validasi permintaan (*Request validation*)

### Layanan Pengumpul Data (Data Collector Service)
Tanggung jawab:
* Mengambil data cuaca
* Mengambil data radar
* Mengambil observasi sungai
* Mengambil citra satelit
* Menjadwalkan tugas pengumpulan (*Schedule collection jobs*)
* Mengulang permintaan yang gagal (*Retry failed requests*)

### Layanan Validasi (Validation Service)
Tanggung jawab:
* Pemeriksaan kualitas data
* Validasi stempel waktu (*Timestamp validation*)
* Validasi geografis
* Deteksi duplikasi

### Layanan Rekayasa Fitur (Feature Engineering Service)
Tanggung jawab:
* Membangun indikator hidrologi
* Menormalisasi dataset
* Menghasilkan fitur siap pakai untuk ML (*ML-ready features*)

### Mesin Hidrologi (Hydrology Engine)
Tanggung jawab:
* Analisis Daerah Aliran Sungai (DAS)
* Estimasi limpasan permukaan (*Surface runoff*)
* Estimasi respons sungai
* Analisis daerah tangkapan air (*Catchment analysis*)

### Mesin Keputusan Banjir (Flood Decision Engine)
Tanggung jawab:
* Perhitungan risiko
* Estimasi ETA
* Estimasi keparahan
* Penentuan skor kepercayaan (*Confidence scoring*)
* Pembuatan rekomendasi

### Layanan Prediksi (Prediction Service)
Tanggung jawab:
* Menyimpan (*persist*) prediksi ke basis data
* Menyajikan API prediksi
* Membandingkan prediksi sebelumnya
* Memicu alur kerja lanjutan (*Trigger downstream workflows*)

### Layanan Notifikasi (Notification Service)
Tanggung jawab:
* Notifikasi *push*
* Penjadwalan
* Deduplikasi
* Pelacakan pengiriman (*Delivery tracking*)
* Aturan eskalasi (*Escalation rules*)

### Layanan Pengguna (User Service)
Tanggung jawab:
* Autentikasi
* Profil pengguna
* Lokasi tersimpan
* Preferensi peringatan (*Alert preferences*)

### Layanan Komunitas (Community Service)
Tanggung jawab:
* Menerima laporan warga
* Memvalidasi laporan
* Melampirkan media (foto/video)
* Penentuan skor reputasi (*Reputation scoring* - masa depan)

### Layanan Analitik (Analytics Service)
Tanggung jawab:
* Dasbor (*Dashboards*)
* Metrik operasional
* Kinerja model
* Analitik penggunaan (*Usage analytics*)

### Layanan Pembelajaran Mesin (Machine Learning Service - Masa Depan)
Tanggung jawab:
* Pelatihan model
* Pemilihan fitur (*Feature selection*)
* Penyempurnaan prediksi
* Deteksi pergeseran (*Drift detection*)
* Evaluasi kinerja

### Portal Administrasi (Administration Portal)
Tanggung jawab:
* Konfigurasi area
* Manajemen ambang batas (*Threshold management*)
* Pemantauan sumber data
* Administrasi pengguna
* Tinjauan insiden (*Incident review*)

---

## 4. Perhatian Lintas Sektoral (Cross-Cutting Concerns)

Semua komponen harus mendukung:
* Pencatatan terstruktur (*Structured logging*)
* Metrik (*Metrics*)
* Pemeriksaan kesehatan (*Health checks*)
* Pelacakan (*Tracing*)
* Manajemen konfigurasi
* Manajemen rahasia (*Secrets management*)

---

## 5. Pola Komunikasi (Communication Pattern)

Komunikasi yang disukai:

**Sinkron (*Synchronous*)**
REST API (Internal)
↓
**Asinkron (*Asynchronous*)**
Antrean Pesan (*Message Queue*)
↓
Pekerja Latar Belakang (*Background Workers*)

---

## 6. Strategi Penerapan (Deployment Strategy)

Setiap komponen harus dapat disebarkan (*deployable*) secara independen menggunakan *container*.

Tumpukan (*stack*) yang direkomendasikan:
* Docker
* Kubernetes (masa depan)
* PostgreSQL
* Redis
* Penyimpanan Objek (*Object Storage*)
* CDN
* Platform Pemantauan (*Monitoring Platform*)

---

## 7. Prinsip Skalabilitas (Scalability Principles)

* Layanan nir-keadaan (*Stateless services*)
* Penskalaan horizontal (*Horizontal scaling*)
* Pemrosesan berbasis peristiwa (*Event-driven processing*)
* Penerapan independen (*Independent deployments*)
* Isolasi kesalahan (*Fault isolation*)

---

## 8. Prinsip Panduan (Guiding Principles)

* Modular secara desain (*Modular by design*).
* Arsitektur yang mengutamakan API (*API-first architecture*).
* Pengembangan yang mengutamakan dokumentasi (*Documentation-first development*).
* Observabilitas sejak hari pertama (*Observability from day one*).
* Prediksi yang dapat dijelaskan lebih diutamakan daripada otomatisasi tak transparan.
* Orientasi yang mudah (*Easy onboarding*) untuk area pemantauan baru tanpa mengubah layanan inti.
