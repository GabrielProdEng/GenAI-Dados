from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

import pandas as pd
import requests

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
TIMEOUT = 30


def _to_brl_date(value: datetime) -> str:
    return value.strftime("%d/%m/%Y")


def _chunks_10y(
    data_inicial: datetime,
    data_final: datetime
) -> Iterable[tuple[datetime, datetime]]:
    atual = data_inicial
    while atual <= data_final:
        limite = min(atual + timedelta(days=3652), data_final)
        yield atual, limite
        atual = limite + timedelta(days=1)


def fetch_serie_periodo(
    codigo: int,
    data_inicial: datetime,
    data_final: datetime
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    for inicio, fim in _chunks_10y(data_inicial, data_final):
        params = {
            "formato": "json",
            "dataInicial": _to_brl_date(inicio),
            "dataFinal": _to_brl_date(fim),
        }
        url = BASE_URL.format(codigo=codigo)
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()

        dados = response.json()
        frame = pd.DataFrame(dados)

        if frame.empty:
            continue

        frame["data"] = pd.to_datetime(
            frame["data"],
            format="%d/%m/%Y",
            errors="coerce"
        )
        frame["valor"] = pd.to_numeric(frame["valor"], errors="coerce")
        frame["codigo"] = codigo
        frames.append(frame)

    if not frames:
        return pd.DataFrame(columns=["data", "valor", "codigo"])

    return (
        pd.concat(frames, ignore_index=True)
        .drop_duplicates()
        .sort_values("data")
    )
