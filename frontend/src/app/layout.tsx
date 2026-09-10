import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aegis AI Auditor | Secure LLM Workflows",
  description: "AI security governance and vulnerability scanning for LLM workflows and agentic pipelines.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
