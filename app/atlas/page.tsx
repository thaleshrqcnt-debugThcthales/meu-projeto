import type { Metadata } from "next";
import AtlasClient from "./atlas-client";
import { SiteFooter, SiteHeader } from "../site-chrome";

export const metadata: Metadata = {
  title: "Atlas dos Povos",
  description: "Mapa acessível e interativo de referências geográficas relacionadas aos povos e às peças do acervo NHANDEREKO.",
};

export default function AtlasPage() {
  return (
    <>
      <a className="skip-link" href="#conteudo">Ir para o conteúdo</a>
      <SiteHeader returnLabel="Início" returnHref="/" />
      <main id="conteudo" className="internal-page atlas-page">
        <header className="internal-hero">
          <p className="eyebrow">Atlas dos Povos</p>
          <h1>Localizar sem reduzir um povo a um ponto.</h1>
          <p>O mapa oferece referências geográficas para orientar a visita. Os pontos são aproximados e não substituem cartografia oficial, limites de Terras Indígenas ou as próprias formas indígenas de compreender território.</p>
        </header>
        <AtlasClient />
        <section className="text-panel atlas-transparency" aria-labelledby="transparencia-atlas">
          <p className="section-kicker">Transparência cartográfica</p>
          <h2 id="transparencia-atlas">O que este mapa representa — e o que não representa</h2>
          <p>O contorno nacional é usado somente como base de orientação e os marcadores indicam áreas de referência. Não foram desenhados polígonos de Terras Indígenas à mão e não há escala métrica simulada. As cores diferenciam apenas regiões cartográficas de referência usadas neste mapa esquemático; não classificam culturalmente os povos e não substituem a delimitação oficial de biomas ou territórios.</p>
          <p>Para limites territoriais oficiais, consulte a <a href="https://www.gov.br/funai/pt-br/atuacao/terras-indigenas" target="_blank" rel="noreferrer">Funai ↗</a>. A base cartográfica oficial brasileira pode ser consultada nas <a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html" target="_blank" rel="noreferrer">Malhas Territoriais do IBGE ↗</a>.</p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
