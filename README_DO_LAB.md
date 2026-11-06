# Claude Lab · Economia & Finanças — PUC-Rio 2026

**PUC-Rio · sexta, 6 de novembro de 2026 · 08h00 às 18h00 · Sala F300**

Um dia de mão na massa: resolvam, com o **Claude**, problemas reais de análise econômica e financeira, usando **dados públicos brasileiros** (Banco Central, IBGE, CVM e relatórios de empresas), com **mentoria** de quem constrói agentes de IA no mercado e apresentação dos resultados no fim do dia.

Este repositório é o ponto de partida de todos os times: aqui estão os **cases**, os **dados**, as **regras** e as instruções de **entrega**.

> **Com apoio de:**  departamento de economia da PUC-Rio 

---

## Como funciona

1. **Forme o time** 4/5 pessoas, e **escolha um case**.
2. **Leia o README do case inteiro antes de começar.** Os dados têm armadilhas, e metade do desafio é interpretá-los certo.
3. **Construa com o Claude.** Explorar dado, escrever código, montar relatório, criar um app: o que fizer o problema andar.
4. **Verifique.** Confira os números do Claude contra a fonte. Isso vale ponto (ver [regras](REGRAS_E_AVALIACAO.md)).
5. **Entregue** até o horário-limite: **vídeo de 2 min**, **artefato público** e **GitHub público** do time.

Nunca usou GitHub ou o Claude? Comece por **[COMO_COMECAR.md](COMO_COMECAR.md)**.

## Os 3 cases

| # | Case | Pergunta central | Dados 
|---|------|------------------|-------|
| 1 | **[Termômetro do Focus](data/case1_focus/README.md)** | Um agente que, toda semana, baixa o Relatório Focus, analisa o que mudou nas expectativas e envia a análise por e-mail | Focus (BCB) + séries do SGS |
| 2 | **[Tradutor do Copom](data/case2_copom/README.md)** | Um site que lê as atas do Copom, mede o tom do Banco Central num índice e explica o que mudou e qual pode ser o principal impacto dessa mudança | Atas do Copom (PDF) + Selic e Focus 
| 3 | **[Comparativo de resultados](data/case3_resultados/README.md)** | Uma apresentação executiva que compara os resultados do 3º trimestre de 2026 da Gerdau e da Usiminas, para o diretor levar ao comitê | ITRs das duas empresas (PDF), já incluídos |

Os três cases buscam resolver problemas de pessoas de dentro do mercado financeiro, de forma que a solução seja realmente uma ferramenta útil no dia a dia. O objetivo é despertar a curiosidade com IA para que vocês sejam capazes de automatizar processos. Por isso, todos os cases são resolvidos pelo **[caminho avançado](avancado/README.md)**, com código de partida em Python, Claude Code, Skills e fluxos automáticos que verificam os próprios números.

## Onde estão os dados

Tudo em **[`data/`](data/)**, uma pasta por case. Cada uma tem um `README.md` com o problema, o dicionário dos dados, os **cuidados de interpretação** e perguntas de partida. Os dados do Banco Central foram baixados com o script em [`scripts/`](scripts/), que você pode rodar de novo para atualizar. Leia **[USO-DOS-DADOS.md](USO-DOS-DADOS.md)** antes de publicar qualquer resultado.

## Cronograma — sexta, 06/11 (Sala F300)

| Horário | Atividade |
|---|---|
| 08h00 – 09h00 | Coffee break · aproveitem para conferir o login no Claude e no GitHub |
| 09h00 – 10h30 | **Palestra de abertura** — introdução ao Claude, apresentação dos participantes e dos cases do dia · com os palestrantes do workshop (ver [Organização](#organização)) |
| 10h30 – 13h00 | **Mão na massa, parte 1** — os times desenvolvem os cases com o Claude (mentoria Taicor · MGV Tech · Visagio) |
| 13h00 – 13h30 | Almoço |
| 13h30 – 14h00 | **Palestra** — apresentação de insights dentro do Claude · Visagio ou MGV Tech, a confirmar |
| 14h00 – 16h30 | **Mão na massa, parte 2** — finalização e entrega dos cases (mentoria Taicor · MGV Tech · Visagio) |
| **16h00** | **Deadline da entrega** (vídeo + artefato + GitHub) |
| 16h30 – 17h00 | Coffee break · banca seleciona os **3 finalistas** |
| 17h00 – 17h30 | Apresentação dos finalistas, anúncio do campeão e encerramento |

## Entrega e avaliação

Três itens, todos **públicos**, até **16h00**:

1. **Vídeo de até 2 minutos** mostrando o problema e a solução funcionando.
2. **Artefato público**: o link publicado do que vocês construíram (app, dashboard, relatório interativo).
3. **GitHub público do time**, com README detalhado do projeto e da equipe (use o [modelo](modelo-repositorio-time/README.md)).

**Entreguem pelo [formulário de entrega](https://github.com/jplucas29/claude-lab-financas-puc2026/issues/new?template=entrega.yml)** até 16h00 (é preciso estar logado no GitHub).

Detalhes, critérios e pesos em **[REGRAS_E_AVALIACAO.md](REGRAS_E_AVALIACAO.md)**. Checklist em **[entrega/CHECKLIST_ENTREGA.md](entrega/CHECKLIST_ENTREGA.md)**. Os links de todos os times ficam em **[ENTREGAS.md](ENTREGAS.md)**.

## Organização

**Organizadores:** [PREENCHER: nomes e cursos]
**Palestrantes, mentoria e banca:**

- [João Henrique Lisboa](https://www.linkedin.com/in/joaolisboa/), Co-Founder da Taicor e Claude Ambassador
- [Diogo Miranda](https://www.linkedin.com/in/d1ogo-miranda/), Co-Founder da MGV Tech
- Visagio, consultoria que aplica IA em seus processos
- [Marco Cauduro](https://www.linkedin.com/in/marcocauduro/), criador da DeepStack, ferramenta voltada para investimentos
- [Igor Peres](https://www.linkedin.com/in/goriperes/), supervisor do LIA e professor do Departamento de Engenharia Industrial da PUC-Rio

**Apoio institucional:**  Departamento de Economia da PUC-Rio 


## Estrutura do repositório

```
claude-lab-financas-puc2026/
├── README.md                    você está aqui
├── COMO_COMECAR.md              setup do Claude e do GitHub — comece aqui
├── REGRAS_E_AVALIACAO.md        regras, horário-limite, critérios e pesos
├── USO-DOS-DADOS.md             fontes, créditos e uso responsável
├── ENTREGAS.md                  links finais de todos os times
├── data/
│   ├── case1_focus/             expectativas Focus + séries SGS (CSV)
│   ├── case2_copom/             atas do Copom (PDF)
│   └── case3_resultados/        ITRs da Gerdau e da Usiminas (PDF)
├── avancado/                    caminho avançado dos cases 1, 2 e 3
│   ├── case1_focus/             análise, acurácia e alertas do Focus
│   ├── case2_copom/             extração, diff e índice de tom das atas
│   ├── case3_resultados/        extrair → verificar → comparar → apresentar
│   └── skills_exemplo/          Skill de exemplo (bcb-sgs)
├── requirements.txt             bibliotecas do caminho avançado
├── scripts/
│   └── baixar_dados_bcb.py      baixa/atualiza os dados do Banco Central
├── modelo-repositorio-time/
│   └── README.md                modelo do README do GitHub de cada time
└── entrega/
    └── CHECKLIST_ENTREGA.md
```
