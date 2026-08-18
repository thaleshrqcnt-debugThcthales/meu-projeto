import type { Metadata } from "next";
import { ExploreMore, SiteFooter, SiteHeader } from "../site-chrome";

export const metadata: Metadata = {
  title: "Metodologia reutilizável",
  description: "Método do acervo NHANDEREKO para documentar procedência, acessibilidade, fontes e lacunas sem transformar hipótese em certeza.",
};

const steps = [
  ["Identificar", "Registrar o que é observável: tipo de objeto, material, dimensões informadas, imagens, documentação de compra e povo indicado pela fonte."],
  ["Documentar", "Separar procedência comprovada, atribuição comercial, autoria individual, território e vocabulário linguístico. O que não estiver confirmado permanece marcado como pendência."],
  ["Tornar acessível", "Produzir audiodescrição, transcrição textual, navegação por teclado, contraste, estrutura semântica e recursos de Libras, mantendo equivalência de informação entre formatos."],
  ["Publicar com transparência", "Exibir fonte, nível de confirmação, curadoria e referências. Corrigir a ficha quando surgir evidência melhor, sem apagar o histórico de cautela documental."],
] as const;

export default function MethodPage() {
  return (
    <>
      <a className="skip-link" href="#conteudo">Ir para o conteúdo</a>
      <SiteHeader returnLabel="Início" returnHref="/" />
      <main id="conteudo" className="internal-page">
        <header className="internal-hero">
          <p className="eyebrow">Método aberto</p>
          <h1>Uma ficha é também um registro do que ainda não sabemos.</h1>
          <p>Esta metodologia pode ser reutilizada por exposições educativas que precisem combinar cultura material, pesquisa, acessibilidade e transparência de procedência.</p>
        </header>

        <section className="method-grid" aria-label="Etapas da metodologia">
          {steps.map(([title, text]) => (
            <article className="method-card" key={title}>
              <p className="section-kicker">Etapa</p>
              <h2>{title}</h2>
              <p>{text}</p>
            </article>
          ))}
        </section>

        <section className="text-panel method-principle" aria-labelledby="regra-central">
          <p className="section-kicker">Regra central</p>
          <h2 id="regra-central">Não completar uma lacuna com uma afirmação bonita.</h2>
          <p>Se um termo na língua de origem não foi confirmado, a ficha diz isso. Se a origem vem apenas de anúncio comercial, a procedência é qualificada. Se uma interpretação de grafismo, uso ritual ou função social não está sustentada por fonte adequada, ela não é publicada como fato.</p>
        </section>

        <section className="text-panel" aria-labelledby="camadas">
          <p className="section-kicker">Estrutura recomendada</p>
          <h2 id="camadas">Camadas mínimas de uma ficha</h2>
          <ul className="principle-list">
            <li>Nome público do objeto e, quando confirmado, nome na língua de origem.</li>
            <li>Povo produtor ou povo indicado pela fonte, com a diferença explicitada.</li>
            <li>Descrição visual objetiva e audiodescrição com transcrição.</li>
            <li>Procedência, tipo de autorização/aquisição e nível de confirmação.</li>
            <li>Referências culturais e institucionais consultáveis.</li>
            <li>Recursos de acessibilidade equivalentes e limitações declaradas.</li>
          </ul>
        </section>
      </main>
      <ExploreMore links={[
        { href: "/#artefatos", title: "Acervo", desc: "Sete peças de seis povos com fichas acessíveis e documentação transparente." },
        { href: "/atlas", title: "Atlas dos Povos", desc: "Mapa de referências geográficas das comunidades representadas no acervo." },
        { href: "/sobre", title: "Sobre", desc: "Equipe, curadoria indígena e princípios do projeto." },
      ]} />
      <SiteFooter />
    </>
  );
}
