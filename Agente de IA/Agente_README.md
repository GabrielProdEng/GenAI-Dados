# 📊 Agente de Monitoramento de Indicadores Econômicos com IA + API do Bacen

Projeto derivado da estrutura do desafio `dio-lab-bia-do-futuro`, adaptado para um caso de uso publicável no GitHub: **monitoramento de indicadores macroeconômicos brasileiros** com foco em dados públicos do **Banco Central do Brasil (BCB)**.

O agente atua como um analista assistente que:
- acompanha séries do SGS/BCData;
- resume comportamento recente de inflação, juros, câmbio e atividade;
- destaca desvios, tendências e possíveis alertas;
- responde somente com base em dados públicos e configurações do projeto.

## 🎯 Caso de uso

Em vez de trabalhar com dados privados de clientes, este repositório usa apenas **dados públicos e não sensíveis** para construir um agente de monitoramento econômico. O objetivo é permitir perguntas como:

- "Como está o comportamento recente da Selic e do IPCA?"
- "O câmbio acelerou nos últimos 30 dias?"
- "Quais indicadores estão acima do limite de alerta?"
- "Quais séries devo observar em um cenário de inflação persistente?"

## 🧱 Estrutura do repositório

```text
lab-monitor-indicadores-bacen/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── catalogo_indicadores.json
│   ├── configuracao_alertas.json
│   ├── historico_consultas.csv
│   ├── contexto_analitico.json
│   └── README.md
│
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
│
├── src/
│   ├── app.py
│   ├── bacen_client.py
│   ├── loaders.py
│   ├── rules.py
│   └── README.md
│
├── notebooks/
│   └── 01_coleta_e_exploracao_bacen.ipynb
│
├── assets/
│   ├── README.md
│   └── arquitetura-mermaid.md
│
└── examples/
    └── README.md
