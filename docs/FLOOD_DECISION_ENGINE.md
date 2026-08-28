# Mesin Keputusan Banjir (FLOOD_DECISION_ENGINE)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Spesifikasi Sistem Inti  
Pemilik: Tim Prediksi  

---

## 1. Tujuan (Purpose)

Mesin Keputusan Banjir (Flood Decision Engine / FDE) adalah lapisan kecerdasan inti dari PRAKIRA.

Tanggung jawabnya adalah mengubah berbagai observasi lingkungan menjadi prediksi banjir yang dapat ditindaklanjuti.

Mesin ini tidak sekadar memprakirakan cuaca.

Sebaliknya, ia menentukan:
* Apakah banjir kemungkinan besar akan terjadi?
* Di mana banjir akan terjadi?
* Kapan banjir akan terjadi?
* Seberapa parah banjir tersebut?
* Apa yang harus dilakukan pengguna?

Setiap keputusan yang dihasilkan oleh mesin ini harus dapat dijelaskan (*explainable*).

---

## 2. Prinsip Inti (Core Principles)

Mesin ini harus:
* Mengutamakan keselamatan manusia.
* Lebih memilih keputusan yang dapat dijelaskan daripada prediksi yang tidak transparan (*opaque*).
* Tidak pernah bergantung hanya pada satu sumber data.
* Terus memperbarui prediksi setiap kali observasi baru masuk.
* Mengkomunikasikan ketidakpastian melalui skor kepercayaan (*confidence scores*).

---

## 3. Masukan (Inputs)

Mesin ini terus-menerus menyerap observasi dari berbagai domain.

### Cuaca (Weather)
* Curah hujan saat ini
* Prakiraan curah hujan
* Intensitas curah hujan
* Durasi curah hujan
* Akumulasi curah hujan

### Radar
* Lokasi sel hujan
* Pergerakan sel hujan
* Intensitas sel hujan
* Pertumbuhan sel hujan
* Peluruhan sel hujan

### Angin (Wind)
* Arah angin
* Kecepatan angin
* Vektor badai

### Satelit (Satellite)
* Perkembangan awan
* Aktivitas konvektif
* Pergerakan awan

### Sungai (River)
* Tinggi muka air
* Debit sungai
* Kecepatan aliran sungai
* Pemanfaatan kapasitas
* Indikator luapan

### Topografi (Terrain)
* Elevasi
* Arah aliran (*Flow direction*)
* Daerah Aliran Sungai (*Watershed*)
* Daerah tangkapan air (*Catchment area*)
* Akumulasi aliran (*Flow accumulation*)

### Drainase (Drainage)
* Status pompa
* Kolam retensi / tandon
* Kapasitas drainase
* Titik kemacetan yang diketahui (*Bottlenecks*)

### Basis Data Historis (Historical Database)
* Kejadian banjir sebelumnya
* Riwayat curah hujan
* Luapan historis
* Tren musiman

### Laporan Masyarakat - Masa Depan (Community Reports)
* Laporan pengguna
* Foto
* Kedalaman air
* Penutupan jalan

---

## 4. Alur Keputusan (Decision Pipeline)

Data Lingkungan Mentah
↓
Validasi
↓
Normalisasi
↓
Rekayasa Fitur (*Feature Engineering*)
↓
Analisis Hidrologi
↓
Evaluasi Aturan (*Rule Evaluation*)
↓
Penilaian Risiko (*Risk Assessment*)
↓
Estimasi ETA
↓
Estimasi Keparahan
↓
Perhitungan Skor Kepercayaan (*Confidence Calculation*)
↓
Pembuatan Rekomendasi
↓
Mesin Notifikasi
↓
Aplikasi Seluler

---

## 5. Tahap Validasi (Validation Stage)

Setiap observasi yang masuk harus divalidasi.

Validasi mencakup:
* Kebaruan stempel waktu (*Timestamp freshness*)
* Nilai yang hilang (*Missing values*)
* Keandalan sensor
* Ketersediaan API
* Deteksi duplikasi
* Konsistensi geografis

Data yang tidak valid akan menurunkan skor kepercayaan dan tidak boleh secara diam-diam memengaruhi prediksi.

---

## 6. Analisis Hidrologi (Hydrological Analysis)

Mesin ini mengestimasi bagaimana curah hujan berubah menjadi limpasan (*runoff*).

Perhitungan yang diperlukan:
* Akumulasi curah hujan
* Kejenuhan daerah tangkapan
* Potensi limpasan permukaan
* Tren debit sungai
* Pemanfaatan kapasitas sungai
* Kemungkinan luapan

Tujuan:
Memahami pergerakan air sebelum memprediksi dampaknya.

---

## 7. Evaluasi Aturan (Rule Evaluation)

Versi 1 menggunakan aturan yang transparan.

Contoh 1:
**JIKA (IF):**
Curah hujan lebat terdeteksi di hulu
**DAN (AND):**
Badai bergerak menuju DAS yang dipantau
**DAN (AND):**
Pemanfaatan kapasitas sungai melampaui ambang batas
**MAKA (THEN):**
Tingkatkan Risiko Banjir.

Contoh 2:
**JIKA (IF):**
Tinggi muka air sungai naik dengan cepat
**DAN (AND):**
Curah hujan terus berlanjut
**MAKA (THEN):**
Kurangi ETA.

Contoh 3:
**JIKA (IF):**
Ada hambatan drainase (*bottleneck*)
**DAN (AND):**
Curah hujan lokal tinggi
**MAKA (THEN):**
Tingkatkan tingkat keparahan banjir lokal.

---

## 8. Skor Risiko Banjir (Flood Risk Score)

Rentang: 0–100

