# FLOW EDITOR — Sistema Operacional de Projetos Culturais

Aplicativo web local para criação, auditoria, revisão e exportação de projetos culturais para editais públicos.

## O que é

O FLOW EDITOR une três ferramentas em um único produto local:

- **FLOW EDITOR**: Processador inteligente de projetos culturais. Recebe edital em PDF, briefing livre e dados do proponente. Gera projeto completo em DOCX com linguagem cultural-artística.
- **EditalOS**: Lê o edital, extrai regras, módulos, valores, prazos e critérios. Transforma a ideia em dossiê técnico completo.
- **Projeto Blindado**: Auditor inteligente que simula parecer de banca, identifica incoerências, avalia riscos formais e gera relatório de correção.

## Para quem serve

Produtores culturais, artistas independentes, MEIs culturais, coletivos, consultores e agentes culturais que inscrevem projetos em editais públicos municipais, estaduais e federais.

Editais suportados: PNAB, Lei Aldir Blanc, editais municipais, estaduais, circulação, formação, produção artística, aniversário de cidade, ocupação cultural.

## Requisitos

- Python 3.11 ou superior
- pip
- Chave de API da Anthropic (para funções de IA)

## Instalação

```bash
git clone <repositório>
cd flow-editor

# Cria ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Instala dependências
pip install -r requirements.txt

# Configura ambiente
cp .env.example .env
```

## Configuração da API

Edite o arquivo `.env` e insira sua chave da Anthropic:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Ou configure pela interface: acesse `http://127.0.0.1:8000/configuracoes` após iniciar o app.

## Como rodar

### Modo rápido (Linux/macOS)
```bash
chmod +x run.sh
./run.sh
```

### Modo manual
```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Acesse: **http://127.0.0.1:8000**

## Fluxo de uso

### 1. Criar projeto
Acesse `/projeto/novo` e preencha os dados básicos: nome, proponente, tipo, cidade, linguagem artística, módulo e valor pretendido.

### 2. Upload do edital
Envie o PDF do edital em `/projeto/{id}/edital`. O sistema extrai texto automaticamente e gera o **Raio-X do Edital** com todos os campos estruturados. Você pode corrigir manualmente qualquer campo.

### 3. Preencher briefing
Em `/projeto/{id}/briefing`, escreva livremente a ideia do projeto. Inclua território, público-alvo, equipe, ações, espaços, referências culturais, parceiros e acessibilidade.

### 4. Gerar projeto completo
Em `/projeto/{id}/gerar`, clique em **Gerar Projeto Completo**. O sistema gera 23 seções em linguagem cultural técnica. Cada seção pode ser editada, regenerada ou humanizada.

### 5. Preencher orçamento e cronograma
Na mesma tela, nas abas **Orçamento** e **Cronograma**, adicione os itens manualmente. O sistema calcula totais e percentuais automaticamente.

### 6. Auditoria de coerência
Em `/projeto/{id}/auditoria`, execute:
- **Auditoria Determinística**: rápida, sem IA, verifica inconsistências por código.
- **Auditoria com IA**: completa, analisa coerência textual, linguagem, territorio e riscos.
- **Riscos Formais**: identifica risco de desclassificação.
- **Acessibilidade**: verifica completude do plano.
- **Checklist Documental**: gera lista de documentos necessários.

### 7. Simulação de banca
Em `/projeto/{id}/banca`, simule o parecer de uma banca avaliadora. Recebe notas por critério (C1-C5), parecer técnico e recomendações.

**Aviso**: A simulação NÃO garante aprovação. Depende da banca, concorrência e critérios reais.

### 8. Exportar
Em `/projeto/{id}/exportar`, baixe:
- `projeto_completo.docx` — projeto formatado para inscrição
- `orcamento.xlsx` — planilha com alertas automáticos
- `relatorio_auditoria.docx` — pendências e recomendações
- `parecer_banca_simulada.docx` — notas e parecer
- `projeto_completo.md` — versão Markdown
- **Pacote ZIP final** — tudo em um arquivo

## Sobre PDF

O sistema não exporta PDF diretamente. Para gerar PDF, abra o DOCX no Word, LibreOffice ou Google Docs.

Com LibreOffice instalado:
```bash
libreoffice --headless --convert-to pdf projeto_completo.docx
```

## Estrutura do projeto

```
flow-editor/
  app/
    main.py              — Aplicação FastAPI
    config.py            — Configurações
    database.py          — Banco SQLite
    models.py            — Modelos de dados
    schemas.py           — Schemas Pydantic
    services/
      ai_provider.py     — Camada de IA (Anthropic)
      pdf_reader.py      — Extração de texto de PDF
      edital_extractor.py— Extrai estrutura do edital
      project_generator.py— Gera seções do projeto
      consistency_auditor.py— Auditoria determinística
      score_simulator.py — Simulação de banca
      humanizer.py       — Reescrita de trechos
      docx_exporter.py   — Exportação DOCX
      xlsx_exporter.py   — Exportação XLSX
      zip_exporter.py    — Pacote ZIP
    agents/              — Agentes especializados
    prompts/             — Prompts em Markdown
    templates/           — Templates HTML
    static/              — CSS e JS
    exports/             — Arquivos exportados
    uploads/             — PDFs enviados
    data/                — Banco SQLite
  tests/                 — Testes automatizados
  docs/                  — Documentação técnica
```

## Executar testes

```bash
cd flow-editor
python -m pytest tests/ -v
```

## Limitações do MVP atual

- Exportação PDF requer LibreOffice externo
- Não há autenticação de usuário (sistema local)
- A IA pode necessitar de ajustes manuais nos textos gerados
- Comparação entre projetos não implementada (MVP 4)
- Banco de territórios e modelos por tipo de edital não implementados (MVP 4)

## Avisos importantes

1. **Este sistema não garante aprovação em editais.** A avaliação real depende da banca, da concorrência e dos critérios definitivos de cada edital.
2. **A IA não inventa dados.** Informações não fornecidas são marcadas como "não informado" ou "necessita confirmação".
3. **Dados enviados para IA:** ao usar funções de IA, trechos do edital e do projeto são enviados para a API da Anthropic. Não há compartilhamento com outros sistemas.
4. **Revise sempre** antes de enviar. O projeto gerado é um ponto de partida técnico, não um produto final automático.

## Próximos passos (MVP 2, 3, 4)

- Painel de versões por seção
- Banco de territórios e dados culturais locais
- Modelos pré-configurados por tipo de edital
- Comparação e ranking entre projetos
- Exportação PDF via LibreOffice headless
- Suporte a OpenAI e Ollama (offline)
- Plugin/skill system para expansão modular
