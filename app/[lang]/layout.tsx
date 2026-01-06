import type { Metadata } from "next";
import { Noto_Sans_JP, Outfit } from "next/font/google"; // Updated fonts
import "../globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  display: 'swap',
});

const notoSansJP = Noto_Sans_JP({
  variable: "--font-noto-sans-jp",
  subsets: ["latin"],
  display: 'swap',
});

export const metadata: Metadata = {
  title: "Wuxu | Full-Stack Developer",
  description: "Personal website of a software developer.",
};

import { LanguageSwitcher } from "@/components/LanguageSwitcher";

export default async function RootLayout({
  children,
  params
}: Readonly<{
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}>) {
  const { lang } = await params;
  return (
    <html lang={lang}>
      <body
        className={`${outfit.variable} ${notoSansJP.variable} font-sans antialiased text-foreground bg-background`}
      >
        <LanguageSwitcher currentLang={lang} />
        {children}
      </body>
    </html>
  );
}
