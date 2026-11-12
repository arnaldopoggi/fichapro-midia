import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from engine import *

OUT = os.path.join(os.path.dirname(__file__), "..")

def base():
    im = background(); d = ImageDraw.Draw(im); header(d); return im, d

def option(d, y, letter, text, h=150):
    rrect(d, (72, y, W - 72, y + h), 30, fill=CARD, outline=LINE)
    d.text((120, y + h / 2 - 46), letter, font=font(80, "Bold"), fill=SAND)
    d.text((220, y + h / 2 - 28), text, font=font(48, "Medium", False), fill=WHITE)

def s1():
    im, d = base()
    rich(d, 72, 300, "Quanto da sua renda vai para *dívidas* todo mês?", size=96)
    for i, (l, t) in enumerate([("A", "Até 10%"), ("B", "De 10% a 30%"), ("C", "Mais de 30%"), ("D", "Prefiro nem saber")]):
        option(d, 760 + i * 180, l, t)
    rich(d, 72, 1520, "Responda *A, B, C ou D* por mensagem.", size=46, w="SemiBold", display=False)
    return im

def s2():
    im, d = base()
    d.text((72, 420), "84,2 milhões", font=font(138, "Black"), fill=SAND)
    rich(d, 72, 640, "de brasileiros inadimplentes. Recorde.", size=80)
    rrect(d, (72, 1000, W - 72, 1003), 1, fill=LINE)
    rich(d, 72, 1070, "Você não está sozinho.\nMas não precisa ficar *parado*.", size=62, w="SemiBold", lh=1.25)
    pill(d, 0, 1400, "Mande TERRA por mensagem", size=40, left=72)
    footnote(d, "Fonte: Serasa, indicador de inadimplência de pessoas físicas, 2026.", y=1560)
    return im

def s3():
    im, d = base()
    rich(d, 72, 280, "Bola de Neve ou *Avalanche*?", size=100)
    cards = [("A", "Bola de Neve", "Quita primeiro a menor dívida. Cada conta zerada dá ânimo para a próxima."),
             ("B", "Avalanche", "Quita primeiro a dívida mais cara. Você paga menos juros no total.")]
    for i, (l, h_, b_) in enumerate(cards):
        y = 620 + i * 430
        rrect(d, (72, y, W - 72, y + 390), 34, fill=CARD, outline=LINE)
        d.text((120, y + 46), l, font=font(64, "Black"), fill=SAND)
        d.text((200, y + 52), h_, font=font(62, "Bold"), fill=WHITE)
        rich(d, 120, y + 170, b_, size=42, w="Regular", display=False, maxw=W - 260, lh=1.35)
    rich(d, 72, 1520, "Vote *A ou B* por mensagem. O app compara os dois com os seus números.", size=40, w="Medium", display=False, lh=1.3)
    return im

def s4():
    im, d = base()
    d.text((72, 300), "PARA QUEM TEM EMPRESA", font=font(30, "SemiBold", False), fill=SAND)
    rich(d, 72, 370, "Se a empresa paga com o seu cartão, a dívida é *sua*.", size=100)
    for i, t in enumerate(["Coloque tudo no papel", "Saia do rotativo primeiro", "Escolha um método e siga toda semana"]):
        y = 980 + i * 150
        d.text((72, y), f"0{i+1}", font=font(48, "Bold"), fill=SAND)
        rich(d, 170, y + 4, t, size=46, w="Medium", display=False, maxw=W - 250)
    rich(d, 72, 1460, "O Terra à Vista organiza as dívidas e cartões no seu nome e mostra a rota até quitar. *Grátis.*",
         size=38, w="Regular", color=MUTED, display=False, lh=1.35)
    return im

def s5():
    im, d = base()
    rich(d, 72, 380, "Quer sair das dívidas com uma *rota*?", size=96)
    rich(d, 72, 760, "Mande por mensagem:", size=48, w="Medium", color=MUTED, display=False)
    rrect(d, (72, 850, W - 72, 1130), 40, fill=SAND)
    f = font(210, "Black"); tw = d.textlength("TERRA", font=f)
    d.text((W / 2 - tw / 2, 862), "TERRA", font=f, fill=BG)
    rich(d, 72, 1200, "e receba o link do app *grátis*.", size=56, w="SemiBold")
    footnote(d, "App gratuito, feito para o celular. Não oferece empréstimos.", y=1500, size=28)
    return im

