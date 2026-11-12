import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from engine import *

OUT = os.path.join(os.path.dirname(__file__), "..")
KW = "TERRA"

def fade_in_out(t, a, b, fi=0.35, fo=0.3):
    return min(prog(t, a, fi), 1 - prog(t, b - fo, fo))

def cta_scene(d, t, t0):
    """Chamada final: Comente TERRA."""
    lt = t - t0
    rich(d, 72, 420, "Quer a rota para *sair das dívidas*?", size=74, reveal=prog(lt, 0, 0.6) )
    a = ease_out(prog(lt, 0.5, 0.4))
    rich(d, 72, 690, "Comente a palavra", size=44, w="Medium", color=MUTED, alpha=a)
    # caixa da palavra-chave pulsando
    s = back_out(prog(lt, 0.7, 0.5)) if lt < 1.2 else 1 + 0.025 * math.sin((lt - 1.2) * 6)
    bw, bh = 820 * s, 250 * s
    cx, cy = W / 2, 900
    if lt > 0.72:
        rrect(d, (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 36 * s, fill=SAND)
        f = font(max(8, int(190 * s)), "Black")
        tw = d.textlength(KW, font=f)
        d.text((cx - tw / 2, cy - 118 * s), KW, font=f, fill=BG)
    b = ease_out(prog(lt, 1.3, 0.5))
    rich(d, 72, 1080, "e receba no direct o link do app *grátis*.", size=50, w="SemiBold", alpha=b, reveal=b)
    c = ease_out(prog(lt, 1.9, 0.4))
    rich(d, 72, 1280, "Prefere ir direto? Link na bio.", size=38, w="Medium", color=MUTED, alpha=c, display=False)
    footnote(d, "App gratuito, feito para o celular. Não oferece empréstimos.", y=1640, alpha=c)

def frame_base(t, total, header_alpha=1.0):
    im = background(); d = ImageDraw.Draw(im)
    header(d, header_alpha)
    progress_bar(d, t, total)
    return im, d

# =====================================================================
# REEL 1 — Notificações
# =====================================================================
NOTIFS = [
    ("CARTÃO", "Sua fatura vence HOJE", RED),
    ("FORNECEDOR", "Boleto em atraso há 5 dias", RED),
    ("BANCO", "Cheque especial em uso", SAND),
    ("EMPRÉSTIMO", "Parcela 7 de 24 vence amanhã", SAND),
    ("COBRANÇA", "3 chamadas perdidas", RED),
    ("CARTÃO 2", "Limite indisponível", RED),
]
R1_T = 19.0
N0, NSTEP = 0.9, 0.85

def reel1(t):
    im, d = frame_base(t, R1_T)
    if t < 6.6:
        rich(d, 72, 240, "Seu celular, *hoje*:", size=92, reveal=prog(t, 0.0, 0.5))
        shake = 0
        y = 470
        count = 0
        for i, (app, msg, col) in enumerate(NOTIFS):
            ti = N0 + i * NSTEP
            p = prog(t, ti, 0.35)
            if p <= 0: continue
            count += 1
            age = t - ti
            if age < 0.35: shake = max(shake, (0.35 - age) * 40)
            e = back_out(p)
            x0 = 72 + (1 - e) * 400
            box = (x0, y, x0 + W - 144, y + 160)
            rrect(d, box, 30, fill=mix(BG, CARD2, p), outline=mix(BG, LINE, p))
            # ícone
            rrect(d, (x0 + 28, y + 36, x0 + 116, y + 124), 22, fill=mix(BG, col, p))
            d.text((x0 + 52, y + 44), "!", font=font(64, "Black"), fill=mix(col, BG, p))
            d.text((x0 + 144, y + 34), app, font=font(26, "SemiBold", False), fill=mix(BG, MUTED, p))
            d.text((x0 + W - 144 - 120, y + 34), "agora", font=font(24, "Regular", False), fill=mix(BG, MUTED, p))
            d.text((x0 + 144, y + 72), msg, font=font(44, "SemiBold", False), fill=mix(BG, WHITE, p))
            y += 182
        if shake > 0:
            dx = int(random.uniform(-shake, shake)); dy = int(random.uniform(-shake, shake) * 0.5)
            im = im.transform(im.size, Image.AFFINE, (1, 0, dx, 0, 1, dy), fillcolor=BG)
        return im
    if t < 7.6:
        im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
        s = back_out(prog(t, 6.6, 0.25))
        f = font(int(230 * s) + 1, "Black")
        tw = d.textlength("PARA.", font=f)
        d.text((W / 2 - tw / 2, H / 2 - 150 * s), "PARA.", font=f, fill=WHITE)
        return im
    if t < 11.4:
        a = fade_in_out(t, 7.6, 11.4)
        rich(d, 72, 560, "Você não precisa pagar tudo hoje.", size=84, alpha=a, reveal=prog(t, 7.6, 0.8))
        rich(d, 72, 860, "Precisa de uma *rota*.", size=120, alpha=a, reveal=prog(t, 9.0, 0.5))
        return im
    if t < 14.4:
        a = fade_in_out(t, 11.4, 14.4, fo=0.25)
        rich(d, 72, 380, "No *Terra à Vista*:", size=80, alpha=a)
        steps = ["Liste dívidas e cartões", "Compare Bola de Neve e Avalanche", "Siga as missões da semana"]
        for i, s_ in enumerate(steps):
            p = ease_out(prog(t, 11.7 + i * 0.6, 0.35)) * a
            y = 600 + i * 210
            rrect(d, (72, y, W - 72, y + 170), 30, fill=mix(BG, CARD, p))
            d.text((120, y + 38), str(i + 1), font=font(84, "Bold"), fill=mix(BG, SAND, p))
            rich(d, 210, y + 56, s_, size=46, w="Medium", alpha=p, display=False, maxw=W - 330)
        return im
    cta_scene(d, t, 14.4)
    return im

# =====================================================================
# REEL 2 — Juros sobre juros (cheque especial)
# =====================================================================
R2_T = 20.0
RATE = 0.08
def reel2(t):
    im, d = frame_base(t, R2_T)
    if t < 2.4:
        rich(d, 72, 620, "Deixei *R$ 1.000* no cheque especial.", size=104, reveal=prog(t, 0, 0.9))
        rich(d, 72, 1060, "E não paguei nada.", size=60, w="Medium", color=MUTED, alpha=ease_out(prog(t, 1.2, 0.4)))
        return im
    if t < 10.0:
        a = fade_in_out(t, 2.4, 10.0, fo=0.3)
        p = ease_in_out(prog(t, 2.9, 5.6))
        months = p * 12
        val = 1000 * (1 + RATE) ** months
        m_int = int(months + 1e-6)
        rich(d, 72, 330, f"Mês {m_int}", size=56, w="SemiBold", color=MUTED, alpha=a)
        col = mix(WHITE, RED, clamp((val - 1600) / 900))
        txt = "R$ " + f"{val:,.0f}".replace(",", ".")
        f = font(200, "Black")
        sh = 0
        if t > 8.5 and t < 9.0: sh = (9.0 - t) * 30
        d.text((72 + random.uniform(-sh, sh), 410), txt, font=f, fill=mix(BG, col, a))
        # barras
        base_y, top_y = 1420, 760
        bw = (W - 144 - 11 * 14) / 12
        maxv = 1000 * (1 + RATE) ** 12
        for i in range(12):
            vi = 1000 * (1 + RATE) ** (i + 1)
            gp = clamp(months - i)
            if gp <= 0: continue
            h = (vi / maxv) * (base_y - top_y) * ease_out(gp)
            x = 72 + i * (bw + 14)
            c = mix(SAND, RED, i / 11)
            rrect(d, (x, base_y - h, x + bw, base_y), 10, fill=mix(BG, c, a))
        d.line((72, base_y + 10, W - 72, base_y + 10), fill=mix(BG, LINE, a), width=3)
        rich(d, 72, 1460, "1 ano depois, a dívida *mais que dobrou*.", size=50, w="SemiBold",
             alpha=a * ease_out(prog(t, 8.6, 0.4)))
        footnote(d, "Exemplo ilustrativo: R$ 1.000 a 8% ao mês (teto do cheque especial para pessoa física e MEI), juros compostos, sem pagamentos. As taxas variam por banco.", y=1590, alpha=a, size=23)
        return im
    if t < 12.6:
        a = fade_in_out(t, 10.0, 12.6)
        rich(d, 72, 600, "Juros sobre juros.", size=110, alpha=a, reveal=prog(t, 10.0, 0.4))
        rich(d, 72, 900, "Cada mês sem *rota* custa mais caro.", size=76, alpha=a, reveal=prog(t, 10.8, 0.7))
        return im
    if t < 15.6:
        a = fade_in_out(t, 12.6, 15.6, fo=0.25)
        rich(d, 72, 360, "No *Terra à Vista* você compara:", size=74, alpha=a)
        cards = [("Bola de Neve", "Quita primeiro a menor dívida. Cada conta zerada dá ânimo."),
                 ("Avalanche", "Quita primeiro a mais cara. Paga menos juros no total.")]
        for i, (h_, b_) in enumerate(cards):
            p = ease_out(prog(t, 12.9 + i * 0.5, 0.4)) * a
            y = 620 + i * 340
            rrect(d, (72, y, W - 72, y + 300), 32, fill=mix(BG, CARD, p), outline=mix(BG, LINE, p))
            d.text((120, y + 44), h_, font=font(60, "Bold"), fill=mix(BG, SAND, p))
            rich(d, 120, y + 140, b_, size=40, w="Regular", alpha=p, display=False, maxw=W - 260, lh=1.3)
        rich(d, 72, 1330, "e vê *quanto tempo* leva em cada um, com os seus números.", size=46, w="Medium",
             alpha=a * ease_out(prog(t, 14.0, 0.4)), display=False)
        return im
    cta_scene(d, t, 15.6)
    return im

# =====================================================================
# REEL 3 — Empresário: dívida da empresa no CPF
# =====================================================================
R3_T = 20.0
CHECKS = ["Cartão pessoal pagando fornecedor", "Empréstimo no seu nome para cobrir o caixa",
          "Cheque especial todo mês", "Não sabe quanto deve, somando tudo"]
def reel3(t):
    im, d = frame_base(t, R3_T)
    if t < 2.6:
        rich(d, 72, 600, "A dívida da empresa foi parar no *seu CPF*?", size=108, reveal=prog(t, 0, 1.0))
        return im
    if t < 8.8:
        a = fade_in_out(t, 2.6, 8.8)
        rich(d, 72, 300, "Marque o que já aconteceu com você:", size=64, alpha=a)
        for i, c in enumerate(CHECKS):
            ti = 3.3 + i * 1.15
            p = ease_out(prog(t, ti, 0.35)) * a
            y = 560 + i * 230
            rrect(d, (72, y, W - 72, y + 190), 30, fill=mix(BG, CARD, p))
            bx = 116
            rrect(d, (bx, y + 55, bx + 80, y + 135), 18, outline=mix(BG, SAND, p), width=5)
            ck = prog(t, ti + 0.45, 0.25)
            if ck > 0:
                rrect(d, (bx, y + 55, bx + 80, y + 135), 18, fill=mix(BG, SAND, ck * a))
                pts = [(bx + 18, y + 96), (bx + 34, y + 114), (bx + 64, y + 74)]
                d.line(pts, fill=BG, width=10, joint="curve")
            rich(d, 236, y + 62, c, size=42, w="SemiBold", alpha=p, display=False, maxw=W - 360, lh=1.2)
        return im
    if t < 12.0:
        a = fade_in_out(t, 8.8, 12.0)
        n = 9.3 * ease_out(prog(t, 8.9, 1.2))
        txt = f"{n:.1f}".replace(".", ",") + " milhões"
        d.text((72, 520), txt, font=font(150, "Black"), fill=mix(BG, SAND, a))
        rich(d, 72, 740, "de empresas inadimplentes no Brasil.", size=72, alpha=a, reveal=prog(t, 9.6, 0.7))
        rich(d, 72, 1000, "*Recorde* da série.", size=72, alpha=a * ease_out(prog(t, 10.4, 0.4)))
        footnote(d, "Fonte: Serasa Experian, indicador de inadimplência das empresas, agosto de 2026.", y=1600, alpha=a)
        return im
    if t < 15.4:
        a = fade_in_out(t, 12.0, 15.4, fo=0.25)
        rich(d, 72, 420, "Sair começa por *enxergar tudo*.", size=100, alpha=a, reveal=prog(t, 12.0, 0.6))
        rich(d, 72, 820, "O Terra à Vista organiza as dívidas e cartões no seu nome e mostra, passo a passo, a rota até quitar.",
             size=50, w="Medium", alpha=a * ease_out(prog(t, 13.0, 0.5)), display=False, lh=1.3)
        return im
    cta_scene(d, t, 15.4)
    return im

if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3"]
    random.seed(7)
    jobs = {
        "1": ("reel-notificacoes.mp4", R1_T, reel1,
              [(N0 + i * NSTEP, "buzz") for i in range(6)] + [(6.6, "stop"), (6.6, "pop"), (14.4, "whoosh"), (15.1, "ding")]),
        "2": ("reel-juros.mp4", R2_T, reel2,
              [(2.4, "whoosh"), (8.5, "buzz"), (10.0, "pop"), (12.6, "whoosh"), (15.6, "whoosh"), (16.3, "ding")]),
        "3": ("reel-empresario.mp4", R3_T, reel3,
              [(3.3 + i * 1.15 + 0.45, "pop") for i in range(4)] + [(8.8, "whoosh"), (12.0, "pop"), (15.4, "whoosh"), (16.1, "ding")]),
    }
    for k in which:
        name, dur, fn, hits = jobs[k]
        wav = f"/tmp/claude-0/-home-claude-fichapro-midia/ae65bafb-d465-55fb-9408-26eab4eea344/scratchpad/{k}.wav"
        synth_track(wav, dur, bpm=[0, 112, 96, 104][int(k)], hits=hits)
        render(os.path.join(OUT, name), dur, fn, audio=wav)
        print("ok", name)
