# Dokumen Kebutuhan Produk (PRD)

**Nama Proyek:** PRAKIRA (Penjaga Banjir)  
**Target Platform:** Mobile (Flutter / Android - Google Play Store)  
**Status:** Draf / Fase 1  

---

## 1. Visi (Vision)
Memberikan setiap keluarga waktu yang cukup untuk melindungi rumah dan kendaraan mereka sebelum banjir melanda.

## 2. Misi (Mission)
Membangun platform prediksi banjir yang akurat, dapat dijelaskan (explainable), dan mudah digunakan dengan menggabungkan:
- Radar cuaca
- Intensitas curah hujan
- Pergerakan angin
- Kondisi sungai
- Analisis daerah aliran sungai (DAS)
- Elevasi dataran (kontur tanah)
- Data historis kejadian banjir
- Kecerdasan Buatan (Artificial Intelligence)

## 3. Pernyataan Masalah (Problem Statement)
Warga sering kali menerima informasi banjir ketika sudah terlambat. Sebagian besar aplikasi cuaca hanya menjawab: *"Apakah akan turun hujan?"* Padahal yang sebenarnya perlu diketahui masyarakat adalah: *"Apakah rumah saya akan kebanjiran?"* PRAKIRA fokus untuk menjawab pertanyaan ini, menjembatani kesenjangan antara prakiraan cuaca umum dengan peringatan dini banjir yang sangat spesifik (hyper-local) dan dapat ditindaklanjuti.

## 4. Tujuan (Goals)
- Memprediksi risiko banjir di tingkat yang sangat spesifik (hyper-local) sebelum banjir terjadi.
- Memperkirakan waktu kedatangan banjir secara akurat.
- Memperkirakan potensi kedalaman genangan banjir.
- Mengirimkan pemberitahuan peringatan dini (push notifications).
- Menjelaskan alasan di balik prediksi tersebut (Explainable AI / AI yang dapat dipahami).
- Membantu warga melindungi rumah, keluarga, dan kendaraan mereka.
- Berhasil menerbitkan aplikasi di Google Play Store.

## 5. Metrik Keberhasilan (Success Metrics)
- **Akurasi Prediksi:** Mencapai tingkat akurasi (true-positive rate) >85% untuk prediksi banjir di area target.
- **Waktu Peringatan Dini:** Memberikan peringatan dini setidaknya 2 jam sebelum banjir tiba.
- **Ketersediaan Sistem (Uptime):** Ketersediaan 99,9%, yang sangat penting terutama selama musim hujan.
- **Adopsi Pengguna:** Mencapai 10.000 pengguna aktif di area target Fase 1 (Tangerang Selatan).
- **Latensi Notifikasi:** Notifikasi dikirimkan dalam waktu kurang dari 60 detik setelah pemicu risiko tinggi terdeteksi.

## 6. Persona Pengguna (User Personas)

**Persona 1: Pemilik Rumah (Budi)**
- **Profil:** 35 tahun, tinggal di Pondok Aren. Memiliki 1 mobil dan 2 sepeda motor.
- **Titik Masalah:** Sering terbangun dengan kondisi air sudah masuk ke garasi. Terlambat memindahkan mobilnya.
- **Kebutuhan:** Peringatan langsung yang mengatakan "Rumah Anda berisiko banjir dalam 2 jam."

**Persona 2: Ketua Lingkungan / RT (Pak Rahmat)**
- **Profil:** 50 tahun, bertanggung jawab atas 50 kepala keluarga di Pondok Kacang Prima.
- **Titik Masalah:** Perlu memutuskan kapan harus menyalakan sirene lingkungan dan membagikan karung pasir, tetapi tidak memiliki data yang dapat diandalkan.
- **Kebutuhan:** Dasbor yang menunjukkan tingkat risiko keseluruhan untuk lingkungannya dan ketinggian air sungai.

**Persona 3: Relawan Bencana (Siti)**
- **Profil:** 28 tahun, bekerja dengan LSM (NGO) lokal.
- **Titik Masalah:** Membuang waktu mencari tahu area mana yang paling membutuhkan perahu karet.
- **Kebutuhan:** Tampilan peta yang memprediksi area mana yang akan mengalami banjir terdalam.

