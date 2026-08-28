# Model Prediksi PRAKIRA

Versi: 1.0  
Status: Draf  
Pemilik: Tim Produk & AI  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan model prediksi banjir konseptual yang digunakan oleh PRAKIRA.

Tujuannya **bukan untuk memprediksi hujan**, melainkan untuk memprediksi **probabilitas, waktu kedatangan, dan potensi keparahan banjir** di lokasi spesifik menggunakan berbagai sumber data lingkungan.

Model prediksi harus transparan, dapat dijelaskan (explainable), dan terus ditingkatkan secara berkelanjutan menggunakan observasi historis dan pembelajaran mesin (machine learning).

---

## 2. Pernyataan Masalah (Problem Statement)

Aplikasi cuaca tradisional hanya menyediakan prakiraan cuaca.

Pengguna masih belum mengetahui:
* Apakah rumah saya akan kebanjiran?
* Kapan air akan tiba?
* Apakah saya harus memindahkan kendaraan saya?
* Seberapa parah banjir yang akan terjadi?

PRAKIRA menjawab pertanyaan-pertanyaan ini.

---

## 3. Tujuan Prediksi (Prediction Goals)

Sistem harus dapat memperkirakan:
* Probabilitas Banjir
* Estimasi Waktu Kedatangan (Estimated Time of Arrival - ETA)
* Estimasi Keparahan Banjir
* Skor Kepercayaan (Confidence Score)
* Rekomendasi Tindakan Pengguna

Contoh:
- Risiko Banjir : TINGGI (87%)
- ETA : 2 jam
- Estimasi Ketinggian Air : 30–50 cm
- Rekomendasi : Pindahkan kendaraan segera.

---

## 4. Filosofi Prediksi (Prediction Philosophy)

Banjir jarang disebabkan secara langsung hanya oleh curah hujan tepat di atas lokasi pengguna.

Banjir perkotaan umumnya dipengaruhi oleh:
* Curah hujan di hulu
* Debit sungai
* Kapasitas sungai
* Kinerja drainase
* Elevasi / topografi lahan
* Limpasan permukaan (Surface runoff)
* Pola banjir historis

Oleh karena itu, curah hujan hanyalah salah satu masukan di antara banyak faktor lainnya.

---

## 5. Faktor Prediksi Inti (Core Prediction Factors)

### Cuaca (Weather)
Variabel:
* Intensitas curah hujan
* Durasi curah hujan
* Akumulasi curah hujan
* Prakiraan curah hujan
* Pergerakan badai

### Angin (Wind)
Variabel:
* Arah angin
* Kecepatan angin
* Arah pergerakan badai

### Radar
Variabel:
* Lokasi sel hujan
* Ukuran sel hujan
* Intensitas hujan
* Pergerakan hujan
* Estimasi kedatangan

### Satelit (Satellite)
Variabel:
* Perkembangan awan
* Sistem konvektif
* Evolusi badai

### Sungai (River)
Variabel:
* Tinggi muka air sungai
* Debit sungai
* Kecepatan aliran sungai
* Kapasitas sungai
* Probabilitas luapan

### Topografi (Terrain)
Variabel:
* Elevasi
* Kemiringan lereng (Slope)
* Akumulasi aliran (Flow accumulation)
* Daerah Aliran Sungai (Watershed)
* Area cekungan (Depression areas)

### Drainase (Drainage)
Variabel:
* Kondisi saluran air
* Kapasitas saluran air
* Status stasiun pompa
* Kolam retensi (Tandon)
* Konektivitas saluran air

### Data Historis (Historical Data)
Variabel:
* Banjir sebelumnya
* Riwayat curah hujan
* Peristiwa luapan sungai
* Pola musiman

---

## 6. Alur Kerja Prediksi (Prediction Workflow)

Data Lingkungan
↓
Validasi Data
↓
Rekayasa Fitur (Feature Engineering)
↓
Analisis Hidrologi
↓
Model Risiko Banjir
↓
Penyesuaian Pembelajaran Mesin (Machine Learning Adjustment)
↓
Penilaian Risiko
↓
Mesin Notifikasi
↓
Aplikasi Seluler

---

## 7. Tingkat Risiko (Risk Levels)

- **Level 1: AMAN (SAFE)**
  - Probabilitas: 0–20%
  - Tidak ada tindakan yang diperlukan.

- **Level 2: WASPADA (WATCH)**
  - Probabilitas: 20–40%
  - Terus lakukan pemantauan.

- **Level 3: SIAGA (ALERT)**
  - Probabilitas: 40–70%
  - Siapkan kendaraan dan barang-barang berharga.

