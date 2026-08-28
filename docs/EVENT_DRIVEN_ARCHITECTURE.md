# Arsitektur Berbasis Peristiwa (EVENT_DRIVEN_ARCHITECTURE)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Spesifikasi Arsitektur Tingkat Lanjut  
Pemilik: Principal Solution Architect  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan bagaimana seluruh layanan (*microservices*) dalam ekosistem PRAKIRA berkomunikasi secara asinkron menggunakan Arsitektur Berbasis Peristiwa (*Event-Driven Architecture / EDA*).

PRAKIRA mengadopsi EDA karena:
* **Decoupling:** Layanan dapat beroperasi dan diskalakan secara independen tanpa ketergantungan API yang saling mengunci (*blocking*).
* **Latensi Rendah:** Pemrosesan secara asinkron memungkinkan sistem menyerap ribuan titik data cuaca dan sensor per detik tanpa bottleneck.
* **Toleransi Kesalahan:** Jika satu layanan (misalnya Notifikasi) mati sementara waktu, peristiwa akan tertahan di antrean dan diproses saat layanan kembali menyala tanpa ada data yang hilang.

---

## 2. Gambaran Arsitektur (Architecture Overview)

Alur peristiwa mengalir melalui platform sebagai berikut:

**Penyedia Eksternal (API Cuaca/Sensor)**
↓ (Tarik/Dorong)
**Layanan Pengumpul (Collectors)**
↓ (Mempublikasikan Peristiwa Mentah)
**Bus Peristiwa (Event Bus)**
↓ (Mengkonsumsi Peristiwa)
**Layanan Pemrosesan (Hydrology, Normalization)**
↓ (Mempublikasikan Peristiwa Terproses)
**Mesin Keputusan (Decision Engine)**
↓ (Mempublikasikan Peristiwa Prediksi)
**Layanan Notifikasi (Notification Service)**
↓ (Mempublikasikan Peringatan)
**API Gateway**
↓ (Koneksi WebSocket / Push)
**Aplikasi Seluler Flutter**

---

## 3. Bus Peristiwa (Event Bus)

Teknologi yang direkomendasikan untuk menengahi (*broker*) semua peristiwa:

* **Redis Streams:** Digunakan untuk versi awal (V1). Sangat cepat, ringan, mendukung grup konsumen (*consumer groups*), ideal untuk infrastruktur startup.
* **RabbitMQ:** Digunakan jika diperlukan perutean pesan (*message routing*) yang kompleks dan jaminan pengiriman (*acknowledgement*) yang sangat ketat (AMQP).
* **Apache Kafka (Masa Depan):** Target arsitektur skala nasional (V3). Cocok untuk log terdistribusi, *replayability* peristiwa masa lalu, retensi jangka panjang, dan *throughput* jutaan peristiwa per menit.

---

## 4. Kategori Peristiwa (Event Categories)

* **Peristiwa Cuaca (Weather Events):** Pembaruan hujan, suhu, badai.
* **Peristiwa Sungai (River Events):** Debit, muka air, luapan.
* **Peristiwa Radar (Radar Events):** Pergerakan awan konvektif.
* **Peristiwa Satelit (Satellite Events):** Estimasi presipitasi satelit.
* **Peristiwa Prediksi (Prediction Events):** Hasil analisis dan ETA banjir.
* **Peristiwa Notifikasi (Notification Events):** Peringatan dikirim, dibaca, gagal.
* **Peristiwa Komunitas (Community Events):** Laporan warga masuk, divalidasi.
* **Peristiwa Sistem (System Events):** Status kesehatan *node*.
* **Peristiwa Admin (Admin Events):** Konfigurasi area diubah, ambang batas disesuaikan.
* **Peristiwa Pengguna (User Events):** Preferensi diperbarui, pindah lokasi.

---

## 5. Struktur Peristiwa Standar (Standard Event Structure)

Setiap peristiwa di sistem PRAKIRA harus mematuhi struktur *payload* JSON berikut:

