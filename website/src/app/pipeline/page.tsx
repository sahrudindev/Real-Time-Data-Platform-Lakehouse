'use client';

import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { FiArrowRight, FiDatabase, FiZap, FiLayers, FiGitBranch, FiCheckCircle, FiBarChart2 } from 'react-icons/fi';

const pipelineSteps = [
    { icon: FiDatabase, name: 'Data Sources', desc: 'Events, CDC, Batch files', color: 'bg-blue-500' },
    { icon: FiZap, name: 'Kafka', desc: 'Event streaming', color: 'bg-orange-500' },
    { icon: FiLayers, name: 'Spark', desc: 'Processing', color: 'bg-red-500' },
    { icon: FiDatabase, name: 'Bronze', desc: 'Raw landing', color: 'bg-amber-600' },
    { icon: FiDatabase, name: 'Silver', desc: 'Cleansed', color: 'bg-gray-400' },
    { icon: FiDatabase, name: 'Gold', desc: 'Aggregated', color: 'bg-yellow-500' },
    { icon: FiGitBranch, name: 'dbt', desc: 'Transform', color: 'bg-purple-500' },
    { icon: FiCheckCircle, name: 'Quality', desc: 'Validation', color: 'bg-green-500' },
    { icon: FiBarChart2, name: 'Analytics', desc: 'Dashboards', color: 'bg-pink-500' },
];

export default function PipelinePage() {
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
                            <span className="gradient-text">Data Pipeline Flow</span>
                        </h1>
                        <p className="text-xl text-dark-500 dark:text-dark-400 max-w-2xl mx-auto">
                            End-to-end data journey from ingestion to analytics
                        </p>
                    </motion.div>

                    {/* Animated Pipeline */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="card-glass p-8 mb-16"
                    >
                        <div className="flex flex-wrap items-center justify-center gap-4">
                            {pipelineSteps.map((step, i) => (
                                <motion.div
                                    key={step.name}
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: 0.3 + i * 0.1 }}
                                    className="flex items-center"
                                >
                                    <div className="flex flex-col items-center">
                                        <motion.div
                                            animate={{ y: [0, -5, 0] }}
                                            transition={{ duration: 2, repeat: Infinity, delay: i * 0.2 }}
                                            className={`w-16 h-16 ${step.color} rounded-xl flex items-center justify-center shadow-lg`}
                                        >
                                            <step.icon className="w-8 h-8 text-white" />
                                        </motion.div>
                                        <span className="mt-2 font-medium text-dark-900 dark:text-white text-sm">{step.name}</span>
                                        <span className="text-xs text-dark-500">{step.desc}</span>
                                    </div>
                                    {i < pipelineSteps.length - 1 && (
                                        <motion.div
                                            animate={{ x: [0, 5, 0] }}
                                            transition={{ duration: 1, repeat: Infinity }}
                                            className="mx-4"
                                        >
                                            <FiArrowRight className="w-6 h-6 text-primary-500" />
                                        </motion.div>
                                    )}
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>

                    {/* Pipeline Details */}
                    <div className="grid md:grid-cols-2 gap-8">
                        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="card">
                            <h3 className="text-xl font-bold mb-4 gradient-text">Real-Time Path</h3>
                            <ul className="space-y-3 text-dark-600 dark:text-dark-300">
                                <li>1. Events published to Kafka topics</li>
                                <li>2. Spark Streaming consumes with watermarking</li>
                                <li>3. Deduplication via event_id</li>
                                <li>4. Write to Bronze Delta Lake</li>
                                <li>5. Continuous processing to Silver/Gold</li>
                                <li>6. Real-time dashboards update</li>
                            </ul>
                        </motion.div>

                        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.6 }} className="card">
                            <h3 className="text-xl font-bold mb-4 gradient-text">Batch Path</h3>
                            <ul className="space-y-3 text-dark-600 dark:text-dark-300">
                                <li>1. Airflow schedules batch ingestion</li>
                                <li>2. Files loaded to Bronze layer</li>
                                <li>3. dbt runs transformations</li>
                                <li>4. Great Expectations validates</li>
                                <li>5. DataHub updates lineage</li>
                                <li>6. Feature Store refreshes</li>
                            </ul>
                        </motion.div>
                    </div>
                </div>
            </section>

            <Footer />
        </main>
    );
}
