#!/usr/bin/env python3
"""Gera a arte do post diário do @oceanosistemas.

Uso:
  python3 -I diario/render.py spec.json saida_sem_extensao [--reel]

Sempre gera <saida>.jpg (1080x1350, feed 4:5).
Com --reel gera também <saida>.mp4 (1080x1920, ~9 s, com trilha sintetizada).

spec.json:
{
  "tipo": "noticia" | "dado" | "vendas",
  "etiqueta": "RADAR DO EMPRESÁRIO",          # faixa superior
  "titulo": "Texto com *destaque* em verde",   # gancho, até ~70 caracteres
  "numero": "8,9 milhões",                      # opcional: número grande
  "numero_legenda": "de empresas inadimplentes",# opcional
  "corpo": ["linha curta 1", "linha curta 2"],  # 1 a 3 frases
  "solucao": "Oceanos Financeiro: DRE e fluxo de caixa automáticos",  # opcional
  "fonte": "Fonte: Serasa Experian, set/2026",  # obrigatório em noticia/dado
  "rodape": "Salve e mande para o seu sócio"
}
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

CORES = {
    "noticia": {"tag_bg": "#F5C04A", "tag_fg": "#1A1300", "acento": "#F5C04A", "icone": "RADAR"},
    "dado": {"tag_bg": "#FF6B5B", "tag_fg": "#2A0500", "acento": "#FF8A7D", "icone": "DADO"},
    "vendas": {"tag_bg": "#34D399", "tag_fg": "#04281C", "acento": "#34D399", "icone": "VENDAS"},
}


def marca(txt: str, cor: str) -> str:
    t = html.escape(txt)
    return re.sub(r"\*(.+?)\*", rf'<span style="color:{cor}">\1</span>', t)


def montar_html(spec: dict, w: int, h: int, etapa: int = 3) -> str:
    c = CORES.get(spec.get("tipo", "noticia"), CORES["noticia"])
    vertical = h > w * 1.4
    pad = 84
    tit_len = len(re.sub(r"\*", "", spec["titulo"]))
    tit_size = 92 if tit_len < 40 else 80 if tit_len < 60 else 68
    if vertical:
        tit_size += 22
    num = spec.get("numero")
    corpo = spec.get("corpo") or []
    show2 = etapa >= 2
    show3 = etapa >= 3

    def vis(flag):
        return "" if flag else "opacity:0;"

    numero_html = ""
    if num:
        numero_html = f"""
        <div class="num" style="{vis(show2)}">
          <div class="n" style="color:{c['acento']}">{html.escape(num)}</div>
          <div class="nl">{html.escape(spec.get('numero_legenda', ''))}</div>
        </div>"""
    corpo_html = "".join(f"<li>{marca(x, c['acento'])}</li>" for x in corpo)
    sol = spec.get("solucao")
    sol_html = (
        f'<div class="sol" style="{vis(show3)}"><span class="sl">SOLUÇÃO</span>{marca(sol, "#34D399")}</div>'
        if sol
        else ""
    )
    fonte = spec.get("fonte", "")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Inter','Inter Display',sans-serif;color:#EEF2F8;
background:radial-gradient(900px 700px at 100% 0%,rgba(52,211,153,.16),transparent 60%),
radial-gradient(800px 600px at 0% 100%,rgba(56,120,255,.14),transparent 60%),#060B16;overflow:hidden;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:54px 54px}}
.wrap{{position:absolute;inset:{pad + (90 if vertical else 0)}px {pad}px {pad + (110 if vertical else 0)}px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px;letter-spacing:.5px}}
.brand svg{{width:44px;height:30px}}
.tag{{background:{c['tag_bg']};color:{c['tag_fg']};font-weight:800;font-size:22px;letter-spacing:3px;padding:10px 18px;border-radius:8px}}
.et{{margin-top:{70 if vertical else 56}px;color:{c['acento']};font-weight:700;letter-spacing:5px;font-size:24px;text-transform:uppercase}}
h1{{margin-top:22px;font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:{tit_size}px;line-height:1.02;letter-spacing:-2.5px}}
.num{{margin-top:{48 if vertical else 36}px;border-left:6px solid {c['acento']};padding-left:28px}}
.n{{font-family:'Inter Display';font-weight:800;font-size:{190 if vertical else 128}px;line-height:1;letter-spacing:-4px}}
.nl{{font-size:{38 if vertical else 32}px;color:#B8C2D3;margin-top:8px}}
ul{{margin-top:{44 if vertical else 34}px;list-style:none;display:flex;flex-direction:column;gap:{26 if vertical else 18}px}}
li{{font-size:{42 if vertical else 33}px;line-height:1.3;color:#D7DEEA;padding-left:34px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:.55em;width:14px;height:14px;border-radius:3px;background:{c['acento']}}}
.sol{{margin-top:auto;background:rgba(52,211,153,.10);border:1.5px solid rgba(52,211,153,.45);border-radius:20px;padding:24px 28px;font-size:30px;line-height:1.3;font-weight:600}}
.sl{{display:block;font-size:19px;letter-spacing:4px;color:#34D399;font-weight:800;margin-bottom:8px}}
.foot{{margin-top:{30 if sol else 0}px;{'' if sol else 'margin-top:auto;'}display:flex;justify-content:space-between;align-items:flex-end;gap:30px;border-top:1px solid rgba(255,255,255,.12);padding-top:24px}}
.fonte{{font-size:21px;color:#8A96AB;max-width:60%;line-height:1.35}}
.rod{{font-size:24px;font-weight:700;color:#EEF2F8;text-align:right}}
</style></head><body><div class="grid"></div><div class="wrap">
<div class="top"><div class="brand"><svg viewBox="0 0 44 30" fill="none" stroke="#34D399" stroke-width="3.4" stroke-linecap="round">
<path d="M2 7c5-5 10 5 15 0s10 5 15 0 7-3 10 0"/><path d="M2 15c5-5 10 5 15 0s10 5 15 0 7-3 10 0"/><path d="M2 23c5-5 10 5 15 0s10 5 15 0 7-3 10 0"/></svg>OCEANOS</div>
<div class="tag">{c['icone']}</div></div>
<div class="et">{html.escape(spec.get('etiqueta', ''))}</div>
<h1>{marca(spec['titulo'], c['acento'])}</h1>
{numero_html}
<ul style="{vis(show3)}">{corpo_html}</ul>
{sol_html}
<div class="foot" style="{vis(show3)}"><div class="fonte">{html.escape(fonte)}</div><div class="rod">{html.escape(spec.get('rodape', ''))}</div></div>
</div></body></html>"""