- **Level 4: BAHAYA (WARNING)**
  - Probabilitas: 70–90%
  - Kemungkinan banjir sangat tinggi. Pindahkan kendaraan segera.

- **Level 5: DARURAT (EMERGENCY)**
  - Probabilitas: 90–100%
  - Banjir dipastikan terjadi. Lakukan evakuasi jika diperlukan.

---

## 8. Tingkat Keparahan Banjir (Flood Severity)

- **Ringan (Minor):** Ketinggian air di bawah 20 cm
- **Sedang (Moderate):** 20–50 cm
- **Parah (Major):** 50–100 cm
- **Ekstrem (Extreme):** Di atas 100 cm

---

## 9. Estimasi Waktu Kedatangan (ETA)

Model harus dapat memperkirakan waktu kedatangan air dalam rentang:
- 30 menit
- 1 jam
- 2 jam
- 4 jam
- 6 jam
- 12 jam

ETA harus diperbarui secara terus-menerus.

---

## 10. Skor Kepercayaan (Confidence Score)

Setiap prediksi harus menyertakan tingkat kepercayaan.

Contoh:
- Probabilitas Banjir: 84%
- Tingkat Kepercayaan: 91%
- Alasan: Curah hujan lebat terdeteksi di hulu, tinggi muka air sungai meningkat, sesuai dengan pola historis.

---

## 11. AI yang Dapat Dijelaskan (Explainable AI)

Setiap prediksi harus menjelaskan MENGAPA prediksi itu dibuat.

Contoh:
Prediksi dibuat karena:
* Curah hujan lebat terdeteksi di hulu
* Debit sungai meningkat
* Sel hujan bergerak menuju hulu DAS
* Mirip dengan peristiwa banjir historis sebelumnya

Pengguna tidak boleh menerima prediksi tanpa penjelasan.

---

## 12. Strategi Pembelajaran Mesin (Machine Learning Strategy)

Versi pertama akan menggunakan prediksi berbasis aturan (Rule-based).
Setelah data historis terkumpul cukup banyak, barulah Pembelajaran Mesin (ML) diperkenalkan.

Progresi yang disarankan:
**Tahap 1:** Mesin Aturan (Rule Engine)
↓
**Tahap 2:** Model Statistik
↓
**Tahap 3:** Pembelajaran Mesin (Machine Learning)
↓
**Tahap 4:** Hibrida AI + Model Hidrologi

---

## 13. Pembelajaran Berkelanjutan (Continuous Learning)

Setelah setiap peristiwa banjir, kumpulkan data berikut:
* Tanggal
* Waktu mulai
* Waktu berakhir
* Kedalaman banjir
* Foto dari pengguna
* Laporan pengguna
* Curah hujan
* Kondisi sungai

Sistem harus terus membaik seiring berjalannya waktu.

---

## 14. Strategi Notifikasi (Notification Strategy)

Hanya kirimkan notifikasi jika benar-benar bermakna.

Contoh:
- Curah hujan lebat terdeteksi di hulu.
- Tinggi muka air sungai meningkat tajam.
- Probabilitas banjir di atas ambang batas.
- ETA berada di bawah batas yang ditentukan pengguna.

Hindari pengiriman notifikasi yang berlebihan (spam).

---

## 15. Peningkatan di Masa Depan (Future Enhancements)

Versi mendatang dapat mencakup:
* Sensor muka air IoT
* Laporan banjir dari komunitas (Crowdsourcing)
* Analisis citra/gambar dengan AI
* Integrasi CCTV
* Prediksi aksesibilitas jalan raya
* Navigasi rute evakuasi yang aman
* Rekomendasi keselamatan kendaraan
* Platform intelijen banjir lintas kota (Multi-city platform)

---

## 16. Metrik Keberhasilan (Success Metrics)

- **Akurasi Prediksi:** Target ≥80%
- **Tingkat Alarm Palsu (False Alarm Rate):** Target <20%
- **Rata-Rata Waktu Peringatan:** Target ≥60 menit sebelum banjir (tergantung kualitas ketersediaan data)
- **Pengiriman Notifikasi:** Target >99%
- **Kepuasan Pengguna:** Target >4.5/5

---

## 17. Prinsip Panduan (Guiding Principles)

* Dapat dijelaskan (Explainable) jauh lebih baik daripada prediksi kotak hitam (black-box).
* Keselamatan manusia lebih diutamakan daripada kompleksitas teknis.
* Kualitas data lebih penting daripada kerumitan model AI.
* Prediksi harus mampu mengkomunikasikan ketidakpastian.
* Sistem harus terus belajar dari setiap peristiwa banjir yang terjadi.
* Arsitektur harus mendukung perluasan dari skala satu lingkungan hingga skala nasional tanpa perlu merancang ulang mesin prediksi.
