# NHANDEREKO — Acervo digital acessível

Site do acervo digital do projeto **NHANDEREKO — Ler, Brincar e Pertencer**
(Chamamento Público nº 02/2026-SMC-PNAB), com sete fichas de artefatos
indígenas, audiodescrição, Libras, procedência documentada, Atlas dos Povos
e metodologia reutilizável para exposições educativas.

Construído em [Next.js](https://nextjs.org) (App Router) com TypeScript e
Tailwind CSS.

## Desenvolvimento

```bash
npm install
npm run dev      # servidor de desenvolvimento
npm run build    # build de produção
npm run start    # servir o build de produção
npm run lint     # eslint
```

## Estrutura

- `app/artifacts.ts` — dados de todas as fichas do acervo (fonte única de verdade).
- `app/site-chrome.tsx` — cabeçalho, navegação e rodapé compartilhados por todas as páginas.
- `app/artefatos/[slug]/` — template único de ficha de artefato.
- `app/exposicao/[slug]/` — modo exposição (layout simplificado para exibição em tela).
- `app/atlas/` — Atlas dos Povos (mapa interativo acessível).
- `app/sobre/`, `app/metodologia/`, `app/acessibilidade/` — páginas institucionais.
- `public/media/` — imagens, áudios (audiodescrição) e vídeos em Libras das peças.

## Responsáveis

- **Proponente:** Wemerson Cunto
- **Produção executiva:** Thales Henrique Cunto e Fabrício de Assis Vicentin
- **Curadoria indígena:** Juá Jacarandá Kixelô Kariri
- **Acessibilidade:** Lucas Horas / Minutos com Horas
- **Tradução e interpretação em Libras:** Bárbara Libras
