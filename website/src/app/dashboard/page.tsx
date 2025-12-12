'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { FiTrendingUp, FiUsers, FiShoppingCart, FiDollarSign, FiPackage, FiActivity, FiCheckCircle, FiAlertTriangle } from 'react-icons/fi';

// Premium Color Palette
const colors = {
    primary: '#6366f1',    // Indigo
    secondary: '#8b5cf6',  // Purple
    accent: '#06b6d4',     // Cyan
    success: '#10b981',    // Emerald
    warning: '#f59e0b',    // Amber
    danger: '#ef4444',     // Red
    gold: '#fbbf24',       // Gold
};

// Sample Data dengan Faker-style
const sampleStats = {
    total_orders: 2847,
    total_customers: 1234,
    total_products: 456,
    total_revenue: 4750000000,
    avg_order_value: 1668420,
    growth_rate: 23.5,
    success_rate: 98.7,
    data_quality_score: 99.2,
};

const recentOrders = [
    { order_id: "ORD-8F4A2B1C", customer: "Budi Santoso", amount: 2450000, status: "completed", time: "2 menit lalu" },
    { order_id: "ORD-7E3D9C2A", customer: "Siti Rahayu", amount: 15750000, status: "processing", time: "5 menit lalu" },
    { order_id: "ORD-6B2A8D1F", customer: "Ahmad Wijaya", amount: 890000, status: "delivered", time: "12 menit lalu" },
    { order_id: "ORD-5C1E7F3B", customer: "Dewi Lestari", amount: 4320000, status: "pending", time: "18 menit lalu" },
    { order_id: "ORD-4D0F6E2C", customer: "Rizky Pratama", amount: 7650000, status: "completed", time: "25 menit lalu" },
];

const topProducts = [
    { name: "Samsung Galaxy S24 Ultra", sales: 342, revenue: 4100000000, trend: 15 },
    { name: "MacBook Pro M3", sales: 156, revenue: 3900000000, trend: 22 },
    { name: "Nike Air Max 270", sales: 892, revenue: 1250000000, trend: -5 },
    { name: "Sony WH-1000XM5", sales: 423, revenue: 1690000000, trend: 8 },
];

const customerSegments = [
    { segment: "Platinum", count: 124, percentage: 10, color: "from-purple-500 to-pink-500" },
    { segment: "Gold", count: 312, percentage: 25, color: "from-yellow-400 to-orange-500" },
    { segment: "Silver", count: 445, percentage: 36, color: "from-gray-300 to-gray-500" },
    { segment: "Bronze", count: 353, percentage: 29, color: "from-amber-600 to-amber-800" },
];

