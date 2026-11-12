# Terra à Vista: Reels e Stories sobre endividamento (v2)

Palavra-chave da campanha: **TERRA**. Quem comenta TERRA num Reel ou manda TERRA por mensagem recebe no direct o link terra.oceanosistemas.com.br.

## Reels (9:16, com trilha original)

### Reel 1: reel-notificacoes.mp4 (19 s)
Gancho: notificações de cobrança chegando uma atrás da outra, a tela treme, aparece "PARA." e o vídeo vira a rota.

Legenda:
"""Se o seu celular parece isso, respira.

Você não precisa pagar tudo hoje. Precisa de uma rota:
1. Liste todas as dívidas e cartões
2. Compare Bola de Neve e Avalanche
3. Siga as missões da semana

O Terra à Vista faz isso com você, no celular e de graça.

💬 Comente TERRA que eu te mando o link no direct.

App gratuito. Não oferece empréstimos.

#sairdasdividas #dividas #endividamento #educacaofinanceira #financaspessoais #cartaodecredito #nomesujo #organizacaofinanceira"""

### Reel 2: reel-juros.mp4 (20 s)
Gancho: R$ 1.000 no cheque especial, com um contador que sobe mês a mês até R$ 2.518.

Legenda:
"""R$ 1.000 esquecidos no cheque especial viram R$ 2.518 em 12 meses.

Juros sobre juros: cada mês sem plano custa mais caro que o anterior.

No Terra à Vista você coloca as suas dívidas, compara Bola de Neve e Avalanche e vê quanto tempo leva para quitar em cada caminho.

💬 Comente TERRA e receba o link do app grátis no direct.

Exemplo ilustrativo: 8% ao mês (teto do cheque especial para pessoa física e MEI), juros compostos, sem nenhum pagamento. As taxas variam por banco.

#chequeespecial #juros #sairdasdividas #dividas #educacaofinanceira #financaspessoais #planejamentofinanceiro"""

### Reel 3: reel-empresario.mp4 (20 s)
Gancho: "A dívida da empresa foi parar no seu CPF?", checklist marcando e o dado da Serasa.

Legenda:
"""Cartão pessoal pagando fornecedor. Empréstimo no seu nome para cobrir o caixa. Cheque especial todo mês.

Se você marcou um desses, a dívida da empresa já está no seu CPF.

Você não está sozinho: o Brasil chegou a 9,3 milhões de empresas inadimplentes, recorde da série (Serasa Experian, agosto de 2026).

Sair começa por enxergar tudo. O Terra à Vista organiza as dívidas e cartões no seu nome e mostra, passo a passo, a rota até quitar.

💬 Comente TERRA e receba o link no direct.

App gratuito. Não oferece empréstimos.

#empreendedor #pequenasempresas #dividas #endividamento #sairdasdividas #fluxodecaixa #gestaofinanceira #joaopessoa"""

## Stories (9:16, sem legenda)

| Arquivo | Formato | Ideia |
|---|---|---|
| story-1-quiz-renda.jpg | Quiz | "Quanto da sua renda vai para dívidas?" A/B/C/D por mensagem. Dica: no app do Instagram, coloque o adesivo de enquete ou teste por cima. |
| story-2-84-milhoes.jpg | Dado | 84,2 milhões de inadimplentes (Serasa, 2026) + "Mande TERRA por mensagem" |
| story-3-bola-avalanche.jpg | Este ou este | Bola de Neve × Avalanche, vota A ou B |
| story-4-empresario.jpg | Dor do empresário | "Se a empresa paga com o seu cartão, a dívida é sua." |
| story-5-cta-terra.jpg | Chamada | TERRA em destaque, mande por mensagem |
| story-6-direct-animado.mp4 | Vídeo de 9 s | Mostra alguém digitando TERRA no direct e recebendo o link na hora |

Sequência sugerida no mesmo dia: 1 → 3 → 2 → 4 → 6 → 5.

## Automação da palavra TERRA (o "robô" do direct)

A Windsor publica posts, mas **não envia DMs**. Então a resposta automática precisa de uma destas opções:

1. **ManyChat**: em Automations, crie um gatilho de comentário com a palavra TERRA em qualquer post e outro de DM com a palavra TERRA. Na resposta, mande o link terra.oceanosistemas.com.br. É o caminho mais rápido.
2. **Seu webhook próprio** (oceanos-instagram-webhook.js, que você já tem e que dispara DM a partir de comentário): é só cadastrar TERRA como palavra-chave e o link como resposta.
3. **Meta Business Suite** (Caixa de entrada → Automações → palavras-chave personalizadas): cobre a palavra enviada por DM. Não confirmei se cobre comentários.

Texto sugerido da DM:
"""Oi! Aqui está o seu link do Terra à Vista, o app gratuito para organizar as dívidas e ver a rota até quitar: https://terra.oceanosistemas.com.br

Comece pelo diagnóstico financeiro, que leva poucos minutos. Bons ventos! ⛵"""

Regra do Instagram: a resposta privada a um comentário só pode ser enviada até 7 dias depois do comentário.

Fontes dos dados:
- Serasa Experian, inadimplência das empresas, agosto de 2026: https://www.serasaexperian.com.br/sala-de-imprensa/indicadores/novo-recorde-inadimplencia-das-empresas-chegou-a-93-milhoes-em-agosto-revela-serasa-experian/
- Serasa, 84,2 milhões de inadimplentes: https://www.band.com.br/economia/macroeconomia/inadimplencia-atinge-recorde-de-842-milhoes-de-pessoas-no-brasil-diz-serasa
