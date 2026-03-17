# 📊 BIA Macro Local — Monitor de Indicadores Econômicos com Bacen + Ollama

Aplicação local para monitoramento de indicadores macroeconômicos brasileiros com foco em:

- acompanhamento de séries públicas do Banco Central;
- visualização de dados e alertas;
- chat local com modelos executados via Ollama;
- uso exclusivo de dados públicos e não sensíveis.

## 🎯 Objetivo

Criar uma aplicação local em que o usuário:

1. escolhe um indicador do Bacen;
2. consulta a série histórica;
3. visualiza gráfico e alertas;
4. conversa com um modelo local do Ollama sobre os dados carregados.

---

## 🧠 Como o agente funciona

A aplicação foi pensada como um **agente analítico local**, dividido em duas partes:

### 1. Camada de dados e monitoramento

Essa camada é responsável por:

- carregar o catálogo de indicadores configurados no projeto;
- consultar a API pública do Banco Central;
- tratar os dados retornados;
- exibir gráfico, tabela e resumo da série;
- aplicar regras simples de alerta.

### 2. Camada conversacional com Ollama

Depois que a série é carregada, a aplicação monta um **contexto estruturado** com:

- nome do indicador;
- código SGS;
- categoria;
- unidade de medida;
- data inicial e final da janela;
- primeiro e último valor da série;
- variação no período;
- últimas observações disponíveis;
- alertas ativados pela aplicação.

Esse contexto é enviado para um **modelo local rodando no Ollama**, que responde em linguagem natural com base apenas nessas informações.

Ou seja, o agente **não acessa a internet sozinho**, **não consulta o Bacen diretamente por conta própria** e **não inventa contexto externo**.  
Quem faz a coleta e preparação dos dados é a aplicação.  
O modelo local entra como uma camada de interpretação e conversa.

---

## 🔄 Fluxo de funcionamento

O fluxo do agente acontece nesta ordem:

1. o usuário abre a aplicação local;
2. escolhe um indicador econômico;
3. define o período de consulta;
4. a aplicação busca os dados na API BCData/SGS do Bacen;
5. os dados são tratados e exibidos em gráfico e tabela;
6. as regras locais verificam se existe algum alerta;
7. a aplicação monta um resumo estruturado da série;
8. o usuário escolhe um modelo disponível no Ollama;
9. a pergunta do usuário é enviada ao modelo junto com o contexto da série;
10. o modelo responde de forma analítica, em linguagem natural, dentro do escopo definido.

---

## 🧩 O que o agente consegue fazer

Com esse fluxo, o agente pode:

- resumir o comportamento recente de um indicador;
- explicar tendências de alta, queda ou estabilidade;
- destacar alertas calculados pela aplicação;
- traduzir a leitura da série para linguagem mais simples;
- responder perguntas sobre inflação, juros, câmbio, atividade e crédito;
- apoiar análises educacionais e exploratórias com dados públicos.

Exemplos de perguntas possíveis:

- "Como está o comportamento recente da inflação?"
- "O câmbio acelerou nesse período?"
- "Explique essa série de forma simples."
- "Quais pontos merecem atenção nesse indicador?"
- "O que os últimos dados sugerem sobre atividade econômica?"

---

## 🚫 O que o agente não faz

Para manter segurança e coerência, o agente não deve:

- recomendar compra ou venda de ativos;
- prever mercado ou decisões futuras;
- afirmar uso de notícias ou fontes externas não carregadas pela aplicação;
- inventar valores, datas ou interpretações sem base nos dados;
- responder fora do escopo macroeconômico do projeto.

---

## 🧠 Papel da IA local

A IA não consulta a internet por conta própria.  
Ela responde com base em:

- regras do projeto;
- catálogo de indicadores;
- série carregada pelo usuário;
- resumo numérico preparado pela aplicação.

Assim, o LLM atua como **camada conversacional e analítica local**.

---

## 🔌 Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- API BCData/SGS do Banco Central
- Ollama local

---

## 🧱 Estrutura

```text
lab-monitor-indicadores-bacen/
├── Agente_README.md
├── requirements.txt
├── data/
├── docs/
├── src/
