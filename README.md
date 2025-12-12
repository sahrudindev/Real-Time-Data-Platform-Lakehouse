# Enterprise Data Platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)

A production-ready, enterprise-grade **Real-Time Data Platform** with Lakehouse architecture, Data Governance, and ML-ready capabilities.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA INGESTION LAYER                             │
│  Kafka Streams  │  Debezium CDC  │  FastAPI REST  │  Batch Files        │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME PROCESSING (Spark)                        │
│  Watermarking  │  Deduplication  │  State Management  │  Checkpoints    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    LAKEHOUSE LAYER (Delta Lake)                          │
│       BRONZE (Raw)  ───▶  SILVER (Cleansed)  ───▶  GOLD (Aggregated)    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  SERVING: Metabase (BI)  │  Feast (Features)  │  FastAPI (REST)         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

> **Note:** Untuk panduan lengkap instalasi di laptop baru, lihat [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md).

```bash
# Clone the repository
git clone https://github.com/your-repo/enterprise-data-platform.git
cd enterprise-data-platform

# Setup Environment Credentials
cd docker
cp .env.example .env

# Start all services (Stable Version)
docker compose -f docker-compose-no-spark.yml up -d

# Verify services are running
docker compose -f docker-compose-no-spark.yml ps
```

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| Streaming | Apache Kafka, Debezium |
| Processing | Apache Spark 3.5 |
| Storage | Delta Lake, MinIO (S3) |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| Quality | Great Expectations |
| Governance | DataHub |
| ML Features | Feast |
| BI | Metabase |
| Monitoring | Prometheus, Grafana |
| API | FastAPI |

## 📁 Project Structure

```
├── docker/                 # Docker Compose & configs
├── kafka/                  # Kafka producers, topics
├── spark/                  # Spark streaming jobs
│   ├── jobs/              # Processing scripts
│   └── utils/             # Delta Lake utilities
├── dbt/                    # dbt models & tests
├── airflow/                # Airflow DAGs
├── great_expectations/     # Data quality suites
├── feature_store/          # Feast definitions
├── api/                    # FastAPI REST service
├── monitoring/             # Prometheus & Grafana
├── website/                # Next.js portfolio
└── docs/                   # Documentation
```

## 🌐 Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow | http://localhost:8080 | admin / admin |
| Spark UI | http://localhost:8082 | - |
| Kafka UI | http://localhost:8081 | - |
| Metabase | http://localhost:3000 | signup |
| Grafana | http://localhost:3001 | admin / admin |
| MinIO | http://localhost:9001 | minioadmin / minioadmin123 |
| API Docs | http://localhost:8000/docs | - |
| Jupyter | http://localhost:8888 | token: enterprise_data_platform |

## ⚡ Running Components

### Start Streaming Ingestion
```bash
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages io.delta:delta-core_2.12:2.4.0 \
  /opt/spark/jobs/streaming_ingestion.py
```

### Run dbt Models
```bash
docker exec -it airflow-worker bash -c "cd /opt/dbt && dbt run && dbt test"
```

### Validate Data Quality
```bash
docker exec -it airflow-worker bash -c \
  "great_expectations checkpoint run bronze_orders_checkpoint"
```

### Produce Test Events
```bash
docker exec -it api python -c "
from kafka.producers.event_producer import main
main()
"
```

## 📊 Data Flow

1. **Ingestion**: Events → Kafka topics
2. **Processing**: Spark Streaming with exactly-once semantics
3. **Bronze**: Raw event landing (full history)
4. **Silver**: Cleansed, deduplicated, SCD2
5. **Gold**: Business aggregations, metrics
6. **Serving**: BI dashboards, ML features, API

## 🔧 Configuration

Key environment variables in `docker/.env`:

```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
SPARK_MASTER=spark://spark-master:7077
DELTA_LAKE_PATH=/data/delta
```

## 📈 Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (dashboards pre-configured)
- Alerts configured for: Pipeline down, High error rate, Kafka lag

## 🎨 Portfolio Website

```bash
cd website
npm install
npm run dev
# Open http://localhost:3000
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file.
