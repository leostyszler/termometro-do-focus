# Termômetro do Focus — Case 1

> Claude Lab · Economia & Finanças · PUC-Rio · 06/11/2026

Um agente que roda sozinho toda segunda-feira, lê o Relatório Focus do Banco Central, calcula o que mudou nas expectativas, pergunta ao Claude o que isso significa, **confere cada número antes de confiar nele** e manda o resultado por e-mail.

**🔗 Artefato público:** https://claude.ai/artifact/DXTbJK26RawubzYJN1vHM3
**🎬 Vídeo (2 min):** _a publicar_

## Equipe

| Nome | Curso / período | Papel no projeto | LinkedIn / GitHub |
|---|---|---|---|
| **Leonardo Tyszler** | _preencher_ | Autor do projeto — concepção, desenvolvimento e verificação | _preencher_ |

## O problema

Toda segunda-feira o Banco Central publica o Relatório Focus, com as expectativas de cerca de 100 instituições para inflação, juros, câmbio e PIB. Em uma gestora, alguém abre o relatório, copia os números para uma planilha, compara com a semana anterior e escreve um resumo para os gestores: trabalho manual, repetitivo e sujeito a erro de digitação.

A demanda da diretora de economia era dupla. Primeiro, automatizar esse resumo. Segundo, responder a uma pergunta que ninguém tinha tempo de investigar: **nos últimos cinco anos, o Focus acertou?**

## A solução

Um agente em Python que executa sete etapas com **um único comando** e está agendado para rodar toda segunda às 10h, depois da divulgação do Focus.

```bash
python avancado/case1_focus/agente_semanal.py
```

