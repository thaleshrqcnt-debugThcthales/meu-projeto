import type { Metadata } from "next";
import Link from "next/link";
import { ExploreMore, SiteFooter, SiteHeader } from "../site-chrome";

export const metadata: Metadata = {
  title: "Sobre a obra",
  description: "Contexto, responsabilidade cultural, equipe e critérios documentais do acervo digital NHANDEREKO.",
};

export default function AboutPage() {
  return (
    <>
      <a className="skip-link" href="#conteudo">Ir para o conteúdo</a>
      <SiteHeader returnLabel="Início" returnHref="/" />
      <main id="conteudo" className="internal-page">
        <header className="internal-hero">
          <p className="eyebrow">Sobre o acervo</p>
          <h1>Uma exposição que documenta também as suas incertezas.</h1>
          <p>NHANDEREKO — Ler, Brincar e Pertencer reúne artefatos, recursos acessíveis e referências de pesquisa em uma experiência educativa. As fichas não tratam procedência comercial, hipótese linguística ou interpretação externa como certeza cultural.</p>
        </header>

        <div className="content-stack">
          <section className="text-panel" aria-labelledby="principios">
            <p className="section-kicker">Princípios</p>
            <h2 id="principios">Como o acervo é apresentado</h2>
            <ul className="principle-list">
              <li><strong>Separar aparência de significado.</strong> A audiodescrição relata características observáveis; significados culturais só entram quando há fonte e validação.</li>
              <li><strong>Mostrar o nível de documentação.</strong> Peças com procedência parcial permanecem identificadas como tal.</li>
              <li><strong>Não preencher lacunas por suposição.</strong> Nomes nas línguas de origem que ainda não foram confirmados continuam marcados como “em verificação”.</li>
              <li><strong>Priorizar fontes indígenas e institucionais.</strong> Quando há divergência de grafia ou classificação, a ficha explicita o critério adotado.</li>
            </ul>
          </section>

          <section id="curadoria" className="text-panel curator-panel" aria-labelledby="curadoria-title">
            <p className="section-kicker">Curadoria indígena</p>
            <h2 id="curadoria-title">Juá Jacarandá Kixelô Kariri</h2>
            <p>Juá acompanha a responsabilidade cultural do acervo, a forma de nomear povos e objetos e a manutenção pública de informações ainda em verificação. A presença da curadoria não é usada para transformar dados comerciais incompletos em atribuições definitivas.</p>
            <p>Nas fichas, a expressão <strong>“em verificação com a curadoria indígena”</strong> é deliberada: ela sinaliza que a informação ainda não deve ser publicada como vocabulário confirmado.</p>
          </section>

          <section className="text-panel" aria-labelledby="procedencia">
            <p className="section-kicker">Transparência</p>
            <h2 id="procedencia">Procedência e documentação</h2>
            <p>O acervo combina peças com povo produtor identificado e itens cuja documentação comercial ainda não permite confirmar autoria individual ou vínculo comunitário direto. O caso do Arco e Flecha é mantido como <strong>procedência parcial</strong> justamente para que o visitante veja a limitação do registro.</p>
            <Link className="text-link" href="/#artefatos">Consultar as fichas do acervo →</Link>
          </section>

          <section className="text-panel" aria-labelledby="equipe">
            <p className="section-kicker">Realização</p>
            <h2 id="equipe">Equipe e responsabilidades</h2>
            <dl className="documentation-list team-list">
              <div><dt>Proponente</dt><dd>Wemerson Cunto</dd></div>
              <div><dt>Produção executiva</dt><dd>Thales Henrique Cunto e Fabrício de Assis Vicentin</dd></div>
              <div><dt>Curadoria indígena</dt><dd>Juá Jacarandá Kixelô Kariri</dd></div>
              <div><dt>Acessibilidade</dt><dd>Lucas Horas / Minutos com Horas</dd></div>
              <div><dt>Libras</dt><dd>Bárbara Libras</dd></div>
              <div><dt>Realização</dt><dd>Chamamento Público nº 02/2026-SMC-PNAB · São José do Rio Preto — SP · 2026</dd></div>
            </dl>
          </section>
        </div>
      </main>
      <ExploreMore links={[
        { href: "/#artefatos", title: "Acervo", desc: "Sete peças de seis povos com fichas acessíveis e documentação transparente." },
        { href: "/atlas", title: "Atlas dos Povos", desc: "Mapa de referências geográficas das comunidades representadas no acervo." },
        { href: "/acessibilidade", title: "Acessibilidade", desc: "Declaração de acessibilidade, recursos disponíveis e limitações conhecidas." },
      ]} />
      <SiteFooter />
    </>
  );
}
