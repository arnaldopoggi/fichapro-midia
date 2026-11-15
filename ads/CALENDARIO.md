# Campanha Gatilhos de vendas — calendário de posts

BASE = https://raw.githubusercontent.com/arnaldopoggi/fichapro-midia/criativos-trafego-pago/ads/

Cada dia: create_image_post com a imagem BASE + caminho e a legenda entre aspas triplas, exatamente como está.

CALENDÁRIO abaixo. Se a data não está no calendário (antes de 16/11/2026 ou depois de 09/12/2026), não publique nada. Se já passou de 09/12/2026, notifique o dono (PushNotification) que a campanha "Gatilhos de vendas" terminou e que ele pode desativar esta tarefa agendada.
PASSO 2: antes de publicar, confira com curl -sI que a URL da peça responde HTTP 200. Use sempre a URL raw abaixo.
PASSO 3: publique exatamente a peça do dia, com a legenda exatamente como está aqui (não reescreva). Publique uma vez só. Não publique peças de outros dias, nem para compensar um dia que falhou.
PASSO 4: termine com um resumo curto em português: o que foi publicado e o ID. Se deu certo, não notifique. Se falhou (inclusive URL sem HTTP 200), notifique (PushNotification) com o erro exato. Se o erro for de permissão (instagram_content_publish), diga ao dono que ele precisa reconectar a conta Oceanos em https://onboard.windsor.ai/app/instagram usando "Connect with Facebook instead" e permitindo todas as permissões. Nunca tente contornar o erro por outro caminho.

URL base (ramo criativos-trafego-pago do repositório fichapro-midia):
BASE = https://raw.githubusercontent.com/arnaldopoggi/fichapro-midia/criativos-trafego-pago/ads/

CALENDÁRIO

16/11/2026 — POST (create_image_post): BASE + ficha-pro/ad-01-perda.jpg
Legenda:
"""Seu prato mais vendido pode estar dando prejuízo.

Quem vende muito de um prato com o custo mal calculado perde um pouco em cada pedido. O Ficha Pro monta a ficha técnica com sub-receitas e calcula o preço com markup e impostos.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

17/11/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-01-dor.jpg
Legenda:
"""Vendeu bem e o dinheiro sumiu?

Venda não é caixa. Sem ver entradas e saídas, o mês fecha e ninguém sabe para onde foi o dinheiro. No Oceanos Financeiro você importa o extrato e vê fluxo de caixa e DRE, sem planilha.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

18/11/2026 — POST (create_image_post): BASE + terra-a-vista/ad-01-alivio.jpg
Legenda:
"""Dívida não se resolve no susto. Se resolve com rota.

O Terra à Vista organiza dívidas e cartões e mostra, passo a passo, o caminho até quitar.

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

19/11/2026 — POST (create_image_post): BASE + preco-certo/ad-01-perda.jpg
Legenda:
"""Preço no chute é lucro indo embora.

Preço certo leva em conta custo, impostos, despesas e margem. O Preço Certo faz essa conta a partir do XML da nota.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""

20/11/2026 — POST (create_image_post): BASE + ficha-pro/ad-02-curiosidade.jpg
Legenda:
"""Quanto sobra de cada prato que sai da cozinha?

Se a resposta é "mais ou menos", falta ficha técnica. No Ficha Pro você vê o custo de cada prato, com sub-receitas, e o CMV real.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

21/11/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-02-facilidade.jpg
Legenda:
"""Importe o extrato. O DRE sai pronto.

O Oceanos Financeiro lê o extrato em OFX ou CSV, faz a conciliação bancária e monta DRE e fluxo de caixa automáticos.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

22/11/2026 — POST (create_image_post): BASE + terra-a-vista/ad-02-juros.jpg
Legenda:
"""R$ 1.000 esquecidos no cheque especial viram R$ 2.518 em 12 meses.

Juros sobre juros: cada mês sem plano custa mais caro que o anterior. No Terra à Vista você coloca as suas dívidas e vê quanto tempo leva para quitar.

Exemplo ilustrativo: 8% ao mês, juros compostos, sem nenhum pagamento. As taxas variam por banco.

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

23/11/2026 — POST (create_image_post): BASE + preco-certo/ad-02-compra-fora.jpg
Legenda:
"""Comprou mercadoria de outro estado?

Então tem ICMS ou ST nessa compra, e ele quase sempre fica fora da conta do preço. O Preço Certo lê o XML da nota, identifica a origem e soma ICMS, ST e MVA.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""

24/11/2026 — POST (create_image_post): BASE + ficha-pro/ad-03-facilidade.jpg
Legenda:
"""Fale a receita. A IA monta a ficha.

Você conta como faz o prato e o Ficha Pro organiza ingredientes, quantidades e custos.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

25/11/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-03-risco-zero.jpg
Legenda:
"""7 dias grátis para testar.

Importe o extrato, concilie e veja o DRE da sua empresa antes de decidir.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

