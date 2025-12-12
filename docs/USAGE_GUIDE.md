# 📘 Panduan Penggunaan Enterprise Data Platform

Dokumentasi lengkap cara menggunakan dan menjalankan Enterprise Data Platform.

---

## 🚀 Quick Start (5 Menit)

### Langkah 1: Clone Repository
```bash
git clone <repository-url>
cd Data_enginer
```

### Langkah 2: Jalankan Docker Compose
```bash
cd docker
docker-compose up -d
```

### Langkah 3: Akses Services
| Service | URL | Login |
|---------|-----|-------|
| 🌐 Website Portfolio | http://localhost:3002 | - |
| 📊 API Documentation | http://localhost:8000/docs | - |
| ✈️ Airflow | http://localhost:8080 | admin / admin |
| ⚡ Spark UI | http://localhost:8082 | - |
| 📨 Kafka UI | http://localhost:8081 | - |
| 📈 Grafana | http://localhost:3001 | admin / admin |
| 🗄️ MinIO Console | http://localhost:9001 | minioadmin / minioadmin123 |
| 📓 Jupyter Lab | http://localhost:8888 | Token: enterprise_data_platform |

---

## 📁 Struktur Folder

```
Data_enginer/
├── docker/              # Docker Compose & konfigurasi
├── kafka/               # Kafka producers & topics
├── spark/               # Spark streaming jobs
├── dbt/                 # dbt models & transformations
├── airflow/             # Airflow DAGs
├── great_expectations/  # Data quality suites
├── api/                 # FastAPI REST endpoints
├── feature_store/       # Feast feature definitions
├── monitoring/          # Prometheus & Grafana
├── website/             # Next.js portfolio
└── docs/                # Dokumentasi
```

---

## 🔧 Menjalankan Komponen Individual

### 1. API dengan Data Faker
```bash
cd api
pip install faker fastapi uvicorn
python main.py
# Akses: http://localhost:8000/docs
```

### 2. Website Portfolio
```bash
cd website
npm install
npm run dev
# Akses: http://localhost:3000
```

### 3. Spark Streaming Job
```bash
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages io.delta:delta-core_2.12:2.4.0 \
  /opt/spark/jobs/streaming_ingestion.py
```

### 4. dbt Transformations
```bash
cd dbt
dbt deps
dbt run
dbt test
dbt docs generate && dbt docs serve
```

### 5. Great Expectations Validation
```bash
cd great_expectations
great_expectations checkpoint run bronze_orders_checkpoint
great_expectations docs build
```

---

## 📊 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/health` | Health check |
| GET | `/api/v1/stats` | Statistik platform |
| GET | `/api/v1/orders` | Daftar orders |
| GET | `/api/v1/customers` | Daftar customers |
| GET | `/api/v1/products` | Daftar products |
| POST | `/api/v1/generate` | Generate data baru |

### Contoh Request
```bash
# Get stats
curl http://localhost:8000/api/v1/stats

# Get orders
curl http://localhost:8000/api/v1/orders?limit=10

# Generate new data
curl -X POST http://localhost:8000/api/v1/generate?orders=50
```

---

## 🧪 Testing & Validasi

### Run All Tests
```bash
# dbt tests
cd dbt && dbt test

# Great Expectations
cd great_expectations && great_expectations checkpoint run bronze_orders_checkpoint
```

### Verify Pipeline
1. Buka Airflow: http://localhost:8080
2. Enable DAG: `batch_ingestion` atau `dbt_build`
3. Trigger DAG secara manual
4. Monitor di Spark UI: http://localhost:8082

---

## 🛠️ Troubleshooting

### Docker containers not starting
```bash
docker-compose down
docker-compose up -d --build
docker-compose logs -f
```

### Check specific service logs
```bash
docker logs api -f
docker logs website -f
docker logs kafka -f
```

### Reset all data
```bash
docker-compose down -v  # Hapus volumes
docker-compose up -d
```

---

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buat issue di repository atau hubungi tim Data Engineering.
