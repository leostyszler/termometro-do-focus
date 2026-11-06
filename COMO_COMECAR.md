# Como começar

Guia rápido para o dia do workshop. Dá para fazer tudo em 15 minutos, e o ideal é fazer **antes** do evento.

## 1. O que você precisa (traga no dia)

- **Notebook carregado** (e carregador; vai ter extensão, mas não para todo mundo ao mesmo tempo).
- **Plano pago do Claude** (Pro ou superior), já logado no navegador e no Claude Code. Todos os participantes precisam ter acesso.
- **Conta no GitHub** (grátis, em github.com), já logada.
- **Python 3.10+ e Claude Code instalados**, com as bibliotecas do `requirements.txt`. É obrigatório: todos os cases são feitos com código. Instruções em [avancado/README.md](avancado/README.md).

## 2. Pegar os dados

**Mais simples:** nesta página do repositório, clique em **Code → Download ZIP** e descompacte. Todos os dados dos cases estão na pasta `data/`.

**Se você usa Git:**

```bash
git clone <URL-DESTE-REPOSITORIO>
cd claude-lab-financas-puc2026
```

## 3. Construir com o Claude

Todos os cases seguem o **caminho avançado**: abram o Claude Code na pasta do repositório e partam do código de partida e da trilha de cada case em **[avancado/](avancado/README.md)**. O chat do claude.ai continua útil para entender o problema, ler PDFs e publicar o **artefato** no fim, mas a solução tem que ser construída com código.

**Dicas que fazem diferença:**

- Comece colando o **README do case** e pedindo um **plano de ataque**, antes de pedir o resultado final.
- Descreva **o problema e o resultado que você quer** ("uma apresentação de 6 slides para um diretor, com 3 números-chave"), não só a tarefa ("analisa isso").
- **Confira os números.** Peça ao Claude para mostrar de onde veio cada número e confira pelo menos alguns na fonte. Vocês são responsáveis pelas conclusões.
- Itere: primeira versão simples funcionando → depois melhora.

## 4. Publicar o artefato

Quando o artefato (app, dashboard, relatório) estiver pronto no Claude, use a opção de **publicar/compartilhar** e copie o **link público**. Abra o link numa aba anônima para conferir que qualquer pessoa consegue ver.

## 5. Criar o GitHub do time (sem precisar de linha de comando)

1. No GitHub, clique em **New repository**. Nome sugerido: `claude-lab-<nome-do-time>`. Marque **Public**.
2. Clique em **Add file → Upload files** e suba o que vocês construíram (código, notebooks, prints, o PDF do relatório).
3. Crie o `README.md` a partir do [modelo](modelo-repositorio-time/README.md) e preencha.
4. Coloque no README os links do **vídeo** e do **artefato**.

Se usar Git no terminal:

```bash
git add .
git commit -m "Primeira versão da solução"
git push
```

## 6. Gravar o vídeo de 2 minutos

Qualquer gravador de tela serve (Loom, OBS, gravador do sistema ou celular). Suba no YouTube como **não listado**, ou no Google Drive com acesso "qualquer pessoa com o link". Roteiro em [entrega/CHECKLIST_ENTREGA.md](entrega/CHECKLIST_ENTREGA.md).

## Travou?

Chame um **mentor**. Eles circulam por todas as mesas. Perguntar cedo é mais barato que perder uma hora.