26/11/2026 — POST (create_image_post): BASE + terra-a-vista/ad-03-escolha.jpg
Legenda:
"""Bola de Neve ou Avalanche?

❄️ Bola de Neve: quita primeiro a menor dívida.
🏔️ Avalanche: quita primeiro a dívida mais cara.

No Terra à Vista, o simulador compara os dois com os seus números. Qual você escolheria?

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

27/11/2026 — POST (create_image_post): BASE + preco-certo/ad-03-exemplo.jpg
Legenda:
"""R$ 28,00 na nota. Mais R$ 3,64 de ICMS que ninguém viu.

Exemplo do simulador: camiseta comprada em SP, empresa no Simples Nacional. Se isso não entra no preço, sai do seu lucro.

Exemplo ilustrativo: os resultados variam de empresa para empresa e não substituem o contador.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""

28/11/2026 — POST (create_image_post): BASE + ficha-pro/ad-04-risco-zero.jpg
Legenda:
"""7 dias grátis, sem cartão.

Comece pela ficha do seu prato principal: ingredientes, sub-receitas, impostos e markup. Dá tempo de conferir o preço dos pratos que mais saem.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

29/11/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-04-preco.jpg
Legenda:
"""Financeiro completo por ≈ R$ 82/mês.

Plano anual de R$ 987, sem fidelidade, com integração Asaas, Banco Cora e Domínio.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

30/11/2026 — POST (create_image_post): BASE + terra-a-vista/ad-04-primeiro-passo.jpg
Legenda:
"""O primeiro passo é enxergar tudo.

Liste todas as dívidas e cartões em um lugar só. O Terra à Vista começa por um diagnóstico financeiro grátis.

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

01/12/2026 — POST (create_image_post): BASE + preco-certo/ad-04-facilidade.jpg
Legenda:
"""Arraste o XML da nota. O preço sai pronto.

O Preço Certo preenche produto, NCM, custo e origem. Você informa o regime e as margens.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""

02/12/2026 — POST (create_image_post): BASE + ficha-pro/ad-05-insumo.jpg
Legenda:
"""O insumo subiu. Seu preço subiu junto?

Quando o custo muda e o cardápio não, a diferença sai da sua margem. O Ficha Pro importa o XML da nota e mostra o CMV real.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

03/12/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-05-mistura.jpg
Legenda:
"""Conta da empresa e pessoal misturadas?

Quando tudo passa pela mesma conta, fica difícil saber se a empresa dá lucro. No Oceanos Financeiro você acompanha várias empresas e as finanças pessoais em um lugar só.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

04/12/2026 — POST (create_image_post): BASE + terra-a-vista/ad-05-progresso.jpg
Legenda:
"""Sair das dívidas é uma missão por semana.

Ninguém quita tudo de uma vez. O Terra à Vista divide o caminho em missões semanais para você não perder o rumo.

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

05/12/2026 — POST (create_image_post): BASE + preco-certo/ad-05-2027.jpg
Legenda:
"""Seu preço está pronto para 2027?

No Preço Certo você vê, para cada produto, o preço de hoje e a estimativa de 2027.

O preço de 2027 é estimativa até a publicação das alíquotas efetivas.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""

06/12/2026 — POST (create_image_post): BASE + ficha-pro/ad-06-contraste.jpg
Legenda:
"""CMV estimado é chute. CMV real é gestão.

O Ficha Pro junta ficha técnica, estoque FEFO e preço com markup e impostos.

👉 Teste 7 dias grátis, sem cartão. Link na bio.

#restaurante #fichatecnica #cmv #precificacao #gastronomia"""

07/12/2026 — POST (create_image_post): BASE + oceanos-financeiro/ad-06-contraste.jpg
Legenda:
"""Lucro no papel não paga boleto.

Uma empresa pode dar lucro no DRE e ficar sem caixa no dia do pagamento. Por isso o Oceanos Financeiro monta os dois, DRE e fluxo de caixa, a partir do extrato.

👉 Teste grátis por 7 dias. Link na bio.

#gestaofinanceira #fluxodecaixa #dre #pequenasempresas #empreendedorismo"""

08/12/2026 — POST (create_image_post): BASE + terra-a-vista/ad-06-gratis.jpg
Legenda:
"""De graça. E não oferece empréstimo.

O Terra à Vista só organiza as suas dívidas e cartões e mostra a rota até quitar.

👉 App gratuito. Não oferece empréstimos. Link na bio.

#sairdasdividas #dividas #educacaofinanceira #financaspessoais #organizacaofinanceira"""

09/12/2026 — POST (create_image_post): BASE + preco-certo/ad-06-tabelas.jpg
Legenda:
"""Um preço só para varejo e atacado?

Quem compra uma peça e quem compra cem não deveriam pagar a mesma margem. O Preço Certo monta até 3 tabelas: consumidor, revenda e atacado.

👉 Teste grátis por 7 dias, sem cartão. Link na bio.

#precodevenda #formacaodepreco #margemdelucro #varejo #lojista"""
