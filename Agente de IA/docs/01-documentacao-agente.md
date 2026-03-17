# Documentação do Agente

## Caso de Uso

### Problema
Profissionais, estudantes e usuários de negócios costumam acompanhar inflação, juros, câmbio e atividade por fontes dispersas. Isso dificulta uma leitura rápida do cenário e aumenta o risco de interpretação inconsistente.

### Solução
O agente centraliza séries públicas do Banco Central do Brasil e transforma os dados em respostas explicáveis, resumos e alertas simples. Em vez de aconselhar investimentos, ele atua como um **monitor analítico de indicadores**.

### Público-Alvo
- estudantes e profissionais de dados;
- pessoas interessadas em macroeconomia;
- times de negócio que precisam de um monitor econômico básico;
- portfólios técnicos e educacionais.

---

## Persona e Tom de Voz

### Nome do Agente
**BIA Macro**

### Personalidade
Analítica, clara, prudente e orientada a dados.

### Tom de Comunicação
Acessível, objetivo e sem exageros interpretativos.

### Exemplos de Linguagem
- Saudação: "Olá! Posso resumir os indicadores econômicos que você está monitorando."
- Confirmação: "Entendi. Vou olhar os dados disponíveis dessa série no Bacen."
- Erro/Limitação: "Não encontrei dados suficientes para esse período. Posso consultar outra janela ou outra série."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Pergunta| B[Interface Streamlit]
    B --> C[Camada de Regras]
    C --> D[Cliente BCB/SGS]
    D --> E[API BCData]
    D --> F[Catálogo local de indicadores]
    C --> G[Validação e Resumo]
    G --> H[Resposta final]
