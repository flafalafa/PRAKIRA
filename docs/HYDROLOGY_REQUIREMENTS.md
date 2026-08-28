# Kebutuhan Hidrologi (HYDROLOGY_REQUIREMENTS)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Spesifikasi Desain  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan semua kebutuhan hidrologi yang diperlukan oleh PRAKIRA untuk memprediksi kejadian banjir.

Tujuannya adalah untuk mengubah data lingkungan mentah menjadi intelijen banjir yang bermakna.

Sistem harus memantau proses hidrologi secara utuh, bukan hanya bergantung pada prakiraan cuaca saja.

---

## 2. Model Area Pemantauan (Monitoring Area Model)

Setiap area yang dipantau direpresentasikan sebagai **Profil Area Hidrologi (Hydrological Area Profile / HAP)**.

Setiap HAP berisi:
* Batas administratif
* Daerah Aliran Sungai (DAS)
* Jaringan sungai
* Jaringan drainase
* Model topografi (Terrain model)
* Area observasi curah hujan
* Riwayat banjir
* Infrastruktur kritis

Contoh:
- ID Area: AREA-001
- Nama: Pondok Kacang Prima
- Status: Area Percontohan (Pilot Area)

---

## 3. Kebutuhan Daerah Aliran Sungai (Watershed Requirements)

Aplikasi harus mengidentifikasi:
* Nama DAS
* Batas DAS
* Luas DAS
* Arah aliran
* Daerah tangkapan air (Catchment area)
* Wilayah hulu
* Wilayah hilir
* Anak sungai (Tributaries)
* Zona akumulasi air

Tujuan:
Menentukan di mana curah hujan berkontribusi pada debit sungai sebelum mencapai area yang dipantau.

---

## 4. Kebutuhan Sungai (River Requirements)

Untuk setiap sungai yang berdampak pada area yang dipantau, kumpulkan:
* Nama Sungai
* ID Sungai
* Klasifikasi Sungai
* Lebar Sungai
* Kedalaman Sungai
* Panjang Sungai
* Penampang Silang (Cross Section)
* Kapasitas Sungai
* Debit Rata-rata
* Debit Puncak (Peak Flow)
* Kapasitas Banjir
* Titik Luapan
* Segmen Kritis
* Lokasi Jembatan
* Riwayat Kejadian Luapan
* Catatan Pemeliharaan (jika tersedia)

---

## 5. Kebutuhan Topografi (Terrain Requirements)

Dataset topografi yang diperlukan:
* Model Elevasi Digital (DEM)
* Kemiringan (Slope)
* Elevasi
* Kontur
* Arah Aliran (Flow Direction)
* Akumulasi Aliran (Flow Accumulation)
* Kelengkungan Medan (Terrain Curvature)
* Area Cekungan (Depression Areas)
* Cekungan Alami (Natural Basins)

Tujuan:
Memperkirakan di mana limpasan permukaan (runoff) berakumulasi secara alami.

---

## 6. Pemantauan Curah Hujan (Rainfall Monitoring)

Sistem harus memantau:
* Curah hujan saat ini
* Prakiraan curah hujan
* Akumulasi per jam
* Akumulasi harian
* Intensitas hujan
* Durasi badai
* Ukuran sel hujan
* Pergerakan hujan
* Arah hujan
* Kecepatan hujan
* Distribusi hujan spasial
* Curah hujan di hulu
* Curah hujan di hilir

---

## 7. Pemantauan Angin (Wind Monitoring)

Pantau:
* Kecepatan angin
* Arah angin
* Hembusan angin (Wind gust)
* Vektor pergerakan badai

Tujuan:
Memperkirakan arah pergerakan hujan di masa mendatang.

---

## 8. Pemantauan Satelit (Satellite Monitoring)

Pantau:
* Perkembangan awan
* Kepadatan awan
* Aktivitas konvektif
* Pertumbuhan badai
* Peluruhan badai
* Pergerakan awan
* Estimasi curah hujan satelit

---

## 9. Infrastruktur Drainase (Drainage Infrastructure)

Kumpulkan:
* Jaringan drainase
* Ukuran drainase
* Kapasitas drainase
* Arah drainase
* Kolam retensi (Tandon)
* Stasiun pompa
* Pintu air
* Kanal
* Titik kemacetan yang diketahui (Bottlenecks)
* Laporan pemeliharaan drainase

---

## 10. Infrastruktur Perkotaan (Urban Infrastructure)

Petakan infrastruktur kritis:
* Jalan raya
* Jembatan
* Rumah sakit
* Sekolah
* Tempat evakuasi
* Rute darurat
* Jembatan rendah (Low bridges)
* Terowongan (Underpasses)
* Area parkir kendaraan
* Stasiun transportasi umum

