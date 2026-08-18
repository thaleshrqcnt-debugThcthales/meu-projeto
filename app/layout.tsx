import type { Metadata, Viewport } from "next";
import "./globals.css";
import LibrasWidget from "./libras-widget";

export const metadata: Metadata = {
  metadataBase: new URL("https://acervonhandereko.vercel.app"),
  title: { default: "NHANDEREKO — Acervo digital acessível", template: "%s | NHANDEREKO" },
  description: "Acervo digital acessível da Mostra de Artefatos do projeto NHANDEREKO.",
  icons: { icon: "/favicon.svg" },
};

export const viewport: Viewport = { colorScheme: "dark", themeColor: "#0f0b07" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>
        {children}
        <LibrasWidget />
      </body>
    </html>
  );
}
