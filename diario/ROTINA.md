# Rotina do post diário — @oceanosistemas

Linha editorial nova, a partir de 14/11/2026. O dono pediu para trocar a propaganda e os carrosséis por notícias do mercado e dicas de vendas, publicadas no automático.

- **Nunca publicar carrossel.** Use só post de 1 imagem (`create_image_post`) ou Reel (`create_video_post`).
- **Duas publicações por dia** (fuso America/Fortaleza). Cada uma vem de uma tarefa agendada:
  - **MANHÃ** (07:47): notícia de mercado ou dado do dia, que aponta uma solução Oceanos.
  - **NOITE** (18:53): dica de vendas tirada de um livro conhecido, com crédito ao autor.
- **Valor primeiro, produto depois.** O produto entra numa linha da arte ("SOLUÇÃO") e numa linha da legenda, no máximo. Em pelo menos 1 de cada 3 posts da noite, não cite produto nenhum.

## Calendário por dia da semana

| Dia | MANHÃ (imagem) | NOITE |
|---|---|---|
| Seg | Notícia + solução (`tipo: noticia`) | Dica de vendas, imagem |
| Ter | Dado do dia (`tipo: dado`) | Dica de vendas, **REEL** |
| Qua | Notícia + solução | Dica de vendas, imagem |
| Qui | Dado do dia | Dica de vendas, **REEL** |
| Sex | Notícia + solução, **REEL** | Dica de vendas, imagem |
| Sáb | Notícia mais forte da semana | Dica de vendas, **REEL** |
| Dom | Dado do dia | Dica de vendas, imagem |

Gire os temas da manhã e não repita o mesmo tema em dois dias seguidos. Para saber o que já saiu, veja `diario/historico.csv`. Os temas:

1. Reforma tributária: CBS, IBS, Imposto Seletivo, Simples híbrido, prazos de 2026 e 2027, split payment, NF-e.
2. Endividamento e inadimplência de empresas e famílias: Serasa, CNC/Peic, Banco Central.
3. Juros, Selic e crédito para PME: Copom, Pronampe, taxa média do cartão e do capital de giro.
4. Varejo, consumo e vendas do comércio: IBGE/PMC, CNC, ICVA, datas como a Black Friday e o Natal.
5. Controle financeiro e gestão: mortalidade de empresas (Sebrae/IBGE), margem, capital de giro, estoque.
6. Restaurantes e food service, supermercados e farmácias: Abrasel, Abras, Abrafarma.

## Regras de verdade (obrigatórias)

- Cada notícia ou dado precisa de **fonte confiável publicada nos últimos 10 dias**. Valem: órgão oficial (IBGE, Banco Central, Receita, Ministério da Fazenda, Agência Brasil, Agência Gov), Serasa Experian, Boa Vista, CNC, Sebrae, CNDL/SPC e veículos grandes (Valor, Folha, Estadão, O Globo, G1, InfoMoney, Exame, CNN Brasil).
- **Confira cada número na fonte primária ou em duas fontes independentes**, e copie o número exatamente como foi publicado. Se não der para confirmar, troque de notícia. Na dúvida, não publique o número.
- A arte sempre traz a linha `fonte` com o órgão, o mês de referência e a data da divulgação.
- Não invente resultado de cliente, depoimento, número da Oceanos nem função de produto. Use **só** as funções da ficha abaixo.
- Livros: **parafraseie** a ideia e dê o crédito (livro + autor). Não copie trechos. Uma frase curta e conhecida, entre aspas, no máximo. Só use um livro se tiver certeza do autor e da ideia. Se o dono citar um título que você não conhece com segurança (por exemplo, "Vendedor 3.0"), pesquise antes. Se não confirmar, não use.
- Imposto e reforma: escreva "estimativa", "segundo a LC 214/2025" etc. Não dê conselho tributário individual.
- Sem política partidária e sem ataque a pessoas ou empresas.

## Ficha dos produtos (funções comprovadas, não acrescente nada)

