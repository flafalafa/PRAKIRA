# Arsitektur Infrastruktur (INFRASTRUCTURE)

Versi: 1.0  
Proyek: PRAKIRA  
Status: Spesifikasi Infrastruktur  
Pemilik: Principal Cloud Architect  

---

## 1. Tujuan (Purpose)

Dokumen ini mendefinisikan infrastruktur awan (*cloud infrastructure*) produksi untuk PRAKIRA Versi 1, sekaligus menjamin fondasi yang dapat diskalakan (*scalable*) untuk penerapan skala nasional di masa depan.

Sasaran infrastruktur:
* **Ketersediaan Tinggi (High Availability):** Waktu aktif (*uptime*) yang maksimal dengan redundansi bawaan.
* **Skalabilitas (Scalability):** Kemampuan untuk menangani lonjakan data lingkungan dan lalu lintas pengguna selama kejadian badai besar.
* **Keandalan (Reliability):** Sistem harus terus memberikan prediksi meskipun beberapa penyedia data hulu mengalami kegagalan.
* **Keamanan (Security):** Perlindungan terhadap data pengguna dan perlindungan sistem dari serangan siber (DDoS).
* **Efisiensi Biaya (Cost Efficiency):** Mengoptimalkan penggunaan sumber daya, memanfaatkan komputasi nirserver (*serverless*) atau penskalaan otomatis (*auto-scaling*).
* **Observabilitas (Observability):** Visibilitas mendalam ke dalam kondisi sistem melalui pencatatan (*logging*), pelacakan (*tracing*), dan metrik.

---

## 2. Gambaran Infrastruktur (Infrastructure Overview)

Alur arsitektur lengkap dari permintaan luar ke lapisan penyimpanan:

**Internet**
↓
**CDN (Jaringan Pengiriman Konten)**
↓
**Load Balancer**
↓
**API Gateway**
↓
**Layanan Aplikasi (Application Services)**
↓
**Antrean Pesan (Message Queue / Event Bus)**
↓
**Pekerja Latar Belakang (Background Workers)**
↓
**Basis Data (Database)**
↓
**Penyimpanan Objek (Object Storage)**
↓
**Pemantauan & Pencadangan (Monitoring & Backup)**

---

## 3. Strategi Lingkungan (Environment Strategy)

Siklus hidup perangkat lunak didukung oleh lingkungan isolasi berikut:

* **Local:** Berjalan di mesin pengembang (menggunakan Docker Compose) untuk iterasi kode yang cepat.
* **Development:** Lingkungan *cloud* dinamis untuk pengujian integrasi harian.
* **Testing:** Khusus untuk Pengujian Jaminan Kualitas (QA) otomatis dan manual.
* **Staging:** Tiruan pasti (*exact replica*) dari produksi. Digunakan untuk validasi pra-rilis (*pre-release*) dan pengujian beban (*load testing*).
* **Production:** Lingkungan langsung yang melayani pengguna nyata. Akses dikontrol sangat ketat.

---

## 4. Lapisan Komputasi (Compute Layer)

Layanan aplikasi di-*hosting* dengan prinsip *Cloud-Native*:

* **Kontainerisasi (Containerization):** Semua layanan dipaketkan sebagai *image* Docker.
* **Penskalaan Horizontal (Horizontal Scaling):** Menambah jumlah instans (*pods*) alih-alih memperbesar ukuran server (*vertical scaling*).
* **Layanan Nir-Keadaan (Stateless Services):** Tidak ada layanan komputasi yang menyimpan data lokal; jika *container* mati, data aman.
* **Mulai Ulang Otomatis (Auto Restart):** Kegagalan *container* langsung memicu penggantian otomatis (*self-healing*).
* **Pemeriksaan Kesehatan (Health Checks):** Liveness & Readiness probe memastikan hanya instans sehat yang menerima *traffic*.

---

## 5. Lapisan Basis Data (Database Layer)

