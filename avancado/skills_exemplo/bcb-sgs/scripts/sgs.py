"""Baixa uma série do SGS do Banco Central.  Uso: python sgs.py 433 --inicio 2024-01-01 --saida ipca.csv"""
import argparse
from datetime import date

import pandas as pd
import requests

ap = argparse.ArgumentParser()
ap.add_argument("codigo", type=int)
ap.add_argument("--inicio", default="2020-01-01")
ap.add_argument("--saida", default=None)
a = ap.parse_args()

url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{a.codigo}/dados"
params = {"formato": "json",
          "dataInicial": pd.Timestamp(a.inicio).strftime("%d/%m/%Y"),
          "dataFinal": date.today().strftime("%d/%m/%Y")}
r = requests.get(url, params=params, timeout=60)
r.raise_for_status()
df = pd.DataFrame(r.json())
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
destino = a.saida or f"sgs_{a.codigo}.csv"
df.to_csv(destino, index=False)
print(f"Série {a.codigo}: {len(df)} observações, de {df['data'].min()} a {df['data'].max()} → {destino}")
print(df.tail(3).to_string(index=False))
