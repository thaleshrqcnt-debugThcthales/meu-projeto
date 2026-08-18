"use client";

import { useEffect } from "react";

declare global {
  interface Window {
    VLibras?: { Widget: new (rootPath: string) => unknown };
    __nhanderekoVlibrasStarted?: boolean;
  }
}

export default function LibrasWidget() {
  useEffect(() => {
    const startWidget = () => {
      if (window.VLibras?.Widget && !window.__nhanderekoVlibrasStarted) {
        new window.VLibras.Widget("https://vlibras.gov.br/app");
        window.__nhanderekoVlibrasStarted = true;
      }
    };
    const existing = document.querySelector<HTMLScriptElement>('script[src="https://vlibras.gov.br/app/vlibras-plugin.js"]');
    if (existing) {
      if (window.VLibras?.Widget) startWidget();
      else existing.addEventListener("load", startWidget, { once: true });
      return;
    }
    const script = document.createElement("script");
    script.src = "https://vlibras.gov.br/app/vlibras-plugin.js";
    script.async = true;
    script.addEventListener("load", startWidget, { once: true });
    document.body.appendChild(script);
  }, []);

  return (
    <div {...({ vw: "" } as Record<string, string>)} className="enabled">
      <div {...({ "vw-access-button": "" } as Record<string, string>)} className="active" />
      <div {...({ "vw-plugin-wrapper": "" } as Record<string, string>)}><div className="vw-plugin-top-wrapper" /></div>
    </div>
  );
}
