import Link from "next/link";

type HeaderProps = {
  returnLabel?: "Início" | "Voltar ao acervo";
  returnHref?: string;
};

export function BrandMark({ hero = false }: { hero?: boolean }) {
  return (
    <div className={`brand-mark${hero ? " brand-mark-hero" : ""}`} aria-label="NHANDEREKO — Ler, Brincar e Pertencer">
      <svg viewBox="0 0 92 92" role="img" aria-hidden="true">
        <circle cx="46" cy="46" r="41" className="brand-ring" />
        <path d="M23 61V31c9 1 17 5 23 12 6-7 14-11 23-12v30c-9 0-17 3-23 9-6-6-14-9-23-9Z" className="brand-book" />
        <path d="M46 43v27" className="brand-path" />
        <path d="M17 73c16-7 42-7 58 0" className="brand-river" />
      </svg>
      <span className="brand-word">
        <b>NHAN</b><em>DEREKO</em>
        <small>Ler · Brincar · Pertencer</small>
      </span>
    </div>
  );
}

export function SiteLogo() {
  return (
    <Link className="site-logo" href="/" aria-label="NHANDEREKO — página inicial">
      <span className="site-logo-name">NHAN<span>DEREKO</span></span>
      <span className="site-logo-tagline">Ler · Brincar · Pertencer</span>
    </Link>
  );
}

export function SiteHeader({ returnLabel, returnHref }: HeaderProps) {
  return (
    <header className="global-header">
      <div className="global-header-inner">
        <SiteLogo />
        <div className="global-nav-wrap">
          {returnLabel && returnHref ? <Link className="return-link" href={returnHref}>← {returnLabel}</Link> : null}
          <nav className="global-nav" aria-label="Navegação principal">
            <Link href="/#artefatos">Acervo</Link>
            <Link href="/atlas">Atlas</Link>
            <Link href="/metodologia">Metodologia</Link>
            <Link href="/sobre">Sobre</Link>
            <Link href="/acessibilidade">Acessibilidade</Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="footer-inner footer-compact">
        <Link href="/" aria-label="NHANDEREKO — página inicial">
          <BrandMark />
        </Link>
        <nav className="footer-links" aria-label="Navegação do rodapé">
          <Link href="/#artefatos">Acervo</Link>
          <Link href="/atlas">Atlas dos Povos</Link>
          <Link href="/metodologia">Metodologia</Link>
          <Link href="/sobre">Sobre</Link>
          <Link href="/acessibilidade">Acessibilidade</Link>
        </nav>
        <small className="footer-note">
          Projeto realizado pelo Chamamento Público nº 02/2026-SMC-PNAB · São José do Rio Preto — SP · 2026.{" "}
          <Link href="/sobre#equipe">Equipe e créditos →</Link>
        </small>
      </div>
    </footer>
  );
}

type ExploreLink = { href: string; title: string; desc: string };

export function ExploreMore({ links }: { links: ExploreLink[] }) {
  return (
    <section className="explore-more" aria-labelledby="explore-title">
      <p className="section-kicker" id="explore-title">Continue explorando</p>
      <div className="explore-grid">
        {links.map(({ href, title, desc }) => (
          <Link key={href} className="explore-card" href={href}>
            <strong>{title}</strong>
            <span>{desc}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}

export function MobileNav({ current }: { current?: string }) {
  const links = [
    { href: "/", label: "Acervo", icon: <path d="M4 5.5h16v13H4zM8 3v5M16 3v5" /> },
    { href: "/atlas", label: "Atlas", icon: <path d="m3 6 5-3 8 3 5-3v15l-5 3-8-3-5 3zM8 3v15M16 6v15" /> },
    { href: "/metodologia", label: "Método", icon: <path d="M5 4h14v16H5zM8 8h8M8 12h8M8 16h5" /> },
    { href: "/sobre", label: "Sobre", icon: <path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 11v6M12 7h.01" /> },
    { href: "/acessibilidade", label: "Acesso", icon: <path d="M12 4a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm-8 3h16M12 7v15M7 22l5-8 5 8" /> },
  ];
  return (
    <nav className="mobile-nav" aria-label="Navegação móvel">
      {links.map(({ href, label, icon }) => (
        <Link key={href} href={href} aria-current={current === href ? "page" : undefined}>
          <svg aria-hidden="true" viewBox="0 0 24 24">{icon}</svg>
          <small>{label}</small>
        </Link>
      ))}
    </nav>
  );
}
