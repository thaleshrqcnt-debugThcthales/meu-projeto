import type { Metadata } from "next";
import { artifacts } from "./artifacts";
import ArtifactGrid from "./artifact-grid";
import { SiteFooter, SiteHeader } from "./site-chrome";

export const metadata: Metadata = {
  title: { absolute: "NHANDEREKO — Acervo digital acessível" },
  description: "Acervo digital de artefatos indígenas com audiodescrição, Libras, procedência documentada, referências culturais e fichas acessíveis.",
  openGraph: {
    title: "NHANDEREKO — Acervo digital acessível",
    description: "Mostra de Artefatos do projeto NHANDEREKO — Ler, Brincar e Pertencer.",
    type: "website",
    images: [{ url: "/media/ritxoko.jpg", alt: "Ritxòkò do acervo NHANDEREKO" }],
  },
  twitter: { card: "summary_large_image", title: "NHANDEREKO — Acervo digital acessível", description: "Mostra de Artefatos do projeto NHANDEREKO.", images: ["/media/ritxoko.jpg"] },
};

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#artefatos">Ir para o acervo</a>
      <SiteHeader />
      <main>
        <header className="hero compact-hero">
          <p className="eyebrow">Acervo acessível</p>
          <h1>NHAN<em>DEREKO</em></h1>
          <div className="hero-signature" aria-label="NHANDEREKO — Ler, Brincar, Pertencer">
            <strong>NHANDEREKO</strong><span>Ler · Brincar · Pertencer</span>
          </div>
          <p className="hero-copy">Peças relacionadas a diferentes povos, com níveis de documentação claramente indicados. Explore cada ficha para ouvir, ler, consultar procedência, território e os recursos de acessibilidade disponíveis.</p>
          <a className="hero-action" href="#artefatos">Explorar o acervo <span aria-hidden="true">↓</span></a>
        </header>

        <section id="artefatos" className="collection compact-collection" aria-labelledby="acervo-title">
          <div className="section-heading">
            <div><p className="section-kicker">Exposição</p><h2 id="acervo-title">Peças do acervo</h2></div>
            <p>Cada ficha separa descrição visual, contexto, procedência e estado de confirmação. Informações ainda não validadas permanecem visíveis como pendências.</p>
          </div>
          <ArtifactGrid artifacts={artifacts} />
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
