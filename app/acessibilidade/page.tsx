import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "../site-chrome";

export const metadata: Metadata = {
  title: "Acessibilidade",
  description: "Declaração de acessibilidade do acervo digital NHANDEREKO, recursos disponíveis, limitações conhecidas e referências adotadas.",
};

export default function AccessibilityPage() {
  return (
    <>
      <a className="skip-link" href="#conteudo">Ir para o conteúdo</a>
      <SiteHeader returnLabel="Início" returnHref="/" />
      <main id="conteudo" className="accessibility-page internal-page">
        <header className="accessibility-header internal-hero">
          <p className="eyebrow">Declaração de acessibilidade</p>
          <h1>Acesso é parte da obra.</h1>
          <p>O acervo foi estruturado para que informação visual, sonora e documental possa ser percorrida por diferentes pessoas, dispositivos e tecnologias assistivas.</p>
        </header>

        <div className="accessibility-sections content-stack">
          <section className="text-panel standards-panel" aria-labelledby="compromisso">
            <p className="section-kicker">Compromisso</p>
            <h2 id="compromisso">Meta técnica e editorial</h2>
            <p>O projeto adota como referência a <strong>WCAG 2.2 nível AA</strong>, o eMAG e a ABNT NBR 17225:2025. Esses referenciais orientam contraste, navegação por teclado, foco visível, semântica, alternativas textuais, mídia e organização do conteúdo.</p>
          </section>

          <section className="text-panel" aria-labelledby="recursos">
            <p className="section-kicker">Recursos disponíveis</p>
            <h2 id="recursos">O que o site oferece</h2>
            <ul>
              <li>Link de salto para o conteúdo principal e navegação por teclado.</li>
              <li>Foco visível e controles com rótulos compreensíveis.</li>
              <li>Textos alternativos nas imagens do acervo.</li>
              <li>Audiodescrição com transcrição textual nas fichas.</li>
              <li>Vídeos dedicados por avatar quando disponíveis, acompanhados de aviso de validação profissional.</li>
              <li>VLibras oficial como recurso automático complementar.</li>
              <li>Conteúdo responsivo para celular, computador e uso em exposição.</li>
              <li>Compatibilidade com preferência de redução de movimento e maior contraste.</li>
            </ul>
          </section>

          <section className="text-panel" aria-labelledby="libras-limitacao">
            <p className="section-kicker">Libras</p>
            <h2 id="libras-limitacao">Automação não substitui interpretação humana</h2>
            <p>O VLibras e os vídeos por avatar são recursos automáticos. Eles ampliam caminhos de acesso, mas podem apresentar limitações linguísticas e não são tratados como equivalentes à interpretação humana. Os vídeos dedicados permanecem identificados como versões em validação profissional.</p>
            <p>No caso do Arco e Flecha, um vídeo recebido foi mantido fora do ar porque apresentava identificação cultural incompatível com a documentação da ficha. A prioridade é não publicar uma tradução visual contraditória.</p>
          </section>

          <section className="text-panel" aria-labelledby="autonomia">
            <p className="section-kicker">Autonomia</p>
            <h2 id="autonomia">Sem interrupções automáticas</h2>
            <p>Nenhum aviso ou modal de atualização, áudio, vídeo ou janela promocional é disparado automaticamente sobre o conteúdo. Mídias só começam quando a pessoa aciona o respectivo controle.</p>
          </section>

          <section className="text-panel" aria-labelledby="responsaveis">
            <p className="section-kicker">Responsáveis</p>
            <h2 id="responsaveis">Acompanhamento</h2>
            <p><strong>Acessibilidade:</strong> Lucas Horas / Minutos com Horas.</p>
            <p><strong>Tradução e interpretação em Libras:</strong> Bárbara Libras.</p>
            <p><strong>Curadoria indígena:</strong> Juá Jacarandá Kixelô Kariri.</p>
          </section>

          <section className="text-panel" aria-labelledby="referencias">
            <p className="section-kicker">Referências</p>
            <h2 id="referencias">Padrões adotados</h2>
            <ul>
              <li><a href="https://www.w3.org/WAI/WCAG22/quickref/" target="_blank" rel="noreferrer">WCAG 2.2 — W3C ↗</a></li>
              <li><a href="https://emag.governoeletronico.gov.br/" target="_blank" rel="noreferrer">eMAG — Modelo de Acessibilidade em Governo Eletrônico ↗</a></li>
              <li><a href="https://bibliotecadigital.anvisa.gov.br/jspui/handle/anvisa/20335" target="_blank" rel="noreferrer">ABNT NBR 17225:2025 ↗</a></li>
              <li><a href="https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/vlibras" target="_blank" rel="noreferrer">VLibras — Governo Digital ↗</a></li>
            </ul>
            <p className="review-date">Última revisão desta declaração: 15 de agosto de 2026.</p>
          </section>
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
