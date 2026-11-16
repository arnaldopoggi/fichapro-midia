#!/usr/bin/env python3
"""Artes do Oceanos Financeiro no estilo azul-marinho (ondas, ciano, telas em celular/tablet).
Uso: python3 -I ads/render_financeiro_azul.py  -> ads/oceanos-financeiro-azul/*-feed.jpg (1080x1350) e *-story.jpg (1080x1920)
Só usa funções comprovadas: extrato OFX/CSV, conciliação, DRE e fluxo de caixa, fatura do cartão em PDF,
várias empresas + finanças pessoais. Números das telas são ilustrativos."""
from pathlib import Path
from playwright.sync_api import sync_playwright

NOME, NOME2 = "Oceanos", "Financeiros"
C, T = "#6FD6E8", "#2EC4C6"
LOGO = '<svg viewBox="0 0 64 64" width="{s}" height="{s}"><circle cx="32" cy="32" r="29" fill="none" stroke="{c}" stroke-width="3.5"/><path d="M12 34c8-12 20-14 28-6-7-1-11 3-10 8 1 5 8 6 12 2 2 8-8 14-18 11-8-2-13-8-12-15z" fill="{c}"/><path d="M10 46c7-4 12 4 19 0s12 4 19 0 6 1 8 0" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/></svg>'
WAVES = "".join(f'<path d="M-50 {y} C 200 {y-90} 420 {y+80} 640 {y-10} S 980 {y-80} 1150 {y+20}" fill="none" stroke="rgba(120,200,255,{a})" stroke-width="2"/>' for y, a in [(260,.07),(520,.06),(820,.08),(1100,.07),(1400,.09),(1650,.08)])

def css(w, h, light):
    bg = ("linear-gradient(180deg,#DCEBFB 0%,#C3DDF7 60%,#B5D3F3 100%)" if light else
          "radial-gradient(900px 700px at 85% 8%,rgba(46,196,198,.20),transparent 60%),radial-gradient(900px 800px at 10% 100%,rgba(60,120,255,.22),transparent 60%),linear-gradient(180deg,#0B1A3D 0%,#0A2250 55%,#0B2E66 100%)")
    fg, sub, ac = ("#0B2A6B", "#1F3F7A", "#0B4FB3") if light else ("#FFFFFF", "#A9CBEF", C)
    k = h / 1350
    return f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Inter',sans-serif;color:{fg};background:{bg};overflow:hidden;position:relative;display:flex;flex-direction:column;padding:{int(70*k)}px 76px {int(56*k)}px}}
