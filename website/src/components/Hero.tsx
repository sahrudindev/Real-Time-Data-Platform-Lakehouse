'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { FiArrowRight, FiDatabase, FiActivity, FiLayers, FiCpu, FiShield, FiBarChart2 } from 'react-icons/fi';

const features = [
    { icon: FiDatabase, title: 'Kafka Streaming', desc: 'Real-time event ingestion with exactly-once semantics' },
    { icon: FiActivity, title: 'Spark Processing', desc: 'Distributed processing with stateful aggregations' },
    { icon: FiLayers, title: 'Delta Lakehouse', desc: 'Bronze-Silver-Gold architecture with time travel' },
    { icon: FiCpu, title: 'dbt Transformations', desc: 'SQL-based models with testing and documentation' },
    { icon: FiShield, title: 'Data Quality', desc: 'Great Expectations validation and data contracts' },
    { icon: FiBarChart2, title: 'ML Features', desc: 'Feast feature store for ML-ready data' },
];

const stats = [
    { value: '10TB+', label: 'Data Processed Daily' },
    { value: '99.9%', label: 'Pipeline Uptime' },
    { value: '<1s', label: 'End-to-End Latency' },
    { value: '50+', label: 'Data Models' },
];

export default function Hero() {
    return (
        <section className="relative min-h-screen pt-24 pb-16 overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-purple-500/5 to-transparent" />
            <div className="absolute top-20 right-20 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse-slow" />
            <div className="absolute bottom-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow" />

            <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Hero Content */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center max-w-4xl mx-auto"
                >
                    <span className="inline-block px-4 py-1.5 mb-6 text-sm font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30 rounded-full">
                        Enterprise-Grade Data Platform
                    </span>

                    <h1 className="text-5xl md:text-7xl font-extrabold mb-6">
                        <span className="gradient-text">Real-Time Data</span>
                        <br />
                        <span className="text-dark-900 dark:text-white">Platform & Lakehouse</span>
                    </h1>

                    <p className="text-xl text-dark-500 dark:text-dark-400 mb-10 max-w-2xl mx-auto">
                        Production-ready architecture with Kafka, Spark, Delta Lake, dbt, Airflow,
                        Great Expectations, and ML Feature Store.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link href="/architecture" className="btn-primary">
                            Explore Architecture <FiArrowRight className="ml-2" />
                        </Link>
                        <Link href="/docs" className="btn-secondary">
                            View Documentation
                        </Link>
                    </div>
                </motion.div>

                {/* Stats */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.8 }}
                    className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
                >
                    {stats.map((stat, i) => (
                        <div key={i} className="card-glass text-center">
                            <div className="text-3xl md:text-4xl font-bold gradient-text">{stat.value}</div>
                            <div className="text-dark-500 dark:text-dark-400 mt-1">{stat.label}</div>
                        </div>
                    ))}
                </motion.div>

                {/* Features Grid */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 0.8 }}
                    className="mt-24"
                >
                    <h2 className="section-title text-center">Key Components</h2>
                    <p className="section-subtitle text-center mb-12">
                        Enterprise-grade components for building modern data infrastructure
                    </p>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {features.map((feature, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.6 + i * 0.1 }}
                                className="card group"
                            >
                                <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                    <feature.icon className="w-6 h-6 text-white" />
                                </div>
                                <h3 className="text-xl font-semibold text-dark-900 dark:text-white mb-2">{feature.title}</h3>
                                <p className="text-dark-500 dark:text-dark-400">{feature.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
