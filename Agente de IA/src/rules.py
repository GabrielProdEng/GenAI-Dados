from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class RuleResult:
    triggered: bool
    detail: str


def evaluate_rule(df: pd.DataFrame, rule: dict) -> RuleResult:
    if df.empty:
        return RuleResult(False, "Sem dados para avaliar a regra.")

    serie = df.sort_values("data").copy()
    tipo = rule.get("tipo_regra")
    limite = float(rule.get("limite", 0))

    if tipo == "valor_maior_que":
        ultimo = float(serie["valor"].iloc[-1])
        triggered = ultimo > limite
        return RuleResult(
            triggered,
            f"Último valor: {ultimo:.4f} | Limite: {limite:.4f}"
        )

    if tipo == "variacao_percentual_maior_que":
        if len(serie) < 2:
            return RuleResult(False, "Dados insuficientes para calcular variação.")

        inicial = float(serie["valor"].iloc[0])
        final = float(serie["valor"].iloc[-1])
        variacao = ((final / inicial) - 1) * 100 if inicial != 0 else 0
        triggered = variacao > limite

        return RuleResult(
            triggered,
            f"Variação: {variacao:.2f}% | Limite: {limite:.2f}%"
        )

    if tipo == "variacao_percentual_menor_que":
        if len(serie) < 2:
            return RuleResult(False, "Dados insuficientes para calcular variação.")

        inicial = float(serie["valor"].iloc[0])
        final = float(serie["valor"].iloc[-1])
        variacao = ((final / inicial) - 1) * 100 if inicial != 0 else 0
        triggered = variacao < limite

        return RuleResult(
            triggered,
            f"Variação: {variacao:.2f}% | Limite: {limite:.2f}%"
        )

    return RuleResult(False, "Tipo de regra não implementado.")
