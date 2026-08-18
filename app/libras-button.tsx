"use client";

import { useState } from "react";

export default function LibrasButton() {
  const [status, setStatus] = useState("Ver em Libras");
  const open = () => {
    const button = document.querySelector<HTMLElement>("[vw-access-button]");
    if (button) {
      button.click();
      setStatus("Libras ativado");
      window.setTimeout(() => setStatus("Ver em Libras"), 2500);
      return;
    }
    setStatus("Carregando Libras…");
    window.setTimeout(open, 700);
  };
  return <button className="libras-button" type="button" onClick={open} aria-label="Ativar tradução da página em Libras"><span aria-hidden="true">✋</span>{status}</button>;
}
