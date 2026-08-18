"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { Artifact } from "./artifacts";
import { peopleFilters } from "./artifacts";

export default function ArtifactGrid({ artifacts }: { artifacts: Artifact[] }) {
  const [filter, setFilter] = useState<(typeof peopleFilters)[number]>("Todos");
  const visible = useMemo(() => filter === "Todos" ? artifacts : artifacts.filter((artifact) => artifact.peopleFilter === filter), [artifacts, filter]);

  return (
    <>
      <div className="filter-panel" aria-label="Filtrar acervo por povo">
        <label htmlFor="people-filter">Filtrar por povo</label>
        <select id="people-filter" value={filter} onChange={(event) => setFilter(event.target.value as (typeof peopleFilters)[number])}>
          {peopleFilters.map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
        <div className="filter-buttons" aria-label="Filtros rápidos">
          {peopleFilters.map((item) => (
            <button key={item} type="button" aria-pressed={filter === item} onClick={() => setFilter(item)}>{item}</button>
          ))}
        </div>
        <p aria-live="polite">{filter === "Todos" ? "Exibindo todas as peças do acervo." : `Exibindo peças relacionadas a ${filter}.`}</p>
      </div>

      <div className="artifact-list compact-list">
        {visible.map((artifact) => (
          <article className="artifact-card compact-card" key={artifact.slug} id={artifact.slug}>
            <div className="artifact-image-wrap compact-image-wrap">
              <picture>
                <source srcSet={artifact.image.replace(".jpg", ".webp")} type="image/webp" />
                <img src={artifact.image} alt={artifact.imageAlt} width={artifact.imageWidth} height={artifact.imageHeight} loading="lazy" decoding="async" />
              </picture>
            </div>
            <div className="artifact-content compact-content">
              <p className="artifact-type">{artifact.type}</p>
              <h3>{artifact.name}</h3>
              <p className="artifact-people">{artifact.people}</p>
              <p className={`provenance-badge ${artifact.badgeTone}`}>{artifact.badgeTone === "confirmed" ? "✓" : "i"} {artifact.badge}</p>
              <Link className="primary-link" href={`/artefatos/${artifact.slug}`}>Conhecer a peça</Link>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}