## 7. Kasus Penggunaan (Use Cases)
1. **Pendaftaran Rumah:** Pengguna mendaftar dan menyematkan (pin) lokasi rumah mereka di peta.
2. **Dasbor Risiko Banjir:** Pengguna membuka aplikasi dan melihat tingkat risiko saat ini (Aman, Waspada, Bahaya) untuk lokasi spesifik mereka.
3. **Peringatan Dini:** Pengguna menerima notifikasi peringatan bahwa banjir diperkirakan terjadi dalam X jam, meminta mereka untuk memindahkan kendaraan.
4. **Radar Hujan & Status Sungai:** Pengguna melihat radar langsung dan ketinggian air sungai saat ini untuk memverifikasi prediksi AI.
5. **Garis Waktu (Timeline) Banjir:** Pengguna melihat garis waktu yang memprediksi kapan air akan naik dan kapan diperkirakan akan surut.

## 8. Kebutuhan Fungsional (Functional Requirements)
- **Autentikasi:** Pendaftaran dan login pengguna yang aman (Email, Google Auth).
- **Layanan Lokasi:** Integrasi peta (OpenStreetMap) untuk menentukan dan menyimpan lokasi rumah pengguna (disimpan di PostGIS).
- **Dasbor:** Antarmuka Pengguna (UI) waktu nyata yang menampilkan tingkat risiko, perkiraan waktu kedatangan, dan kedalaman.
- **Notifikasi Push:** Integrasi Firebase Cloud Messaging (FCM) untuk peringatan waktu nyata.
- **Integrasi Cuaca:** Proses latar belakang (cron jobs) di server untuk mengambil dan memproses data BMKG/OpenWeather.
- **API Mesin Prediksi:** Endpoint FastAPI yang menerima koordinat lokasi dan mengembalikan analisis risiko dari mesin AI.
- **Modul Penjelasan (Explainability):** Komponen UI yang merinci prediksi (misal: "Risiko Tinggi karena: Hujan Lebat (40mm/jam) + Ketinggian Sungai (2,5m) + Elevasi Rendah").

## 9. Kebutuhan Non-Fungsional (Non-Functional Requirements)
- **Skalabilitas:** Backend harus mampu menangani lonjakan lalu lintas yang tiba-tiba (10x beban normal) saat badai melanda.
- **Performa:** Waktu dari peluncuran aplikasi hingga dasbor dimuat harus di bawah 2 detik.
- **Keamanan:** Data lokasi pengguna harus dienkripsi dan dianonimkan (anonymized) saat digunakan untuk pelaporan agregat.
- **Performa AI:** Inferensi model prediksi harus mengembalikan hasil dalam waktu di bawah 500 milidetik per batch.
- **Ketahanan:** Penurunan fungsi secara bertahap (graceful degradation) jika API cuaca pihak ketiga mati (misalnya mundur ke rata-rata historis atau API sekunder).

## 10. Risiko (Risks)
- **Risiko Ketergantungan Data:** Sangat bergantung pada API pihak ketiga (BMKG, OpenWeather). Jika layanan mereka mati atau mengubah harga, sistem akan gagal. *(Mitigasi: Terapkan beberapa sumber data).*
- **Positif Palsu/Negatif Palsu (False Positives/Negatives):** Memprediksi banjir yang tidak terjadi (menyebabkan kelelahan peringatan/alert fatigue) atau melewatkan banjir (menyebabkan hilangnya kepercayaan). *(Mitigasi: Pelatihan model berkelanjutan dan putaran umpan balik/feedback loop).*
- **Biaya Infrastruktur:** Biaya tinggi yang terkait dengan pengambilan data cuaca yang sering dan menjalankan model AI. *(Mitigasi: Optimalkan caching dengan Redis dan optimalkan ukuran model).*

## 11. Peta Jalan (Roadmap)
- **Fase 1 (MVP):** Fokus secara ketat pada Pondok Kacang Prima, Pondok Aren, dan Tangerang Selatan. Menghadirkan mesin prediksi inti, aplikasi Flutter, dan notifikasi push. Publikasi ke Google Play Store.
- **Fase 2 (Ekspansi):** Memperluas cakupan ke Jabodetabek. Menerapkan pelaporan berbasis komunitas (crowdsourcing kedalaman banjir).
- **Fase 3 (Nasional & Ekosistem):** Mendukung seluruh Indonesia. Memperkenalkan dasbor pemeliharaan prediktif untuk pemerintah daerah (misal: mengidentifikasi saluran air yang tersumbat).

## 12. Lingkup Masa Depan (Future Scope)
- **Integrasi IoT:** Menghubungkan dengan sistem rumah pintar untuk mematikan listrik secara otomatis saat air banjir menyentuh sensor.
- **Kemitraan Asuransi:** Menawarkan premi asuransi mikro berdasarkan data risiko banjir yang sangat spesifik.
- **Koordinasi Bantuan Otomatis:** Mengirimkan permintaan SOS secara otomatis ke relawan terdekat berdasarkan perkiraan kedalaman banjir.