- **Oceanos Financeiro**: importa extrato OFX e CSV, faz conciliação bancária, monta DRE e fluxo de caixa automáticos, lê a fatura do cartão do PDF e guarda várias empresas e as finanças pessoais num lugar só. Integra com Asaas, Banco Cora e Domínio. Teste de 40 dias grátis, sem cartão.
- **Preço Certo**: forma o preço de venda a partir do XML da nota. Valida o NCM na base da Receita, calcula IBS e CBS com a calculadora oficial e soma ICMS, ST e MVA de compra interestadual. Atende Simples, Simples híbrido e Lucro Presumido e monta até 3 tabelas (consumidor, revenda, atacado). Mostra o preço de hoje e a estimativa de 2027, em PDF ou Excel. Teste de 7 dias grátis.
- **Ficha Pro** (restaurantes): ficha técnica com sub-receitas, preço com markup e impostos, estoque FEFO, CMV real. A IA monta a ficha a partir da receita falada. Importa o XML da nota e consulta NCM e CEST. Teste de 7 dias grátis.
- **Oceano de Compras**: classificação ABC × XYZ, alerta de pré-ruptura com o prazo do fornecedor, perda em R$ por item zerado, cotação às cegas. Teste de 7 dias grátis.
- **CRM Oceanos**: WhatsApp Business integrado ao funil, funil Kanban, até 5 usuários, ranking gamificado da equipe. R$ 300/mês. Teste de 7 dias grátis.
- **Plano de Negócios**: 8 etapas guiadas, IA consultiva que revisa cada etapa, projeções com DRE, VPL e TIR, PDF executivo. R$ 29,90/mês.
- **Terra à Vista** (pessoa física, grátis): organiza dívidas e cartões, simulador Bola de Neve × Avalanche, missões semanais. Não oferece empréstimo.

Qual produto combina com cada tema:

| Tema | Produto |
|---|---|
| Inadimplência, caixa, juros | Oceanos Financeiro |
| Reforma, imposto, preço, margem | Preço Certo |
| Estoque, varejo, supermercado, farmácia | Oceano de Compras |
| Restaurante | Ficha Pro |
| Vendas, WhatsApp, equipe, follow-up | CRM Oceanos |
| Abrir negócio, crédito no banco | Plano de Negócios |
| Dívida pessoal do empreendedor | Terra à Vista |

## Banco de livros para as dicas de vendas

Gire os livros e não repita o mesmo livro na mesma semana. Cada dica tem três partes:

1. Uma técnica.
2. Um exemplo de fala para o balcão ou o WhatsApp de um pequeno negócio.
3. Um "faça hoje".

| Livro | Autor | Ideias para usar |
|---|---|---|
| As Armas da Persuasão | Robert Cialdini | Reciprocidade, compromisso e coerência, prova social, afeição, autoridade, escassez (e, na edição nova, unidade). |
| Alcançando Excelência em Vendas: SPIN Selling | Neil Rackham | Perguntas de Situação, Problema, Implicação e Necessidade de solução. Nas vendas grandes, pergunte mais do que fale. |
| Vendedor Pitbull | Thiago Concer | Persistência com método, follow-up, ritmo de prospecção e atitude do vendedor. |
| Como Fazer Amigos e Influenciar Pessoas | Dale Carnegie | Interesse sincero pelo outro, usar o nome da pessoa, ouvir mais, nada de crítica. |
| A Bíblia de Vendas / O Livro Vermelho de Vendas | Jeffrey Gitomer | As pessoas adoram comprar e odeiam que empurrem; o cliente compra o vendedor; valor antes de preço. |
| Negocie como se sua Vida Dependesse Disso | Chris Voss | Espelhamento, rotular emoções, perguntas calibradas ("como eu faço isso?"), o "não" que abre a conversa. |
| A Venda Desafiadora (The Challenger Sale) | Matthew Dixon e Brent Adamson | Ensinar algo novo ao cliente, adaptar a conversa e assumir o controle. |
| Receita Previsível | Aaron Ross | Especializar prospecção, venda e pós-venda; funil medido. |
| A Psicologia de Vendas | Brian Tracy | Autoconceito do vendedor, fechamento por alternativa, metas diárias. |
| Gatilhos Mentais | Gustavo Ferreira | Urgência, novidade e porquê. Use com ética e sem urgência falsa. |
| A Arte da Guerra | Sun Tzu (domínio público) | Conhecer o cliente e o concorrente, escolher onde competir. |

## Modelo de legenda (até ~1.300 caracteres)

