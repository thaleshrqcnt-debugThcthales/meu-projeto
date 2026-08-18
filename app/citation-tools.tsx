"use client";

import { useState } from "react";

export default function CitationTools({ name, slug }: { name: string; slug: string }) {
  const [style, setStyle] = useState<"ABNT" | "APA">("ABNT");
  const [copied, setCopied] = useState(false);
  const url = `https://nhandereko-acervo-oficial.netlify.app/artefatos/${slug}`;
  const abnt = `PROJETO NHANDEREKO. ${name}: ficha digital do acervo. Curadoria indígena: Juá Jacarandá Kixelô Kariri. Produção executiva: Thales Henrique Cunto e Fabrício de Assis Vicentin. São José do Rio Preto: SMC-PNAB, 2026. Disponível em: ${url}.`;
  const apa = `Projeto NHANDEREKO. (2026). ${name} [Ficha digital do acervo]. Curadoria indígena: Juá Jacarandá Kixelô Kariri. Produção executiva: T. H. Cunto & F. A. Vicentin. SMC-PNAB. ${url}`;
  const citation = style === "ABNT" ? abnt : apa;
  const whatsapp = `https://api.whatsapp.com/send?text=${encodeURIComponent(`${name} — Acervo NHANDEREKO: ${url}`)}`;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(citation);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2200);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="citation-tools">
      <div className="citation-tabs" role="group" aria-label="Estilo de citação">
        <button type="button" aria-pressed={style === "ABNT"} onClick={() => setStyle("ABNT")}>ABNT</button>
        <button type="button" aria-pressed={style === "APA"} onClick={() => setStyle("APA")}>APA</button>
      </div>
      <p className="citation-text">{citation}</p>
      <div className="citation-actions">
        <button className="secondary-button" type="button" onClick={copy}>{copied ? "Citação copiada" : "Copiar citação"}</button>
        <a className="whatsapp-link" href={whatsapp} target="_blank" rel="noreferrer">Compartilhar no WhatsApp ↗</a>
      </div>
    </div>
  );
}
