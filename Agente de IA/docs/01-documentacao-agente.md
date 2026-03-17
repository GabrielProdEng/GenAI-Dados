# Documentação do Agente

## Caso de Uso

### Problema
Acompanhar indicadores como inflação, Selic, câmbio e atividade econômica exige ler séries dispersas e interpretar dados manualmente.

### Solução
A aplicação integra:
- séries públicas do Bacen;
- regras locais de alerta;
- um modelo local rodando no Ollama para responder perguntas em linguagem natural.

O resultado é uma assistente chamada **BIA Macro Local**, capaz de transformar dados numéricos em explicações mais acessíveis.

---

## Persona

### Nome
**BIA Macro Local**

### Papel
Analista assistente de monitoramento econômico.

### Estilo
Objetiva, prudente, explicável e baseada em dados carregados no app.

---

## Arquitetura

```mermaid
flowchart TD
    A[Usuário] --> B[Streamlit]
    B --> C[Consulta BCData/SGS]
    C --> D[Dados do Bacen]
    B --> E[Camada de regras]
    E --> F[Resumo estruturado]
    F --> G[Prompt contextual]
    G --> H[Ollama local]
    H --> I[Resposta no chat]
