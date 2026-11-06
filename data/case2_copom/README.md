# Case 2 — Tradutor do Copom

Claude Lab · Economia & Finanças · PUC-Rio · 06/11/2026

## Contexto

A cada 45 dias o Comitê de Política Monetária (Copom) decide a Selic e, alguns dias depois, publica uma **ata** explicando o raciocínio. O mercado lê cada ata palavra por palavra: uma troca de "vigilante" por "atento", ou um parágrafo novo sobre câmbio, pode mexer nos juros futuros. Mas as atas são longas, técnicas e parecidas entre si, e é difícil ver **o que mudou** e **o que isso significa**.

Neste case, vocês são o time de análise de um banco que precisa traduzir as atas para quem decide.

## A demanda

> **De:** Economista-chefe
> **Para:** time de análise
> **Assunto:** Leitura das atas do Copom
>
> "No dia em que sai uma ata, preciso entender em poucos minutos se o Banco Central ficou mais duro ou mais brando, o que mudou em relação à ata anterior e o que isso pode significar para os juros. Não aceito resumo sem fonte: **toda conclusão tem que vir com o trecho exato da ata que a sustenta**. E quero poder fazer perguntas sobre as atas sem ter que ler o documento inteiro."

## Resultado esperado

Um **site** (web app) que interprete o tom do Banco Central e mostre, de forma que um leigo entenda:

1. **Um índice de tom**: uma nota para cada ata, numa régua de −2 (muito brando, *dovish*) a +2 (muito duro, *hawkish*), e como ela evoluiu nas últimas 6 reuniões;
2. **O que mudou**: as principais diferenças da ata mais recente em relação à anterior;
3. **O principal impacto**: o que essa mudança pode significar para a Selic, os juros futuros, o câmbio ou as expectativas do mercado;
4. **Um chat com as atas**: o usuário sobe uma ata recente ou faz perguntas ("o que o Copom disse sobre câmbio?") e o Claude responde com base nos documentos.

**Evidência é obrigatória em tudo**: cada nota de tom, cada mudança e cada resposta do chat cita o **nº do parágrafo e o trecho exato** da ata. Sem trecho, não vale.

O site é o **artefato** que o time entrega (ver [regras](../../REGRAS_E_AVALIACAO.md)), construído com código (Python + Claude Code).

> A diferença para os outros cases: o Case 1 é um fluxo automático que manda e-mail; o Case 3 é uma apresentação para a diretoria. Aqui o produto é um **site para entender e conversar com as atas**.

## Os dados

As **6 atas mais recentes** do Copom publicadas antes do workshop **já estão no repositório**, na pasta [`atas/`](atas/):

| Arquivo | Reunião | Data da reunião | Decisão |
|---|---|---|---|
| [`ata_276_2026-01-28.pdf`](atas/ata_276_2026-01-28.pdf) | 276ª | 27 e 28/01/2026 | manteve a Selic em 15,00% |
| [`ata_277_2026-03-18.pdf`](atas/ata_277_2026-03-18.pdf) | 277ª | 17 e 18/03/2026 | reduziu para 14,75% |
| [`ata_278_2026-04-29.pdf`](atas/ata_278_2026-04-29.pdf) | 278ª | 28 e 29/04/2026 | reduziu para 14,50% |
| [`ata_279_2026-06-17.pdf`](atas/ata_279_2026-06-17.pdf) | 279ª | 16 e 17/06/2026 | reduziu para 14,25% |
| [`ata_280_2026-08-05.pdf`](atas/ata_280_2026-08-05.pdf) | 280ª | 4 e 5/08/2026 | reduziu para 14,00% |
| [`ata_281_2026-09-16.pdf`](atas/ata_281_2026-09-16.pdf) | 281ª | 15 e 16/09/2026 | reduziu para 13,75% |