.wv{{position:absolute;inset:0;width:100%;height:100%}}
body>*:not(.wv){{position:relative}}
.logo{{display:flex;align-items:center;gap:20px;font-size:44px;font-weight:700;line-height:1;letter-spacing:-.5px}} .logo small{{display:block;font-size:34px;font-weight:400;opacity:.9;margin-top:4px}}
h1{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:92px;line-height:1.04;letter-spacing:-3px;margin-top:{int(54*k)}px;text-wrap:balance}}
h1 b{{color:{ac};font-weight:800}}
.sub{{font-size:40px;line-height:1.28;color:{sub};margin-top:26px;text-wrap:balance}}
.pill{{align-self:flex-start;margin-top:34px;background:linear-gradient(90deg,{C},{T});color:#07224A;font-weight:800;font-size:46px;letter-spacing:-1px;padding:24px 48px;border-radius:26px;box-shadow:0 14px 40px rgba(46,196,198,.25)}}
.stage{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin:{int(34*k)}px 0}}
.foot{{font-size:27px;color:{sub};display:flex;justify-content:space-between;align-items:center;border-top:1px solid {'rgba(11,42,107,.18)' if light else 'rgba(140,200,255,.22)'};padding-top:24px}}
.foot b{{color:{fg};font-weight:700}}
.dev{{background:#0A1022;border-radius:54px;padding:16px;box-shadow:0 30px 80px rgba(0,0,0,.45),0 0 0 2px rgba(255,255,255,.12)}}
.scr{{background:#F3F7FD;border-radius:40px;color:#0C1B3A;padding:38px 34px;height:100%}}
.scr.dk{{background:#121C36;color:#fff}}
.scr h3{{font-size:34px;font-weight:800;letter-spacing:-.5px;margin-bottom:22px;display:flex;justify-content:space-between;align-items:center}} .scr h3 i{{font-style:normal;font-size:22px;font-weight:600;color:#2EAE8F}}
.cd{{background:#fff;border-radius:22px;padding:24px 26px;margin-top:16px;box-shadow:0 6px 18px rgba(20,50,110,.08);font-size:27px}}
.dk .cd{{background:#1B2748;box-shadow:none}}
.cd .l{{color:#5B6B8C;font-size:23px}} .dk .cd .l{{color:#9FB2D6}}
.cd .v{{font-weight:800;font-size:38px;letter-spacing:-1px;margin-top:4px}}
.row{{display:flex;justify-content:space-between;align-items:center;padding:17px 0;border-bottom:1px solid #E3EAF5;font-size:27px}} .row:last-child{{border:0}} .row b{{font-weight:700;white-space:nowrap}}
.dk .row{{border-color:#26345A}}
.g{{color:#12A37A}} .r{{color:#E0564A}} .dk .g{{color:#4ADE9E}} .dk .r{{color:#FF8A7D}}
.bars{{display:flex;align-items:flex-end;gap:14px;height:170px;margin-top:18px}} .bars div{{flex:1;border-radius:8px 8px 0 0}}
.ic{{width:50px;height:50px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:22px;margin-right:16px;flex:none}}
.pnl{{background:#fff;border-radius:34px;padding:34px;color:#0C1B3A;box-shadow:0 24px 60px rgba(20,60,130,.18)}} .pnl h3{{font-size:30px;font-weight:800;color:#0B2A6B;margin-bottom:10px}}
.note{{font-size:21px;opacity:.6;margin-top:10px;text-align:center}}"""

def logo(light): 
    return f'<div class="logo">{LOGO.format(s=92, c="#0B5FC2" if light else C)}<div>{NOME}<small>{NOME2}</small></div></div>'
def doc(w, h, light, inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css(w,h,light)}</style></head><body><svg class="wv" viewBox="0 0 1080 1920" preserveAspectRatio="none">{"" if light else WAVES}</svg>{logo(light)}{inner}<div class="foot"><b>{NOME} {NOME2}</b><span>app.oceanosistemas.com.br · telas ilustrativas</span></div></body></html>'

def phone(body, dk=False, w=520, h=None):
    return f'<div class="dev" style="width:{w}px;{"height:"+str(h)+"px" if h else ""}"><div class="scr {"dk" if dk else ""}">{body}</div></div>'
LINE = '<svg viewBox="0 0 520 170" width="100%" height="170" style="margin-top:14px"><path d="M0 140 L70 96 L140 108 L210 74 L280 88 L350 52 L420 60 L520 30 L520 170 L0 170Z" fill="rgba(111,214,232,.18)"/><path d="M0 140 L70 96 L140 108 L210 74 L280 88 L350 52 L420 60 L520 30" fill="none" stroke="#6FD6E8" stroke-width="5" stroke-linejoin="round"/></svg>'
def bars(vals): return '<div class="bars">' + "".join(f'<div style="height:{v}%;background:{"#2EC4C6" if i%2==0 else "#F2857A"}"></div>' for i, v in enumerate(vals)) + '</div>'

ARTS = {
 "01-controle": (False, lambda k: f'<h1>Sua empresa no controle, <b>sem planilha.</b></h1><div class="pill">Teste grátis por 7 dias</div><div class="stage"><div class="dev" style="width:900px;border-radius:44px"><div class="scr dk" style="border-radius:30px"><h3>Painel financeiro <i>● Novembro</i></h3><div style="display:flex;gap:16px">' + "".join(f'<div class="cd" style="flex:1;margin:0"><div class="l">{l}</div><div class="v {c}">{v}</div></div>' for l, v, c in [("Receitas","R$ 48.200","g"),("Despesas","R$ 39.650","r"),("Resultado","R$ 8.550","")]) + f'</div><div class="cd"><div class="l">Fluxo de caixa do mês</div>{LINE}</div></div></div></div>'),
 "02-planilha": (False, lambda k: '<div class="stage" style="flex-direction:column;align-items:flex-start"><h1 style="font-size:118px;margin:0">Chega de digitar cada despesa em <b>planilha.</b></h1><div class="sub" style="font-size:48px;margin-top:40px">Importe o extrato do banco e veja para onde o dinheiro da empresa está indo.</div><div class="pill" style="margin-top:56px">Teste grátis por 7 dias</div></div>'),
 "03-pdf-cartao": (True, lambda k: '<div class="stage" style="gap:34px"><div class="pnl" style="flex:1.5;font-size:24px"><h3>FATURA DO CARTÃO</h3><div style="display:inline-block;background:#0B5FC2;color:#fff;font-weight:800;font-size:22px;padding:8px 16px;border-radius:10px;margin-bottom:8px">PDF</div>' + "".join(f'<div class="row" style="font-size:24px"><span style="display:flex;align-items:center"><span class="ic" style="background:{c};width:42px;height:42px;margin-right:12px">{i}</span>{n}</span><b>{v}</b></div>' for n, v, c, i in [("Fornecedor","R$ 1.250,00","#3B82F6","F"),("Combustível","R$ 380,00","#F28C38","C"),("Assinaturas","R$ 139,90","#8B5CF6","A"),("Refeições","R$ 265,30","#22A565","R")]) + '</div><div style="font-size:60px;color:#0B5FC2;font-weight:800">→</div><div class="pnl" style="flex:1"><h3>Lançamentos</h3>' + "".join(f'<div class="row"><span>{n}</span><b class="g">✓</b></div>' for n in ["Fornecedor","Combustível","Assinaturas","Refeições"]) + '<div style="background:#DDEBFE;color:#0B4FB3;font-weight:700;font-size:22px;padding:14px 16px;border-radius:14px;margin-top:14px">Fatura lida do PDF</div></div></div><h1 style="margin-top:0">Importou o PDF do cartão. <b>Pronto.</b></h1><div class="sub" style="margin-bottom:34px">O Oceanos Financeiros lê a fatura do cartão direto do PDF. Sem digitar linha por linha.</div>'),
 "04-dre": (False, lambda k: '<div class="stage">' + phone('<h3>DRE do mês</h3>' + "".join(f'<div class="cd"><div class="row" style="padding:0;border:0"><span>{n}</span><b class="{c}">{v}</b></div></div>' for n, v, c in [("Receita","R$ 48.200","g"),("Custos","− R$ 21.300","r"),("Despesas","− R$ 18.350","r"),("Resultado","R$ 8.550","g")]) + '<div class="note" style="color:#5B6B8C;opacity:1">Gerado a partir do extrato</div>') + '</div><h1 style="margin-top:0;text-align:center">Importe o extrato. <b>O DRE sai pronto.</b></h1><div class="pill" style="align-self:center;margin-bottom:34px">Teste grátis por 7 dias</div>'),
 "05-empresas-pessoal": (False, lambda k: '<div class="stage">' + phone('<h3>Minhas contas</h3>' + "".join(f'<div class="cd"><div style="display:flex;align-items:center"><span class="ic" style="background:{c}">{i}</span><div><b>{n}</b><div class="l">{d}</div></div></div></div>' for n, d, c, i in [("Empresa 1","DRE e fluxo de caixa","#0B5FC2","E"),("Empresa 2","DRE e fluxo de caixa","#2EC4C6","E"),("Pessoal","Suas finanças pessoais","#F2B33D","P")])) + '</div><h1 style="margin-top:0;text-align:center">Suas empresas e a vida pessoal <b>em um só lugar.</b></h1><div class="sub" style="text-align:center;margin-bottom:34px">Pare de misturar tudo na mesma planilha.</div>'),
 "06-caixa": (False, lambda k: '<h1>Vendeu bem e <b>o dinheiro sumiu?</b></h1><div class="sub">Venda não é caixa. Veja entradas e saídas lado a lado.</div><div class="stage">' + phone('<h3>Fluxo de caixa <i style="color:#5B6B8C">semanas</i></h3><div class="cd">' + bars([78,52,64,70,90,61,58,84]) + '<div style="display:flex;gap:24px;font-size:22px;margin-top:14px"><span><b style="color:#2EC4C6">■</b> Entradas</span><span><b style="color:#F2857A">■</b> Saídas</span></div></div>' + ('<div class="cd"><div class="l">Saldo do mês</div><div class="v g">R$ 8.550</div></div>' if k > 1.2 else ''), w=600) + '</div><div class="pill" style="align-self:center;margin:0 0 34px">Teste grátis por 7 dias</div>'),
}
def meta(n, a, t, pct, c, i):
    return f'<div class="cd"><div style="display:flex;align-items:center"><span class="ic" style="background:{c}">{i}</span><div><b>{n}</b><div class="l">R$ {a} de R$ {t}</div></div></div><div style="height:14px;background:#DCE6F5;border-radius:9px;margin-top:16px"><div style="width:{pct}%;height:14px;border-radius:9px;background:linear-gradient(90deg,#2EC4C6,#0B5FC2)"></div></div></div>'
DEBT = '<svg viewBox="0 0 800 420" width="100%"><g fill="rgba(46,196,198,.55)"><rect x="60" y="90" width="120" height="290" rx="8"/><rect x="250" y="160" width="120" height="220" rx="8"/><rect x="440" y="235" width="120" height="145" rx="8"/><rect x="630" y="310" width="120" height="70" rx="8"/></g><path d="M40 60 L760 285" stroke="#7CF0C0" stroke-width="7" stroke-linecap="round"/><g fill="#A9CBEF" font-size="30" font-family="Inter" text-anchor="middle"><text x="120" y="415">Mês 1</text><text x="310" y="415">Mês 2</text><text x="500" y="415">Mês 3</text><text x="690" y="415">Mês 4</text></g></svg>'
STORIES = {
 "story-1-dor": (False, lambda k: '<div class="stage" style="flex-direction:column;align-items:flex-start"><h1 style="font-size:124px;margin:0">Chega de digitar cada despesa em <b>planilha.</b></h1><div class="sub" style="font-size:52px;margin-top:44px">Você sente o dinheiro indo embora e nem sabe para onde vai.</div></div>'),
 "story-2-solucao": (True, lambda k: '<div class="stage" style="gap:30px"><div class="pnl" style="flex:1.5"><h3>EXTRATO DO CARTÃO</h3><div style="display:inline-block;background:#0B5FC2;color:#fff;font-weight:800;font-size:22px;padding:8px 16px;border-radius:10px;margin-bottom:8px">PDF</div>' + "".join(f'<div class="row" style="font-size:24px"><span style="display:flex;align-items:center"><span class="ic" style="background:{c};width:42px;height:42px;margin-right:12px">{i}</span>{n}</span><b>{v}</b></div>' for n, v, c, i in [("Supermercado","R$ 120,50","#3B82F6","S"),("Combustível","R$ 80,00","#F28C38","C"),("Streaming","R$ 39,90","#8B5CF6","T"),("Restaurante","R$ 65,30","#22A565","R")]) + '</div><div style="font-size:60px;color:#0B5FC2;font-weight:800">→</div><div class="pnl" style="flex:1.1"><h3>Classificado</h3>' + "".join(f'<div class="row" style="font-size:24px"><span>{n}</span><b class="g">✓</b></div>' for n in ["Alimentação","Transporte","Lazer","Alimentação"]) + '</div></div><h1 style="margin-top:0;font-size:104px">Importou o PDF do cartão. <b>Pronto.</b></h1><div class="sub" style="font-size:46px">Ele já preenche e classifica suas despesas por você. Sem digitar nada.</div><div class="sub" style="font-size:36px;margin-bottom:60px;opacity:.85">Funciona também com o extrato bancário.</div>'),
 "story-3-dividas": (False, lambda k: f'<h1 style="font-size:108px;margin-top:110px">Controle e elimine <b>todas as suas dívidas.</b></h1><div class="stage"><div style="width:100%">{DEBT}<div class="note">Gráfico ilustrativo</div></div></div><div class="sub" style="font-size:50px;text-align:center;margin:0 0 80px;color:#8FE3F0">Com o método testado e aprovado por Arnaldo Poggi.</div>'),
 "story-4-poupanca": (False, lambda k: '<div class="stage">' + phone('<h3>Metas de poupança</h3>' + meta("Viagem","3.200","5.000",64,"#2EC4C6","V") + meta("Reserva de emergência","1.200","2.000",60,"#0B5FC2","R") + meta("Novo notebook","600","1.500",40,"#F2B33D","N"), w=620) + '</div><h1 style="margin-top:0;text-align:center;font-size:100px">Comece a poupar <b>sem dor</b> e sem perder tempo.</h1><div class="pill" style="align-self:center;margin:44px 0 70px;font-size:50px">Sugestões e metas automáticas</div>'),
}

def sug(t, d, v, c, i):
    return f'<div class="cd"><div style="display:flex;align-items:center"><span class="ic" style="background:{c}">{i}</span><div style="flex:1"><b>{t}</b><div class="l">{d}</div></div>' + (f'<span style="background:#1FAE7B;color:#fff;font-weight:700;font-size:21px;padding:8px 12px;border-radius:10px;white-space:nowrap">{v}</span>' if v else '') + '</div></div>'
PIE = '<div style="width:{d}px;height:{d}px;border-radius:50%;background:conic-gradient(#0B4FA8 0 35%,#12A8B8 35% 60%,#1F74C4 60% 75%,#4A9BD9 75% 90%,#5CC8D6 90% 100%);box-shadow:0 10px 30px rgba(20,60,130,.2)"></div>'
LEG = "".join(f'<span style="display:inline-flex;align-items:center;margin:8px 18px 0 0;font-size:27px"><b style="display:inline-block;width:22px;height:22px;border-radius:6px;background:{c};margin-right:10px"></b>{n}</span>' for n, c in [("Moradia · 35%","#0B4FA8"),("Alimentação · 25%","#12A8B8"),("Transporte · 15%","#1F74C4"),("Investimentos · 15%","#4A9BD9"),("Lazer · 10%","#5CC8D6")])
ARTS.update({
 "07-sugestoes": (False, lambda k: '<h1 style="text-align:center">Ele te diz o que fazer para <b>economizar mais.</b></h1><div class="sub" style="text-align:center">Sugestões inteligentes + metas de poupança automáticas.</div><div class="stage">' + phone('<h3>Sugestões de economia</h3>' + sug("Reduza assinaturas","Streaming que você não usa","−R$ 45/mês","#12A8B8","A") + sug("Cozinhar em casa","Em vez de delivery","−R$ 120/mês","#0B5FC2","C") + (meta("Meta: Viagem","1.200","2.000",60,"#F2B33D","M") if k > 1.2 else ''), w=640) + '</div>'),
 "08-para-onde-vai": (True, lambda k: f'<h1 style="text-align:center">Você sabe para onde vai <b>seu dinheiro?</b></h1><div class="sub" style="text-align:center">Com o Oceanos, você sabe. Sem planilha, sem digitar.</div><div class="stage"><div class="pnl" style="width:100%;text-align:center"><div style="display:flex;justify-content:center;margin:10px 0 26px">{PIE.format(d=int(330*min(k,1.3)))}</div>{LEG}</div></div>'),
 "09-extrato-aprende": (False, lambda k: '<h1 style="text-align:center">Importa o extrato do banco. <b>Ele já aprende tudo.</b></h1><div class="stage">' + phone('<h3>Importando… <i>92%</i></h3><div style="height:14px;background:#DCE6F5;border-radius:9px"><div style="width:92%;height:14px;border-radius:9px;background:linear-gradient(90deg,#2EC4C6,#0B5FC2)"></div></div><div class="cd"><div class="row" style="padding:0;border:0"><span><b style="color:#0B5FC2">PDF</b> &nbsp;Extrato bancário</span><b class="g">✓</b></div></div>' + sug("Alimentação","R$ 840,50 · Restaurantes","","#12A8B8","A") + sug("Transporte","R$ 220,00 · Aplicativo","","#0B5FC2","T") + (sug("Moradia","R$ 1.200,00 · Aluguel","","#F2B33D","M") if k > 1.2 else ''), w=640) + '</div><div class="sub" style="text-align:center;margin:0 0 34px;color:#8FC8FF">Ele aprende o que é cada despesa e classifica corretamente para você.</div>'),
})
out = Path(__file__).resolve().parent / "oceanos-financeiro-azul"; out.mkdir(exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for (w, h, suf) in [(1080, 1350, "feed"), (1080, 1920, "story")]:
        pg = b.new_page(viewport={"width": w, "height": h})
        for slug, (light, fn) in ARTS.items():
            pg.set_content(doc(w, h, light, fn(h / 1350))); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"{slug}-{suf}.jpg"), type="jpeg", quality=92)
        if suf == "story":
            for slug, (light, fn) in STORIES.items():
                pg.set_content(doc(w, h, light, fn(h / 1350))); pg.wait_for_timeout(150)
                pg.screenshot(path=str(out / f"{slug}.jpg"), type="jpeg", quality=92)
    b.close()
