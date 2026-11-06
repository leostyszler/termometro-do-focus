"""
Case 2 — Tradutor do Copom · índice de tom com a API do Claude (OPCIONAL).

Precisa de uma chave da API da Anthropic. Sem chave? Use o Claude Code:
peça para ele ler saida/paragrafos_atas.csv e classificar os parágrafos
seguindo a mesma régua descrita em PROMPT abaixo.

    pip install anthropic
    export ANTHROPIC_API_KEY=...            # Windows: set ANTHROPIC_API_KEY=...
    python avancado/case2_copom/classificar_tom.py

Rode antes extrair_atas.py. Saídas em avancado/case2_copom/saida/:
    tom_paragrafos.csv    nota, tema e justificativa por parágrafo
    tom_por_reuniao.csv   média por reunião
"""
import json
import os
from pathlib import Path

import pandas as pd
from anthropic import Anthropic

SAIDA = Path(__file__).resolve().parent / "saida"
MODELO = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")

PROMPT = """Você é um economista que analisa comunicação de bancos centrais.
Classifique o parágrafo abaixo, de uma ata do Copom, quanto ao TOM de política monetária:

 +2 = muito duro (hawkish): sinaliza alta de juros ou juros altos por mais tempo com ênfase
 +1 = duro
  0 = neutro ou descritivo (fatos, dados, sem sinalização)
 -1 = brando (dovish)
 -2 = muito brando: sinaliza corte de juros com ênfase

Responda APENAS com um JSON, sem texto antes ou depois:
{{"tom": <inteiro de -2 a 2>, "tema": "<inflação | atividade | cenário externo | câmbio | fiscal | expectativas | decisão | outro>", "justificativa": "<até 20 palavras, com suas palavras>"}}

Parágrafo:
\"\"\"{texto}\"\"\""""


def classificar(cliente: Anthropic, texto: str) -> dict:
    r = cliente.messages.create(model=MODELO, max_tokens=200,
                                messages=[{"role": "user", "content": PROMPT.format(texto=texto)}])
    bruto = r.content[0].text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(bruto)


if __name__ == "__main__":
    pars = pd.read_csv(SAIDA / "paragrafos_atas.csv")
    destino = SAIDA / "tom_paragrafos.csv"
    feitos = pd.read_csv(destino) if destino.exists() else pd.DataFrame(columns=["arquivo", "n_paragrafo"])
    chaves = set(zip(feitos["arquivo"], feitos["n_paragrafo"]))

    cliente = Anthropic()
    novos = []
    for _, p in pars.iterrows():
        if (p["arquivo"], p["n_paragrafo"]) in chaves:
            continue                                       # já classificado: não gasta de novo
        try:
            res = classificar(cliente, p["texto"])
        except (json.JSONDecodeError, KeyError) as e:
            res = {"tom": None, "tema": "erro", "justificativa": str(e)[:80]}
        novos.append({**p.to_dict(), **res})
        print(p["arquivo"], p["n_paragrafo"], res.get("tom"), res.get("tema"))

    tudo = pd.concat([feitos, pd.DataFrame(novos)], ignore_index=True)
    tudo.to_csv(destino, index=False)
    resumo = (tudo.dropna(subset=["tom"]).groupby(["reuniao", "data_reuniao"])["tom"]
              .agg(["mean", "count"]).round(2).reset_index())
    resumo.to_csv(SAIDA / "tom_por_reuniao.csv", index=False)
    print("\nTom médio por reunião:\n", resumo.to_string(index=False))
    # TODO: a média de todos os parágrafos é a melhor medida? Parágrafos neutros
    #       diluem o sinal. Testem pesos por tema, ou só a seção de decisão.
