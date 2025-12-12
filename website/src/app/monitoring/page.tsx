'use client';

import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function MonitoringPage() {
    return (
        <main className="min-h-screen">
            <Navbar />

            <section className="pt-32 pb-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
                        <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Monitoring & Observability</span></h1>
                        <p className="text-xl text-dark-500 dark:text-dark-400">Real-time metrics, alerts, and pipeline health</p>
                    </motion.div>

                    <div className="grid md:grid-cols-3 gap-6 mb-8">
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card text-center">
                            <div className="text-4xl font-bold text-green-500 mb-2">99.9%</div>
                            <div className="text-dark-500">Uptime</div>
                        </motion.div>
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="card text-center">
                            <div className="text-4xl font-bold text-blue-500 mb-2">0.8s</div>
                            <div className="text-dark-500">Avg Latency</div>
                        </motion.div>
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="card text-center">
                            <div className="text-4xl font-bold text-purple-500 mb-2">0</div>
                            <div className="text-dark-500">Active Alerts</div>
                        </motion.div>
                    </div>

                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }} className="card mb-8">
                        <h3 className="text-xl font-bold mb-4">Grafana Dashboard Preview</h3>
                        <div className="bg-dark-900 rounded-lg p-4 font-mono text-sm">
                            <pre className="text-dark-300">{`
┌──────────────────────────────────────────────────────────────┐
│  ENTERPRISE DATA PLATFORM - OVERVIEW DASHBOARD               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Services Up: ██████████ 100%    Error Rate: ░░░░░░░░░░ 0%   │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Request Latency (P95)                                  ││
│  │    ▂▃▄▅▆▅▄▃▂▃▄▅▆▇▆▅▄▃▂▁▂▃▄▅▆▅▄▃▂▃▄▅                    ││
│  │    0.5s ──────────────────────────────── 2.0s           ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Throughput (msgs/sec)                                  ││
│  │    ▁▂▃▅▇█████▇▅▃▂▅▇████████▅▃▂▅▇█████                  ││
│  │    0 ─────────────────────────────────── 10k            ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└──────────────────────────────────────────────────────────────┘
              `}</pre>
                        </div>
                    </motion.div>

                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} className="card">
                        <h3 className="text-xl font-bold mb-4">Alert Rules</h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between p-3 bg-dark-50 dark:bg-dark-900 rounded-lg">
                                <span>Pipeline Down</span>
                                <span className="text-green-500">OK</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-dark-50 dark:bg-dark-900 rounded-lg">
                                <span>High Error Rate (&gt;10%)</span>
                                <span className="text-green-500">OK</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-dark-50 dark:bg-dark-900 rounded-lg">
                                <span>Kafka Consumer Lag</span>
                                <span className="text-green-500">OK</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-dark-50 dark:bg-dark-900 rounded-lg">
                                <span>Low Disk Space</span>
                                <span className="text-green-500">OK</span>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            <Footer />
        </main>
    );
}
