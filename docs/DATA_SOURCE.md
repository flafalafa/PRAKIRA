# Katalog Sumber Data (Data Source Catalog)

Dokumen ini memetakan seluruh sumber data internal dan eksternal yang dibutuhkan oleh platform **PRAKIRA** untuk memodelkan dan memprediksi banjir secara akurat.

---

## 1. Cuaca Umum (Weather)
- **Tujuan (Purpose):** Memberikan informasi kondisi meteorologi secara umum (suhu, kelembaban, tekanan udara) sebagai fondasi dasar bagi model prediksi curah hujan dan penguapan.
- **Interval Pembaruan (Update Interval):** Setiap 1 hingga 3 jam (bergantung pada penyedia layanan).
- **Kualitas Data (Data Quality):** Sedang hingga tinggi. Data dari stasiun resmi sangat tepercaya, meskipun resolusi spasialnya terbatas.
- **API:** API Cuaca Publik BMKG, OpenWeatherMap API, atau WeatherAPI.
- **Keterbatasan (Limitations):** Hanya memberikan gambaran makro. Kondisi spesifik di lokasi pengguna yang jauh dari stasiun cuaca mungkin sedikit berbeda.

## 2. Radar Hujan (Rain Radar)
- **Tujuan (Purpose):** Mendeteksi intensitas (dBZ), lokasi, dan pergerakan presipitasi curah hujan secara langsung (*real-time*) untuk memperkirakan waktu kedatangan badai di kawasan target.
- **Interval Pembaruan (Update Interval):** Setiap 5 hingga 10 menit.
- **Kualitas Data (Data Quality):** Sangat tinggi untuk menangkap dinamika spasial curah hujan jangka pendek.
- **API:** API Radar Cuaca BMKG, RainViewer API.
- **Keterbatasan (Limitations):** Jangkauan sinyal radar bisa terhalang oleh pegunungan atau deretan gedung tinggi (fenomena *beam blockage*). Estimasi intensitas terkadang butuh kalibrasi dengan sensor di darat.

## 3. Satelit (Satellite)
- **Tujuan (Purpose):** Memantau pembentukan sistem awan skala besar, pergerakan badai regional, serta mendeteksi konsentrasi air di atmosfer.
- **Interval Pembaruan (Update Interval):** Setiap 10 hingga 30 menit (Satelit Geostasioner seperti Himawari).
- **Kualitas Data (Data Quality):** Tinggi dan sangat konsisten untuk cakupan wilayah yang luas.
- **API:** Satelit Himawari-8/9 (melalui portal BMKG), JAXA, atau NOAA.
- **Keterbatasan (Limitations):** Resolusi per piksel terlalu besar (sekitar 1-4 km) sehingga tidak cukup detail untuk memprediksi genangan genangan di level satu jalan raya. Sensor optik bisa terhalang lapisan awan bagian atas.

## 4. Ketinggian Sungai (River)
- **Tujuan (Purpose):** Mengukur debit air dan Tinggi Muka Air (TMA) pada sungai, waduk, serta pintu air utama penahan banjir.
- **Interval Pembaruan (Update Interval):** *Real-time*, umumnya diperbarui setiap 5 hingga 15 menit.
- **Kualitas Data (Data Quality):** Tinggi, langsung diukur di lapangan menggunakan sensor ultrasonik atau pendataan manual periodik dari petugas penjaga pintu air.
- **API:** API Dinas Sumber Daya Air (SDA), BPBD, atau Kementerian PUPR.
- **Keterbatasan (Limitations):** Sensor perangkat keras rentan terhadap gangguan fisik akibat sampah sungai, vandalisme, atau hilangnya koneksi internet di pos pemantau.

## 5. Topografi (Topography)
- **Tujuan (Purpose):** Memahami kemiringan lereng, bentuk permukaan tanah, serta mengidentifikasi area cekungan di mana air hujan secara alami akan mengalir dan berkumpul.
- **Interval Pembaruan (Update Interval):** Sangat jarang (statis), kecuali jika terdapat pembangunan infrastruktur makro.
- **Kualitas Data (Data Quality):** Sedang hingga tinggi (bergantung pada skala peta yang digunakan).
- **API:** OpenTopography API, InaGeoportal (Badan Informasi Geospasial/BIG).
- **Keterbatasan (Limitations):** Peta kontur konvensional mungkin tidak memperhitungkan gundukan buatan, tanggul lingkungan baru, atau selokan yang dibangun warga setelah peta dirilis.

