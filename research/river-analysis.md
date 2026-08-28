# Analisis Sungai: Dampak Terhadap Pondok Kacang Prima

**Penyusun:** Analis Riset Hidrologi (Tim PRAKIRA)  
**Tujuan:** Memetakan karakteristik jaringan hidrologis yang memengaruhi area Pondok Kacang Prima dan Kecamatan Pondok Aren.

Secara geografis dan hidrologis, wilayah Pondok Kacang Prima sangat dipengaruhi oleh satu sungai/saluran makro utama, yaitu **Kali Serua**, serta terdampak secara makro oleh kondisi di aliran **Kali Angke**. 

Berikut adalah rincian analisis untuk sungai yang paling memengaruhi kawasan tersebut:

---

## 1. Kali Serua (Primary Cause of Local Flooding)

Kali Serua adalah saluran drainase makro utama yang membelah kawasan Pondok Kacang Timur, Pondok Aren. Limpasan dari sungai ini merupakan penyumbang utama genangan banjir di perumahan sekitar, seperti Pondok Kacang Prima dan Pondok Maharta.

- **Nama Sungai (River Name):** Kali Serua
- **Hierarki Sungai (River Hierarchy):** Anak sungai tingkat 2 (Sungai Orde 2) / Saluran Drainase Makro Perkotaan.
- **Daerah Aliran Sungai (Watershed):** Sub-DAS Kali Serua. Merupakan bagian dari sistem drainase metropolitan yang lebih besar yang bermuara pada sistem DAS Angke-Pesanggrahan.
- **Lebar Sungai (River Width):** Sangat bervariasi. Pada area yang sudah dinormalisasi lebarnya berkisar **3 hingga 5 meter**. Namun, di titik-titik padat pemukiman, lebar sungai mengalami penyempitan parah (bottleneck) hingga tersisa sekitar **1,5 hingga 2 meter**.
- **Kedalaman Sungai (River Depth):** Rata-rata kedalaman normal berkisar antara **1 hingga 2 meter**. Kedalaman ini sangat dinamis akibat tingkat sedimentasi (lumpur) yang tinggi dan sering menjadi sasaran pengerukan dinas terkait.
- **Penampang Silang (Cross Section):** Berbentuk U atau kotak (persegi panjang) pada segmen yang sudah diperkuat dengan turap beton (sheet pile), dan berbentuk tidak beraturan (trapesium alami) pada segmen yang masih berupa bantaran tanah.
- **Kapasitas Sungai (River Capacity):** Berdasarkan pengamatan historis, kapasitas penampang Kali Serua terbukti **tidak memadai (under-capacity)** untuk menampung volume *run-off* (limpasan permukaan) yang dihasilkan oleh hujan lokal berintensitas ekstrem (di atas 50 mm/jam).
- **Debit Sungai (River Discharge):** Memiliki karakteristik *flashy* (merespon curah hujan dengan sangat cepat). Debit air sangat rendah atau nyaris kering di puncak kemarau, namun melonjak drastis hingga meluap dalam waktu kurang dari 2 jam setelah hujan lebat di daerah tangkapan airnya.
- **Riwayat Banjir (Flood History):** Merupakan tersangka utama (penyebab langsung) insiden banjir mematikan di Pondok Kacang Prima. Sering meluap dan mencatat insiden "tanggul jebol" pada tahun 2020, 2025, dan awal 2026.
- **Hulu (Upstream):** Berasal dari kawasan resapan air yang semakin menyusut di selatan Tangerang Selatan (berhulu di sekitar area Ciater / Serpong).
- **Hilir (Downstream):** Mengalir ke arah utara-timur, membawa aliran air menuju perbatasan dengan Jakarta Selatan / Kota Tangerang dan bermuara pada sistem Kali Angke.
- **Anak Sungai (Tributaries):** Tidak memiliki anak sungai besar secara alami, namun berfungsi sebagai muara bagi ratusan saluran air sekunder (got dan parit) dari perumahan warga di sepanjang Pondok Aren.
- **Koneksi Drainase (Drainage Connections):** Terhubung langsung dengan pintu-pintu air pembuangan dari Pondok Kacang Prima. **Kelemahan Kritis:** Ketika muka air Kali Serua naik sejajar dengan daratan, air dari drainase perumahan tidak dapat mengalir keluar, sehingga menyebabkan genangan internal (*backwater effect*).

---

## 2. Kali Angke (Macro Influence)

Meskipun letaknya sedikit lebih jauh dan tidak langsung menembus Pondok Kacang Prima, sistem aliran Kali Angke memengaruhi wilayah Tangerang Selatan secara keseluruhan.

- **Nama Sungai (River Name):** Kali Angke
- **Hierarki Sungai (River Hierarchy):** Sungai Utama (Sungai Orde 1)
- **Daerah Aliran Sungai (Watershed):** DAS Angke.
- **Lebar & Kedalaman:** Lebih besar dari Kali Serua, dengan lebar berkisar **10 hingga 20 meter** dan kedalaman rata-rata **2 hingga 4 meter**.
- **Kapasitas & Debit:** Sangat dipengaruhi oleh air "kiriman" dari daerah Bogor dan Depok.
- **Koneksi Drainase (Drainage Connections):** Jika Kali Angke meluap atau tinggi muka airnya kritis, kemampuan anak-anak sungainya (termasuk jaringan Kali Serua) untuk membuang air ke arah hilir menjadi terhambat. Hal ini menyebabkan penumpukan volume air di kawasan Pondok Aren.

---
**Catatan untuk Pemodelan AI (Prediction Engine):**
1. **Sensor Node Kritis:** Sistem PRAKIRA wajib memprioritaskan pemantauan tinggi muka air (TMA) di titik hulu Kali Serua dan titik penyempitan sebelum masuk ke perumahan Pondok Kacang Prima.
2. **Aturan Fallback (Rule-Based):** Jika TMA Kali Serua di hulu menunjukkan tren naik tajam dalam 30 menit, peringatan *early warning* harus segera dipancarkan ke warga Pondok Kacang Prima meskipun hujan lokal di lokasi perumahan belum terlampau lebat.
