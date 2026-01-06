import type { Metadata } from "next";
import { Noto_Sans_JP, Outfit } from "next/font/google"; // Updated fonts
import "./globals.css";

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
  title: "Tokyo Lifestyler | Full-Stack Developer",
  description: "Personal website of a Tokyo-based software developer.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${outfit.variable} ${notoSansJP.variable} font-sans antialiased text-foreground bg-background`}
      >
        {children}
      </body>
    </html>
  );
}
