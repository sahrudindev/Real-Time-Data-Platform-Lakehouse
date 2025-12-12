'use client';

import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

const architectureDiagram = `
graph TB
    subgraph Ingestion["📥 Data Ingestion"]
        KAFKA[("🔄 Kafka")]
        CDC["📋 Debezium CDC"]
        REST["🌐 FastAPI"]
        BATCH["📁 Batch Files"]
    end

    subgraph Processing["⚡ Processing"]
        SPARK["🔥 Spark Streaming"]
    end

    subgraph Lakehouse["🏠 Lakehouse"]
        BRONZE[("🥉 Bronze")]
        SILVER[("🥈 Silver")]
        GOLD[("🥇 Gold")]
    end

    subgraph Transform["🔧 Transform"]
        DBT["📊 dbt"]
    end

    subgraph Quality["✅ Quality"]
        GE["🧪 Great Expectations"]
    end

    subgraph Serving["🚀 Serving"]
        BI["📈 Metabase"]
        FEAST["🍽️ Feature Store"]
        API["🔌 REST API"]
    end

    KAFKA --> SPARK
    CDC --> KAFKA
    REST --> KAFKA
    BATCH --> SPARK
    SPARK --> BRONZE
    BRONZE --> SILVER
    SILVER --> GOLD
    GOLD --> DBT
    DBT --> GE
    GOLD --> BI
    GOLD --> FEAST
    GOLD --> API
`;

const layers = [
    {
        name: 'Data Ingestion',
        color: 'from-blue-500 to-cyan-500',
        components: [
            { name: 'Apache Kafka', desc: 'Event streaming with exactly-once semantics' },
            { name: 'Debezium CDC', desc: 'Change Data Capture from databases' },
            { name: 'FastAPI REST', desc: 'HTTP endpoint for event ingestion' },
            { name: 'Batch Ingestion', desc: 'Scheduled file processing via Airflow' },
        ],
    },
    {
        name: 'Processing',
        color: 'from-orange-500 to-red-500',
        components: [
            { name: 'Spark Streaming', desc: 'Micro-batch and streaming processing' },
            { name: 'Watermarking', desc: 'Late data handling with configurable delays' },
            { name: 'Deduplication', desc: 'Exactly-once processing guarantees' },
            { name: 'Checkpointing', desc: 'Fault tolerance and recovery' },
        ],
    },
    {
        name: 'Lakehouse',
        color: 'from-green-500 to-emerald-500',
        components: [
            { name: 'Bronze Layer', desc: 'Raw data landing with full history' },
            { name: 'Silver Layer', desc: 'Cleansed and deduplicated data' },
            { name: 'Gold Layer', desc: 'Business aggregations and metrics' },
            { name: 'Delta Lake', desc: 'ACID transactions, time travel, schema evolution' },
        ],
    },
    {
        name: 'Transformation',
        color: 'from-purple-500 to-pink-500',
        components: [
            { name: 'dbt Models', desc: 'SQL transformations with dependencies' },
            { name: 'Staging', desc: 'Source data standardization' },
            { name: 'Intermediate', desc: 'Business logic implementation' },
            { name: 'Marts', desc: 'Analytics-ready dimensional models' },
        ],
    },
];

export default function ArchitecturePage() {
    return (
        <main className="min-h-screen">
            <Navbar />

            <section className="pt-32 pb-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center mb-16"
                    >
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            <span className="gradient-text">System Architecture</span>
                        </h1>
                        <p className="text-xl text-dark-500 dark:text-dark-400 max-w-2xl mx-auto">
                            Enterprise-grade data platform with modular, scalable components
                        </p>
                    </motion.div>

                    {/* Architecture Diagram */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                        className="card-glass mb-16 overflow-hidden"
                    >
                        <h3 className="text-xl font-semibold mb-4">High-Level Architecture</h3>
                        <div className="bg-dark-900 rounded-lg p-8 text-center">
                            <pre className="text-xs md:text-sm text-dark-300 font-mono whitespace-pre overflow-x-auto">
                                {`┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA INGESTION LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Kafka   │  │ Debezium │  │ FastAPI  │  │  Batch   │                 │
│  │ Streams  │  │   CDC    │  │   REST   │  │  Files   │                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
└───────┼─────────────┼─────────────┼─────────────┼───────────────────────┘
        └─────────────┴──────┬──────┴─────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME PROCESSING LAYER                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Spark Structured Streaming                      │   │
│  │  • Watermarking  • Deduplication  • State Management  • Checkpoints│   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         LAKEHOUSE LAYER (Delta Lake)                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │    BRONZE    │───▶│    SILVER    │───▶│     GOLD     │              │
│  │  Raw Events  │    │   Cleansed   │    │  Aggregated  │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       TRANSFORMATION LAYER (dbt)                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   Staging    │───▶│ Intermediate │───▶│    Marts     │              │
│  └──────────────┘    └──────────────┘    └──────────────┘              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          SERVING LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │   Metabase   │  │ Feature Store│  │   REST API   │                  │
│  │  Dashboards  │  │    (Feast)   │  │   (FastAPI)  │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘`}
                            </pre>
                        </div>
                    </motion.div>

                    {/* Layer Details */}
                    <div className="space-y-8">
                        {layers.map((layer, i) => (
                            <motion.div
                                key={layer.name}
                                initial={{ opacity: 0, x: i % 2 === 0 ? -30 : 30 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.3 + i * 0.1 }}
                                className="card"
                            >
                                <div className={`inline-block px-4 py-1 rounded-full text-white text-sm font-medium mb-4 bg-gradient-to-r ${layer.color}`}>
                                    {layer.name}
                                </div>
                                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                                    {layer.components.map((comp) => (
                                        <div key={comp.name} className="bg-dark-50 dark:bg-dark-900 rounded-lg p-4">
                                            <h4 className="font-semibold text-dark-900 dark:text-white mb-1">{comp.name}</h4>
                                            <p className="text-sm text-dark-500 dark:text-dark-400">{comp.desc}</p>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            <Footer />
        </main>
    );
}
