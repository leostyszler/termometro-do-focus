"""
Case 1 — Termômetro do Focus · o AGENTE SEMANAL (esqueleto que já roda de ponta a ponta).

Rode da raiz do repositório:
    python avancado/case1_focus/agente_semanal.py                 # fluxo completo
    python avancado/case1_focus/agente_semanal.py --sem-email     # gera o relatório, mas não envia
    python avancado/case1_focus/agente_semanal.py --sem-download  # usa os CSVs que já estão em data/

As etapas:
  1. baixar   — dados novos do Banco Central (scripts/baixar_dados_bcb.py)
  2. calcular — o termômetro da semana, salvo em saida/resumo_semana.json
  3. checar   — se algo estiver errado, o agente PARA e avisa o time
  4. analisar — o Claude escreve a análise via Claude Code (`claude -p`), usando o seu plano do Claude
  5. conferir — todo número do texto precisa existir no JSON
  6. montar   — relatório em HTML (é também o artefato web): saida/relatorio_semana.html
  7. enviar   — e-mail pelo Gmail (enviar_email.py + .env)

Os pontos marcados com TODO são o desafio do time.
"""
import argparse
import base64
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
SAIDA = AQUI / "saida"
sys.path.insert(0, str(AQUI))

from inicio_focus import (META_INFLACAO, carregar_focus, carregar_sgs,  # noqa: E402
                          grafico_acuracia, resumo_acuracia, serie_semanal)

INDICADORES = ["IPCA", "Selic", "Câmbio", "PIB Total"]
# TODO: limiares chutados. Calibrem com o histórico (ex.: 2 desvios-padrão das variações de 4 semanas).
LIMIAR_4S = {"IPCA": 0.3, "Selic": 0.5, "Câmbio": 0.15, "PIB Total": 0.3}
# Faixas plausíveis para a checagem: fora disso, provavelmente é erro de dado.
FAIXA = {"IPCA": (0, 20), "Selic": (0, 30), "Câmbio": (2, 10), "PIB Total": (-10, 10)}
MAX_DIAS_DEFASAGEM = 10
ANOS_ACURACIA = 5          # quantos anos fechados entram no histórico de acerto
CID_GRAFICO = "grafico_acuracia"   # identificador da imagem anexada ao e-mail


# ------------------------------------------------------------------ 1. baixar
def baixar() -> None:
    subprocess.run([sys.executable, str(RAIZ / "scripts" / "baixar_dados_bcb.py")], check=True)


# ------------------------------------------------------------------ 2. calcular
def calcular() -> dict:
    focus = carregar_focus()
    data_focus = focus["Data"].max()
    resumo = {"data_focus": f"{data_focus:%d/%m/%Y}", "gerado_em": f"{date.today():%d/%m/%Y}",
              "indicadores": [], "alertas": []}
    for ind in INDICADORES:
        for ano in (data_focus.year, data_focus.year + 1):
            s = serie_semanal(focus, ind, ano)
            if len(s) < 5:
                continue
            linha = {"indicador": ind, "ano": int(ano), "mediana": round(float(s.iloc[-1]), 2),
                     "var_semana": round(float(s.iloc[-1] - s.iloc[-2]), 2),
                     "var_4_semanas": round(float(s.iloc[-1] - s.iloc[-5]), 2)}
            disp = focus[(focus["Indicador"] == ind) & (focus["DataReferencia"] == ano)
                         & (focus["Data"] == focus["Data"].max())]["DesvioPadrao"]
            if not disp.empty:
                linha["desvio_padrao"] = round(float(disp.iloc[0]), 2)
            if ind == "IPCA":
                linha["distancia_da_meta"] = round(linha["mediana"] - META_INFLACAO, 2)
            resumo["indicadores"].append(linha)
            if abs(linha["var_4_semanas"]) >= LIMIAR_4S[ind]:
                resumo["alertas"].append(f"{ind} {ano}: variou {linha['var_4_semanas']:+.2f} em 4 semanas")

    # Histórico de acerto pedido pela diretora: expectativa × realizado nos últimos
    # 5 anos fechados. Entra no JSON para que a análise possa citar esses números.
    resumo["acuracia"] = resumo_acuracia(focus, carregar_sgs(), ANOS_ACURACIA)
    # TODO: o que mais um gestor quer ver toda segunda? Selic atual vs. esperada?
    return resumo