Fonte: Banco Central do Brasil, [Atas do Copom](https://www.bcb.gov.br/publicacoes/atascopom). Cada ata é publicada alguns dias depois da reunião; a data de publicação está na página do BC (ver cuidado nº 1).

> **Bônus do dia:** a ata da reunião desta semana (282ª) deve ser publicada na própria sexta, 06/11. Se sair a tempo, baixem e testem o site com ela: é o uso real do produto, uma ata nova chegando.

**A Selic e as expectativas** (usadas no passo 5):

- **Selic meta realizada:** [histórico das taxas de juros](https://www.bcb.gov.br/controleinflacao/historicotaxasjuros) no site do Banco Central (ou série 432 do SGS);
- **Expectativas de Selic do mercado:** [Relatório Focus](https://www.bcb.gov.br/publicacoes/focus), publicado toda segunda-feira.

O script `scripts/baixar_dados_bcb.py` baixa a Selic e o Focus de uma vez (gera `sgs_realizado.csv` e `focus_anuais.csv` em `data/case1_focus/`).

**Onde guardar as atas.** O agente só responde bem se tiver as atas à mão. Definam um lugar fixo:

- **pasta local** `data/case2_copom/atas/`: as atas já estão lá, e é onde os scripts procuram;
- para o **chat**, as mesmas atas (ou o texto extraído delas) ficam disponíveis para o Claude consultar: num **Projeto do claude.ai** (como conhecimento do projeto), numa pasta do Google Drive conectada ao Claude ou embutidas no próprio site.

## Guia sugerido

O guia é uma sugestão de caminho, não uma receita. O que importa é entregar o resultado esperado, com evidências.

### 1. Entender a ata

Antes de medir qualquer coisa, o time precisa saber ler uma ata. Suba a ata mais recente no Claude e peça:

> "Explique a estrutura desta ata do Copom, seção por seção. Em quais seções o Banco Central costuma sinalizar os próximos passos da Selic? Dê exemplos de frases que indicam um tom mais duro e um tom mais brando, citando o nº do parágrafo."

Ao final, o time deve saber onde ficam a avaliação do cenário, o balanço de riscos e a decisão com a orientação para as próximas reuniões. É ali que o tom aparece com mais força.

### 2. Definir a régua do índice

Esta é a decisão mais importante do case, e a banca vai perguntar sobre ela. Sugestão de régua, aplicada **parágrafo a parágrafo**:

| Nota | Significado | Exemplo de sinal |
|---|---|---|
| +2 | muito duro | indica alta de juros ou juros altos "por período prolongado", com ênfase |
| +1 | duro | preocupação com inflação, expectativas desancoradas, riscos para cima |
| 0 | neutro | descrição de dados e fatos, sem sinalização |
| −1 | brando | inflação cedendo, atividade desacelerando, riscos para baixo |
| −2 | muito brando | indica corte de juros com ênfase |

Depois, decidam **como juntar os parágrafos num número por ata**. A média simples é o ponto de partida, mas parágrafos neutros diluem o sinal. Testem ignorar as notas 0 ou dar peso maior à seção da decisão. Escrevam a régua e a regra de agregação no README do time.

### 3. Medir o tom das 6 atas e conferir

Peçam ao Claude para classificar cada parágrafo das 6 atas com a régua, sempre com **nº do parágrafo, nota e o trecho exato que justifica a nota**, e para calcular o índice de cada ata.

Antes de confiar no índice, **validem**: o time classifica 10 parágrafos à mão, sem olhar a resposta do Claude, e compara. Confiram também se os trechos citados existem de verdade na ata (o Claude pode parafrasear achando que está citando). Onde discordarem, ajustem a régua e rodem de novo.

### 4. Encontrar o que mudou

Comparem a ata mais recente com a anterior: parágrafos novos, removidos e alterados (palavras trocadas). Escolham as **3 mudanças mais relevantes** e, para cada uma, registrem o nº do parágrafo, o **trecho exato** (curto) e o efeito no índice: endureceu ou suavizou?

> "Compare a ata nova com a anterior. Liste parágrafos novos, removidos e alterados, citando o nº do parágrafo e o trecho exato. Depois aponte as 3 mudanças que mais alteram o tom e explique por quê."

### 5. Interpretar o principal impacto

Para a mudança mais relevante, respondam: **o que ela sinaliza para a próxima decisão da Selic?** Usem os dados para fundamentar:

- a trajetória da **Selic meta**: o tom acompanhou o que o Copom fez depois?
- as **expectativas de Selic do Focus**: o mercado já esperava essa mudança? As expectativas se moveram depois da ata?

Escrevam o "principal impacto" em 2 ou 3 frases simples, citando os canais (Selic, juros futuros, câmbio, crédito e consumo, inflação esperada) e usando linguagem condicional ("sinaliza", "pode"). Interpretação não é previsão.

### 6. Montar o site com o chat

Gerem o site **a partir dos resultados dos passos anteriores** (por exemplo, um JSON com índice, mudanças, impacto e trechos), não de memória. Uma estrutura que funciona:

1. **Topo:** a última reunião, a decisão e o índice atual, num "termômetro" do tom;
2. **Gráfico:** o índice nas 6 reuniões, com a Selic meta ao lado;
3. **O que mudou:** as 3 mudanças, com nº do parágrafo, trecho exato e efeito no tom;
4. **Principal impacto:** o texto do passo 5;
5. **Pergunte às atas:** o chat, em que o usuário faz perguntas ou sobe uma ata nova e recebe respostas sempre com o trecho de onde tirou;
6. **Como medimos:** a régua, a regra de agregação e como o time conferiu;
7. **Rodapé:** fonte (Banco Central do Brasil, atas do Copom, datas) e aviso de que não é recomendação de investimento.

Para o chat funcionar **dentro do plano pago, sem chave de API**, o caminho mais simples é publicar o site como um **artefato do claude.ai que usa o próprio Claude para responder** (peçam ao Claude um "artefato com IA" e passem o texto das atas para ele). Testem o chat com perguntas cuja resposta vocês já sabem.

### Ritmo sugerido no dia

| Momento | Passos |
|---|---|
| Manhã (10h30–13h00) | 1 a 4: régua definida, índice das 6 atas conferido e mudanças identificadas |
| Tarde (14h00–16h00) | 5 e 6: impacto escrito, site com o chat publicado, vídeo gravado |

## Como resolver com código

O script do Banco Central baixa a Selic e o Focus, outros scripts extraem as atas, geram o diff e classificam os parágrafos automaticamente, e o site é montado a partir desses resultados. Código de partida e trilha em **[avancado/case2_copom](../../avancado/case2_copom/README.md)**.

## Cuidados com os dados

1. **Data da reunião ≠ data da ata.** A decisão sai no dia da reunião; a ata é publicada alguns dias depois. Para medir reação de mercado, isso importa.
2. **Mudança de tom não é mudança de juros.** Uma ata pode manter a Selic e endurecer muito o discurso. Separe "o que decidiram" de "como falaram".
3. **Sem trecho, não vale.** Toda nota, mudança e resposta do chat precisa do nº do parágrafo e do trecho exato. Confiram se o trecho existe mesmo na ata.
4. **Trechos curtos.** Citem só o necessário para sustentar a conclusão e linkem a ata original (ver [uso dos dados](../../USO-DOS-DADOS.md)).
5. **Selic no Focus é a taxa esperada para o fim do ano**, não a da próxima reunião. Leiam com cuidado antes de dizer "o mercado esperava".
6. **Impacto é interpretação, não previsão.** Fundamentem nos dados e no texto, deixem claro o que é hipótese e coloquem o aviso de que não é recomendação de investimento.

## O que a banca vai olhar neste case

- O impacto usa a **Selic e o Focus** para se fundamentar, citando a data dos dados?
- A régua do índice é clara e o resultado é **reprodutível**?
- Toda conclusão tem **evidência**: nº do parágrafo e trecho exato que existe de fato na ata?
- O **chat** responde certo e sempre mostra de onde tirou a resposta?
- O site é claro para quem não é economista?

## Perguntas para atacar

- O tom endureceu ou suavizou ao longo das 6 reuniões? O índice antecipou o que a Selic fez depois?
- As expectativas de Selic do Focus se moveram depois das atas mais duras?
- Qual seção da ata mais mexe no índice?
- Que perguntas um investidor faria ao chat? O chat responde bem a elas?