A entrega é um e-mail com três partes: o que mudou na semana, uma análise escrita pelo Claude e o histórico de acerto de 2021 a 2025 com gráfico. O mesmo conteúdo vira a [versão web](https://claude.ai/artifact/DXTbJK26RawubzYJN1vHM3), que é o artefato público.

**A descoberta principal:** projetando com 12 meses de antecedência, o Focus subestimou inflação e juros em **todos os cinco anos**, sem exceção — erro médio de +2,34 pp no IPCA e +5,05 pp na Selic. Não é azar, é viés, e tem direção. O erro encolhe conforme o ano avança: no meio do ano cai para +0,33 pp e +0,80 pp. Isso tem consequência prática direta — a projeção para o ano seguinte merece bem menos peso do que a do ano corrente.

## Como funciona

| # | Etapa | O que faz |
|---|---|---|
| 1 | `baixar` | Busca expectativas (API Olinda) e séries realizadas (API SGS) direto do Banco Central. Sem cadastro nem chave. |
| 2 | `calcular` | Mediana, variação na semana e em 4 semanas, dispersão, distância da meta e o histórico de acerto. Tudo vai para `saida/resumo_semana.json`, que é **a única fonte de números** do relatório. |
| 3 | `checar` | Se o Focus estiver desatualizado (>10 dias) ou um valor sair da faixa plausível, o agente **para**, não envia o relatório e manda um e-mail de alerta. |
| 4 | `analisar` | O Claude escreve a análise via Claude Code (`claude -p`), recebendo **apenas o JSON já calculado** — nunca os dados brutos. |
| 5 | `conferir` | Todo número do texto é comparado com o JSON. Se algum não tiver base, o agente pede reescrita (até 2 tentativas) e só envia se passar. |
| 6 | `montar` | Gera o relatório HTML, que é também o corpo do e-mail. |
| 7 | `enviar` | E-mail pelo Gmail, com o gráfico anexado. |

A separação entre as etapas 2 e 4 é deliberada: **o Claude não calcula nada**. Ele recebe números prontos e escreve sobre eles. Isso torna a etapa 5 possível, porque existe uma fonte da verdade contra a qual conferir.

### Arquivos

| Arquivo | O que é |
|---|---|
| [`avancado/case1_focus/agente_semanal.py`](avancado/case1_focus/agente_semanal.py) | O agente: as sete etapas e o fluxo |
| [`avancado/case1_focus/inicio_focus.py`](avancado/case1_focus/inicio_focus.py) | Carga dos dados, séries semanais, acurácia e gráficos |
| [`avancado/case1_focus/prompt_analise.md`](avancado/case1_focus/prompt_analise.md) | O prompt que o Claude recebe junto com o JSON |
| [`avancado/case1_focus/enviar_email.py`](avancado/case1_focus/enviar_email.py) | Envio pelo Gmail, com imagem anexada por `cid:` |
| [`avancado/case1_focus/rodar_agente.cmd`](avancado/case1_focus/rodar_agente.cmd) | Wrapper da tarefa agendada do Windows, com log |
| [`entrega/relatorio_web.html`](entrega/relatorio_web.html) | A versão web do relatório (o artefato público) |
| [`scripts/baixar_dados_bcb.py`](scripts/baixar_dados_bcb.py) | Download das duas APIs do Banco Central |

## Dados usados

Os dados **não vêm prontos**: o próprio agente busca a cada execução nas APIs abertas do Banco Central.

| Fonte | O que traz | Período |
|---|---|---|
| API Olinda — Expectativas de Mercado Anuais | IPCA, Selic, Câmbio e PIB Total; mediana, média, desvio-padrão, nº de respondentes | desde 01/01/2020 |
| API SGS | IPCA mensal (433), IPCA 12m (13522), Selic meta (432), dólar PTAX (1), IBC-Br (24363) | desde 01/01/2020 |

**Dados desta execução:** Relatório Focus de **30/10/2026**, coletado em 06/11/2026.

### Como tratamos os cuidados do case

- **`Data` ≠ `DataReferencia`.** Toda consulta filtra explicitamente o ano de referência. A série semanal é construída por `DataReferencia`, e a data da coleta aparece no cabeçalho do relatório.
- **`baseCalculo` filtrado.** Usamos apenas `baseCalculo = 0` (projeções dos últimos 30 dias), como o relatório oficial. Sem esse filtro cada data apareceria duas vezes.
- **IPCA composto, não somado.** O IPCA anual é `(1+m₁/100)×…×(1+m₁₂/100)−1`. Conferimos contra a série `ipca_12m` (ver abaixo).
- **Selic é a taxa no fim do ano**, não a média — usamos o último valor de dezembro da série 432.
- **PIB ficou de fora da acurácia.** O PIB oficial não está no pacote de séries usado e o IBC-Br é apenas uma aproximação mensal. Preferimos não medir a acertar por aproximação.
- **Toda análise diz a data dos dados.** O relatório e o e-mail declaram de qual Focus estão falando.

## Como verificamos os resultados

### 1. IPCA composto contra uma série independente do próprio BC

O IPCA anual que calculamos vem da composição das 12 variações mensais (série 433). Comparamos com a série `ipca_12m` (13522), que o Banco Central publica separadamente:

| Ano | Nosso cálculo | Série oficial `ipca_12m` | Diferença |
|---|---|---|---|
| 2021 | 10,0611 | 10,06 | 0,0011 |
| 2022 | 5,7848 | 5,79 | 0,0052 |
| 2023 | 4,6211 | 4,62 | 0,0011 |
| 2024 | 4,8313 | 4,83 | 0,0013 |
| 2025 | 4,2644 | 4,26 | 0,0044 |

Bate nos cinco anos. A diferença é o arredondamento da série publicada, que vem com duas casas.

### 2. A conferência pegou um número sem base — e isso mudou o código

Numa execução, a etapa 5 acusou o número `0,15` no texto da análise. A frase era *"ambas com alta de menos de 0,15 em 4 semanas"*, e era **verdadeira** (as variações eram 0,14 e 0,12). Mas `0,15` é o limiar de alerta que está no código, não um dado do JSON: o Claude pegou emprestado um número que o leitor não teria como conferir.

Foi o que motivou implementar a reescrita automática. Hoje o agente devolve o texto ao Claude com a lista de números sem base e pede correção, até duas vezes; se ainda falhar, **não envia** e manda alerta.

### 3. Testamos a reescrita de propósito

Injetamos dois números falsos (`3,77` e `9,99`) num texto e rodamos a conferência: os dois foram detectados, e o texto reescrito voltou com zero suspeitos.

### 4. Um bug na API do Banco Central

O script de download falhava com `HTTP 400 Bad Request`. A causa: a API Olinda só aceita espaços codificados como `%20`, e a biblioteca `requests` os envia como `+`. A correção está em [`scripts/baixar_dados_bcb.py`](scripts/baixar_dados_bcb.py), que agora monta a query manualmente.

### O que ainda não foi verificado

**Não conferimos os números à mão contra o PDF oficial do Relatório Focus** publicado no site do Banco Central. As verificações acima são internas e cruzadas entre séries da própria instituição, o que é forte mas não substitui abrir o boletim e comparar. É o próximo passo de validação.

## Como reproduzir

**Pré-requisitos:** Python 3.10+ e [Claude Code](https://claude.com/claude-code) instalado e logado com um plano pago (o agente usa `claude -p`, sem chave de API).

```bash
pip install -r requirements.txt
```

```bash
python avancado/case1_focus/agente_semanal.py --sem-email
```

Isso roda tudo menos o envio e salva o relatório em `avancado/case1_focus/saida/relatorio_semana.html`.

Para ligar o e-mail, copie `avancado/case1_focus/.env.exemplo` para `.env` na mesma pasta e preencha com uma senha de app do Gmail. **O `.env` nunca vai para o repositório** — o `.gitignore` o ignora.

```bash
python avancado/case1_focus/enviar_email.py
```

```bash
python avancado/case1_focus/agente_semanal.py
```

Outras opções: `--sem-download` reaproveita os CSVs já baixados.

### Agendamento

A tarefa `Termometro do Focus` roda toda segunda às 10h pelo Agendador de Tarefas do Windows, apontando para [`rodar_agente.cmd`](avancado/case1_focus/rodar_agente.cmd), que resolve o PATH e acumula log em `saida/agente.log`.

Dois detalhes que só apareceram testando: o Windows aborta tarefas agendadas quando a máquina está na bateria (`DisallowStartIfOnBatteries`, ligado por padrão) e **reporta sucesso mesmo assim**; e o PATH que a tarefa herda não é o do terminal, então o `claude` não era encontrado. Ambos estão resolvidos.

## Limitações e próximos passos

**Limitações**

- O computador precisa estar **ligado e com o usuário logado** no horário agendado, e o Claude Code precisa estar logado. Se a sessão expirar, a etapa 4 falha — o log registra, mas nenhum e-mail chega.
- Os **limiares de alerta** (`LIMIAR_4S`) ainda são valores arbitrários, não calibrados com o histórico. Um alerta hoje significa "passou de um número que escolhemos", não "isto é estatisticamente anormal".
- A **acurácia cobre só IPCA e Selic**. Câmbio e PIB ficaram de fora pelos motivos descritos acima.
- O **artefato público é uma foto** da semana de 30/10/2026. Ele não se atualiza sozinho: a cada segunda seria preciso republicar no mesmo endereço.
- A conferência da etapa 5 compara **números**, não afirmações. Uma frase logicamente errada feita só com números corretos passaria.

**Próximos passos**

1. Calibrar os limiares com o histórico — por exemplo, dois desvios-padrão das variações de 4 semanas de cada indicador.
2. Conferir os números contra o boletim oficial em PDF.
3. Fazer o agente republicar o artefato a cada execução, mantendo o link.
4. Permitir que cada assinante escolha quais indicadores quer receber.

## Aviso

Projeto acadêmico desenvolvido em workshop. **Não constitui recomendação de investimento.**

Fonte dos dados: Banco Central do Brasil — Relatório Focus (expectativas de mercado) e Sistema Gerenciador de Séries Temporais (valores realizados).

---

**Autor:** Leonardo Tyszler
**Feito com:** Claude Code, Python, pandas, matplotlib

O material original do laboratório está em [README_DO_LAB.md](README_DO_LAB.md).