# ---------- story animado: simulação do direct ----------
ST = 9.0
def s6(t):
    im = background(); d = ImageDraw.Draw(im); header(d)
    rich(d, 72, 260, "É só mandar *uma palavra*.", size=84, reveal=prog(t, 0, 0.6))
    # janela de conversa
    top, bot = 520, 1560
    rrect(d, (60, top, W - 60, bot), 44, fill=(9, 17, 32), outline=LINE)
    d.text((110, top + 40), "Mensagens", font=font(36, "SemiBold", False), fill=WHITE)
    d.line((60, top + 110, W - 60, top + 110), fill=LINE, width=2)
    # campo de digitação
    word = "TERRA"
    typed = int(clamp((t - 1.2) / 1.0) * len(word) + 0.0001) if t < 2.6 else (0 if t >= 2.6 else len(word))
    fy = bot - 140
    rrect(d, (100, fy, W - 220, fy + 96), 48, fill=CARD2)
    if t < 2.6:
        txt = word[:typed]
        d.text((140, fy + 22), txt if txt else "Mensagem...", font=font(44, "Medium", False), fill=WHITE if txt else MUTED)
        if txt and int(t * 3) % 2 == 0:
            cx = 140 + d.textlength(txt, font=font(44, "Medium", False)) + 4
            d.line((cx, fy + 24, cx, fy + 72), fill=SAND, width=4)
    else:
        d.text((140, fy + 22), "Mensagem...", font=font(44, "Medium", False), fill=MUTED)
    pr = 1 + 0.15 * (1 - abs(clamp((t - 2.45) / 0.15) * 2 - 1)) if 2.3 < t < 2.6 else 1
    r = 48 * pr
    d.ellipse((W - 200 + 48 - r, fy + 48 - r, W - 200 + 48 + r, fy + 48 + r), fill=SAND)
    d.polygon([(W - 172, fy + 30), (W - 120, fy + 48), (W - 172, fy + 66)], fill=BG)
    # bolha enviada
    if t > 2.6:
        p = back_out(prog(t, 2.6, 0.3))
        f = font(46, "Bold", False); tw = d.textlength(word, font=f)
        bw = tw + 80; x1 = W - 110; y0 = top + 170 + (1 - p) * 60
        rrect(d, (x1 - bw, y0, x1, y0 + 100), 40, fill=mix(BG, SAND, clamp(p)))
        d.text((x1 - bw + 40, y0 + 22), word, font=f, fill=BG)
    # digitando...
    if 3.2 < t < 4.4:
        y0 = top + 320
        rrect(d, (110, y0, 290, y0 + 90), 40, fill=CARD2)
        for k in range(3):
            a = 0.4 + 0.6 * abs(math.sin(t * 6 + k))
            d.ellipse((150 + k * 44, y0 + 33, 174 + k * 44, y0 + 57), fill=mix(CARD2, WHITE, a))
    if t > 4.4:
        p = ease_out(prog(t, 4.4, 0.35))
        y0 = top + 320 + (1 - p) * 40
        rrect(d, (110, y0, W - 180, y0 + 300), 40, fill=mix(BG, CARD2, p))
        rich(d, 150, y0 + 36, "Aqui está o link do *Terra à Vista*, o app gratuito para sair das dívidas:", size=40,
             w="Medium", display=False, maxw=W - 380, alpha=p, lh=1.3)
        d.text((150, y0 + 220), "terra.oceanosistemas.com.br", font=font(38, "SemiBold", False), fill=mix(BG, TEAL, p))
    if t > 5.6:
        a = ease_out(prog(t, 5.6, 0.5))
        pill(d, W / 2, 1640, "Mande TERRA agora", size=46, alpha=a)
    return im

if __name__ == "__main__":
    for name, fn in [("story-1-quiz-renda", s1), ("story-2-84-milhoes", s2), ("story-3-bola-avalanche", s3),
                     ("story-4-empresario", s4), ("story-5-cta-terra", s5)]:
        fn().save(os.path.join(OUT, name + ".jpg"), quality=93)
    if "video" in sys.argv:
        wav = "/tmp/claude-0/-home-claude-fichapro-midia/ae65bafb-d465-55fb-9408-26eab4eea344/scratchpad/s6.wav"
        synth_track(wav, ST, bpm=100, hits=[(1.2 + i * 0.2, "pop") for i in range(5)] + [(2.6, "whoosh"), (4.4, "ding")], intensity=0.6)
        render(os.path.join(OUT, "story-6-direct-animado.mp4"), ST, s6, audio=wav)
    print("ok")
