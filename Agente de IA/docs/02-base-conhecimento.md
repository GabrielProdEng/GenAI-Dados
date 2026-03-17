
## `docs/02-base-conhecimento.md`

```md
# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `catalogo_indicadores.json` | JSON | Define séries, categorias, unidade e objetivo analítico |
| `configuracao_alertas.json` | JSON | Estabelece regras simples de monitoramento |
| `contexto_analitico.json` | JSON | Define objetivo, perguntas frequentes e restrições |
| `historico_consultas.csv` | CSV | Exemplifica interações passadas sem dados pessoais |

---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos JSON e CSV locais são carregados no início da aplicação para montar o contexto do agente e listar os indicadores disponíveis.

### Como os dados são usados no prompt?
Os arquivos locais dão contexto e regras. Os **valores numéricos reais** vêm da API do Bacen em tempo de execução.

### Como os dados externos entram no fluxo?
Quando o usuário escolhe um indicador e um intervalo de datas, a aplicação consulta a API BCData/SGS, trata os dados e só então gera o resumo e os alertas.

---

## Exemplo de Contexto Montado

```text
Contexto do agente:
- Objetivo: monitorar indicadores macroeconômicos do Brasil
- Escopo: inflação, juros, câmbio, atividade e crédito
- Restrições: não recomendar ativos; não inventar dados

Indicador selecionado:
- Nome: IPCA
- Código: 433
- Categoria: inflação
- Unidade: %

Regras aplicáveis:
- Se a última leitura for maior que 0,5%, emitir alerta
