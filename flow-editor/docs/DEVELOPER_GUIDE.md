# DEVELOPER GUIDE — FLOW EDITOR

## Arquitetura

```
app/
  main.py           FastAPI app + registro de routers
  config.py         Settings via pydantic-settings + .env
  database.py       Engine SQLite + SessionLocal + init_db()
  models.py         SQLAlchemy ORM (9 tabelas)
  schemas.py        Pydantic schemas (request/response)
  routers/          Rotas por domínio
  services/         Lógica de negócio
  agents/           Agentes especializados (composição de services)
  prompts/          Prompts em Markdown
  templates/        Jinja2 HTML
  static/           CSS + JS
```

## Banco de dados

SQLite via SQLAlchemy. Tabelas:
- `projects`: projeto principal
- `edicts`: edital PDF + texto + JSON extraído
- `briefings`: briefing livre + campos auxiliares
- `project_sections`: seções do projeto (com versioning)
- `budgets`: itens do orçamento
- `schedules`: cronograma
- `audits`: resultados de auditoria
- `score_simulations`: simulações de banca
- `exports`: registro de arquivos exportados
- `app_settings`: configurações persistidas

## Serviços centrais

### ai_provider.py
Camada de abstração. Métodos:
- `complete(prompt, system, max_tokens)` → str
- `complete_json(prompt)` → dict

Para adicionar OpenAI: implementar `_openai_complete()` e registrar em `self.provider`.

### edital_extractor.py
- `extract_edict(text)` → dict (via IA)
- `extract_edict_from_pdf(path)` → (dict, text, pages, status)

### project_generator.py
- `generate_project(project, briefing, edital_json)` → dict[section_name, content]
- `parse_sections(raw_text)` → dict — divide texto por marcadores `### [SECAO]`

### consistency_auditor.py
Auditoria determinística. Cada função retorna `list[Finding]`.
Sem IA, puro código. Adicionar novas verificações como funções independentes.

### score_simulator.py
- `simulate_score(project, sections, budgets, schedules, edital_json)` → dict
- Usa prompt `simular_banca.md`

## Prompts

Todos em `app/prompts/*.md`. Carregados via `load_prompt(name)`.
- `system_base.md`: sistema base compartilhado por todos os agentes
- `raio_x_edital.md`: extração estruturada do edital
- `gerar_projeto.md`: geração das 23 seções
- `auditar_coerencia.md`: auditoria textual via IA
- `simular_banca.md`: simulação de parecer de banca
- `humanizar_texto.md`: reescrita sem marcas de IA

## Como expandir

### Adicionar nova seção
1. Adicionar nome em `SECTION_NAMES` em `project_generator.py`
2. Adicionar label em `SECTION_LABELS`
3. Adicionar ao `section_order` em `docx_exporter.py`
4. Atualizar prompt `gerar_projeto.md`

### Adicionar novo provider de IA
1. Em `ai_provider.py`, adicionar método `_<provider>_complete()`
2. Registrar em `complete()` com `elif self.provider == '<provider>'`
3. Atualizar `.env.example` com `AI_PROVIDER=<provider>`

### Adicionar novo agente
1. Criar `app/agents/agente_<nome>.py`
2. Implementar função principal com assinatura `(project, ...) -> dict`
3. Registrar rota em `app/routers/audit.py`
4. Criar prompt se necessário em `app/prompts/`

## Testes

```bash
python -m pytest tests/ -v
```

Testes existentes:
- `test_consistency_auditor.py`: auditoria determinística
- `test_budget_auditor.py`: cálculos de orçamento
- `test_edital_extractor.py`: extração de edital (com mock de IA)
- `test_docx_exporter.py`: geração de DOCX

Testes que usam IA são mockados com `unittest.mock.patch`.
