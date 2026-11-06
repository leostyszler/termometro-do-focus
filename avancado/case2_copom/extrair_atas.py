"""
Case 2 — Tradutor do Copom · extração e comparação das atas.

Rode da raiz do repositório:
    python avancado/case2_copom/extrair_atas.py                  # extrai todas e compara as 2 mais recentes
    python avancado/case2_copom/extrair_atas.py --comparar A.pdf B.pdf

Saídas em avancado/case2_copom/saida/:
    paragrafos_atas.csv   um parágrafo por linha (arquivo, reunião, data, nº, texto)
    diff_<A>_vs_<B>.md    o que entrou, saiu e mudou entre duas atas

Os arquivos devem seguir o padrão ata_<nº da reunião>_<AAAA-MM-DD>.pdf.
"""
import argparse
import difflib
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

RAIZ = Path(__file__).resolve().parents[2]
ATAS = RAIZ / "data" / "case2_copom" / "atas"
SAIDA = Path(__file__).resolve().parent / "saida"
MIN_CARACTERES = 80          # descarta cabeçalhos, rodapés e números de página


def texto_do_pdf(caminho: Path) -> str:
    paginas = [p.extract_text() or "" for p in PdfReader(caminho).pages]
    return "\n".join(paginas)


def em_paragrafos(texto: str) -> list[str]:
    """As atas numeram os parágrafos ('1. ...', '2. ...'). Quebra por isso;
    se não achar numeração, quebra por linhas em branco."""
    texto = re.sub(r"-\n(?=[a-zà-ú])", "", texto)                # hifenização de fim de linha
    partes = re.split(r"\n\s*(?=\d{1,2}\.\s+[A-ZÀ-Ú])", texto)
    if len(partes) < 2:
        partes = re.split(r"\n\s*\n", texto)
    limpos = [re.sub(r"\s+", " ", p).strip() for p in partes]
    return [p for p in limpos if len(p) >= MIN_CARACTERES]


def metadados(caminho: Path) -> dict:
    m = re.match(r"ata_(\d+)_(\d{4}-\d{2}-\d{2})", caminho.stem)
    return {"reuniao": int(m.group(1)), "data_reuniao": m.group(2)} if m else {"reuniao": None, "data_reuniao": None}


def extrair_todas() -> pd.DataFrame:
    linhas = []
    for pdf in sorted(ATAS.glob("*.pdf")):
        meta = metadados(pdf)
        for i, par in enumerate(em_paragrafos(texto_do_pdf(pdf)), start=1):
            linhas.append({"arquivo": pdf.name, **meta, "n_paragrafo": i, "texto": par})
        print(f"{pdf.name}: {sum(1 for l in linhas if l['arquivo'] == pdf.name)} parágrafos")
    return pd.DataFrame(linhas)


def diff_palavras(a: str, b: str) -> str:
    """Mostra ~~removido~~ e **adicionado** palavra a palavra."""
    pa, pb = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb).get_opcodes():
        if op == "equal":
            out.append(" ".join(pb[j1:j2]))
        if op in ("delete", "replace"):
            out.append("~~" + " ".join(pa[i1:i2]) + "~~")
        if op in ("insert", "replace"):
            out.append("**" + " ".join(pb[j1:j2]) + "**")
    return " ".join(out)


def comparar(pa: list[str], pb: list[str], nome_a: str, nome_b: str) -> str:
    usados, secoes = set(), {"novo": [], "alterado": [], "igual": 0}
    for par in pb:
        notas = [(difflib.SequenceMatcher(None, par, x).ratio(), k) for k, x in enumerate(pa)]
        nota, k = max(notas) if notas else (0, None)
        if nota >= 0.95:
            secoes["igual"] += 1; usados.add(k)
        elif nota >= 0.5:
            secoes["alterado"].append((nota, diff_palavras(pa[k], par))); usados.add(k)
        else:
            secoes["novo"].append(par)
    removidos = [x for k, x in enumerate(pa) if k not in usados]

    md = [f"# O que mudou: {nome_a} → {nome_b}\n",
          f"Parágrafos praticamente iguais: {secoes['igual']} · alterados: {len(secoes['alterado'])} · "
          f"novos: {len(secoes['novo'])} · removidos: {len(removidos)}\n",
          "> Diff automático por similaridade de texto. **Confiram no PDF** antes de concluir: "
          "a quebra de parágrafos pode falhar.\n",
          "## Parágrafos alterados (~~saiu~~ **entrou**)\n"]
    md += [f"- *(similaridade {n:.0%})* {t}\n" for n, t in sorted(secoes["alterado"])]
    md += ["\n## Parágrafos novos\n"] + [f"- {t}\n" for t in secoes["novo"]]
    md += ["\n## Parágrafos removidos\n"] + [f"- {t}\n" for t in removidos]
    return "\n".join(md)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--comparar", nargs=2, metavar=("ANTERIOR", "NOVA"))
    args = ap.parse_args()
    SAIDA.mkdir(exist_ok=True)

    df = extrair_todas()
    if df.empty:
        raise SystemExit(f"Nenhum PDF em {ATAS}")
    df.to_csv(SAIDA / "paragrafos_atas.csv", index=False)

    arquivos = args.comparar or sorted(df["arquivo"].unique(), key=lambda n: metadados(Path(n))["data_reuniao"] or n)[-2:]
    a, b = (Path(x).name for x in arquivos)
    rel = comparar(df[df.arquivo == a]["texto"].tolist(), df[df.arquivo == b]["texto"].tolist(), a, b)
    destino = SAIDA / f"diff_{Path(a).stem}_vs_{Path(b).stem}.md"
    destino.write_text(rel, encoding="utf-8")
    print("Comparação salva em", destino)
