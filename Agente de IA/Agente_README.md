# 📊 BIA Macro Local — Monitor de Indicadores Econômicos com Bacen + Ollama

Projeto derivado da estrutura do laboratório `dio-lab-bia-do-futuro`, adaptado para um caso publicável no GitHub com foco em:

- monitoramento de indicadores macroeconômicos;
- consumo de séries públicas do Banco Central;
- chat local com modelos executados via Ollama;
- zero dados sensíveis.

## 🎯 Objetivo

Criar uma aplicação local em que o usuário:
1. escolhe um indicador do Bacen;
2. consulta a série histórica;
3. visualiza gráfico e alertas;
4. conversa com um modelo local do Ollama sobre os dados carregados.

## 🧠 Papel da IA local

A IA não consulta a internet por conta própria.
Ela responde com base em:
- regras do projeto;
- catálogo de indicadores;
- série carregada pelo usuário;
- resumo numérico preparado pela aplicação.

Assim, o LLM atua como **camada conversacional e analítica local**.

## 🔌 Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- API BCData/SGS do Banco Central
- Ollama local

## 🧱 Estrutura

```text
lab-monitor-indicadores-bacen/
├── README.md
├── requirements.txt
├── data/
├── docs/
├── src/
├── notebooks/
├── assets/
└── examples/