## 6. Model Elevasi Digital (DEM)
- **Tujuan (Purpose):** Digunakan oleh mesin simulasi hidrologi spasial 3D untuk memprediksi area luapan secara presisi dan memperkirakan kedalaman air banjir.
- **Interval Pembaruan (Update Interval):** Statis (dirilis setiap beberapa tahun).
- **Kualitas Data (Data Quality):** Sangat tinggi. Bersumber dari pemindaian satelit resolusi tinggi atau pemetaan udara LiDAR.
- **API:** DEMNAS (DEM Nasional BIG), SRTM (Shuttle Radar Topography Mission) dari NASA.
- **Keterbatasan (Limitations):** Dataset yang gratis sering kali beresolusi 8 meter (DEMNAS) hingga 30 meter. Permukaan atas struktur seperti jembatan kadang terekam secara keliru sebagai "bendungan" yang menahan air pada simulasi model mentah.

## 7. Angin (Wind)
- **Tujuan (Purpose):** Memprediksi arah (vektor) dan kecepatan pergerakan sel awan hujan dari laut atau pegunungan yang menuju ke area pengguna.
- **Interval Pembaruan (Update Interval):** Setiap 1 hingga 3 jam.
- **Kualitas Data (Data Quality):** Sedang hingga tinggi.
- **API:** Windy API, OpenWeatherMap, API BMKG.
- **Keterbatasan (Limitations):** Pola angin di permukaan tanah terdistorsi oleh gedung dan jalanan. Kecepatan angin di tingkat awan bisa berbeda drastis dengan kecepatan yang dirasakan di darat.

## 8. Curah Hujan (Rainfall)
- **Tujuan (Purpose):** Mengukur volume presipitasi absolut di titik lokasi yang akurat menggunakan jaringan penakar hujan otomatis (*Automatic Weather Station* / AWS). Berfungsi sebagai *Ground Truth*.
- **Interval Pembaruan (Update Interval):** Setiap 10 menit hingga 1 jam.
- **Kualitas Data (Data Quality):** Paling akurat dibandingkan radar dan satelit, namun hanya untuk wilayah yang sangat sempit.
- **API:** API AWS BMKG, Sensor cuaca pihak ketiga/IOT.
- **Keterbatasan (Limitations):** Titik sampel terbatas. Hujan ekstrem yang turun sejauh 2 kilometer dari stasiun AWS bisa jadi tidak terdeteksi sama sekali oleh stasiun tersebut.

## 9. Data Historis Banjir (Historical Flood)
- **Tujuan (Purpose):** Berfungsi sebagai dataset pelatihan (label) untuk model Kecerdasan Buatan (AI) agar sistem mampu mengenali pola pemicu banjir di masa lampau dan mengujinya terhadap pola saat ini.
- **Interval Pembaruan (Update Interval):** Insidental, tercatat setelah suatu peristiwa banjir usai.
- **Kualitas Data (Data Quality):** Sangat variatif dan tidak terstruktur. Sebagian besar mengandalkan laporan warga (*crowdsourcing*) dan pencatatan petugas lapangan.
- **API:** PetaBencana API, Laporan BPBD, Jakarta Open Data.
- **Keterbatasan (Limitations):** Lokasi laporan terkadang meleset. Pengukuran kedalaman banjir sering kali bersifat subjektif (misal: "setinggi lutut", "sepinggang") alih-alih data metrik yang baku.

## 10. Data Terbuka Pemerintah (Government Open Data)
- **Tujuan (Purpose):** Melengkapi sistem dengan data spasial tata letak kota, kapasitas jaringan drainase, zonasi tata ruang, titik kumpul evakuasi, dan fasilitas tanggap darurat (rumah sakit/pemadam).
- **Interval Pembaruan (Update Interval):** Tahunan atau saat peluncuran publikasi dinas terkait.
- **Kualitas Data (Data Quality):** Terpercaya dan resmi (*authoritative*).
- **API:** Portal Satu Data Indonesia, Jakarta Open Data, Tangerang Selatan Open Data.
- **Keterbatasan (Limitations):** Banyak dataset berharga belum tersedia via REST API yang stabil; kebanyakan masih berupa dokumen unduhan (CSV, Excel, PDF, atau Shapefile) yang menuntut pemrosesan secara manual.