* **Basis Data Primer (Primary Database):** Menangani semua transaksi tulis (Write). Dilengkapi dengan ekstensi spasial (contoh: PostGIS).
* **Replika Baca (Read Replica):** Menangani permintaan baca berat (*heavy reads*) seperti memuat dasbor dan riwayat banjir, terpisah dari proses penulisan (*Write*) untuk menghindari hambatan.
* **Strategi Pencadangan (Backup Strategy):** *Snapshot* otomatis harian dan retensi jangka panjang.
* **Pemulihan Titik Waktu (Point-in-Time Recovery / PITR):** Kemampuan mengembalikan (*rollback*) basis data ke menit tertentu sebelum terjadi kerusakan data.
* **Connection Pooling:** Menggunakan *pgbouncer* atau sejenisnya untuk mengelola ribuan koneksi konkuren.
* **Klaster Masa Depan (Future Clustering):** Multi-master atau sharding saat mencapai skala nasional.

---

## 6. Lapisan Cache (Cache Layer)

Redis digunakan secara ekstensif untuk meningkatkan kecepatan respons:

* **Prediction Cache:** Menyimpan sementara prediksi ETA dan Skor Risiko agar tidak membebani basis data saat dibaca ribuan pengguna secara serentak.
* **Session Cache:** Manajemen sesi pengguna / token.
* **Rate Limiting:** Mengelola kuota panggilan API untuk mencegah *abuse* / DDoS tingkat aplikasi.
* **Temporary Storage:** Menyimpan data perantara selama kalkulasi hidrologi.
* **Job Queue:** Manajemen antrean internal untuk tugas-tugas singkat (*celery/bull queue*).

---

## 7. Penyimpanan Objek (Object Storage)

Sistem penyimpanan berbasis *bucket* (seperti Amazon S3 atau GCS) untuk berkas yang tidak terstruktur:

* **Foto (Photos):** Profil pengguna dan lampiran laporan.
* **Laporan Masyarakat (Community Reports):** Unggahan media saksi mata dari lokasi banjir.
* **Log (Logs):** Arsip log aplikasi *cold storage*.
* **Dataset Historis (Historical datasets):** Cadangan data pelatihan Machine Learning historis.
* **Citra Satelit (Satellite images):** Peta atau citra satelit statis.
* **Pencadangan (Backups):** Salinan arsip basis data terenkripsi.

---

## 8. Jaringan (Networking)

* **Jaringan Privat (Private Network):** Basis data, Redis, dan *workers* hanya berada di dalam VPC/Subnet privat tanpa akses internet langsung.
* **Jaringan Publik (Public Network):** Hanya Load Balancer dan API Gateway yang terekspos.
* **Firewall (WAF):** Mengamankan sistem dari serangan SQL Injection, XSS, dan bot berbahaya.
* **Grup Keamanan (Security Groups):** Aturan lalu lintas jaringan masuk (*ingress*) dan keluar (*egress*) tingkat *port/IP*.
* **TLS:** Enkripsi *end-to-end* (HTTPS/SSL) untuk lalu lintas eksternal dan internal.
* **DNS & Reverse Proxy:** Resolusi nama domain tingkat tinggi dan perutean terbalik (*reverse routing*).

---

## 9. API Gateway

Tanggung Jawab Utama (berada di depan seluruh layanan mikro):

* **Autentikasi (Authentication):** Memverifikasi JWT sebelum meneruskan permintaan ke layanan.
* **Perutean (Routing):** Mengarahkan *path* (misal `/api/v1/predictions`) ke layanan komputasi yang tepat.
* **Pembatasan Laju (Rate Limiting):** Melindungi layanan di belakangnya dari banjir permintaan.
* **Pembuatan Versi (Versioning):** Penanganan v1, v2 secara transparan.
* **Pencatatan (Logging):** Mencatat setiap permintaan masuk (metrik latensi, HTTP status).

---

## 10. Pekerja Latar Belakang (Background Workers)

Proses yang berjalan tanpa antarmuka (*headless*), mengkonsumsi dari Event Bus:

* **Prediction Jobs:** Menjalankan model kalkulasi saat data hidrologi siap.
* **Collector Jobs:** Melakukan pemanggilan (*polling*) API eksternal (BMKG dll).
* **Notification Jobs:** Mengirimkan *push notification* ke Firebase (FCM) dalam *batch*.
* **Cleanup Jobs:** Menghapus data *cache* dan log kedaluwarsa.
* **Training Jobs:** Melatih ulang model regresi data historis saat beban rendah.

