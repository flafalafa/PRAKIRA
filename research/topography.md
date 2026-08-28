# Analisis Topografi dan Medan: Pondok Kacang Prima

**Penyusun:** Analis Riset Hidrologi (Tim PRAKIRA)  
**Tujuan:** Memetakan karakteristik topografi, kontur tanah, dan arah aliran limpasan air (run-off) di kawasan Pondok Kacang Prima, Tangerang Selatan.

Analisis medan (terrain) sangat krusial dalam pemodelan risiko banjir karena gravitasi dan bentuk permukaan tanah menentukan ke mana air akan mengalir dan berakumulasi. Berikut adalah rincian analisis topografi untuk wilayah Pondok Kacang Prima:

---

## 1. Elevasi (Elevation)
- Wilayah Tangerang Selatan secara makro berada di rentang dataran rendah (0 hingga 25 mdpl).
- Berdasarkan data pemetaan, rata-rata elevasi di Kecamatan Pondok Aren berada di kisaran **30 mdpl**.
- Secara spesifik, titik elevasi di kawasan Pondok Kacang Timur/Prima tercatat lebih rendah, yaitu rata-rata sekitar **24 meter di atas permukaan laut (mdpl)**. Perbedaan elevasi lokal ini membuat air secara alami mengalir dan tertahan di area ini.

## 2. Model Elevasi Digital (Digital Elevation Model / DEM)
- Analisis DEM pada kawasan ini menunjukkan profil dataran yang relatif rata namun dipenuhi oleh cekungan-cekungan mikro (micro-depressions). 
- Banyak perumahan di Pondok Kacang Prima dibangun di area yang secara historis (berdasarkan DEM masa lalu) merupakan daerah rawa, daerah tangkapan air alami, atau bantaran limpasan sungai. Akibatnya, profil DEM area perumahan sering kali berada di bawah atau sejajar dengan tanggul sungai.

## 3. Kemiringan Lereng (Slope)
- Berbeda dengan area utara Tangerang yang sangat datar (0-3%), wilayah Pondok Aren memiliki kemiringan lereng yang sedikit lebih curam, berkisar antara **3% hingga 8%**.
- Kemiringan ini cukup untuk memberikan kecepatan aliran air permukaan (*surface run-off velocity*) yang moderat dari area yang lebih tinggi, yang kemudian langsung menghantam area cekungan tanpa sempat terserap maksimal oleh tanah latosol di wilayah tersebut.

## 4. Karakteristik Dataran Rendah (Lowland)
- Pondok Kacang Prima berfungsi sebagai semacam "mangkuk" atau dataran rendah lokal (*localized lowland*) jika dibandingkan dengan kawasan selatan Tangerang Selatan seperti Pamulang atau Serpong yang elevasinya lebih tinggi. 
- Kombinasi antara elevasi rendah dan tutupan lahan (beton/aspal) yang mencapai lebih dari 80% menyebabkan kawasan ini sangat rentan terhadap genangan.

## 5. Akumulasi Aliran (Flow Accumulation)
- Dalam pemodelan hidrologi spasial, *flow accumulation* di kawasan ini terpusat sangat padat pada jaringan jalan-jalan utama perumahan.
- Jalan aspal sering kali berubah fungsi menjadi "sungai dadakan" karena volume aliran permukaan gagal masuk ke saluran drainase (selokan) yang ukurannya terlalu kecil atau tersumbat, sehingga air terus berakumulasi di titik terendah perumahan.

## 6. Arah Aliran (Flow Direction)
- Sesuai dengan hukum gravitasi dan kemiringan topografi regional, arah aliran air permukaan (*flow direction*) bergerak secara dominan dari arah **Selatan / Barat Daya** menuju **Utara / Timur Laut**.
- Limpasan air bergerak meninggalkan dataran tinggi Serpong/Pamulang menuju muara sistem drainase di perbatasan Jakarta Selatan dan Kota Tangerang.

## 7. Potensi Jalur Air (Potential Water Path)
- **Jalur Alami:** Seharusnya mengikuti gravitasi menuju celah drainase yang mengarah ke Kali Serua.
- **Jalur Aktual (Masalah):** Karena masifnya pembangunan tembok, perkerasan jalan, dan penyumbatan selokan, jalur air alami terpotong. Air mencari jalur dengan hambatan terkecil (*path of least resistance*), yang kini sering kali berupa garasi rumah warga, gang-gang sempit, dan jalan raya utama.

## 8. Batas Daerah Aliran Sungai (Watershed Boundary)
- Secara hidrologis, Pondok Kacang Prima masuk ke dalam **Sub-DAS Kali Serua**.
- Batas tangkapan air (*catchment area boundary*) dari sub-DAS ini beririsan langsung dengan batas wilayah permukiman padat. Segala presipitasi (hujan) yang jatuh di dalam batas topografi ini secara eksklusif akan membebani kapasitas Kali Serua, sebelum akhirnya disalurkan ke sistem **DAS Angke-Pesanggrahan** di wilayah hilir.

---
**Kesimpulan untuk Mesin Prediksi (Prediction Engine):**
Data topografi ini menegaskan perlunya model prediktif kita (PRAKIRA) untuk tidak hanya bergantung pada "apakah hujan turun di Pondok Kacang?", melainkan harus menghitung presipitasi di area elevasi tinggi (radius 5-10 km di arah Barat Daya), karena kemiringan lahan dan arah aliran pasti akan membawa air tersebut ke cekungan Pondok Kacang Prima.