1. **Linha 1, o gancho**: fato surpreendente, número ou pergunta. Até 90 caracteres, sem emoji no começo.
2. Linha em branco, depois 3 a 6 linhas curtas com o contexto ("O que isso significa para você").
3. "O que fazer:" seguido de 2 ou 3 ações práticas.
4. Uma linha com o produto, quando couber. Exemplo: "No Oceanos Financeiro você vê isso no fluxo de caixa sem planilha."
5. Chamada para ação variada, uma por post. Opções: "Salve para não esquecer", "Mande para o seu sócio", "Comente CAIXA que eu te mando o teste grátis", "Link na bio".
6. Notícia ou dado: "Fonte: …" na legenda também.
7. De 5 a 8 hashtags: 2 amplas (#empreendedorismo #pequenasempresas), 3 a 4 do tema e 1 ou 2 locais (#joaopessoa #paraiba #nordeste).

## Especificação da arte (`render.py`)

Grave `diario/posts/AAAA-MM-DD-manha.json` ou `diario/posts/AAAA-MM-DD-noite.json` e rode:

```
python3 -I diario/render.py diario/posts/AAAA-MM-DD-SLOT.json diario/posts/AAAA-MM-DD-SLOT [--reel]
```

O comando gera o `.jpg` (1080x1350) e, com `--reel`, também o `.mp4` (1080x1920, 9 s, trilha original). Campos do JSON:

| Campo | O que vai |
|---|---|
| `tipo` | `noticia`, `dado` ou `vendas` |
| `etiqueta` | Manhã: "Radar do Empresário · DD/MM" ou "Dado do dia · DD/MM". Noite: "Lição de vendas · Nome do livro". |
| `titulo` | Gancho de até 70 caracteres. Marque 1 ou 2 palavras com `*asteriscos*` para destacar. |
| `numero` e `numero_legenda` | Opcionais; use quando houver um número forte. |
| `corpo` | De 1 a 3 frases curtas, de até 55 caracteres cada. |
| `solucao` | Opcional: uma frase com o produto entre `*asteriscos*`. |
| `fonte` | Na notícia ou no dado: "Fonte: órgão, referência, divulgado em DD/MM/AAAA". Na dica: "Baseado em <Livro>, de <Autor>". |
| `rodape` | Uma chamada para ação curta. |

**Abra o JPG com Read e confira** se o texto coube, sem corte nem sobreposição. Se não couber, encurte o texto e gere de novo.

## Passo a passo de cada execução

1. Veja a data e a hora em America/Fortaleza e defina o SLOT (manha ou noite), o dia da semana e o formato pelo calendário.
2. Se `diario/historico.csv` já tem uma linha com esta data e este SLOT com status `publicado`, não faça nada (evita publicar duas vezes).
3. Pesquise (WebSearch) e confirme os fatos (regras de verdade). Na noite, escolha livro e técnica que não aparecem no histórico dos últimos 7 dias.
4. Escreva o JSON da arte e a legenda. Grave a legenda em `diario/posts/AAAA-MM-DD-SLOT.txt`. Gere a arte e confira o JPG.
5. Commit e push no `main`: `git add diario && git commit -m "Post diário AAAA-MM-DD SLOT" && git push origin main`. Se o push falhar, faça `git pull --rebase origin main` e tente de novo.
6. URL pública: `https://raw.githubusercontent.com/arnaldopoggi/fichapro-midia/main/diario/posts/<arquivo>`. Confira com `curl -sI` se responde HTTP 200. Se ainda não responder, espere 30 s e tente de novo, até 5 vezes.
7. Publique pela Windsor.ai (`mcp__Windsor_ai__execute_action`, connector `instagram`, account `17841464906332474`), **uma vez só**:
   - Imagem: `create_image_post` com `image_url` e `caption`.
   - Reel: `create_video_post` com `video_url`, `caption`, `share_to_feed: true` e `thumb_offset: 8000`.
8. Acrescente a linha em `diario/historico.csv` (`data,slot,tipo,tema_ou_livro,titulo,formato,media_id,status`), faça commit e push.
9. Erros:
   - **Permissão** (instagram_content_publish): notifique o dono para reconectar a conta Oceanos em https://onboard.windsor.ai/app/instagram com "Connect with Facebook instead", permitindo todas as permissões. Não tente outro caminho.
   - Qualquer outra falha: registre `erro` no histórico e notifique com o erro exato. Não publique conteúdo de outro dia para compensar.
   - Deu certo: não notifique; só escreva o resumo curto no fim.