export default function DashboardPage() {
    const [stats, setStats] = useState(sampleStats);
    const [isLive, setIsLive] = useState(true);

    const formatCurrency = (amount: number) => {
        if (amount >= 1000000000) return `Rp ${(amount / 1000000000).toFixed(1)}M`;
        if (amount >= 1000000) return `Rp ${(amount / 1000000).toFixed(1)}Jt`;
        return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(amount);
    };

    const getStatusStyle = (status: string) => {
        const styles: Record<string, string> = {
            completed: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
            delivered: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
            processing: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
            pending: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
        };
        return styles[status] || 'bg-gray-500/20 text-gray-400';
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950">
            <Navbar />

            <section className="pt-28 pb-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                    {/* Header */}
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
                        <div className="flex items-center justify-between flex-wrap gap-4">
                            <div>
                                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                    Analytics Dashboard
                                </h1>
                                <p className="text-slate-400">Real-time business intelligence & data insights</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <span className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium ${isLive ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-700 text-slate-400'}`}>
                                    <span className={`w-2 h-2 rounded-full ${isLive ? 'bg-emerald-400 animate-pulse' : 'bg-slate-500'}`}></span>
                                    {isLive ? 'Live Data' : 'Offline'}
                                </span>
                                <span className="px-4 py-2 rounded-full text-sm font-medium bg-indigo-500/20 text-indigo-400">
                                    Last update: Just now
                                </span>
                            </div>
                        </div>
                    </motion.div>

                    {/* KPI Cards */}
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                        {[
                            { icon: FiDollarSign, label: 'Total Revenue', value: formatCurrency(stats.total_revenue), change: '+23.5%', color: 'from-emerald-500 to-teal-600', positive: true },
                            { icon: FiShoppingCart, label: 'Total Orders', value: stats.total_orders.toLocaleString(), change: '+18.2%', color: 'from-indigo-500 to-purple-600', positive: true },
                            { icon: FiUsers, label: 'Customers', value: stats.total_customers.toLocaleString(), change: '+12.8%', color: 'from-cyan-500 to-blue-600', positive: true },
                            { icon: FiPackage, label: 'Products', value: stats.total_products.toLocaleString(), change: '+5.4%', color: 'from-amber-500 to-orange-600', positive: true },
                        ].map((kpi, i) => (
                            <motion.div
                                key={kpi.label}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="relative overflow-hidden rounded-2xl bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-5 group hover:border-slate-600 transition-all"
                            >
                                <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br ${kpi.color} opacity-10 rounded-full blur-2xl group-hover:opacity-20 transition-opacity`}></div>
                                <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${kpi.color} mb-3`}>
                                    <kpi.icon className="w-5 h-5 text-white" />
                                </div>
                                <p className="text-sm text-slate-400 mb-1">{kpi.label}</p>
                                <p className="text-2xl lg:text-3xl font-bold text-white mb-1">{kpi.value}</p>
                                <span className={`text-xs font-medium ${kpi.positive ? 'text-emerald-400' : 'text-red-400'}`}>
                                    {kpi.change} vs last month
                                </span>
                            </motion.div>
                        ))}
                    </div>

                    {/* Middle Section */}
                    <div className="grid lg:grid-cols-3 gap-6 mb-8">

                        {/* Revenue Chart Placeholder */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.3 }}
                            className="lg:col-span-2 rounded-2xl bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-6"
                        >
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-semibold text-white">Revenue Trend</h3>
                                <div className="flex gap-2">
                                    {['7D', '1M', '3M', '1Y'].map((period) => (
                                        <button key={period} className="px-3 py-1 text-xs rounded-lg bg-slate-700/50 text-slate-400 hover:bg-indigo-500/20 hover:text-indigo-400 transition-colors">
                                            {period}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="h-48 flex items-end justify-between gap-2 px-4">
                                {[65, 45, 78, 52, 89, 67, 94, 73, 86, 91, 77, 95].map((height, i) => (
                                    <motion.div
                                        key={i}
                                        initial={{ height: 0 }}
                                        animate={{ height: `${height}%` }}
                                        transition={{ delay: 0.5 + i * 0.05, duration: 0.5 }}
                                        className="flex-1 bg-gradient-to-t from-indigo-600 to-purple-500 rounded-t-lg opacity-80 hover:opacity-100 transition-opacity cursor-pointer"
                                    ></motion.div>
                                ))}
                            </div>
                            <div className="flex justify-between mt-4 text-xs text-slate-500">
                                <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span>
                                <span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span>
                            </div>
                        </motion.div>

                        {/* Customer Segments */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.4 }}
                            className="rounded-2xl bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-6"
                        >
                            <h3 className="text-lg font-semibold text-white mb-6">Customer Segments</h3>
                            <div className="space-y-4">
                                {customerSegments.map((seg, i) => (
                                    <motion.div
                                        key={seg.segment}
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: 0.5 + i * 0.1 }}
                                    >
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="text-slate-300">{seg.segment}</span>
                                            <span className="text-slate-400">{seg.count} ({seg.percentage}%)</span>
                                        </div>
                                        <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${seg.percentage}%` }}
                                                transition={{ delay: 0.6 + i * 0.1, duration: 0.5 }}
                                                className={`h-full bg-gradient-to-r ${seg.color} rounded-full`}
                                            ></motion.div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    </div>

                    {/* Bottom Section */}
                    <div className="grid lg:grid-cols-2 gap-6 mb-8">

                        {/* Recent Orders */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 }}
                            className="rounded-2xl bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-6"
                        >
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-semibold text-white">Recent Orders</h3>
                                <span className="text-xs text-indigo-400 cursor-pointer hover:underline">View All →</span>
                            </div>
                            <div className="space-y-3">
                                {recentOrders.map((order, i) => (
                                    <motion.div
                                        key={order.order_id}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: 0.6 + i * 0.05 }}
                                        className="flex items-center justify-between p-3 rounded-xl bg-slate-900/50 hover:bg-slate-700/30 transition-colors"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-medium text-sm">
                                                {order.customer.split(' ').map(n => n[0]).join('')}
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-white">{order.customer}</p>
                                                <p className="text-xs text-slate-500">{order.order_id} • {order.time}</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-semibold text-white">{formatCurrency(order.amount)}</p>
                                            <span className={`text-xs px-2 py-0.5 rounded-full border ${getStatusStyle(order.status)}`}>
                                                {order.status}
                                            </span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>

                        {/* Top Products */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6 }}
                            className="rounded-2xl bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 p-6"
                        >
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-semibold text-white">Top Products</h3>
                                <span className="text-xs text-indigo-400 cursor-pointer hover:underline">View All →</span>
                            </div>
                            <div className="space-y-3">
                                {topProducts.map((product, i) => (
                                    <motion.div
                                        key={product.name}
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: 0.7 + i * 0.05 }}
                                        className="flex items-center justify-between p-3 rounded-xl bg-slate-900/50 hover:bg-slate-700/30 transition-colors"
                                    >
                                        <div className="flex items-center gap-3">
                                            <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold text-sm">
                                                #{i + 1}
                                            </span>
                                            <div>
                                                <p className="text-sm font-medium text-white">{product.name}</p>
                                                <p className="text-xs text-slate-500">{product.sales} sales</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-semibold text-white">{formatCurrency(product.revenue)}</p>
                                            <span className={`text-xs ${product.trend > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                                {product.trend > 0 ? '↑' : '↓'} {Math.abs(product.trend)}%
                                            </span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    </div>

                    {/* Data Quality & Pipeline Health */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.7 }}
                        className="rounded-2xl bg-gradient-to-r from-indigo-600/20 via-purple-600/20 to-pink-600/20 backdrop-blur-xl border border-indigo-500/30 p-6"
                    >
                        <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                            <FiActivity className="text-indigo-400" />
                            Pipeline Health & Data Quality
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {[
                                { label: 'Data Quality Score', value: '99.2%', icon: FiCheckCircle, status: 'success' },
                                { label: 'Pipeline Uptime', value: '99.9%', icon: FiActivity, status: 'success' },
                                { label: 'Processing Latency', value: '0.8s', icon: FiTrendingUp, status: 'success' },
                                { label: 'Active Alerts', value: '0', icon: FiAlertTriangle, status: 'success' },
                            ].map((metric, i) => (
                                <motion.div
                                    key={metric.label}
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ delay: 0.8 + i * 0.1 }}
                                    className="bg-slate-900/50 rounded-xl p-4 text-center"
                                >
                                    <metric.icon className={`w-8 h-8 mx-auto mb-2 ${metric.status === 'success' ? 'text-emerald-400' : 'text-amber-400'}`} />
                                    <p className="text-2xl font-bold text-white">{metric.value}</p>
                                    <p className="text-xs text-slate-400 mt-1">{metric.label}</p>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>

                </div>
            </section>

            <Footer />
        </main>
    );
}
