"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { Artifact } from "./artifacts";
import { peopleFilters } from "./artifacts";

export default function ArtifactGrid({ artifacts }: { artifacts: Artifact[] }) {
  const [filter, setFilter] = useState<(typeof peopleFilters)[number]>("Todos");
  const visible = useMemo(
    () => (filter === "Todos" ? artifacts : artifacts.filter((a) => a.peopleFilter === filter)),
    [artifacts, filter],
  );

  return (
    <>
      <div className="artifact-filters" aria-label="Filtrar peças por povo">
        <label htmlFor="mobile-people-filter">Filtrar por povo</label>
        <select
          id="mobile-people-filter"
          className="mobile-filter-select"
          value={filter}
          onChange={(e) => setFilter(e.target.value as (typeof peopleFilters)[number])}
        >
          {peopleFilters.map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
        <div className="filter-buttons">
          {peopleFilters.map((item) => (
            <button key={item} type="button" aria-pressed={filter === item} onClick={() => setFilter(item)}>
              {item}
            </button>
          ))}
        </div>
        <p className="sr-only" aria-live="polite" aria-atomic="true">
          {filter === "Todos" ? `Exibindo ${visible.length} peças de todos os povos.` : `Exibindo ${visible.length} peça${visible.length === 1 ? "" : "s"} do povo ${filter}.`}
        </p>
      </div>

      <div className="artifact-list compact-list">
        {visible.map((artifact, idx) => {
          const num = String(artifacts.indexOf(artifact) + 1).padStart(2, "0");
          return (
            <article className={`artifact-card compact-card artifact-${artifact.slug}`} key={artifact.slug} id={artifact.slug}>
              <div className="artifact-image-wrap compact-image-wrap">
                <span className="artifact-number" aria-hidden="true">{num}</span>
                <picture>
                  <source srcSet={artifact.image.replace(".jpg", ".webp")} type="image/webp" />
                  <img
                    src={artifact.image}
                    alt={artifact.imageAlt}
                    width={artifact.imageWidth}
                    height={artifact.imageHeight}
                    loading={idx === 0 ? "eager" : "lazy"}
                    fetchPriority={idx === 0 ? "high" : "auto"}
                    decoding="async"
                  />
                </picture>
              </div>
              <div className="artifact-content compact-content">
                <h3>{artifact.name}</h3>
                <p className="artifact-people">{artifact.people}</p>
                {artifact.badgeTone === "partial" && (
                  <p className="card-status card-status-partial">{artifact.badge}</p>
                )}
                <Link className="primary-link" href={`/artefatos/${artifact.slug}`}>Conhecer a peça</Link>
              </div>
            </article>
          );
        })}
      </div>
    </>
  );
}
