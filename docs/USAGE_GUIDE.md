# 📘 Panduan Migrasi & Instalasi di Laptop Lain

Panduan ini berisi langkah-langkah untuk menjalankan Enterprise Data Platform ini di mesin baru dari nol.

## 📋 Prasyarat (Requirements)

Pastikan laptop tujuan sudah terinstall:
1. **Docker Desktop** (atau Docker Engine + Docker Compose)
2. **Git**
3. **RAM**: Minimal 8GB (rekomendasi 16GB)
4. **Disk**: Minimal 10GB free space

---

## � Langkah Instalasi (5 Menit)

### 1. Clone Repository
Buka terminal/command prompt dan jalankan:
```bash
git clone <URL_REPOSITORY_GITHUB_ANDA>
cd Data_enginer
```

### 2. Setup Environment Variables
Platform ini butuh credentials. Kita sudah siapkan file template aman.
**PENTING:** Anda harus melakukan ini agar container bisa jalan.

```bash
cd docker
cp .env.example .env
```
*(Opsional: Anda bisa edit file `.env` jika ingin mengubah password/port default, tapi defaultnya sudah cukup aman untuk development)*

### 3. Jalankan Container
Kita menggunakan konfigurasi khusus `docker-compose-no-spark.yml` untuk kestabilan services utama.

```bash
# Pastikan Anda masih di dalam folder /docker
docker compose -f docker-compose-no-spark.yml up -d
```
*Tunggu sekitar 2-5 menit hingga semua image ter-download dan container berjalan.*

### 4. Verifikasi Instalasi
Cek apakah semua container sudah berjalan:
```bash
docker compose -f docker-compose-no-spark.yml ps
```
Anda harus melihat status **running** (atau `Up`) untuk semua service.

---

## 🌐 Akses Aplikasi

Berikut adalah URL untuk mengakses semua services yang berjalan.
**Note:** Port mungkin berbeda dari default Docker biasanya untuk menghindari konflik.

| Service | URL | Login Default |
|---------|-----|---------------|
| **Website Portfolio** | http://localhost:3002 | - |
| **API Backend** | http://localhost:8005 | - |
| **Kafka UI** | http://localhost:8081 | - |
| **Metabase (BI)** | http://localhost:3000 | Setup saat buka pertama kali |
| **Grafana** | http://localhost:3001 | `admin` / `admin` |
| **MinIO Console** | http://localhost:9001 | `minioadmin` / `minioadmin123` |
| **Prometheus** | http://localhost:9091 | - |
| **PostgreSQL** | `localhost:5433` | `airflow` / `airflow` |
| **Redis** | `localhost:6379` | - |

---

## 🛠️ Troubleshooting Umum

### "Port already in use"
Jika error port bentrok, cek file `.env` atau `docker-compose-no-spark.yml` dan ubah port sebelah kiri (misal: `8006:8000`).
Saat ini ports yang digunakan adalah: `3000, 3001, 3002, 8005, 8081, 9091, 5433, 6379, 9000, 9001, 9093, 2181`.

### Container gagal start
Cek logs untuk melihat errornya:
```bash
docker compose -f docker-compose-no-spark.yml logs -f [nama-service]
# Contoh: docker compose -f docker-compose-no-spark.yml logs -f api
```

### Reset Data
Jika ingin menghapus semua database dsb dan mulai dari nol:
```bash
docker compose -f docker-compose-no-spark.yml down -v
```

---
*Dokumentasi dibuat otomatis oleh Assistant.*
