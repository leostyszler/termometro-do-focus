# Caminho avançado

É o caminho de **todos os times**: código em Python, **Claude Code**, fluxos automáticos e agentes, para os cases **1 (Focus)**, **2 (Copom)** e **3 (Comparativo de resultados)**.

> Código **não ganha ponto só por ser código**. A banca avalia utilidade, rigor e produto (ver [regras](../REGRAS_E_AVALIACAO.md)). Um fluxo automatizado que **verifica os próprios números** é o que diferencia.

## Preparação (obrigatória, antes do evento)

1. **Python 3.10+** instalado.
2. Na raiz do repositório:
   ```bash
   pip install -r requirements.txt
   ```
3. **Claude Code** instalado e logado ([documentação](https://docs.claude.com/en/docs/claude-code/overview)). Rode `claude` dentro da pasta do repositório.
   > Todos os participantes precisam de um **plano pago do Claude** (Pro ou superior), que é o que dá acesso ao Claude Code. Testem a instalação e o login antes do dia 06/11.
4. *Opcional:* chave da API da Anthropic (`ANTHROPIC_API_KEY`), **cobrada à parte do plano do Claude**. Só é usada pelo `classificar_tom.py` do Case 2. Sem chave, o próprio Claude Code faz a mesma tarefa. O agente do Case 1 **não** precisa de chave: ele chama o Claude pelo Claude Code (`claude -p`), que usa o plano. **Nunca subam a chave para o GitHub** (o `.gitignore` já ignora `.env`).

## Os guias

| Case | Guia | Código de partida |
|---|---|---|
| 1 — Termômetro do Focus | [case1_focus/README.md](case1_focus/README.md) | análise, acurácia e alertas |
| 2 — Tradutor do Copom | [case2_copom/README.md](case2_copom/README.md) | extração, diff de atas e índice de tom |
| 3 — Comparativo de resultados | [case3_resultados/README.md](case3_resultados/README.md) | extração, verificador de números e roteiro da apresentação |
| Skills | [skills_exemplo/README.md](skills_exemplo/README.md) | Skill completa de exemplo (`bcb-sgs`) |

## Como a trilha se encaixa no dia

| Momento | Nível | Foco |
|---|---|---|
| Manhã (10h30–13h00) | 1 e 2 | Rodar o código de partida, **entender e conferir** cada número, resolver os `TODO` |
| Palestra (13h30–14h00) | — | Insights dentro do Claude |
| Tarde (14h00–16h00) | 3 | Transformar a análise num **fluxo que roda sozinho e se verifica**, e publicar o resultado como artefato |

## Regras de ouro

- **Leiam o código antes de rodar.** Peçam ao Claude Code para explicar o que não entenderem.
- **Número só entra no texto depois de calculado ou verificado.** O Claude escreve a partir dos resultados, nunca de memória.
- **Commits pequenos e frequentes.** Se algo quebrar, dá para voltar.
- Tudo que for gerado cai em pastas `saida/`: coloquem no GitHub do time só o que for resultado final.