* **Event ID:** UUID unik untuk peristiwa tersebut.
* **Event Name:** Nama peristiwa secara *camelCase* (contoh: `WeatherUpdated`).
* **Timestamp:** Waktu kejadian dalam format ISO-8601 UTC.
* **Source:** Layanan yang memancarkan peristiwa (contoh: `collector-service`).
* **Version:** Versi skema peristiwa (contoh: `v1`).
* **Correlation ID:** ID yang melacak rantai peristiwa ini dari awal hingga akhir (untuk *tracing*).
* **Payload:** Objek JSON yang berisi data aktual (misal: suhu, lokasi).
* **Metadata:** Konteks ekstra (contoh: area ID, tag lingkungan).

---

## 6. Daftar Peristiwa (Event List)

Berikut adalah daftar peristiwa inti:

* **Pencarian Data (Ingestion):**
  * `WeatherUpdated`
  * `RadarUpdated`
  * `RiverLevelUpdated`
  * `StormDetected`
  * `StormMoving`
* **Inteligensi & Keputusan:**
  * `PredictionGenerated`
  * `PredictionUpdated`
  * `RiskChanged`
  * `FloodDetected`
* **Notifikasi:**
  * `NotificationRequested`
  * `NotificationSent`
  * `NotificationFailed`
* **Komunitas & Pengguna:**
  * `CommunityReportCreated`
  * `UserLocationChanged`
* **Sistem & Infrastruktur:**
  * `SensorOffline`
  * `CollectorFailed`
  * `AreaConfigurationChanged`
  * `ModelRecalculated`
  * `HistoricalDataImported`
  * `ScheduleTriggered`
  * `HeartbeatReceived`

---

## 7. Layanan Produsen (Producer Services)

Layanan mana yang *mempublikasikan* (publish) peristiwa:
* **Data Collector Service:** `WeatherUpdated`, `RadarUpdated`, `RiverLevelUpdated`.
* **Feature Engineering / Hydrology:** `StormDetected`, `StormMoving`.
* **Decision Engine:** `PredictionGenerated`, `RiskChanged`, `NotificationRequested`.
* **Notification Service:** `NotificationSent`, `NotificationFailed`.
* **Community Service:** `CommunityReportCreated`.
* **User Service:** `UserLocationChanged`.
* **Admin Portal:** `AreaConfigurationChanged`.

---

## 8. Layanan Konsumen (Consumer Services)

Layanan mana yang *berlangganan* (subscribe) ke peristiwa:
* **Hydrology Engine:** Berlangganan ke `WeatherUpdated`, `RadarUpdated`, `RiverLevelUpdated`.
* **Decision Engine:** Berlangganan ke `StormDetected`, `CommunityReportCreated`, dan hasil dari Hydrology Engine.
* **Prediction Service:** Berlangganan ke `PredictionGenerated` (untuk menyimpannya ke *database*).
* **Notification Service:** Berlangganan ke `NotificationRequested`, `RiskChanged`.
* **Analytics Service:** Berlangganan ke semua peristiwa (sebagai sistem pencatatan/gudang data).

---

## 9. Contoh Alur Peristiwa (Event Flow Examples)

**Contoh 1: Deteksi Hujan Lebat**
Hujan terdeteksi oleh BMKG API
↓
`Collector Service` mempublikasikan `WeatherUpdated`
↓
`Hydrology Engine` menghitung limpasan, mempublikasikan `CatchmentSaturated`
↓
`Decision Engine` menaikkan skor risiko, mempublikasikan `PredictionGenerated`
↓
`Notification Service` mempublikasikan `NotificationRequested` lalu mengirim Push
↓
Aplikasi Seluler menampilkan Peringatan.

**Contoh 2: Kegagalan Sensor**
Sensor IoT gagal mengirim ping selama 10 menit
↓
`Collector Service` mempublikasikan `SensorOffline`
↓
`Decision Engine` menurunkan *Confidence Score* pada prediksi berikutnya.
↓
`Analytics Service` mencatat insiden pemeliharaan.

---

## 10. Strategi Pengulangan Peristiwa (Event Retry Strategy)

