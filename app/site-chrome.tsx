import Link from "next/link";

type HeaderProps = {
  returnLabel?: "Início" | "Voltar ao acervo";
  returnHref?: string;
};

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
      <div className="footer-inner">
        <div>
          <SiteLogo />
          <p className="footer-title">Mostra de Artefatos — acervo digital acessível</p>
        </div>
        <div className="footer-credits">
          <p><strong>Proponente:</strong> Wemerson Cunto</p>
          <p><strong>Produção executiva:</strong> Thales Henrique Cunto e Fabrício de Assis Vicentin</p>
          <p><strong>Curadoria indígena:</strong> Juá Jacarandá Kixelô Kariri</p>
          <p><strong>Acessibilidade:</strong> Lucas Horas / Minutos com Horas</p>
          <p><strong>Tradução e interpretação em Libras:</strong> Bárbara Libras</p>
          <p><strong>Realização:</strong> Chamamento Público nº 02/2026-SMC-PNAB</p>
          <p>São José do Rio Preto — SP · 2026</p>
        </div>
        <nav className="footer-nav" aria-label="Navegação do rodapé">
          <Link href="/#artefatos">Acervo</Link>
          <Link href="/atlas">Atlas dos Povos</Link>
          <Link href="/metodologia">Metodologia reutilizável</Link>
          <Link href="/sobre">Sobre a obra</Link>
          <Link href="/acessibilidade">Recursos de acessibilidade</Link>
        </nav>
      </div>
    </footer>
  );
}
