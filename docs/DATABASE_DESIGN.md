# Desain Basis Data (DATABASE_DESIGN)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Desain Basis Data Logis  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan model data logis dari PRAKIRA.

Basis data dirancang untuk skalabilitas, analisis historis, kemudahan penjelasan (*explainability*), dan pembelajaran mesin (*machine learning*).

---

## 2. Domain Inti (Core Domains)

Platform ini dibagi ke dalam domain-domain berikut:
* Geografi
* Hidrologi
* Cuaca
* Prediksi
* Notifikasi
* Pengguna
* Laporan Masyarakat
* Pembelajaran Mesin
* Log Audit

---

## 3. Entitas Utama (Primary Entities)

### Area (Areas)
Menyimpan lokasi yang dipantau.
Contoh:
* AREA-001
* Pondok Kacang Prima

### Daerah Aliran Sungai (Watersheds)
Menyimpan batas DAS dan metadatanya.

### Sungai (Rivers)
Menyimpan geometri dan karakteristik sungai.

### Observasi Sungai (River Observations)
Rangkaian waktu (*time-series*) dari:
* Tinggi muka air
* Debit aliran
* Kapasitas
* Kecepatan aliran

### Observasi Cuaca (Weather Observations)
Rangkaian waktu dari:
* Curah hujan
* Suhu
* Kelembapan
* Tekanan udara
* Angin

### Observasi Radar (Radar Observations)
Menyimpan intensitas dan pergerakan sel hujan.

### Observasi Satelit (Satellite Observations)
Menyimpan estimasi presipitasi dan awan.

### Topografi (Terrain)
Menyimpan informasi turunan DEM (Model Elevasi Digital).

### Infrastruktur Drainase (Drainage Infrastructure)
Menyimpan:
* Saluran air (Drains)
* Pompa
* Kolam retensi / Tandon
* Pintu air

### Kejadian Banjir (Flood Events)
Menyimpan insiden banjir yang diobservasi.
Atribut mencakup:
* Waktu mulai
* Waktu berakhir
* Kedalaman air
* Penyebab
* Keparahan
* Dampak

### Prediksi (Predictions)
Menyimpan setiap prediksi yang dihasilkan.
*Field*:
* Skor Risiko
* ETA
* Kepercayaan (*Confidence*)
* Keparahan (*Severity*)
* Rekomendasi
* Versi Keputusan

### Notifikasi (Notifications)
Menyimpan riwayat notifikasi.
Status:
* Tertunda (*Pending*)
* Terkirim (*Delivered*)
* Gagal (*Failed*)
* Telah dibaca (*Read*)

### Pengguna (Users)
Menyimpan:
* Akun
* Lokasi Rumah
* Preferensi Peringatan
* Area Favorit

### Laporan Masyarakat (Community Reports)
Menyimpan:
* Foto
* Kedalaman air
* Kondisi jalan
* Komentar
* Status validasi

### Log Keputusan (Decision Logs)
Menyimpan setiap keputusan yang dibuat oleh Mesin Keputusan Banjir (FDE).
Mendukung audit dan perbaikan model di masa mendatang.

---

## 4. Relasi (Relationships)

Area
↓
Daerah Aliran Sungai (Watershed)
↓
Sungai (River)
↓
Observasi Sungai
↓
Prediksi
↓
Notifikasi

Pengguna
↓
Preferensi Peringatan
↓
Notifikasi

Kejadian Banjir
↓
Dataset Pelatihan Historis (Historical Training Dataset)

---

## 5. Strategi Rangkaian Waktu (Time-Series Strategy)

* Observasi lingkungan bersifat *append-only* (hanya bisa ditambahkan).
* Rekaman historis tidak boleh pernah ditimpa (*overwritten*).

---

## 6. Retensi Data (Data Retention)

* Observasi mentah: ≥5 tahun
* Prediksi: Permanen
* Kejadian Banjir: Permanen
* Log Audit: Permanen

---

## 7. Strategi Kinerja (Performance Strategy)

* Pengindeksan spasial (*Spatial indexing*)
* Partisi rangkaian waktu (*Time-series partitioning*)
* Replika baca (*Read replicas*)
* Lapisan *caching*
* Tampilan terwujud (*Materialized views*)

---

## 8. Keamanan (Security)

* Otorisasi tingkat baris (*Row-level authorization*)
* Kredensial terenkripsi
* Riwayat audit yang tidak dapat diubah (*Immutable audit history*)
* Manajemen kunci API

---

## 9. Ekstensi Masa Depan (Future Extensions)

* Sensor IoT
* Metadata CCTV
* Telemetri kendaraan
* Integrasi layanan darurat
* Katalog banjir nasional
