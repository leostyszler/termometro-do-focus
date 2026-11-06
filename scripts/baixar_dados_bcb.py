"""
Baixa os dados do Banco Central usados nos Cases 1 e 2.

- Expectativas de mercado (Focus) via API Olinda (OData)
- Séries realizadas via SGS

Uso:
    pip install requests pandas
    python scripts/baixar_dados_bcb.py

Saída: data/case1_focus/focus_anuais.csv e data/case1_focus/sgs_realizado.csv
As APIs são públicas e não exigem cadastro nem chave.
"""
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlencode

import pandas as pd
import requests

SAIDA = Path(__file__).resolve().parent.parent / "data" / "case1_focus"
INICIO = "2020-01-01"  # cobre as previsões dos últimos 5 anos fechados

OLINDA = ("https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
          "ExpectativasMercadoAnuais")
INDICADORES = ["IPCA", "Selic", "Câmbio", "PIB Total"]

SGS = {  # nome: código
    "ipca_mensal": 433,
    "ipca_12m": 13522,
    "selic_meta": 432,
    "dolar_ptax_venda": 1,
    "ibc_br": 24363,
}


def baixar_focus() -> pd.DataFrame:
    partes = []
    for ind in INDICADORES:
        params = {
            "$filter": f"Indicador eq '{ind}' and Data ge '{INICIO}'",
            "$select": ("Indicador,Data,DataReferencia,Media,Mediana,DesvioPadrao,"
                        "Minimo,Maximo,numeroRespondentes,baseCalculo"),
            "$orderby": "Data asc",
            "$format": "json",
            "$top": "100000",
        }
        # A API Olinda só aceita espaços como %20; o requests os enviaria como "+"
        # (e devolveria HTTP 400). Por isso montamos a query à mão.
        r = requests.get(f"{OLINDA}?{urlencode(params, quote_via=quote)}", timeout=120)
        r.raise_for_status()
        df = pd.DataFrame(r.json()["value"])
        print(f"Focus {ind}: {len(df)} linhas")
        partes.append(df)
    return pd.concat(partes, ignore_index=True)


def baixar_sgs() -> pd.DataFrame:
    ini = pd.Timestamp(INICIO).strftime("%d/%m/%Y")
    fim = date.today().strftime("%d/%m/%Y")
    partes = []
    for nome, cod in SGS.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{cod}/dados"
        r = requests.get(url, params={"formato": "json", "dataInicial": ini, "dataFinal": fim}, timeout=120)
        r.raise_for_status()
        df = pd.DataFrame(r.json())
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["serie"] = nome
        df["codigo_sgs"] = cod
        print(f"SGS {nome} ({cod}): {len(df)} linhas")
        partes.append(df[["data", "serie", "codigo_sgs", "valor"]])
    return pd.concat(partes, ignore_index=True)


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    baixar_focus().to_csv(SAIDA / "focus_anuais.csv", index=False)
    baixar_sgs().to_csv(SAIDA / "sgs_realizado.csv", index=False)
    print(f"Pronto. Arquivos em {SAIDA} (dados até {date.today():%d/%m/%Y}).")