* **Idempotensi (Idempotency):** Setiap konsumen HARUS kebal terhadap pemrosesan ganda. `Event ID` digunakan untuk melacak jika pesan sudah pernah diproses.
* **Pengulangan (Retry):** Jika pemrosesan gagal (misal basis data terkunci), konsumen akan mencoba ulang.
* **Backoff Eksponensial:** Waktu tunggu antar percobaan ulang akan dilipatgandakan (misal 1 dtk, 2 dtk, 4 dtk) agar tidak membanjiri sistem yang sedang pulih.
* **Dead Letter Queue (DLQ):** Setelah 5 kali gagal berturut-turut, pesan dibuang ke DLQ untuk diselidiki secara manual oleh insinyur perangkat lunak.

---

## 11. Strategi Pengurutan (Ordering Strategy)

* Urutan (*ordering*) sangat penting. Muka air yang naik lalu turun tidak boleh diproses terbalik.
* **Partisi Berdasarkan Kunci:** Pesan akan disiarkan (*hashed*) berdasarkan `Area ID` atau `River ID`. Ini memastikan semua peristiwa yang ditujukan untuk Pondok Kacang Prima selalu dimasukkan ke dalam antrean yang sama dan diproses secara berurutan (*in-order*) oleh pekerja (*worker*) yang sama.

---

## 12. Pembuatan Versi Peristiwa (Event Versioning)

Untuk menjaga *backward compatibility* seiring evolusi PRAKIRA:
* Penambahan data selalu bersifat opsional (*non-breaking*).
* Dilarang menghapus atau mengubah tipe atribut yang sudah ada di sebuah peristiwa.
* Jika perubahan radikal diperlukan, sistem akan memancarkan peristiwa baru (misalnya `PredictionGenerated.v2`).

---

## 13. Pemantauan (Monitoring)

* **Correlation ID Tracing:** Menggunakan alat seperti Jaeger atau OpenTelemetry untuk melacak berapa milidetik yang dihabiskan sejak data cuaca diambil hingga pengguna menerima notifikasi.
* **Queue Length:** Pemantauan ketat pada *consumer lag* (panjang antrean). Jika antrean bertambah panjang melebihi 1.000 pesan, Kubernetes harus otomatis menambah (*scale up*) jumlah pod layanan terkait.
* **Kegagalan & Latensi:** Metrik direkam di Prometheus / Grafana.

---

## 14. Keamanan (Security)

* **Otentikasi Peristiwa:** Event Bus dilindungi kredensial yang disuntikkan saat *deployment*.
* **Enkripsi:** Lalu lintas (TLS) dan penyimpanan pada antrean dienkripsi (*at rest*).
* **Otorisasi:** Layanan `Collector` hanya memiliki izin (*role*) untuk MENCIPTAKAN peristiwa, tetapi tidak memiliki izin untuk KONSUMSI peristiwa keputusan.

---

## 15. Skalabilitas (Scalability)

* **Penskalaan Horizontal:** Konsumen (misal *Decision Engine*) dikelompokkan ke dalam *Consumer Groups*. Menambahkan pod baru secara otomatis mendistribusikan beban kerja pemrosesan peristiwa.
* **Partisi:** Data didistribusikan (*sharded*) melintasi banyak node antrean untuk mencegah *bottleneck* I/O.
* **Deployment Multi-Region (Masa Depan):** Menjalankan *cluster* terpisah di zona AWS/GCP yang berbeda untuk memastikan sistem tetap hidup saat ada bencana besar di satu pusat data.

---

## 16. Pemulihan Kegagalan (Failure Recovery)

* Jika layanan *crash* di tengah proses, ia tidak akan mengirimkan status *ACK* (Acknowledge) ke bus peristiwa.
* Saat layanan dinyalakan kembali (*restart*), ia akan mengambil kembali (*fetch*) peristiwa yang tidak sempat di-*ACK* tersebut dan memprosesnya dari titik henti terakhir (*checkpoint*).

---

## 17. Praktik Terbaik (Best Practices)

* **Event-Carried State Transfer:** Bawa semua data yang dibutuhkan di dalam *Payload* untuk meminimalkan kueri ulang basis data (*database roundtrips*).
* **Asinkron Sebagai Default:** Segala hal yang tidak membutuhkan jawaban instan ke pengguna (API Request) harus dilempar ke belakang (*background*) sebagai peristiwa.
* **Desain Pertahanan:** Sistem tidak boleh lumpuh hanya karena format JSON dari penyedia eksternal tiba-tiba berubah format (validasi ketat di gerbang depan).
