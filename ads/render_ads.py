#!/usr/bin/env python3
"""Gera criativos 1080x1080 para tráfego pago (Ficha Pro e Oceanos Financeiro).
Uso: python3 -I ads/render_ads.py   (grava em ads/<produto>/)"""
import html, re
from pathlib import Path
from playwright.sync_api import sync_playwright

FP = dict(pasta="ficha-pro", nome="FICHA", nome2="PRO", cor="#FF8A4C", escuro="#2A1200", cta="7 dias grátis · sem cartão",
  icone='<svg width="44" height="44" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="3.4" stroke-linecap="round"><circle cx="27" cy="22" r="13"/><circle cx="27" cy="22" r="6"/><path d="M6 8v28M2 8v8a4 4 0 0 0 8 0V8"/></svg>')
OF = dict(pasta="oceanos-financeiro", nome="OCEANOS", nome2="FINANCEIRO", cor="#34D399", escuro="#04281C", cta="40 dias grátis · sem cartão",
  icone='<svg width="44" height="44" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="3.4" stroke-linecap="round"><path d="M3 12c5-5 9 5 14 0s9 5 14 0 6 2 10 0M3 22c5-5 9 5 14 0s9 5 14 0 6 2 10 0M3 32c5-5 9 5 14 0s9 5 14 0 6 2 10 0"/></svg>')

TV = dict(pasta="terra-a-vista", nome="TERRA", nome2="À VISTA", cor="#E8CE94", escuro="#231A05", cta="Comece grátis · no celular",
  nota="App gratuito. Não oferece empréstimos.",
  icone='<svg width="44" height="44" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="3.4" stroke-linecap="round"><circle cx="22" cy="12" r="5"/><path d="M8 26c4-7 24-7 28 0M3 36c5-5 9 5 14 0s9 5 14 0 6 2 10 0"/></svg>')
PC = dict(pasta="preco-certo", nome="PREÇO", nome2="CERTO", cor="#D4B25A", escuro="#1F1600", cta="Teste grátis 7 dias · sem cartão",
  direita="POGGI · TECNOLOGIA OCEANOS",
  icone='<svg width="44" height="44" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="3.4" stroke-linejoin="round"><path d="M22 4l18 18-18 18L4 22z"/><path d="M22 15l7 7-7 7-7-7z"/></svg>')

ADS = [
 (TV, "01-alivio", "Para organizar as dívidas", "Dívida não se resolve no susto. *Se resolve com rota.*", "Liste dívidas e cartões e veja o caminho até quitar."),
 (TV, "02-juros", "Juros sobre juros", "R$ 1.000 no cheque especial viram *R$ 2.518* em 12 meses.", "Exemplo: 8% ao mês, sem nenhum pagamento. As taxas variam por banco."),
 (TV, "03-escolha", "Qual é o seu caminho?", "Bola de Neve ou *Avalanche*?", "O simulador compara os dois com os seus números."),
 (TV, "04-primeiro-passo", "Comece pelo começo", "O primeiro passo é *enxergar tudo*.", "Diagnóstico financeiro grátis, em poucos minutos."),
 (TV, "05-progresso", "Um pouco toda semana", "Sair das dívidas é *uma missão por semana*.", "Missões semanais para você não perder o rumo."),
 (TV, "06-gratis", "Sem pegadinha", "*De graça.* E não oferece empréstimo.", "Só organiza dívidas e cartões e mostra a rota até quitar."),
 (PC, "01-perda", "Formação de preço", "Preço no chute é *lucro indo embora*.", "Forme o preço com custo, impostos, despesas e margem."),
 (PC, "02-compra-fora", "Compra de outro estado", "Comprou de outro estado? *Seu preço pode estar errado.*", "O Preço Certo soma ICMS, ST e MVA no custo, sozinho."),
 (PC, "03-exemplo", "Exemplo do simulador", "R$ 28,00 na nota. *+ R$ 3,64* de ICMS que ninguém viu.", "Camiseta comprada em SP, Simples Nacional. Fora do preço, sai do lucro."),
 (PC, "04-facilidade", "Sem planilha", "Arraste o XML da nota. *O preço sai pronto.*", "Produto, NCM, custo e origem preenchidos para você."),
 (PC, "05-2027", "Reforma tributária", "Seu preço está pronto para *2027*?", "Veja o preço de hoje e a estimativa de 2027, produto a produto."),
 (PC, "06-tabelas", "Varejo e atacado", "Um preço só para varejo e atacado? *Alguém perde.*", "Monte até 3 tabelas: consumidor, revenda e atacado."),
]
ADS += [
 (FP, "01-perda", "Para restaurantes", "Seu prato mais vendido pode estar *dando prejuízo*.", "Descubra o custo real com ficha técnica, impostos e markup."),
 (FP, "02-curiosidade", "Para restaurantes", "Quanto *sobra* de cada prato que sai da cozinha?", "Ficha técnica com sub-receitas e CMV real."),
 (FP, "03-facilidade", "Novo jeito de fazer ficha", "Fale a receita. *A IA monta a ficha.*", "Ingredientes, quantidades e custos organizados para você."),
 (FP, "04-risco-zero", "Teste antes de decidir", "*7 dias grátis.* Sem cartão.", "Monte a ficha do seu prato principal e veja o preço certo."),
 (FP, "05-insumo", "Para restaurantes", "O insumo subiu. *Seu preço subiu junto?*", "O Ficha Pro importa o XML da nota e mostra o CMV real."),
 (FP, "06-contraste", "Para restaurantes", "CMV estimado é chute. *CMV real é gestão.*", "Ficha técnica, estoque FEFO e preço com markup e impostos."),
 (OF, "01-dor", "Para donos de pequenas empresas", "Vendeu bem e *o dinheiro sumiu*?", "Veja o fluxo de caixa e o DRE da sua empresa, sem planilha."),
 (OF, "02-facilidade", "Sem planilha", "Importe o extrato. *O DRE sai pronto.*", "OFX ou CSV, com conciliação bancária."),
 (OF, "03-risco-zero", "Teste antes de decidir", "*40 dias grátis.* Sem cartão.", "Tempo para fechar um mês inteiro no sistema antes de pagar."),
 (OF, "04-preco", "Quanto custa", "Financeiro completo por *≈ R$ 82/mês*.", "Plano anual de R$ 987, sem fidelidade."),
 (OF, "05-mistura", "Para donos de pequenas empresas", "Conta da empresa e pessoal *misturadas*?", "Várias empresas e as finanças pessoais em um lugar só."),
 (OF, "06-contraste", "Para donos de pequenas empresas", "Lucro no papel *não paga boleto*.", "DRE e fluxo de caixa automáticos, a partir do extrato."),
]

