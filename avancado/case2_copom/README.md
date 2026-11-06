# Caminho avançado — Case 2 · Tradutor do Copom

Leia antes o [README do case](../../data/case2_copom/README.md) (problema e cuidados com os dados).

## Ponto de partida

As 6 atas já estão em `data/case2_copom/atas/`, no padrão `ata_<nº da reunião>_<AAAA-MM-DD>.pdf` que o script espera. Para a Selic e o Focus, rodem `python scripts/baixar_dados_bcb.py`.

```bash
python avancado/case2_copom/extrair_atas.py
```

O script [`extrair_atas.py`](extrair_atas.py) extrai o texto das atas, quebra em parágrafos e gera um **diff** entre as duas mais recentes (o que entrou, saiu e mudou, palavra por palavra) em `saida/`. É o "diff de tom da ata" do material do workshop, só que feito por vocês.

## Trilha sugerida

**Manhã — nível 1: o diff confiável**
- Rodem o script e **confiram no PDF** se a quebra em parágrafos funcionou. PDF é traiçoeiro: cabeçalho, rodapé e tabelas atrapalham. Ajustem `em_paragrafos()` se precisar.
- Com o diff em mãos, escrevam (com o Claude) a nota "o que mudou nesta ata" para um investidor leigo.

**Manhã — nível 2: índice de tom**
- Classifiquem cada parágrafo numa régua de −2 (muito brando) a +2 (muito duro).
  - **Com chave da API:** [`classificar_tom.py`](classificar_tom.py) faz isso sozinho.
  - **Sem chave:** peçam ao Claude Code para classificar `saida/paragrafos_atas.csv` usando a mesma régua do `PROMPT` do script.
- **Validem o índice:** peguem 10 parágrafos, classifiquem vocês mesmos e comparem com o Claude. Onde discordam, e por quê?

**Tarde (depois da palestra das 13h30) — nível 3: o site do índice de tom**

O objetivo final do case é um **site** com o índice de tom, o que mudou e o principal impacto (ver o [README do case](../../data/case2_copom/README.md#o-objetivo)). No caminho avançado, o site é gerado a partir dos resultados dos scripts, não escrito à mão:

1. extrair as atas (`extrair_atas.py`);
2. comparar a mais recente com a anterior (diff);
3. classificar o tom de cada parágrafo e calcular o índice por reunião (`classificar_tom.py` ou Claude Code);
4. cruzar o índice com a trajetória da Selic e das expectativas de Selic do Focus (dados do Case 1);
5. pedir ao Claude o texto do "principal impacto" **a partir desses resultados**, e **um segundo Claude revisa** procurando afirmações sem base no texto da ata (padrão *evaluator-optimizer*);
6. juntar tudo num JSON (índice, mudanças, impacto) e gerar o site a partir dele, para que uma ata nova atualize o site rodando o fluxo de novo;
7. publicar o site como artefato.

## Onde o Claude Code ajuda

- "A função em_paragrafos está juntando o rodapé com o parágrafo 12. Corrija."
- "Faça um gráfico do tom médio por reunião com a Selic meta no eixo secundário."
- "Leia o diff e liste as 3 mudanças mais relevantes, citando o nº do parágrafo."
