# Karakteristik Curah Hujan: Tangerang Selatan

**Penyusun:** Analis Riset Hidrologi (Tim PRAKIRA)  
**Tujuan:** Menganalisis pola cuaca, tren curah hujan, dan ketersediaan data meteorologi di wilayah Tangerang Selatan (termasuk Pondok Aren) sebagai landasan variabel utama dalam *Prediction Engine*.

---

## 1. Curah Hujan Bulanan (Monthly Rainfall)
- **Iklim Makro:** Tangerang Selatan memiliki iklim hutan hujan tropis (*tropical rainforest climate* - Af) dengan curah hujan yang relatif tinggi dan turun hampir sepanjang tahun.
- **Puncak Musim:** Puncak intensitas hujan (baik secara frekuensi maupun volume) umumnya jatuh pada bulan **Januari dan Februari**, seiring dengan kuatnya angin Monsun Asia.
- **Masa Transisi (Pancaroba):** Bulan-bulan peralihan seperti Maret-April dan September-Oktober sering ditandai dengan hujan konvektif lokal berdurasi singkat namun sangat lebat.

## 2. Curah Hujan Ekstrem (Extreme Rainfall)
- **Definisi BMKG:** Hujan diklasifikasikan sebagai 'ekstrem' jika volume presipitasi melampaui **100 mm/hari** atau **20 mm/jam**.
- **Karakteristik Lokal:** Hujan di Tangerang Selatan sangat dipengaruhi oleh fenomena lokal seperti pembentukan awan *Cumulonimbus* raksasa yang mengakibatkan hujan es, badai petir, atau *microburst* (pusaran angin kencang ke bawah) dengan curah hujan yang luar biasa padat di area yang sempit (radius 2-5 km).

## 3. Badai Historis (Historical Storms)
Sejumlah badai dan anomali cuaca historis yang tercatat berdampak parah:
- **1 Januari 2020:** Hujan ekstrem lintas wilayah (skala Jabodetabek) dengan rekor intensitas di atas 300 mm/hari, memicu banjir paling merusak dalam dekade terakhir.
- **7 November 2021:** Curah hujan mencapai **117 mm/hari** tercatat di Stasiun Klimatologi Tangerang Selatan, memicu luapan langsung Kali Angke dan Kali Serua.
- **10 Maret 2023:** Hujan intens (>50 mm) dipadukan dengan *squall line* (garis badai berangin kencang) yang melanda Pondok Aren, merobohkan papan reklame dan pohon besar, sekaligus memutus aliran listrik pada sistem pompa banjir.

## 4. Tren Curah Hujan (Rainfall Trend)
- **Variabilitas:** Curah hujan di Tangerang Selatan menunjukkan tren variabilitas yang semakin tinggi dari tahun 1990 hingga 2020.
- **Pergeseran Pola:** Walaupun total curah hujan tahunan mungkin stabil secara statistik, frekuensi terjadinya "hari dengan hujan ekstrem" semakin meningkat. Ini sering dikaitkan dengan faktor global seperti **La Niña**, **Dipole Mode Negatif (IOD -)**, serta gelombang atmosfer regional (Madden-Julian Oscillation/MJO).
- **Dampak Hidrologi:** Hujan tidak lagi merata berhari-hari (hujan rintik), melainkan turun sekaligus secara masif dalam hitungan 1-2 jam, yang mana infrastruktur drainase Pondok Kacang Prima tidak dirancang untuk itu.

## 5. Stasiun Pemantau BMKG (BMKG Stations)
- Wilayah Tangerang Selatan memiliki pusat observasi resmi, yaitu **Stasiun Klimatologi Banten (Tangerang Selatan)** yang menyajikan data *Ground Truth*.
- Terdapat pula beberapa stasiun cuaca otomatis (*Automatic Weather Station* / AWS) dan stasiun pemantau curah hujan (*Automatic Rain Gauge* / ARG) yang tersebar di wilayah Banten/Tangerang.
- **Tantangan Model PRAKIRA:** Karena hujan sering bersifat sangat lokal (hujan deras di Serpong, tapi kering di Pondok Aren), sistem peringatan tidak bisa hanya bergantung pada satu stasiun BMKG pusat, melainkan membutuhkan ekstrapolasi spasial dari jaringan stasiun di sekitarnya.

## 6. Curah Hujan Berbasis Satelit (Satellite Rainfall)
Untuk menutupi celah ("*blind spot*") dari sensor darat BMKG, analisis curah hujan juga menggunakan data satelit:
- **Satelit Himawari-8/9:** Menyediakan pantauan suhu puncak awan inframerah setiap 10 menit, yang dikonversi menjadi estimasi curah hujan (*Rainfall Estimation*). Berguna untuk melacak pergerakan badai pembawa banjir secara *real-time*.
- **GPM (Global Precipitation Measurement) / TRMM:** Memberikan dataset riwayat curah hujan (*historical grid data*) dalam format spasial, yang sangat krusial digunakan sebagai data pelatihan (*training data*) bagi mesin AI untuk mempelajari pola distribusi hujan di atas DAS Serua sebelum tahun 2026.