def pagina(p, tag, tit, sub):
    c = p["cor"]
    tit = tit.replace("R$ ", "R$\u00a0"); sub = sub.replace("R$ ", "R$\u00a0")
    t = re.sub(r"\*(.+?)\*", rf'<span style="color:{c}">\1</span>', html.escape(tit))
    n = len(tit.replace("*", ""))
    fs = 124 if n < 30 else 108 if n < 42 else 94
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;font-family:'Inter',sans-serif;color:#EEF2F8;overflow:hidden;
background:radial-gradient(800px 620px at 100% 0%,{c}40,transparent 62%),radial-gradient(700px 520px at 0% 100%,{c}1F,transparent 60%),#060B16;
padding:80px;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:18px;font-weight:800;font-size:36px;letter-spacing:.5px}}
.top i{{margin-left:auto;font-style:normal;font-weight:600;font-size:21px;letter-spacing:5px;color:#8B97AD}}
.tag{{margin-top:70px;font-weight:700;font-size:25px;letter-spacing:7px;text-transform:uppercase;color:{c}}}
h1{{margin-top:26px;font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:{fs}px;line-height:1.02;letter-spacing:-3.5px;text-wrap:balance}}
p{{margin-top:36px;font-size:40px;line-height:1.3;color:#C3CCDB;max-width:860px;text-wrap:balance}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:28px}}small{{font-size:22px;color:#8B97AD;line-height:1.3}}
.cta{{white-space:nowrap;background:{c};color:{p['escuro']};font-weight:800;font-size:40px;letter-spacing:-.8px;padding:26px 46px;border-radius:999px}}
</style></head><body>
<div class="top">{p['icone'].format(c=c)}<span>{p['nome']} <span style="color:{c}">{p['nome2']}</span></span><i>{p.get('direita','OCEANOS SISTEMAS')}</i></div>
<div class="tag">{html.escape(tag)}</div><h1>{t}</h1><p>{html.escape(sub)}</p>
<div class="foot"><div class="cta">{p['cta']}</div><small>{p.get('nota','')}</small></div></body></html>"""

base = Path(__file__).resolve().parent
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1080})
    for p, slug, tag, tit, sub in ADS:
        d = base / p["pasta"]; d.mkdir(exist_ok=True)
        pg.set_content(pagina(p, tag, tit, sub)); pg.wait_for_timeout(150)
        pg.screenshot(path=str(d / f"ad-{slug}.jpg"), type="jpeg", quality=92)
    b.close()
