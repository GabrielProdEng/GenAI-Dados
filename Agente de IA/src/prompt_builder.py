from __future__ import annotations

import pandas as pd


SYSTEM_PROMPT = """
Você é a BIA Macro, uma assistente local de monitoramento econômico.

Seu papel é analisar indicadores macroeconômicos brasileiros com base EXCLUSIVAMENTE:
1. no contexto fornecido pela aplicação,
2. nas regras locais do projeto,
3. nos dados da série carregada pelo usuário.

Regras obrigatórias:
- Não invente valores.
- Não afirme ter consultado fontes externas.
- Não recomende compra, venda ou alocação de ativos.
- Diferencie fatos observados de interpretação.
- Se faltarem dados, diga isso claramente.
- Seja objetiva, clara e prudente.
- Responda em português do Brasil.
"""


def build_series_context(
    indicador: dict,
    df: pd.DataFrame,
    alerts: list[str] | None = None,
) -> str:
    if df.empty:
        return f"""
Indicador selecionado:
- Nome: {indicador['nome']}
- Código: {indicador['codigo']}
- Categoria: {indicador['categoria']}
- Unidade: {indicador['unidade']}

Não há dados disponíveis na janela selecionada.
"""

    serie = df.sort_values("data").copy()
    first = serie.iloc[0]
    last = serie.iloc[-1]

    variacao = None
    if len(serie) >= 2 and float(first["valor"]) != 0:
        variacao = ((float(last["valor"]) / float(first["valor"])) - 1) * 100

    ultimos = serie.tail(8).copy()
    ultimos_texto = "\n".join(
        [
            f"- {row['data'].strftime('%Y-%m-%d')}: {float(row['valor']):.4f}"
            for _, row in ultimos.iterrows()
        ]
    )

    alertas_txt = "\n".join([f"- {a}" for a in alerts]) if alerts else "- Nenhum alerta ativo"

    variacao_txt = f"{variacao:.2f}%" if variacao is not None else "não calculada"

    return f"""
Indicador selecionado:
- Nome: {indicador['nome']}
- Código: {indicador['codigo']}
- Categoria: {indicador['categoria']}
- Unidade: {indicador['unidade']}

Resumo numérico:
- Data inicial da janela: {serie['data'].min().strftime('%Y-%m-%d')}
- Data final da janela: {serie['data'].max().strftime('%Y-%m-%d')}
- Primeiro valor da janela: {float(first['valor']):.4f}
- Último valor da janela: {float(last['valor']):.4f}
- Variação percentual da janela: {variacao_txt}
- Quantidade de observações: {len(serie)}

Últimas observações:
{ultimos_texto}

Alertas:
{alertas_txt}
"""


def build_messages(
    user_question: str,
    indicador: dict,
    df: pd.DataFrame,
    alerts: list[str] | None = None,
    chat_history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    context_message = {
        "role": "system",
        "content": SYSTEM_PROMPT + "\n\n" + build_series_context(indicador, df, alerts)
    }

    messages: list[dict[str, str]] = [context_message]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": user_question})
    return messages