# ------------------------------------------------------------------ 3. checar
def checar(resumo: dict) -> list[str]:
    problemas = []
    dias = (date.today() - date(*map(int, reversed(resumo["data_focus"].split("/"))))).days
    if dias > MAX_DIAS_DEFASAGEM:
        problemas.append(f"o Focus mais recente é de {resumo['data_focus']} ({dias} dias atrás)")
    if not resumo["indicadores"]:
        problemas.append("nenhum indicador calculado")
    for l in resumo["indicadores"]:
        lo, hi = FAIXA[l["indicador"]]
        if not lo <= l["mediana"] <= hi:
            problemas.append(f"{l['indicador']} {l['ano']} = {l['mediana']} fora da faixa plausível")
    # TODO: outras checagens? (ex.: número de respondentes muito baixo, semana repetida)
    return problemas


# ------------------------------------------------------------------ 4. analisar
def analisar(resumo: dict, texto_anterior: str = "", suspeitos: list[str] | None = None) -> str:
    """Pede a análise ao Claude. Se `suspeitos` vier preenchido, pede uma reescrita
    do `texto_anterior` removendo os números que não têm base no JSON."""
    claude = shutil.which("claude")
    if not claude:
        raise SystemExit("Claude Code não encontrado. Instale e faça login (ver avancado/README.md).")
    prompt = (AQUI / "prompt_analise.md").read_text(encoding="utf-8")
    entrada = prompt + "\n" + json.dumps(resumo, ensure_ascii=False, indent=2)

    if suspeitos:
        entrada += f"""

ATENÇÃO — REESCRITA NECESSÁRIA

Você já escreveu o texto abaixo, mas ele contém números que NÃO existem no JSON acima:
{", ".join(suspeitos)}

Reescreva o texto inteiro removendo ou substituindo esses números. Um número só pode
aparecer se estiver literalmente no JSON. Não compare com limiares, metas ou valores de
referência que não estejam lá: prefira descrever em palavras ("variação pequena",
"praticamente estável") a citar um número sem base. Mantenha a mesma estrutura e o mesmo
tom. Responda só com o HTML.

Texto anterior:
{texto_anterior}"""

    r = subprocess.run([claude, "-p"], input=entrada, capture_output=True, text=True,
                       encoding="utf-8", timeout=300)
    if r.returncode != 0:
        raise SystemExit(f"Erro ao chamar o Claude Code:\n{r.stderr}")
    return r.stdout.strip().removeprefix("```html").removesuffix("```").strip()


# ------------------------------------------------------------------ 5. conferir
def conferir(texto: str, resumo: dict) -> list[str]:
    """Todo número decimal do texto precisa aparecer no JSON (pega número inventado)."""
    validos = set()
    for v in re.findall(r"-?\d+(?:[.,]\d+)?", json.dumps(resumo)):
        x = float(v.replace(",", "."))
        validos |= {round(x, 2), round(abs(x), 2)}
    suspeitos = []
    for v in re.findall(r"\d+,\d+|\d+\.\d+", re.sub(r"<[^>]+>", " ", texto)):
        if round(float(v.replace(",", ".")), 2) not in validos:
            suspeitos.append(v)
    return suspeitos


