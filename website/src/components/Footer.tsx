'use client';

import Link from 'next/link';
import { FiGithub, FiLinkedin, FiMail, FiHeart } from 'react-icons/fi';

export default function Footer() {
    return (
        <footer className="bg-dark-900 text-white py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid md:grid-cols-4 gap-12">
                    <div className="col-span-2">
                        <div className="flex items-center space-x-2 mb-4">
                            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg" />
                            <span className="font-bold text-lg">Enterprise Data Platform</span>
                        </div>
                        <p className="text-dark-400 max-w-md">
                            A production-ready, enterprise-grade real-time data platform with lakehouse architecture,
                            governance, and ML-ready capabilities.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4">Quick Links</h4>
                        <ul className="space-y-2 text-dark-400">
                            <li><Link href="/architecture" className="hover:text-primary-400">Architecture</Link></li>
                            <li><Link href="/pipeline" className="hover:text-primary-400">Pipeline Flow</Link></li>
                            <li><Link href="/docs" className="hover:text-primary-400">Documentation</Link></li>
                            <li><Link href="/code" className="hover:text-primary-400">Code Explorer</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4">Tech Stack</h4>
                        <ul className="space-y-2 text-dark-400">
                            <li>Apache Kafka</li>
                            <li>Apache Spark</li>
                            <li>Delta Lake</li>
                            <li>Apache Airflow</li>
                            <li>dbt</li>
                            <li>Great Expectations</li>
                        </ul>
                    </div>
                </div>

                <div className="border-t border-dark-800 mt-12 pt-8 flex flex-col md:flex-row items-center justify-between">
                    <p className="text-dark-400 flex items-center">
                        Built with <FiHeart className="mx-1 text-red-500" /> for Data Engineering
                    </p>
                    <div className="flex items-center space-x-4 mt-4 md:mt-0">
                        <a href="https://github.com" className="text-dark-400 hover:text-white"><FiGithub className="w-5 h-5" /></a>
                        <a href="https://linkedin.com" className="text-dark-400 hover:text-white"><FiLinkedin className="w-5 h-5" /></a>
                        <a href="mailto:contact@example.com" className="text-dark-400 hover:text-white"><FiMail className="w-5 h-5" /></a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
