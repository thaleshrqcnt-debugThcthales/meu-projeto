# NHANDEREKO — revisão integral do acervo digital

## Alterações aplicadas

- Curadoria indígena unificada em **Juá Jacarandá Kixelô Kariri** em fichas, páginas institucionais, citações e rodapé.
- Créditos padronizados: Wemerson Cunto como proponente; Thales Henrique Cunto e Fabrício de Assis Vicentin na produção executiva; Lucas Horas / Minutos com Horas em acessibilidade; Bárbara Libras em Libras.
- Removida a contagem visual `01–07`, `Peça X de 7`, `Explorar as 7 peças` e equivalentes.
- Homepage com navegação completa: Acervo, Atlas, Metodologia, Sobre e Acessibilidade.
- Retorno das páginas internas padronizado como `← Início`; fichas usam `← Voltar ao acervo`.
- Títulos e metadados padronizados em `NHANDEREKO`, com Open Graph nas fichas.
- Arco e Flecha incorporado ao grid e ao filtro Kariri-Xocó, com imagem, audiodescrição e procedência parcial explicitada.
- Vídeo recebido para Arco e Flecha **não publicado** por conter identificação cultural incompatível (`Povo Guarani` / `artefato ritual`) com a ficha atual; o site informa que o vídeo está em revisão antes de validação profissional.
- Dois áudios fornecidos do Zunidor unidos em uma faixa única, inserida como player independente `Ouça o som do zunidor`, sem substituir a audiodescrição.
- Ritxoko corrigido para **Ritxòkò**, com forma masculina `ritxò` documentada.
- Zunidor: nome `matapu` incorporado; **Waujá** adotado como etnônimo principal, mantendo Waurá apenas como grafia histórica/comercial.
- Cesto de Buriti: `kaj` e `kajatê` incorporados com cautela documental.
- Maracá: identificação ampliada para `Asurini do Xingu (Awaeté)` e termo específico da língua mantido em verificação.
- Cerâmica: Waujá como etnônimo principal; nome específico do objeto continua em verificação.
- Remo Xipaya: nome específico na língua continua em verificação.
- Modo exposição criado para todas as fichas.
- Citação ABNT/APA e compartilhamento por WhatsApp padronizados.
- Página Sobre recriada com princípios de procedência, curadoria Juá e equipe completa.
- Página Metodologia recriada sem numeração decorativa e com protocolo reutilizável.
- Página Acessibilidade atualizada com WCAG 2.2 AA, eMAG, ABNT NBR 17225:2025, limitações de Libras automatizada e compromisso de não abrir pop-up `nova versão`.
- Atlas reconstruído como ferramenta interativa e acessível:
  - marcadores em controles nativos de botão;
  - navegação por teclado e foco visível;
  - tooltip em hover/foco;
  - clique abre e destaca o povo correspondente;
  - rótulos `Cerrado · Maranhão` e `Nordeste · baixo São Francisco`;
  - entrada Waujá apresenta Zunidor e Cerâmica Waujá e informa duas peças no acervo;
  - seis povos com cartões expansíveis;
  - seta Norte;
  - sem escala métrica simulada e sem polígonos territoriais inventados;
  - links para Funai e IBGE para limites oficiais.
- Não existe código customizado de service worker/toast/modal de atualização no pacote final.

## Validação

- Verificação estática de TSX/TypeScript executada com sucesso.
- Verificação de presença de mídias referenciadas executada com sucesso.
- Áudio unido do Zunidor: cerca de 22 segundos.
- Audiodescrição do Arco e Flecha: cerca de 121 segundos.
- Build completo não executado neste ambiente porque o instalador do projeto depende do `registry.npmjs.org`, inacessível no contêiner atual.
