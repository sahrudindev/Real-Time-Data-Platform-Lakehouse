import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'Enterprise Data Platform | Portfolio',
    description: 'Real-Time Data Platform with Lakehouse, Governance, and ML-ready System',
    keywords: ['Data Engineering', 'Kafka', 'Spark', 'Delta Lake', 'dbt', 'Airflow'],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className="dark">
            <body className={inter.className}>{children}</body>
        </html>
    )
}