Contoh:
- **0–20:** AMAN (SAFE)
- **20–40:** WASPADA (WATCH)
- **40–70:** SIAGA (ALERT)
- **70–90:** BAHAYA (WARNING)
- **90–100:** DARURAT (EMERGENCY)

Skor risiko harus dihitung ulang setiap kali data baru yang signifikan diterima.

---

## 9. Mesin ETA (ETA Engine)

Mesin ETA memperkirakan kapan dampak banjir mungkin mencapai lokasi yang dipantau.

Masukan:
* Curah hujan
* Kecepatan sungai
* Jarak dari hulu
* Respons daerah tangkapan
* Waktu (*timing*) historis
* Efisiensi drainase

Keluaran:
* 30 menit
* 1 jam
* 2 jam
* 4 jam
* 6 jam
* 12 jam

---

## 10. Mesin Keparahan (Severity Engine)

Mengestimasi keparahan banjir.

Keluaran:
* Ringan (*Minor*)
* Sedang (*Moderate*)
* Parah (*Major*)
* Ekstrem (*Extreme*)

Indikator yang memungkinkan:
* Estimasi kedalaman
* Perkiraan jalan tergenang
* Dampak pada rumah
* Risiko pada kendaraan

---

## 11. Mesin Kepercayaan (Confidence Engine)

Setiap prediksi mencakup tingkat kepercayaan.

Tingkat kepercayaan dipengaruhi oleh:
* Kebaruan data
* Jumlah sumber yang tersedia
* Kesesuaian antar sumber
* Kemiripan historis
* Keandalan sensor

Contoh:
* Risiko Banjir: 82%
* Kepercayaan: 91%

---

## 12. Mesin Rekomendasi (Recommendation Engine)

Mesin ini mengubah prediksi menjadi tindakan sederhana.

Contoh:
* Terus lakukan pemantauan.
* Siapkan barang-barang berharga.
* Pindahkan sepeda motor.
* Pindahkan mobil.
* Hindari jalan tertentu.
* Bersiap untuk evakuasi.
* Evakuasi segera.

Rekomendasi harus ringkas, dapat ditindaklanjuti, dan diprioritaskan.

---

## 13. Mesin Notifikasi (Notification Engine)

Notifikasi bersifat *event-driven* (didorong oleh kejadian).

Contoh:
* Curah hujan lebat terdeteksi di hulu.
* Probabilitas banjir meningkat menjadi 72%.
* ETA dipersingkat menjadi 90 menit.
* Kapasitas sungai terlampaui.

Notifikasi harus menghindari pengulangan yang tidak perlu, dengan tetap memastikan keselamatan pengguna.

---

## 14. Mesin Penjelasan (Explainability Engine)

Setiap prediksi harus mencakup penjelasan yang dapat dibaca oleh manusia.

Contoh:
Probabilitas banjir meningkat karena:
* Curah hujan hulu lebat.
* Tinggi muka air sungai meningkat.
* Badai bergerak menuju DAS.
* Kemiripan dengan pola historis.

Penjelasan ini harus dapat dipahami oleh pengguna non-teknis.

---

## 15. Mesin Pembelajaran (Learning Engine)

Mesin ini terus berkembang dan membaik.

Setelah setiap kejadian banjir, kumpulkan:
* Kedalaman air yang diobservasi
* Durasi banjir
* Laporan pengguna
* Foto
* Penutupan jalan
* Akurasi prediksi
* Kesalahan prediksi

Sistem harus menggunakan observasi ini untuk mengkalibrasi ulang prediksi di masa mendatang.

---

## 16. Riwayat Keputusan (Decision History)

Setiap prediksi harus disimpan.

Rekam:
* Stempel waktu (*Timestamp*)
* Cuplikan masukan (*Input snapshot*)
* Keputusan
* ETA
* Risiko
* Kepercayaan
* Rekomendasi

Ini memungkinkan audit dan penyempurnaan model.

---

## 17. Strategi Kegagalan (Failure Strategy)

Jika data kritis tidak tersedia:
* Kurangi skor kepercayaan.
* Beritahu sistem pemantauan internal.
* Terus gunakan sumber tepercaya yang tersisa.
* Jangan pernah memalsukan atau mengarang observasi yang hilang.

---

## 18. Peta Jalan Versi (Version Roadmap)

* **Versi 1:** Mesin Keputusan Berbasis Aturan (*Rule-Based Decision Engine*)
* **Versi 2:** Simulasi Hidrologi
* **Versi 3:** Keputusan Dibantu Pembelajaran Mesin (*Machine Learning Assisted Decisions*)
* **Versi 4:** Hibrida Hidrologi + AI
* **Versi 5:** Platform Intelijen Banjir yang Belajar Mandiri (*Self-Learning Flood Intelligence Platform*)

---

## 19. Kriteria Keberhasilan (Success Criteria)

Mesin Keputusan harus:
* Menghasilkan prediksi yang dapat dijelaskan.
* Mendeteksi peningkatan risiko banjir sejak dini.
* Memberikan estimasi ETA yang berguna.
* Meminimalkan alarm palsu.
* Terus beradaptasi seiring ketersediaan bukti baru.
* Mendukung banyak area pemantauan tanpa perlu merombak desain.

---

## 20. Filosofi Panduan (Guiding Philosophy)

PRAKIRA bukanlah sebuah aplikasi cuaca.

PRAKIRA adalah **Platform Intelijen Banjir**.

Tujuannya bukan sekadar memberi tahu pengguna bahwa hujan sedang turun.

Tujuannya adalah memberikan informasi tepercaya dan waktu yang cukup bagi masyarakat agar mereka bisa mengambil keputusan yang lebih aman sebelum banjir melanda.
