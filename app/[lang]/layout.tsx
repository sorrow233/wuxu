import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/app/globals.css";

export default async function LangLayout({
    children,
    params,
}: Readonly<{
    children: React.ReactNode;
    params: Promise<{ lang: string }>;
}>) {
    const { lang } = await params;
    return (
        <div lang={lang}>
            {children}
        </div>
    );
}
