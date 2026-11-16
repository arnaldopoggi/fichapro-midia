#!/usr/bin/env python3
"""Refaz reel.mp4, story-1.jpg e story-2.jpg do Oceanos Financeiro (teste de 7 dias).
Uso: python3 -I apps/render_financeiro.py   (a trilha vem do reel atual)"""
import subprocess, tempfile, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

G = "#34D399"
D = Path(__file__).resolve().parent / "oceanos-financeiro"
WAVE = '<svg width="{s}" height="{s}" viewBox="0 0 44 44" fill="none" stroke="#34D399" stroke-width="3.4" stroke-linecap="round"><path d="M3 12c5-5 9 5 14 0s9 5 14 0 6 2 10 0M3 22c5-5 9 5 14 0s9 5 14 0 6 2 10 0M3 32c5-5 9 5 14 0s9 5 14 0 6 2 10 0"/></svg>'
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:'Inter',sans-serif;color:#EEF2F8;overflow:hidden;position:relative;
background:radial-gradient(900px 700px at 100% 0%,rgba(52,211,153,.26),transparent 62%),radial-gradient(800px 600px at 0% 100%,rgba(52,211,153,.12),transparent 60%),#060B16}}
.top{{position:absolute;top:190px;left:56px;right:56px;display:flex;align-items:center;gap:18px;font-weight:800;font-size:36px;letter-spacing:.5px}}
.top i{{margin-left:auto;font-style:normal;font-weight:600;font-size:22px;letter-spacing:5px;color:#8B97AD}}
g{{color:{G}}}
h1{{font-family:'Inter Display','Inter',sans-serif;font-weight:800;letter-spacing:-4px;line-height:1.04}}
.pill{{display:inline-block;background:{G};color:#04281C;font-weight:800;font-size:40px;letter-spacing:-.8px;padding:26px 46px;border-radius:999px}}
.url{{font-size:30px;color:#8B97AD;margin-top:30px}}
.mid{{position:absolute;left:56px;right:56px;top:50%;transform:translateY(-50%)}}
.n{{font-weight:800;font-size:40px;letter-spacing:6px;color:{G};margin-bottom:26px}}
.bar{{position:absolute;left:56px;right:56px;top:1620px;display:flex;gap:14px}}
.bar b{{flex:1;height:8px;border-radius:8px;background:#232B3B}} .bar b.on{{background:{G}}}
.opt{{display:flex;align-items:center;gap:44px;background:#0E1A33;border:1px solid #1B2944;border-radius:28px;padding:44px 52px;margin-top:28px;font-size:44px}}
.opt span{{font-weight:800;font-size:68px;color:{G};width:50px}}
.st{{position:absolute;left:80px;right:80px;top:350px}} .st h1{{font-size:128px;margin-bottom:60px}}
.st p{{font-size:40px;color:#C3CCDB;margin:56px 0 60px}}"""
TOP = f'<div class="top">{WAVE.format(s=48)}<span>OCEANOS <g>FINANCEIRO</g></span><i>OCEANOS SISTEMAS</i></div>'

def page(body): return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{TOP}{body}</body></html>'
def bar(k): return '<div class="bar">' + "".join(f'<b class="{"on" if i < k else ""}"></b>' for i in range(5)) + '</div>'
def scene(k, n, h): return page(f'<div class="mid">{f"<div class=n>{n}</div>" if n else ""}<h1 style="font-size:132px">{h}</h1></div>{bar(k)}')

SCENES = [
 scene(1, "", "A planilha <g>não fecha</g> de novo?"),
 scene(2, "01", "Importe o extrato <g>OFX</g> do banco"),
 scene(3, "02", "<g>Concilie</g> extrato, lançamentos e cartão"),
 scene(4, "03", "<g>DRE</g> e <g>fluxo de caixa</g> prontos"),
 page(f'<div class="mid">{WAVE.format(s=150)}<h1 style="font-size:150px;margin:40px 0 56px">Oceanos<br><g>Financeiro</g></h1><div class="pill" style="font-size:48px">7 dias grátis</div><div class="url" style="font-size:36px">app.oceanosistemas.com.br</div></div>{bar(5)}'),
]
def story(h, opts, p):
    o = "".join(f'<div class="opt"><span>{i+1}</span>{t}</div>' for i, t in enumerate(opts))
    return page(f'<div class="st"><h1>{h}</h1>{o}<p>{p}</p><div class="pill">7 dias grátis</div><div class="url">app.oceanosistemas.com.br</div></div>')
STORIES = {
 "story-1.jpg": story("Você mistura a conta da empresa com a <g>pessoal</g>?", ["Sim, direto", "Às vezes", "Nunca"], "Responda 1, 2 ou 3 nas mensagens."),
 "story-2.jpg": story("Teste grátis por <g>7 dias</g>", ["Crie sua conta", "Importe o extrato do banco", "Veja o DRE do seu mês"], "Sem fidelidade. Suporte pelo WhatsApp."),
}
DUR = [2.9, 2.9, 2.9, 2.9, 6.1]; X = 0.4   # soma - 4*X = 16.1 s

tmp = Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for name, h in STORIES.items():
        pg.set_content(h); pg.wait_for_timeout(150); pg.screenshot(path=str(D / name), type="jpeg", quality=92)
    for i, h in enumerate(SCENES):
        pg.set_content(h); pg.wait_for_timeout(150); pg.screenshot(path=str(tmp / f"s{i}.png"))
    b.close()
old = tmp / "old.mp4"; shutil.copy(D / "reel.mp4", old)
cmd = ["ffmpeg", "-v", "error", "-y"]
for i, d in enumerate(DUR): cmd += ["-loop", "1", "-t", str(d), "-r", "30", "-i", str(tmp / f"s{i}.png")]
cmd += ["-i", str(old)]
f, last, off = [], "[0:v]", 0.0
for i in range(1, 5):
    off += DUR[i-1] - X
    f.append(f"{last}[{i}:v]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"); last = f"[x{i}]"
cmd += ["-filter_complex", ";".join(f) + f";{last}format=yuv420p[v]", "-map", "[v]", "-map", "5:a", "-c:v", "libx264", "-crf", "18", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-t", "16.1", "-movflags", "+faststart", str(D / "reel.mp4")]
subprocess.run(cmd, check=True)
