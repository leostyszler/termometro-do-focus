# Case 1 — Termômetro do Focus

Claude Lab · Economia & Finanças · PUC-Rio · 06/11/2026

## Contexto

Toda segunda-feira o Banco Central publica o **Relatório Focus**, com as expectativas de cerca de 100 instituições (bancos, gestoras, consultorias) para inflação, juros, câmbio e crescimento. É um dos documentos mais lidos do mercado. Numa gestora, alguém abre o relatório toda segunda, copia os números para uma planilha, compara com a semana anterior e escreve um resumo para os gestores: trabalho manual, repetitivo e sujeito a erro de digitação. E fica sempre a pergunta: **vale a pena levar o Focus a sério? O mercado costuma acertar?**

Neste case, vocês são o time de análise que vai automatizar esse trabalho.

## A demanda

> **De:** Diretora de Economia
> **Para:** time de análise
> **Assunto:** Automatizar o resumo semanal do Focus
>
> "Quero parar de fazer o resumo do Focus na mão. Preciso que, toda segunda, depois da divulgação, chegue no meu e-mail o que mudou nas expectativas da semana, com os números conferidos e uma análise curta. No mesmo e-mail, quero o histórico: **nos últimos 5 anos, o Focus acertou a inflação e a Selic?** Com gráfico. Se o dado vier errado ou atrasado, prefiro não receber o relatório e ser avisada."

## Resultado esperado

Um **agente** que roda sozinho toda segunda e entrega:

1. **o que mudou na semana**: variação das expectativas na semana e em 4 semanas, distância da meta de inflação, dispersão e alertas;
2. **uma análise curta** escrita pelo Claude, só com números calculados e conferidos;
3. **o histórico de acerto**: expectativa × realizado de IPCA e Selic nos últimos 5 anos fechados, com um gráfico;
4. tudo isso **por e-mail**, com checagens que param o agente e avisam o time quando algo está errado.

O artefato público é a **versão web do relatório da semana**. No vídeo, mostrem o agente rodando e o e-mail chegando.

> A diferença para o Case 2: lá o produto é um site para entender e conversar com as atas. Aqui o produto é um **fluxo automático e recorrente**, que trabalha sozinho toda segunda-feira.

Tudo roda no computador do time e cabe no **plano pago do Claude**: o agente chama o Claude pelo Claude Code em modo não interativo (`claude -p`), que usa o login do plano. Não precisa de chave de API.

## Os dados

Os dados **não vêm prontos**: o próprio agente busca toda semana nas APIs abertas do Banco Central, sem cadastro nem chave. O script [`scripts/baixar_dados_bcb.py`](../../scripts/baixar_dados_bcb.py) é o ponto de partida dessa etapa: baixa os dados desde 2020 (o suficiente para avaliar as previsões dos últimos 5 anos fechados) e gera dois arquivos em `data/case1_focus/`:

| Arquivo | O que é |
|---|---|
| `focus_anuais.csv` | Expectativas anuais (IPCA, Selic, Câmbio, PIB Total), uma linha por data de coleta e ano de referência |
| `sgs_realizado.csv` | Séries realizadas do Banco Central (formato longo: data, série, valor) |

### focus_anuais.csv

| Coluna | Nota |
|---|---|
| `Indicador` | `IPCA`, `Selic`, `Câmbio`, `PIB Total` |
| `Data` | **data em que a expectativa foi coletada** |
| `DataReferencia` | **ano ao qual a expectativa se refere** (ex.: 2026, 2027) |
| `Mediana` / `Media` | estatística das projeções das instituições; o Focus divulga a **mediana** |
| `DesvioPadrao`, `Minimo`, `Maximo` | dispersão das projeções |
| `numeroRespondentes` | quantas instituições responderam |
| `baseCalculo` | `0` = projeções dos últimos 30 dias; `1` = só dos últimos 5 dias úteis |

### sgs_realizado.csv

| `serie` | Código SGS | Unidade |
|---|---|---|
| `ipca_mensal` | 433 | variação % no mês |
| `ipca_12m` | 13522 | variação % acumulada em 12 meses |
| `selic_meta` | 432 | % ao ano |
| `dolar_ptax_venda` | 1 | R$ por US$, diário |
| `ibc_br` | 24363 | índice (proxy mensal do PIB) |

## Guia sugerido

O guia é uma sugestão de caminho, não uma receita: o que importa é entregar o resultado esperado. O time **não começa do zero**: [`avancado/case1_focus/agente_semanal.py`](../../avancado/case1_focus/agente_semanal.py) é um esqueleto que já roda de ponta a ponta (baixar → calcular → checar → analisar → conferir → montar → enviar). O trabalho do dia é entender cada etapa, conferir e deixar cada uma melhor. Os pontos a melhorar estão marcados com `TODO` no código.

### 0. Preparar o computador (antes do dia)

- Python 3.10+ e `pip install -r requirements.txt` na raiz do repositório;
- **Claude Code** instalado e logado com o plano pago: digitar `claude` no terminal tem que abrir o Claude;
- uma conta **Gmail** com verificação em duas etapas, para gerar a "senha de app" do passo 5.

### 1. Rodar o agente pela primeira vez

```bash
python avancado/case1_focus/agente_semanal.py --sem-email
```

Ele baixa os dados, calcula, pede a análise ao Claude e salva `avancado/case1_focus/saida/relatorio_semana.html`. Abram esse arquivo no navegador. Depois:

- peçam ao Claude Code: *"Leia agente_semanal.py e me explique cada etapa"*;
- abram o [Relatório Focus](https://www.bcb.gov.br/publicacoes/focus) da última segunda no site do BC e **confiram 2 números** do relatório de vocês contra o oficial.

### 2. Melhorar o termômetro (etapa `calcular`)

Hoje ela calcula mediana, variação na semana e em 4 semanas, dispersão e distância da meta. O time decide **o que um gestor quer ver toda segunda** e completa:

- **calibrar os alertas**: os limiares do código são chutes. Usem o histórico (por exemplo, 2 desvios-padrão das variações de 4 semanas);
- montar o **histórico de acerto** pedido pela diretora: expectativa × realizado de IPCA e Selic nos últimos 5 anos fechados. A função `tabela_acuracia` em `inicio_focus.py` já faz a conta; falta escolher como mostrar e gerar o gráfico (salvo em `saida/`);
- incluir o que mais fizer sentido: a Selic atual contra a esperada, a dispersão subindo.

Tudo vai para `saida/resumo_semana.json`, que é **a única fonte dos números do e-mail**.

### 3. Reforçar as checagens (etapa `checar`)

O agente já para se o Focus estiver desatualizado ou se um valor sair da faixa plausível, e nesse caso manda um e-mail de alerta em vez do relatório. Acrescentem pelo menos uma checagem de vocês (por exemplo, número de respondentes muito baixo ou semana repetida) e **testem**: alterem um dado de propósito e vejam o agente parar.

### 4. Melhorar a análise (etapas `analisar` e `conferir`)

- O texto sai do prompt em [`prompt_analise.md`](../../avancado/case1_focus/prompt_analise.md). Ajustem o tom, o formato e o que a análise deve destacar.
- A etapa `conferir` já detecta números no texto que não existem no JSON, mas só avisa. **Desafio:** quando isso acontecer, o agente pede ao Claude para reescrever (até 2 tentativas) e só envia se passar.

### 5. Ligar o e-mail

1. Gerem uma **senha de app** do Gmail (myaccount.google.com/apppasswords);
2. copiem `avancado/case1_focus/.env.exemplo` para `.env` na mesma pasta e preencham. **O `.env` nunca vai para o GitHub** (o `.gitignore` já o ignora);
3. testem: `python avancado/case1_focus/enviar_email.py`;
4. rodem o agente completo, agora sem `--sem-email`.

Incluam o gráfico do histórico de acerto (como imagem anexada ao e-mail ou na versão web do relatório) e deixem o e-mail com a cara do time.

### 6. Agendar toda semana

O Focus sai segunda de manhã. Agendem o agente para rodar depois disso, no próprio computador:

- **Windows:** *Agendador de Tarefas → Criar Tarefa Básica →* Semanal, segunda, 10h *→ Iniciar um programa*: o caminho completo do `python.exe` em "Programa" e o caminho completo do `agente_semanal.py` em "Argumentos";
- **Mac/Linux:** uma linha no `crontab -e`, por exemplo `0 10 * * 1 cd /caminho/do/repo && python3 avancado/case1_focus/agente_semanal.py`.

Limitação a registrar no README do time: o computador precisa estar ligado e com o Claude Code logado na hora agendada. No dia, a demonstração é **rodar o agente na hora** e mostrar o e-mail chegando.

### 7. Publicar o artefato

O artefato público é a **versão web do relatório da semana**: o `relatorio_semana.html` publicado (por exemplo, como artefato no claude.ai). No vídeo, mostrem o agente rodando e o e-mail chegando.

### Ritmo sugerido no dia

| Momento | Passos |
|---|---|
| Manhã (10h30–13h00) | 1 a 3: agente rodando, termômetro melhorado e checagens testadas |
| Tarde (14h00–16h00) | 4 a 7: análise, e-mail, agendamento e artefato |

Guia técnico em **[avancado/case1_focus](../../avancado/case1_focus/README.md)**.

## Cuidados com os dados (leia antes de concluir qualquer coisa)

1. **`Data` ≠ `DataReferencia`.** Uma linha com `Data = 2026-03-06` e `DataReferencia = 2026` é "o que o mercado esperava, em março, para o IPCA do ano todo de 2026". Misturar as duas é o erro mais comum.
2. **Filtre `baseCalculo`.** Há duas linhas por data e indicador (0 e 1). Sem filtrar, você conta tudo em dobro. O relatório oficial usa `baseCalculo = 0`.
3. **IPCA mensal não se soma, se compõe.** Para acumular 12 meses: `(1+m1/100)×(1+m2/100)×…−1`. Use `ipca_12m` para conferir o seu cálculo.
4. **Selic no Focus é a taxa no fim do ano**, não a média do ano.
5. **Expectativa de PIB é para o ano inteiro**, e o PIB oficial só sai trimestralmente, com atraso. O IBC-Br é só uma aproximação mensal.
6. **Toda análise diz a data dos dados.** O e-mail precisa dizer de qual Focus está falando.
7. **Segurança:** a senha de app do Gmail fica só no `.env` e nunca vai para o GitHub. E o agente só envia e-mail para quem pediu para receber (vocês e a banca).

## O que a banca vai olhar neste case

- O agente **roda sozinho** do começo ao fim, com um único comando, e está agendado para toda semana?
- Os números do e-mail **batem com o Relatório Focus** oficial?
- O histórico de 5 anos (expectativa × realizado) está **correto** e bem explicado?
- O agente **para** quando os dados estão errados ou desatualizados?
- A análise é **útil** para quem recebe e não inventa números?
- A senha do e-mail está **protegida** (fora do código e do GitHub)?

## Perguntas para atacar

- Quais são os 3 números que um gestor quer ver toda segunda?
- Qual variação semanal é "normal" e qual merece alerta? Como calibrar isso com o histórico?
- A dispersão (`DesvioPadrao`) aumenta antes de mudanças de rumo? Incerteza é informação.
- O mercado erra mais para cima ou para baixo? Erra mais em anos de choque?
- Bônus: cada assinante escolhe quais indicadores quer receber?
