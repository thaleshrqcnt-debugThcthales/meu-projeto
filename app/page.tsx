import type { Metadata } from "next";
import { artifacts } from "./artifacts";
import ArtifactGrid from "./artifact-grid";
import { BrandMark, SiteFooter, SiteHeader } from "./site-chrome";

export const metadata: Metadata = {
  title: { absolute: "NHANDEREKO — Acervo digital acessível" },
  description: "Sete peças relacionadas a seis povos, com níveis de documentação claramente indicados.",
  openGraph: {
    title: "NHANDEREKO — Acervo digital acessível",
    description: "Sete peças relacionadas a seis povos, com níveis de documentação claramente indicados.",
    type: "website",
    images: [{ url: "/media/ritxoko.jpg", alt: "Ritxòkò do acervo NHANDEREKO" }],
  },
  twitter: { card: "summary_large_image", title: "NHANDEREKO — Acervo digital acessível", description: "Sete peças relacionadas a seis povos, com níveis de documentação claramente indicados.", images: ["/media/ritxoko.jpg"] },
};

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#artefatos">Ir para os artefatos</a>
      <SiteHeader />
      <header className="hero compact-hero">
        <p className="eyebrow">Acervo acessível · Mostra de Artefatos</p>
        <h1 className="sr-only">NHANDEREKO</h1>
        <BrandMark hero />
        <p className="hero-copy">Sete peças relacionadas a seis povos, com níveis de documentação claramente indicados.</p>
        <a className="hero-action" href="#artefatos">Explorar as 7 peças <span aria-hidden="true">↓</span></a>
      </header>

      <main id="artefatos" className="collection compact-collection">
        <div className="section-heading">
          <div><p className="section-kicker">Exposição</p><h2>Peças do acervo</h2></div>
          <p>Cada ficha apresenta descrição visual, procedência, contexto e os recursos de acessibilidade disponíveis para aquela peça.</p>
        </div>
        <ArtifactGrid artifacts={artifacts} />
      </main>
      <SiteFooter />
    </>
  );
}
