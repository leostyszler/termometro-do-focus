# Skills de exemplo

Uma **Skill** é uma pasta com um arquivo `SKILL.md` que ensina ao Claude um procedimento repetível, com scripts para a parte que precisa ser exata (cálculos, download de dados). O Claude só carrega a Skill quando o pedido combina com a `description`.

[`bcb-sgs/`](bcb-sgs/SKILL.md) é um exemplo completo: ensina o Claude a buscar séries do Banco Central **rodando um script**, em vez de responder de memória, e a sempre citar a fonte.

## Como usar no Claude Code

Copie a pasta para `.claude/skills/` na raiz do repositório (ou em `~/.claude/skills/` para valer em qualquer projeto):

```bash
mkdir -p .claude/skills
cp -r avancado/skills_exemplo/bcb-sgs .claude/skills/
```

Depois é só pedir, por exemplo: "qual foi o IPCA acumulado em 12 meses no último dado disponível?"

## Desafio da tarde

Criem a Skill do **seu** case, por exemplo:
- `focus-semanal`: roda o termômetro e escreve o relatório no formato do time;
- `ata-copom`: extrai, compara e classifica o tom de uma ata nova;
- `apresentacao-resultados`: extrai, verifica e monta os slides no padrão da casa.

Uma boa Skill diz **quando** usar, **o passo a passo**, **o que nunca fazer** (ex.: inventar números) e **como verificar** o resultado.
