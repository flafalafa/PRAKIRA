# Alur Data Sistem (SYSTEM_DATA_FLOW)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Spesifikasi Arsitektur  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan bagaimana data bergerak di seluruh platform PRAKIRA.

Tujuannya adalah untuk mengubah observasi lingkungan mentah menjadi intelijen banjir yang andal dengan latensi minimal.

---

## 2. Alur Data Tingkat Tinggi (High-Level Data Flow)

Sumber Data Eksternal
↓
Pengumpul Data (*Data Collectors*)
↓
Lapisan Validasi (*Validation Layer*)
↓
Lapisan Normalisasi (*Normalization Layer*)
↓
Rekayasa Fitur (*Feature Engineering*)
↓
Mesin Hidrologi (*Hydrology Engine*)
↓
Mesin Keputusan Banjir (*Flood Decision Engine*)
↓
Layanan Prediksi (*Prediction Service*)
↓
Layanan Notifikasi (*Notification Service*)
↓
API Gateway
↓
Aplikasi Seluler Flutter

---

## 3. Sumber Data (Data Sources)

Penyedia eksternal yang didukung:
* API Prakiraan Cuaca
* API Radar Hujan
* Citra Satelit
* API Pemantauan Sungai
* Data Terbuka Pemerintah (*Government Open Data*)
* Model Elevasi Digital (DEM)
* OpenStreetMap
* Laporan Masyarakat (masa depan)
* Sensor IoT (masa depan)

Setiap sumber harus menyertakan metadata:
* Stempel waktu (*Timestamp*)
* Cakupan geografis
* Interval pembaruan
* Skor keandalan

---

## 4. Lapisan Pengumpulan Data (Data Collection Layer)

Tanggung jawab:
* Mengambil data (*Polling*) dari API
* Menerima kejadian webhook (*Webhook events* - masa depan)
* Mengulang (*Retry*) permintaan yang gagal
* Memvalidasi autentikasi
* Menyimpan respons mentah
* Mendeteksi data ganda (*Duplicate data*)

Keluaran:
* Dataset Lingkungan Mentah (*Raw Environmental Dataset*)

---

## 5. Lapisan Validasi (Validation Layer)

Pemeriksaan:
* Nilai yang hilang (*Missing values*)
* Koordinat yang tidak valid
* Observasi ganda (*Duplicate observations*)
* Kebaruan stempel waktu (*Timestamp freshness*)
* Deteksi anomali (*Outlier detection*)
* Ketersediaan penyedia layanan (*Provider availability*)

Observasi yang tidak valid dikarantina dan dikeluarkan dari proses prediksi.

---

## 6. Lapisan Normalisasi (Normalization Layer)

Mengonversi semua data penyedia ke dalam format yang seragam (*common format*).

Contoh:
**Curah Hujan (Rainfall)**
* Penyedia A → mm/jam
* Penyedia B → mm/15 menit
↓
* **Unit Standar** → mm/jam

---

## 7. Rekayasa Fitur (Feature Engineering)

Menghasilkan indikator turunan (*derived indicators*):
* Akumulasi curah hujan
* Indeks Hujan Pendahulu (*Antecedent Rainfall Index*)
* Kejenuhan Daerah Tangkapan (*Catchment Saturation*)
* Pemanfaatan Kapasitas Sungai
* Arah Aliran (*Flow Direction*)
* Kecepatan Badai (*Storm Velocity*)
* ETA Badai
* Masukan Probabilitas Banjir

---

## 8. Jalur Prediksi (Prediction Pipeline)

Analisis Hidrologi
↓
Mesin Aturan (*Rule Engine*)
↓
Penyesuaian Pembelajaran Mesin (*Machine Learning Adjustment* - masa depan)
↓
Skor Risiko
↓
ETA
↓
Keparahan (*Severity*)
↓
Kepercayaan (*Confidence*)
↓
Rekomendasi

---

## 9. Jalur Notifikasi (Notification Pipeline)

Prediksi Dihasilkan
↓
Evaluasi Ambang Batas (*Threshold Evaluation*)
↓
Deduplikasi
↓
Penugasan Prioritas (*Priority Assignment*)
↓
Notifikasi Push (*Push Notification*)
↓
SMS / WhatsApp (masa depan)
↓
Siaran Darurat (*Emergency Broadcast* - masa depan)

---

## 10. Alur API Seluler (Mobile API Flow)

Permintaan Klien (*Client Request*)
↓
API Gateway
↓
Autentikasi
↓
Layanan Prediksi (*Prediction Service*)
↓
Pemformat Respons (*Response Formatter*)
↓
Aplikasi Flutter

---

## 11. Strategi Penyimpanan (Storage Strategy)

* **Data Mentah** → *Immutable* (Tidak dapat diubah)
↓
* **Data Terproses** → *Queryable* (Dapat dikueri)
↓
* **Hasil Prediksi** → *Versioned* (Berdasarkan versi)
↓
* **Arsip Historis** → Penyimpanan Jangka Panjang (*Long-term Storage*)

---

## 12. Pencatatan & Observabilitas (Logging & Observability)

Setiap komponen harus memancarkan (*emit*):
* Log terstruktur (*Structured logs*)
* Metrik (*Metrics*)
* Jejak (*Traces*)
* Status kesehatan (*Health status*)
* Laporan kesalahan (*Error reports*)

---

## 13. Sasaran Keandalan (Reliability Goals)

* Pengulangan otomatis (*Automatic retries*)
* Degradasi bertahap (*Graceful degradation*)
* Prediksi parsial ketika beberapa penyedia gagal (*Partial prediction*)
* Pemantauan ujung-ke-ujung (*End-to-end monitoring*)
* Jejak audit lengkap (*Full audit trail*)
