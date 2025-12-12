'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiMenu, FiX, FiMoon, FiSun, FiGithub, FiExternalLink } from 'react-icons/fi';

const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Architecture', href: '/architecture' },
    { name: 'Pipeline', href: '/pipeline' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Code', href: '/code' },
    { name: 'Docs', href: '/docs' },
    { name: 'Monitoring', href: '/monitoring' },
];

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [isDark, setIsDark] = useState(true);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 50);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const toggleTheme = () => {
        setIsDark(!isDark);
        document.documentElement.classList.toggle('dark');
    };

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/80 dark:bg-dark-900/80 backdrop-blur-xl shadow-lg' : 'bg-transparent'
                }`}
        >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <Link href="/" className="flex items-center space-x-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg" />
                        <span className="font-bold text-lg text-dark-900 dark:text-white">DataPlatform</span>
                    </Link>

                    <div className="hidden md:flex items-center space-x-6">
                        {navigation.map((item) => (
                            <Link key={item.name} href={item.href} className="nav-link">
                                {item.name}
                            </Link>
                        ))}
                        <button onClick={toggleTheme} className="p-2 rounded-lg hover:bg-dark-100 dark:hover:bg-dark-800">
                            {isDark ? <FiSun className="w-5 h-5" /> : <FiMoon className="w-5 h-5" />}
                        </button>
                        <a href="https://github.com" className="btn-primary text-sm py-2 px-4" target="_blank" rel="noopener">
                            <FiGithub className="w-4 h-4 mr-2" /> GitHub
                        </a>
                    </div>

                    <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2">
                        {isOpen ? <FiX className="w-6 h-6" /> : <FiMenu className="w-6 h-6" />}
                    </button>
                </div>
            </div>

            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="md:hidden bg-white dark:bg-dark-900 border-t border-dark-100 dark:border-dark-800"
                >
                    <div className="px-4 py-4 space-y-2">
                        {navigation.map((item) => (
                            <Link key={item.name} href={item.href} onClick={() => setIsOpen(false)}
                                className="block px-4 py-2 rounded-lg hover:bg-dark-100 dark:hover:bg-dark-800">
                                {item.name}
                            </Link>
                        ))}
                    </div>
                </motion.div>
            )}
        </motion.nav>
    );
}
