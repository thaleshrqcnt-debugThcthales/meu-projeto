import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { artifacts, getArtifact } from "../../artifacts";

export function generateStaticParams() { return artifacts.map(({ slug }) => ({ slug })); }

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const artifact = getArtifact((await params).slug);
  return artifact ? { title: `Modo exposição — ${artifact.name}`, robots: { index: false, follow: true } } : { title: "Modo exposição" };
}

export default async function ExhibitionPage({ params }: Props) {
  const artifact = getArtifact((await params).slug);
  if (!artifact) notFound();
  return (
    <main className="exhibition-page">
      <a className="skip-link" href="#exhibition-content">Ir para o conteúdo</a>
      <header className="exhibition-topbar"><Link href={`/artefatos/${artifact.slug}`}>← Sair do modo exposição</Link><span>NHANDEREKO</span></header>
      <div id="exhibition-content" className="exhibition-layout">
        <div className="exhibition-image"><img src={artifact.image} alt={artifact.imageAlt}/></div>
        <section className="exhibition-content">
          <p className="artifact-type">{artifact.type}</p>
          <h1>{artifact.name}</h1>
          <p className="origin-name">{artifact.originalName}</p>
          <p className="artifact-people">{artifact.people}</p>
          <p>{artifact.visualDescription}</p>
          {artifact.audio ? <div className="audio-block"><span>{artifact.slug === "zunidor" ? "Ouça a audiodescrição e o som do zunidor" : "Ouça a audiodescrição"}</span><audio controls preload="metadata"><source src={artifact.audio} type="audio/mpeg"/></audio></div> : null}
          <details className="transcript"><summary>Ler transcrição completa</summary><div>{artifact.transcript.map((p) => <p key={p}>{p}</p>)}</div></details>
          {artifact.librasVideo ? <div className="exhibition-video"><video controls preload="metadata"><source src={artifact.librasVideo} type="video/mp4"/></video><p>{artifact.librasStatus}</p></div> : <p className="exhibition-warning"><strong>Vídeo dedicado em revisão.</strong> O material recebido não será exibido enquanto houver identificação cultural contraditória.</p>}
        </section>
      </div>
    </main>
  );
}
