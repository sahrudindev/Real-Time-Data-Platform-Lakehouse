'use client';

import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { FiFolder, FiFile, FiChevronRight, FiCode } from 'react-icons/fi';

const codeStructure = [
    { type: 'folder', name: 'docker/', files: ['docker-compose.yml', '.env'] },
    { type: 'folder', name: 'kafka/', files: ['config/topics.json', 'scripts/create_topics.sh', 'producers/event_producer.py'] },
    { type: 'folder', name: 'spark/', files: ['jobs/streaming_ingestion.py', 'jobs/silver_processor.py', 'jobs/gold_processor.py', 'utils/delta_utils.py'] },
    { type: 'folder', name: 'dbt/', files: ['dbt_project.yml', 'models/staging/*.sql', 'models/marts/*.sql'] },
    { type: 'folder', name: 'airflow/', files: ['dags/batch_ingestion_dag.py', 'dags/dbt_build_dag.py', 'dags/quality_validation_dag.py'] },
    { type: 'folder', name: 'great_expectations/', files: ['great_expectations.yml', 'expectations/*.json', 'checkpoints/*.yml'] },
    { type: 'folder', name: 'api/', files: ['main.py', 'Dockerfile', 'requirements.txt'] },
    { type: 'folder', name: 'feature_store/', files: ['feature_store.yaml', 'features/customer_features.py'] },
    { type: 'folder', name: 'monitoring/', files: ['prometheus/prometheus.yml', 'grafana/dashboards/*.json'] },
    { type: 'folder', name: 'website/', files: ['package.json', 'src/app/*.tsx', 'src/components/*.tsx'] },
];

export default function CodePage() {
    return (
        <main className="min-h-screen">
            <Navbar />

            <section className="pt-32 pb-16">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
                        <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Code Explorer</span></h1>
                        <p className="text-xl text-dark-500 dark:text-dark-400">Project structure and key components</p>
                    </motion.div>

                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="card">
                        <h3 className="text-xl font-bold mb-6 flex items-center"><FiCode className="mr-2" /> Project Structure</h3>
                        <div className="space-y-4">
                            {codeStructure.map((item, i) => (
                                <motion.div
                                    key={item.name}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.1 * i }}
                                    className="border-l-2 border-primary-500 pl-4"
                                >
                                    <div className="flex items-center text-dark-900 dark:text-white font-medium">
                                        <FiFolder className="mr-2 text-primary-500" />
                                        {item.name}
                                    </div>
                                    <div className="ml-6 mt-2 space-y-1">
                                        {item.files.map((file) => (
                                            <div key={file} className="flex items-center text-sm text-dark-500 dark:text-dark-400">
                                                <FiFile className="mr-2" />
                                                {file}
                                            </div>
                                        ))}
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>

                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} className="card mt-8">
                        <h3 className="text-xl font-bold mb-4">Statistics</h3>
                        <div className="grid grid-cols-3 gap-4 text-center">
                            <div className="bg-dark-50 dark:bg-dark-900 rounded-lg p-4">
                                <div className="text-3xl font-bold gradient-text">130+</div>
                                <div className="text-sm text-dark-500">Files</div>
                            </div>
                            <div className="bg-dark-50 dark:bg-dark-900 rounded-lg p-4">
                                <div className="text-3xl font-bold gradient-text">13k+</div>
                                <div className="text-sm text-dark-500">Lines of Code</div>
                            </div>
                            <div className="bg-dark-50 dark:bg-dark-900 rounded-lg p-4">
                                <div className="text-3xl font-bold gradient-text">20+</div>
                                <div className="text-sm text-dark-500">Services</div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            <Footer />
        </main>
    );
}