# ------------------------------------------------------------------ 6. montar
def montar(resumo: dict, analise: str, src_grafico: str = "") -> str:
    """Monta o relatório. `src_grafico` é o src da imagem: base64 no arquivo HTML
    (que é o artefato web) ou cid:... no e-mail, porque o Gmail bloqueia data URI."""
    linhas = "".join(
        f"<tr><td>{l['indicador']}</td><td>{l['ano']}</td><td>{l['mediana']:.2f}</td>"
        f"<td>{l['var_semana']:+.2f}</td><td>{l['var_4_semanas']:+.2f}</td></tr>"
        for l in resumo["indicadores"])

    acc = resumo.get("acuracia", {})
    bloco_acuracia = ""
    if acc.get("por_horizonte"):
        linhas_acc = "".join(
            f"<tr><td>{h['indicador']}</td><td>{h['quando']}</td>"
            f"<td>{h['erro_medio']:+.2f}</td><td>{h['erro_absoluto_medio']:.2f}</td>"
            f"<td>{h['vezes_que_subestimou']} de {h['anos_considerados']}</td></tr>"
            for h in acc["por_horizonte"])
        periodo = f"{acc['anos'][0]}–{acc['anos'][-1]}" if acc.get("anos") else ""
        imagem = (f'<p><img src="{src_grafico}" alt="Expectativa contra realizado de IPCA e Selic" '
                  f'style="width:100%;max-width:680px"></p>') if src_grafico else ""
        bloco_acuracia = f"""
<h3>O Focus acertou? Histórico de {periodo}</h3>
{imagem}
<table border="1" cellpadding="6" style="border-collapse:collapse;font-size:14px">
<tr><th>Indicador</th><th>Quando</th><th>Erro médio</th><th>Erro absoluto médio</th><th>Subestimou</th></tr>
{linhas_acc}</table>
<p style="font-size:12px;color:#666">Erro = realizado menos esperado, em pontos percentuais.
Positivo significa que o valor observado veio acima do que o mercado projetava.</p>"""

    return f"""<html><body style="font-family:Arial,sans-serif;max-width:680px;margin:auto">
<h2>Termômetro do Focus — {resumo['data_focus']}</h2>
{analise}
<h3>Números da semana (mediana)</h3>
<table border="1" cellpadding="6" style="border-collapse:collapse">
<tr><th>Indicador</th><th>Ano</th><th>Mediana</th><th>Var. semana</th><th>Var. 4 semanas</th></tr>
{linhas}</table>
{bloco_acuracia}
<p style="font-size:12px;color:#666">Fonte: Banco Central do Brasil, Relatório Focus de {resumo['data_focus']}.
Análise gerada automaticamente com o Claude e conferida contra os dados. Não constitui recomendação de investimento.</p>
</body></html>"""


# ------------------------------------------------------------------ fluxo
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-download", action="store_true")
    ap.add_argument("--sem-email", action="store_true")
    args = ap.parse_args()
    SAIDA.mkdir(exist_ok=True)

    if not args.sem_download:
        print("1. Baixando dados..."); baixar()
    print("2. Calculando o termômetro..."); resumo = calcular()
    (SAIDA / "resumo_semana.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    print("3. Checando..."); problemas = checar(resumo)
    if problemas:
        aviso = "<p>O agente parou. Problemas encontrados:</p><ul>" + \
                "".join(f"<li>{html.escape(p)}</li>" for p in problemas) + "</ul>"
        print("   PAROU:", "; ".join(problemas))
        if not args.sem_email:
            from enviar_email import enviar
            enviar("[ALERTA] Agente do Focus parou", aviso)
        sys.exit(1)

    print("4. Pedindo a análise ao Claude..."); analise = analisar(resumo)

    print("5. Conferindo números do texto...")
    suspeitos = conferir(analise, resumo)
    for tentativa in (1, 2):
        if not suspeitos:
            break
        print(f"   sem base no JSON: {', '.join(suspeitos)} — pedindo reescrita ({tentativa}/2)")
        analise = analisar(resumo, analise, suspeitos)
        suspeitos = conferir(analise, resumo)

    if suspeitos:
        # Esgotadas as tentativas, não enviamos um relatório com número inventado.
        aviso = ("<p>O agente parou: a análise continha números sem base nos dados "
                 "mesmo após duas reescritas.</p><ul>" +
                 "".join(f"<li>{html.escape(s)}</li>" for s in suspeitos) + "</ul>")
        print("   PAROU: a análise ainda cita", ", ".join(suspeitos))
        if not args.sem_email:
            from enviar_email import enviar
            enviar("[ALERTA] Agente do Focus parou na conferência", aviso)
        sys.exit(1)
    print("   todos os números conferem com o JSON")

    print("6. Montando o relatório...")
    grafico = grafico_acuracia(carregar_focus(), carregar_sgs(), ANOS_ACURACIA)
    print("   gráfico de acurácia em", grafico)

    # No arquivo HTML a imagem vai embutida em base64, para o artefato web ser um
    # arquivo único. No e-mail ela vai anexada e referenciada por cid:, porque o
    # Gmail não exibe data URI.
    embutida = "data:image/png;base64," + base64.b64encode(grafico.read_bytes()).decode()
    destino = SAIDA / "relatorio_semana.html"
    destino.write_text(montar(resumo, analise, embutida), encoding="utf-8")
    print("   salvo em", destino)

    if not args.sem_email:
        from enviar_email import enviar
        corpo = montar(resumo, analise, f"cid:{CID_GRAFICO}")
        para = enviar(f"Termômetro do Focus — {resumo['data_focus']}", corpo,
                      imagens={CID_GRAFICO: grafico})
        print("7. E-mail enviado para", ", ".join(para))


if __name__ == "__main__":
    main()
