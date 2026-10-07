import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "APSA-2026 · Autonomous Money Hunter Operations Desk",
  description:
    "Operator monitoring & verification workbench for the APSA-2026 Autonomous Profit & Sweep Architecture — 4 receive-only payout rails, x402 payment protocol, SentinelShield audit service, and a 12-test verification suite.",
  keywords: [
    "APSA-2026",
    "x402",
    "Base L2",
    "USDC",
    "SentinelShield",
    "autonomous agent",
    "receive-only wallet",
    "EIP-712",
    "ERC-3009",
  ],
  authors: [{ name: "APSA-2026 Protocol" }],
  icons: {
    icon: "https://z-cdn.chatglm.cn/z-ai/static/logo.svg",
  },
  openGraph: {
    title: "APSA-2026 · Autonomous Money Hunter",
    description: "Autonomous Profit & Sweep Architecture — operator operations desk",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "APSA-2026 · Autonomous Money Hunter",
    description: "Autonomous Profit & Sweep Architecture — operator operations desk",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Toaster />
      </body>
    </html>
  );
}