---

## 11. Basis Data Banjir Historis (Historical Flood Database)

Untuk setiap kejadian banjir yang tercatat:
* Tanggal
* Waktu
* Kedalaman air
* Durasi
* Jalan yang terdampak
* Rumah yang terdampak
* Kondisi sungai
* Curah hujan
* Penyebab
* Foto
* Video
* Laporan pemerintah
* Laporan masyarakat
* Waktu pemulihan (Recovery time)

---

## 12. Kebutuhan Data Waktu Nyata (Real-Time Data Requirements)

Platform harus menyerap:
* API Cuaca
* API Radar
* API Satelit
* API Tinggi Muka Air Sungai
* API Hidrologi
* Sensor IoT (di masa depan)
* Laporan Masyarakat
* Informasi Lalu Lintas
* Laporan Darurat

---

## 13. Interval Pembaruan Data (Data Refresh Interval)

* **Cuaca:** Setiap 5–15 menit (tergantung sumber)
* **Radar:** Setiap 5–10 menit
* **Satelit:** Setiap 10–15 menit
* **Tinggi Muka Air:** Sesering mungkin (target ≤10 menit)
* **Mesin Prediksi (Prediction Engine):** Setiap 5 menit atau setiap kali ada data baru yang signifikan

---

## 14. Kualitas Data (Data Quality)

Setiap sumber data harus menyertakan:
* Sumber (Source)
* Stempel waktu (Timestamp)
* Akurasi
* Cakupan (Coverage)
* Resolusi
* Skor Keandalan (Reliability Score)
* Indikator Data Hilang (Missing Data Indicator)

---

## 15. Indikator Hidrologi (Hydrological Indicators)

Platform harus menghitung:
* Indeks Hujan Pendahulu (Antecedent Rainfall Index)
* Akumulasi Curah Hujan
* Indeks Kejenuhan Daerah Tangkapan (Catchment Saturation Index)
* Pemanfaatan Kapasitas Sungai
* Estimasi Limpasan Permukaan (Runoff)
* Kecepatan Aliran (diestimasi atau diobservasi)
* Probabilitas Luapan
* Skor Risiko Banjir
* Estimasi Waktu Kedatangan (ETA)
* Skor Kepercayaan (Confidence Score)

---

## 16. Aturan Pengambilan Keputusan (Decision Rules - Versi 1)

Prediksi awal harus menggunakan aturan yang transparan.

Contoh:
**JIKA (IF):**
Curah hujan lebat terdeteksi di hulu
**DAN**
Kapasitas sungai melebihi ambang batas
**DAN**
Air mengalir / bermuara menuju area yang dipantau
**MAKA (THEN):**
Tingkatkan probabilitas banjir.

Ambang batas pastinya akan dikalibrasi selama proses validasi lapangan.

---

## 17. Input Pembelajaran Mesin di Masa Depan (Future Machine Learning Inputs)

Model AI di kemudian hari mungkin menggunakan:
* Label banjir historis
* Citra radar
* Citra satelit
* Telemetri sungai
* Fitur turunan DEM
* Prakiraan cuaca
* Laporan masyarakat
* Sensor IoT
* Kondisi lalu lintas
* Perubahan tata guna lahan

---

## 18. Konfigurasi Area Percontohan (Pilot Area Configuration)

* **Area Percontohan:** AREA-001
* **Lokasi:** Pondok Kacang Prima
* **Wilayah Administratif:** Pondok Aren, Tangerang Selatan
* **Tujuan:** Memvalidasi model prediksi sebelum berekspansi ke area tambahan.

---

## 19. Strategi Ekspansi (Expansion Strategy)

Mesin prediksi harus tetap tidak terikat lokasi (*location-independent*).

Untuk menambahkan kota baru, hanya langkah berikut yang diperlukan:
1. Buat Profil Area Hidrologi baru (HAP).
2. Impor data DAS.
3. Impor data topografi.
4. Impor jaringan sungai.
5. Impor riwayat banjir.
6. Konfigurasikan radius pemantauan.

Tidak boleh ada perubahan arsitektur yang diperlukan pada mesin prediksi inti (*core prediction engine*).

---

## 20. Kriteria Penerimaan (Acceptance Criteria)

Platform dianggap siap secara hidrologi apabila dapat:
* Terus memantau semua variabel lingkungan yang diperlukan.
* Menghubungkan kondisi hulu dengan risiko banjir di hilir.
* Menjelaskan setiap prediksi menggunakan bukti yang dapat diamati (*observable evidence*).
* Menghasilkan estimasi ETA dengan tingkat kepercayaan yang dicantumkan.
* Mendukung banyak area pemantauan menggunakan arsitektur sistem yang sama.