def shot(page, html_txt: str, w: int, h: int, out: Path):
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(html_txt, wait_until="load")
    page.wait_for_timeout(150)
    page.screenshot(path=str(out), type="jpeg", quality=92)


def trilha(path: Path, dur: float):
    # trilha original sintetizada: acorde suave + pulso leve, sem direitos de terceiros
    expr = (
        "0.10*sin(2*PI*220*t)+0.08*sin(2*PI*277.18*t)+0.07*sin(2*PI*329.63*t)"
        "+0.05*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*2*t))"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         f"aevalsrc='{expr}':s=44100:d={dur}",
         "-af", f"afade=t=in:d=1,afade=t=out:st={dur-1.2}:d=1.2,volume=0.9",
         "-c:a", "aac", "-b:a", "128k", str(path)], check=True)


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    reel = "--reel" in sys.argv
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(device_scale_factor=1)
        shot(page, montar_html(spec, 1080, 1350), 1080, 1350, out.with_suffix(".jpg"))
        if reel:
            tmp = Path(tempfile.mkdtemp())
            for e in (1, 2, 3):
                shot(page, montar_html(spec, 1080, 1920, e), 1080, 1920, tmp / f"f{e}.jpg")
            b.close()
            durs = [2.2, 2.3, 4.5]
            total = sum(durs)
            trilha(tmp / "a.m4a", total)
            inputs = []
            for i, d in enumerate(durs, 1):
                inputs += ["-loop", "1", "-t", str(d + 0.5), "-i", str(tmp / f"f{i}.jpg")]
            fc = (
                "[0:v]scale=1080:1920,setsar=1,fps=30[v0];[1:v]scale=1080:1920,setsar=1,fps=30[v1];"
                "[2:v]scale=1080:1920,setsar=1,fps=30[v2];"
                f"[v0][v1]xfade=transition=fade:duration=0.5:offset={durs[0]}[x1];"
                f"[x1][v2]xfade=transition=fade:duration=0.5:offset={durs[0]+durs[1]}[x2];"
                f"[x2]zoompan=z='min(1+0.0004*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p[v]"
            )
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", str(tmp / "a.m4a"),
                 "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-t", str(total),
                 "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac",
                 "-movflags", "+faststart", str(out.with_suffix(".mp4"))], check=True)
        else:
            b.close()
    print("ok", out.with_suffix(".jpg"), out.with_suffix(".mp4") if reel else "")


if __name__ == "__main__":
    main()
