import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GitHub PR Test Coverage Assistant",
  description: "Monitor and improve test coverage in your GitHub pull requests",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-gray-50 dark:bg-gray-900`} suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
