"use client";
import React from 'react';
import Link from 'next/link';

// Иконки можно будет заменить на реальные из heroicons
const SidebarLink = ({ href, label }: { href: string; label: string }) => (
    <Link href={href} className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg hover:bg-gray-100">
        {label}
    </Link>
);

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div>
            <aside className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0">
                <div className="h-full px-3 py-4 overflow-y-auto bg-gray-50">
                    <Link href="/dashboard" className="flex items-center pl-2.5 mb-5">
                        <span className="self-center text-xl font-semibold whitespace-nowrap">Discipline AI</span>
                    </Link>
                    <ul className="space-y-2">
                        <li>
                            <SidebarLink href="/dashboard" label="Дашборд" />
                        </li>
                        <li>
                            <SidebarLink href="/calendar" label="Календарь" />
                        </li>
                        <li>
                            <SidebarLink href="/agents" label="AI Агенты" />
                        </li>
                        <li>
                            <SidebarLink href="/settings" label="Настройки" />
                        </li>
                    </ul>
                </div>
            </aside>

            <main className="p-4 sm:ml-64">
                <div className="p-4 border-2 border-gray-200 border-dashed rounded-lg">
                    {children}
                </div>
            </main>
        </div>
    );
} 