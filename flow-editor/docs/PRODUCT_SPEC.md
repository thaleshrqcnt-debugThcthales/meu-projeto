# PRODUCT SPEC — FLOW EDITOR

## Visão Geral

Sistema local de produção, auditoria, revisão, exportação e blindagem de projetos culturais para editais públicos.

## Módulos

1. **Gerenciamento de Projetos**: CRUD completo com status e histórico
2. **Extração de Edital**: PDF → texto → JSON estruturado via IA
3. **Briefing**: Coleta de dados livre + campos auxiliares estruturados
4. **Geração de Projeto**: 23 seções em linguagem cultural técnica
5. **Orçamento**: Tabela com itens, categorias, percentuais e alertas
6. **Cronograma**: Fases, atividades, responsáveis e comprovações
7. **Auditoria Determinística**: Verificações por código puro, sem IA
8. **Auditoria por IA**: Análise textual e semântica completa
9. **Simulação de Banca**: Notas C1-C5, parecer e recomendações
10. **Exportação**: DOCX, XLSX, MD, ZIP

## Fluxos

### Fluxo principal (etapas 1-8)
1. Criar projeto → 2. Upload edital → 3. Raio-x → 4. Briefing → 5. Gerar → 6. Auditar → 7. Banca → 8. Exportar

### Fluxo de correção
Auditoria → Identificar problema → Editar seção → Humanizar → Re-auditar → Exportar

## Regras de Negócio

### Dados
- Parceiros desejados ≠ parceiros confirmados
- Espaços desejados ≠ espaços confirmados
- Histórico não comprovado → apresentado como "relatado pelo proponente"
- Dados territoriais sem fonte → "conforme percepção da equipe"

### Auditoria determinística — alertas críticos
- Soma do orçamento diverge >10% do valor pretendido
- Seções obrigatórias ausentes (RESUMO, METODOLOGIA, PUBLICO_ALVO)
- Marcadores de IA no texto ([inserir], placeholder, conforme solicitado)
- Libras prometido mas sem rubrica orçamentária

### Auditoria determinística — alertas médios
- Comunicação prometida sem rubrica
- Equipe sem remuneração correspondente
- Cronograma com execução antes de divulgação

### Score de banca
- C1 Mérito cultural: 0-20
- C2 Adequação ao edital: 0-20
- C3 Viabilidade técnica: 0-20
- C4 Orçamento e cronograma: 0-20
- C5 Equipe, acessibilidade, impacto: 0-20
- Total: 0-100
- Nunca prometer aprovação

## Critérios de Aceite

1. App inicia localmente sem erros
2. Tela inicial abre no navegador
3. Usuário cria projeto
4. Usuário sobe PDF
5. Sistema extrai texto do PDF
6. Sistema gera raio-x do edital
7. Usuário preenche briefing
8. Sistema gera projeto completo (23 seções)
9. Sistema gera orçamento e cronograma
10. Sistema roda auditoria de coerência
11. Sistema simula banca
12. Sistema exporta DOCX
13. Sistema exporta XLSX
14. Sistema exporta ZIP
15. README explica instalação e uso
16. Testes principais passam
17. Código organizado e prompts separados
18. Sistema não inventa dados sem marcar como sugestão
