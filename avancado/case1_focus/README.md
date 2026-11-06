# Caminho avançado — Case 1 · Termômetro do Focus

Leia antes o [README do case](../../data/case1_focus/README.md) (problema e cuidados com os dados).

## Ponto de partida

O objetivo do case é o **agente semanal** descrito no [README do case](../../data/case1_focus/README.md#o-objetivo). Ele já existe em versão inicial e roda de ponta a ponta:

```bash
python avancado/case1_focus/agente_semanal.py --sem-email     # roda tudo, menos o envio
python avancado/case1_focus/enviar_email.py                   # testa o e-mail (depois de criar o .env)
python avancado/case1_focus/agente_semanal.py                 # fluxo completo
```

| Arquivo | O que faz |
|---|---|
| [`agente_semanal.py`](agente_semanal.py) | o agente: baixar → calcular → checar → analisar (`claude -p`) → conferir → montar → enviar |
| [`inicio_focus.py`](inicio_focus.py) | funções de carga, séries semanais, acurácia e alertas (usadas pelo agente) |
| [`prompt_analise.md`](prompt_analise.md) | o prompt fixo que o Claude recebe junto com o JSON da semana |
| [`enviar_email.py`](enviar_email.py) | envio pelo Gmail, lendo a senha de app do `.env` |
| [`.env.exemplo`](.env.exemplo) | modelo do `.env` (copiem para `.env` e preencham; o `.env` não vai para o GitHub) |

O Claude é chamado pelo Claude Code em modo não interativo (`claude -p`), que usa o login do plano pago. **Leiam o código antes de usar**: vocês vão ter que defender cada número.

## Trilha sugerida

**Manhã — nível 1: entender e conferir**
- Rodem o agente com `--sem-email` e abram `saida/relatorio_semana.html`.
- **Confiram 3 números à mão** contra o Relatório Focus oficial.
- Testem a parada: alterem um dado de propósito e vejam o agente parar.

**Manhã — nível 2: um termômetro que vale a pena receber**
- Calibrem os limiares de alerta com o histórico, em vez dos valores chutados.
- Incluam o que um gestor quer ver toda segunda (dispersão, Selic atual × esperada, acurácia).
- Acrescentem uma checagem nova na etapa `checar`.

**Tarde (depois da palestra das 13h30) — nível 3: o agente pronto para rodar sozinho**
1. melhorar o `prompt_analise.md` e fazer o agente **pedir reescrita** quando a conferência acusar número sem base no JSON;
2. ligar o e-mail (`.env`) e deixar o e-mail com a cara do time;
3. agendar no Agendador de Tarefas do Windows ou no `cron` (ver o README do case);
4. publicar o `relatorio_semana.html` como artefato.

Bônus: transformem o procedimento numa **Skill** (veja o [exemplo](../skills_exemplo/bcb-sgs/SKILL.md)) para que qualquer pessoa rode o termômetro com um pedido só.

## Onde o Claude Code ajuda

- "Leia `inicio_focus.py` e o README do case e me explique o que cada função faz."
- "Adicione a acurácia do câmbio usando o último valor de dezembro da série dolar_ptax_venda."
- "Escreva um teste que confere o IPCA anual composto contra a série ipca_12m."