---

## 11. Penjadwal (Scheduler)

Sistem *Cron* terdistribusi untuk mengeksekusi tugas pada interval tertentu:

* **Weather Polling:** Setiap 10 menit.
* **Radar Updates:** Setiap 5 menit.
* **Prediction Refresh:** Dipaksa kalkulasi ulang setiap 15 menit, terlepas dari ada/tidaknya event.
* **Backup:** Setiap jam 02:00 AM lokal.
* **Health Check:** Ping mendalam ke sensor setiap 1 menit.
* **Maintenance:** Tugas re-indeks basis data mingguan.

---

## 12. Pemantauan (Monitoring)

* **Metrik (Metrics):** Penggunaan CPU, memori, panjang antrean, jumlah koneksi, status HTTP (200, 400, 500).
* **Pelacakan (Tracing):** Melacak pergerakan satu *request* melewati berbagai *microservices* menggunakan *Correlation ID*.
* **Pencatatan (Logging):** Sentralisasi log dari semua *pod/container*.
* **Peringatan (Alerting):** Peringatan Slack/PagerDuty otomatis jika latensi API >2 detik atau basis data down.
* **Dasbor (Dashboards):** Panel operasional (Grafana/Kibana) untuk tim *engineering*.

---

## 13. Pencatatan (Logging)

* **Log Terstruktur (Structured logs):** Memaksa format JSON untuk semua log agar mudah difilter.
* **Retensi (Retention):** *Hot storage* untuk 30 hari, *Cold storage* (S3) untuk 1 tahun.
* **Agregasi (Aggregation):** Pengumpulan otomatis ke satu pusat log (seperti ElasticSearch atau Loki).
* **Pencarian Log (Log Search):** Kemampuan untuk mencari kejadian "*error*" lintas ratusan kontainer secara *real-time*.

---

## 14. Strategi Pencadangan (Backup Strategy)

* **Pencadangan Basis Data:** *Snapshot* harian dan *log replikasi* (WAL) untuk PITR.
* **Pencadangan Penyimpanan Objek:** *Versioning* diaktifkan pada objek yang tidak dapat diubah (*immutable*).
* **Pencadangan Konfigurasi:** Skrip Infrastruktur (*Infrastructure-as-Code*) disimpan di kontrol versi (Git).
* **Pemulihan Bencana (Disaster Recovery):** Uji pemulihan basis data secara berkala ke klaster terpisah.

---

## 15. Pemulihan Bencana (Disaster Recovery)

* **Tujuan Pemulihan (Recovery Objectives):** RPO (*Recovery Point Objective*) maksimal 5 menit kehilangan data, RTO (*Recovery Time Objective*) maksimal 30 menit *downtime*.
* **Failover:** Pengalihan DNS otomatis ke situs atau replika cadangan jika situs primer jatuh.
* **Data Restoration:** Prosedur operasi standar (SOP) otomatis untuk memutar ulang cadangan log.
* **Kelangsungan Bisnis (Business Continuity):** Jika API eksternal (*Weather API*) jatuh total, platform harus tetap menyajikan prediksi berbasis sensor independen / historis tanpa membekukan antarmuka (UI).

---

## 16. Keamanan (Security)

* **Manajemen Rahasia (Secrets Management):** Token, kata sandi, dan API Key tidak pernah disimpan di dalam repositori kode (menggunakan *Vault* atau *Secret Manager* awan).
* **Enkripsi (Encryption):** Enkripsi *at rest* (untuk penyimpanan disk) dan *in transit* (TLS 1.2+).
* **Manajemen Identitas (IAM):** Akun layanan hanya diberi izin ke sumber daya yang benar-benar mereka butuhkan.
* **Isolasi Jaringan (Network Isolation):** Pencegahan lateral *movement* melalui segmentasi *subnet*.
* **Hak Istimewa Terkecil (Least Privilege):** Konfigurasi ketat akses staf (*engineers*).

---

## 17. Skalabilitas (Scalability)

Bagaimana infrastruktur menangani pertumbuhan:

* **1 Area Terpantau:** *Database* tunggal dan sekelompok kecil layanan di dalam satu klaster Docker.
* **100 Area Terpantau:** Penskalaan *Compute layer* secara horizontal. Penerapan *Read Replica* untuk database dan menambah kuota CPU.
* **1000 Area Terpantau:** Penggantian *Event Bus* dari Redis ke Kafka. Implementasi pemartisian data spasial (sharding) di *Database layer*.
* **Platform Nasional:** Penerapan sistem di berbagai *Availability Zones* atau *Region*, dengan penyampaian notifikasi tingkat masif menggunakan klaster *queue* yang dioptimalkan tinggi.

---

## 18. Pengoptimalan Biaya (Cost Optimization)

* **Penyimpanan (Storage):** Kebijakan daur hidup (Lifecycle policy) memindahkan data lama ke penyimpanan arsip murah (*Glacier/Coldline*).
* **Komputasi (Compute):** Penskalaan turun (*Scale-to-zero* atau pengurangan instans) selama musim kemarau saat tidak ada aktivitas hujan.
* **Bandwidth:** Menerapkan CDN ekstensif untuk menyajikan aset gambar satelit (sehingga *traffic* tidak kembali ke peladen utama).
* **Caching:** Memaksimalkan efisiensi basis data utama, menekan ongkos baca-tulis basis data awan yang mahal.
* **Pemrosesan Latar (Background processing):** Menggunakan instans *Spot/Preemptible* untuk tugas yang tidak sensitif terhadap waktu (seperti pelatihan *Machine Learning* malam hari).

---

## 19. Rekomendasi Tumpukan Teknologi (Recommended Technology Stack)

Tumpukan kelas produksi (*production-grade*) yang dianjurkan untuk PRAKIRA:

* **Platform Kontainer (Container platform):** **Google Kubernetes Engine (GKE)** atau **AWS EKS** (Keandalan tertinggi dan ekosistem *auto-scaling* terbaik).
* **Basis Data (Database):** **PostgreSQL + PostGIS** terkelola (Alat standar industri untuk operasi relasional dan geospasial).
* **Cache:** **Redis** (Kinerja struktur data dalam memori yang sangat cepat).
* **Pemantauan (Monitoring):** **Prometheus** (Metrik) + **Grafana** (Dasbor) + **Datadog** atau **OpenTelemetry** (Pelacakan APM).
* **Penyimpanan (Storage):** **Amazon S3** atau **Google Cloud Storage** (Ketahanan 99.999999999%).
* **CDN:** **Cloudflare** (Perlindungan WAF bawaan dan kinerja proksi luar biasa).
* **Antrean (Queue):** **RabbitMQ** (Skala menengah) lalu bermigrasi ke **Apache Kafka** (Skala Nasional).
* **CI/CD:** **GitHub Actions** atau **GitLab CI** (Integrasi terpadu untuk pengujian dan penerapan *Infrastructure as Code* seperti Terraform).

---

## 20. Ekspansi Masa Depan (Future Expansion)

Infrastruktur dirancang sedemikian rupa agar tidak perlu rombak ulang jika terjadi penambahan:

* **Sensor IoT:** Lapisan *API Gateway* dapat disiapkan untuk menerima ribuan ping perangkat IoT via protokol MQTT menggunakan broker tambahan, dan diteruskan ke *Event Bus*.
* **CCTV Real-Time:** Integrasi aliran video dipisahkan (*offloaded*) ke penyimpanan objek terdistribusi atau diserahkan ke layanan *Video Streaming/AI Vision* mandiri.
* **Machine Learning:** Layanan ML dapat membaca data dari *Read Replica* secara statis untuk pelatihan tanpa memengaruhi prediksi harian, lalu menyuntikkan (publish) skor *inference* ke antrean prediksi.
* **Penyebaran Nasional (National deployment):** *Stateless design* memungkinkan replikasi klaster di berbagai kota tanpa saling terkait.
* **Multi-region deployment:** Penggunaan DNS global dan basis data yang direplikasi secara geografis (mis. Aurora Global Database) untuk ketersediaan antar benua.
