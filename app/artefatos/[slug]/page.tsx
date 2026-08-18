import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { artifacts, getArtifact } from "../../artifacts";
import CitationTools from "../../citation-tools";
import LibrasButton from "../../libras-button";
import { SiteFooter, SiteHeader } from "../../site-chrome";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return artifacts.map(({ slug }) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const artifact = getArtifact((await params).slug);
  if (!artifact) return { title: "Artefato não encontrado" };
  const title = artifact.titleName ?? artifact.name;
  return {
    title,
    description: artifact.metaDescription,
    alternates: { canonical: `/artefatos/${artifact.slug}` },
    openGraph: {
      title: `${title} | NHANDEREKO`,
      description: artifact.metaDescription,
      type: "article",
      url: `/artefatos/${artifact.slug}`,
      images: [{ url: artifact.image, alt: artifact.imageAlt }],
    },
    twitter: { card: "summary_large_image", title: `${title} | NHANDEREKO`, description: artifact.metaDescription, images: [artifact.image] },
  };
}

export default async function ArtifactPage({ params }: Props) {
  const artifact = getArtifact((await params).slug);
  if (!artifact) notFound();
  const currentIndex = artifacts.findIndex(({ slug }) => slug === artifact.slug);
  const previousArtifact = currentIndex > 0 ? artifacts[currentIndex - 1] : undefined;
  const nextArtifact = currentIndex < artifacts.length - 1 ? artifacts[currentIndex + 1] : undefined;

  return (
    <>
      <a className="skip-link" href="#conteudo">Ir para o conteúdo da peça</a>
      <SiteHeader returnLabel="Voltar ao acervo" returnHref="/#artefatos" />
      <main id="conteudo" className="detail-page">
        <p className="collection-breadcrumb">Acervo · {artifact.name}</p>

        <article className="detail-card">
          <div className="detail-image">
            <picture>
              <source srcSet={artifact.image.replace(".jpg", ".webp")} type="image/webp" />
              <img src={artifact.image} alt={artifact.imageAlt} width={artifact.imageWidth} height={artifact.imageHeight} loading="eager" fetchPriority="high" decoding="async" />
            </picture>
          </div>
          <div className="detail-content">
            <p className="artifact-type">{artifact.type}</p>
            <h1>{artifact.name}</h1>
            <p className="origin-name">{artifact.originalName}</p>
            <p className="artifact-people">{artifact.people}</p>
            <p className={`provenance-badge ${artifact.badgeTone}`}>{artifact.badgeTone === "confirmed" ? "✓" : "i"} {artifact.badge}</p>
            <p className="detail-description">{artifact.description}</p>

            {artifact.audio ? (
              <section className="audio-block detail-audio" aria-labelledby={`audio-${artifact.slug}`}>
                <span id={`audio-${artifact.slug}`}>{artifact.slug === "zunidor" ? "Ouça a audiodescrição e o som do zunidor" : "Ouça a audiodescrição"}</span>
                <audio controls preload="metadata" aria-label={artifact.slug === "zunidor" ? `Audiodescrição de ${artifact.name} seguida do registro sonoro do movimento` : `Audiodescrição de ${artifact.name}`}>
                  <source src={artifact.audio} type="audio/mpeg" />
                  Seu navegador não consegue reproduzir este áudio.
                </audio>
                <details className="transcript">
                  <summary>Ler transcrição completa do áudio</summary>
                  <div>{artifact.transcript.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}</div>
                </details>
              </section>
            ) : null}

            <Link className="exhibition-link" href={`/exposicao/${artifact.slug}`}>Abrir modo exposição ↗</Link>
          </div>
        </article>

        <section className="access-media-panel" aria-labelledby="libras-piece">
          <div className="section-heading compact-heading">
            <div><p className="section-kicker">Acessibilidade</p><h2 id="libras-piece">Conteúdo em Libras</h2></div>
            <p>O VLibras global permanece disponível em todas as páginas. Os vídeos dedicados são versões por avatar e continuam sujeitos à revisão profissional.</p>
          </div>
          {artifact.librasVideo ? (
            <div className="libras-video-wrap">
              <video controls preload="metadata" aria-label={`Vídeo em Libras sobre ${artifact.name}`}>
                <source src={artifact.librasVideo} type="video/mp4" />
                Seu navegador não consegue reproduzir este vídeo. Use a transcrição completa disponível nesta página.
              </video>
              <p className="libras-status">{artifact.librasStatus}</p>
            </div>
          ) : (
            <div className="libras-review-note">
              <strong>Vídeo dedicado em revisão.</strong>
              <p>O material recebido para Arco e Flecha contém uma identificação visual incompatível com a procedência registrada nesta ficha. Para não publicar uma atribuição cultural contraditória, o vídeo permanece fora do ar até correção e validação por profissional de Libras.</p>
            </div>
          )}
          <LibrasButton />
          <p className="libras-note">O botão abre o VLibras oficial, recurso automático que requer conexão com a internet e não substitui interpretação humana.</p>
        </section>

        <div className="detail-grid">
          <section className="text-panel" aria-labelledby="descricao-visual">
            <p className="section-kicker">Descrição objetiva</p>
            <h2 id="descricao-visual">Como a peça aparece</h2>
            <p>{artifact.visualDescription}</p>
          </section>
          <section className="text-panel" aria-labelledby="dados-peca">
            <p className="section-kicker">Contexto e dados da peça</p>
            <h2 id="dados-peca">Características documentadas</h2>
            <ul>{artifact.details.map((detail) => <li key={detail}>{detail}</li>)}</ul>
          </section>
        </div>

        <section className="text-panel documentation-panel" aria-labelledby="documentacao">
          <p className="section-kicker">Procedência e referências</p>
          <h2 id="documentacao">Nível de confirmação e fontes</h2>
          <dl className="documentation-list">
            <div><dt>Fonte</dt><dd>{artifact.source}</dd></div>
            <div><dt>Procedência documentada</dt><dd>{artifact.provenance}</dd></div>
            <div><dt>Tipo de autorização</dt><dd>{artifact.authorization}</dd></div>
            <div><dt>Referências culturais</dt><dd>{artifact.references.map((reference, index) => <span key={reference.href}>{index > 0 ? " · " : ""}<a href={reference.href} target="_blank" rel="noreferrer">{reference.label} ↗</a></span>)}</dd></div>
          </dl>
        </section>

        <section className="text-panel curator-panel" aria-labelledby="curadoria">
          <p className="section-kicker">Responsabilidade cultural</p>
          <h2 id="curadoria">Ficha acompanhada pela curadoria indígena</h2>
          <p><strong>Juá Jacarandá Kixelô Kariri</strong> acompanha a identificação cultural e mantém visíveis os dados ainda em verificação. A curadoria não transforma atribuições comerciais, hipóteses linguísticas ou lacunas documentais em certezas.</p>
          <Link className="text-link" href="/sobre#curadoria">Conheça a responsabilidade cultural e a equipe →</Link>
        </section>

        <section className="text-panel citation-panel" aria-labelledby="citacao">
          <p className="section-kicker">Pesquisa, referência e circulação</p>
          <h2 id="citacao">Como citar e compartilhar esta ficha</h2>
          <CitationTools name={artifact.name} slug={artifact.slug} />
        </section>

        <nav className="artifact-pagination" aria-label="Navegação entre peças">
          {previousArtifact ? <Link href={`/artefatos/${previousArtifact.slug}`}><span>← Peça anterior</span><strong>{previousArtifact.name}</strong></Link> : <Link href="/#artefatos"><span>Início do percurso</span><strong>Voltar ao acervo</strong></Link>}
          {nextArtifact ? <Link href={`/artefatos/${nextArtifact.slug}`} className="pagination-next"><span>Próxima peça →</span><strong>{nextArtifact.name}</strong></Link> : <Link href="/#artefatos" className="pagination-next"><span>Fim do percurso</span><strong>Voltar ao acervo</strong></Link>}
        </nav>
      </main>
      <SiteFooter />
    </>
  );
}
