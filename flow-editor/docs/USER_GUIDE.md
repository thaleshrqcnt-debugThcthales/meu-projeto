# GUIA DO USUÁRIO — FLOW EDITOR

## Instalação (passo a passo)

### 1. Verifique o Python
Abra o terminal e digite:
```
python3 --version
```
Precisa ser 3.11 ou superior.

### 2. Baixe o FLOW EDITOR
Coloque a pasta `flow-editor` em qualquer local do seu computador.

### 3. Abra o terminal dentro da pasta

### 4. Execute o script de instalação
```bash
./run.sh
```

Aguarde instalar as dependências (primeira vez pode demorar 2-3 minutos).

### 5. Configure a API key
Quando solicitado (ou antes de usar funções de IA), abra o arquivo `.env` e insira:
```
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

Ou acesse **Configurações** no sistema após abrir o navegador.

### 6. Acesse o sistema
Abra o navegador em: **http://127.0.0.1:8000**

---

## Como criar seu primeiro projeto

1. Clique em **"+ Novo Projeto"** no dashboard
2. Preencha:
   - Nome interno (sem espaços, ex: `festival-2024`)
   - Título público do projeto
   - Nome do proponente
   - Tipo de proponente
   - Cidade e estado
   - Linguagem artística e modalidade
   - Módulo e valor pretendido
3. Clique em **"Criar projeto"**

---

## Como subir o edital

1. No projeto, clique em **"Edital"**
2. Arraste o PDF do edital ou clique em "Selecionar PDF"
3. Aguarde a extração (30-60 segundos)
4. Revise o Raio-X: clique nos campos e corrija o que estiver errado
5. Clique em **"Salvar correções"**

---

## Como preencher o briefing

1. No projeto, clique em **"Briefing"**
2. No campo grande, escreva livremente sua ideia
3. Preencha os campos auxiliares: território, público, equipe, ações, espaços
4. **Atenção:** parceiros desejados e espaços desejados serão tratados como "em negociação", não como confirmados
5. Clique em **"Salvar briefing"**

---

## Como gerar o projeto

1. No projeto, clique em **"Gerar"**
2. Clique em **"⚡ Gerar Projeto Completo"**
3. Aguarde 30-90 segundos (depende do tamanho do briefing e edital)
4. Revise cada seção — você pode:
   - Editar manualmente o texto
   - Clicar em **"✨ Humanizar"** para melhorar a linguagem
   - Clicar em **"↻ Regenerar"** para gerar novamente com a IA
   - Clicar em **"Salvar"** para guardar as alterações

---

## Como preencher orçamento e cronograma

**Orçamento (aba "Orçamento"):**
- Clique em **"+ Adicionar item"**
- Preencha: item, categoria, unidade, quantidade, valor unitário, justificativa
- O total é calculado automaticamente
- Clique em **"Salvar orçamento"**

Categorias disponíveis: recursos humanos, serviços, materiais, comunicação, acessibilidade, registro, outros.

**Cronograma (aba "Cronograma"):**
- Clique em **"+ Adicionar fase"**
- Preencha: fase, mês, atividade, responsável, comprovação
- Clique em **"Salvar cronograma"**

---

## Como auditar o projeto

1. No projeto, clique em **"Auditoria"**
2. Execute a **"Auditoria Determinística"** primeiro (mais rápida, sem IA)
3. Veja os alertas por nível:
   - 🚨 **Críticos**: corrigir antes de enviar (risco de desclassificação)
   - ⚠ **Médios**: corrigir se possível (risco de perda de pontos)
   - 💡 **Leves**: melhorias opcionais
4. Execute a **"Auditoria com IA"** para análise mais completa
5. Execute **"Riscos Formais"** para identificar riscos de desclassificação
6. Execute **"Checklist Documental"** para saber quais documentos preparar

---

## Como simular a banca

1. No projeto, clique em **"Banca"**
2. Leia o aviso: esta é uma simulação técnica, não garante aprovação
3. Clique em **"🎯 Simular Parecer de Banca"**
4. Aguarde 30-60 segundos
5. Veja as notas por critério (C1-C5), o parecer e as recomendações
6. Use as recomendações para melhorar o projeto antes de exportar

---

## Como exportar

1. No projeto, clique em **"Exportar"**
2. Escolha o arquivo que deseja:
   - **DOCX**: projeto completo formatado
   - **XLSX**: planilha orçamentária
   - **Auditoria DOCX**: relatório de pendências
   - **Parecer DOCX**: resultado da simulação de banca
   - **Pacote ZIP**: todos os arquivos juntos
3. O arquivo é baixado diretamente no seu navegador

---

## Dicas importantes

- **Revise sempre** o texto gerado. A IA pode ter imprecisões.
- **Corrija manualmente** informações que estiverem erradas.
- **Execute a auditoria** antes de exportar para identificar pendências.
- **Verifique o orçamento**: a soma deve bater com o valor do módulo.
- **Acessibilidade**: sempre inclua uma rubrica de acessibilidade no orçamento, mesmo que pequena.
- **Não envie** um projeto com alertas críticos sem resolver.

## Aviso final

O FLOW EDITOR é uma ferramenta de apoio técnico. A aprovação em editais depende da qualidade final do projeto, dos documentos apresentados, da banca avaliadora, da concorrência e dos critérios específicos de cada edital. Nenhuma ferramenta automatizada garante aprovação.
