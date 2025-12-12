'use client';

import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function DocsPage() {
    return (
        <main className="min-h-screen">
            <Navbar />

            <section className="pt-32 pb-16">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
                        <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Documentation</span></h1>
                        <p className="text-xl text-dark-500 dark:text-dark-400">Complete guide to the Enterprise Data Platform</p>
                    </motion.div>

                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="prose prose-lg dark:prose-invert max-w-none">
                        <div className="card mb-8">
                            <h2 className="text-2xl font-bold mb-4">Quick Start</h2>
                            <div className="code-block mb-4">
                                <code>git clone https://github.com/your-repo/enterprise-data-platform.git</code><br />
                                <code>cd enterprise-data-platform/docker</code><br />
                                <code>docker-compose up -d</code>
                            </div>
                            <p className="text-dark-600 dark:text-dark-400">This will start all services including Kafka, Spark, Airflow, and more.</p>
                        </div>

                        <div className="card mb-8">
                            <h2 className="text-2xl font-bold mb-4">Architecture Overview</h2>
                            <ul className="space-y-2 text-dark-600 dark:text-dark-400">
                                <li><strong>Ingestion:</strong> Kafka for streaming, Airflow for batch</li>
                                <li><strong>Processing:</strong> Spark Structured Streaming with exactly-once semantics</li>
                                <li><strong>Storage:</strong> Delta Lake with Bronze/Silver/Gold layers</li>
                                <li><strong>Transformation:</strong> dbt for SQL-based modeling</li>
                                <li><strong>Quality:</strong> Great Expectations for validation</li>
                                <li><strong>Serving:</strong> Metabase dashboards, Feast features, REST API</li>
                            </ul>
                        </div>

                        <div className="card mb-8">
                            <h2 className="text-2xl font-bold mb-4">Running Components</h2>
                            <h3 className="text-lg font-semibold mt-4">Start Streaming Ingestion</h3>
                            <div className="code-block mb-4">
                                <code>spark-submit --master spark://spark-master:7077 spark/jobs/streaming_ingestion.py</code>
                            </div>
                            <h3 className="text-lg font-semibold mt-4">Run dbt Models</h3>
                            <div className="code-block mb-4">
                                <code>cd dbt && dbt run && dbt test</code>
                            </div>
                            <h3 className="text-lg font-semibold mt-4">Validate Data Quality</h3>
                            <div className="code-block">
                                <code>great_expectations checkpoint run bronze_orders_checkpoint</code>
                            </div>
                        </div>

                        <div className="card">
                            <h2 className="text-2xl font-bold mb-4">Service URLs</h2>
                            <table className="w-full text-sm">
                                <thead><tr className="border-b border-dark-200 dark:border-dark-700">
                                    <th className="text-left py-2">Service</th><th className="text-left py-2">URL</th>
                                </tr></thead>
                                <tbody className="text-dark-600 dark:text-dark-400">
                                    <tr><td className="py-2">Airflow</td><td>http://localhost:8080</td></tr>
                                    <tr><td className="py-2">Spark UI</td><td>http://localhost:8082</td></tr>
                                    <tr><td className="py-2">Kafka UI</td><td>http://localhost:8081</td></tr>
                                    <tr><td className="py-2">Metabase</td><td>http://localhost:3000</td></tr>
                                    <tr><td className="py-2">Grafana</td><td>http://localhost:3001</td></tr>
                                    <tr><td className="py-2">MinIO</td><td>http://localhost:9001</td></tr>
                                    <tr><td className="py-2">API</td><td>http://localhost:8000</td></tr>
                                    <tr><td className="py-2">Jupyter</td><td>http://localhost:8888</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                </div>
            </section>

            <Footer />
        </main>
    );
}
