"""Motor de criativos Terra à Vista (9:16). Desenha quadros com PIL e gera MP4 com ffmpeg."""
import math, subprocess, wave, struct, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS = 30
BG = (5, 11, 22)
CARD = (13, 24, 44)
CARD2 = (19, 34, 60)
LINE = (34, 52, 82)
WHITE = (244, 246, 250)
MUTED = (150, 163, 184)
SAND = (233, 201, 138)
TEAL = (64, 190, 200)
RED = (238, 84, 84)
GREEN = (88, 204, 140)

FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def font(size, w="Bold", display=True):
    key = (size, w, display)
    if key not in _fc:
        name = f"InterDisplay-{w}.otf" if display else f"Inter-{w}.otf"
        _fc[key] = ImageFont.truetype(FD + name, size)
    return _fc[key]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur): return clamp((t - start) / dur) if dur > 0 else (1.0 if t >= start else 0.0)
def ease_out(x): return 1 - (1 - x) ** 3
def ease_in_out(x): return 3 * x * x - 2 * x * x * x
def back_out(x, s=1.70158):
    x = x - 1
    return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))

# ---------- background ----------
_bg = None
def background():
    global _bg
    if _bg is None:
        im = Image.new("RGB", (W, H), BG)
        glow = Image.new("RGB", (W, H), (0, 0, 0))
        g = ImageDraw.Draw(glow)
        g.ellipse((560, -420, 1500, 520), fill=(18, 78, 96))
        g.ellipse((-500, 1500, 380, 2350), fill=(10, 40, 64))
        glow = glow.filter(ImageFilter.GaussianBlur(190))
        im = Image.fromarray(np.clip(np.asarray(im, dtype=np.int16) + np.asarray(glow, dtype=np.int16), 0, 255).astype(np.uint8))
        _bg = im
    return _bg.copy()

def logo(d, x, y, s=1.0, alpha=1.0):
    """Sol nascendo sobre ondas + nome."""
    c = mix(BG, SAND, alpha); t = mix(BG, TEAL, alpha); wcol = mix(BG, WHITE, alpha)
    r = int(13 * s)
    d.pieslice((x, y, x + 2 * r, y + 2 * r), 180, 360, fill=c)
    for k in range(2):
        yy = y + r + int((6 + 7 * k) * s)
        pts = [(x - 4 * s + i, yy + 2.6 * s * math.sin(i / (4.2 * s))) for i in range(int(2 * r + 8 * s))]
        d.line(pts, fill=t, width=max(2, int(3 * s)))
    f = font(int(30 * s), "Bold")
    tx = x + 2 * r + int(16 * s)
    d.text((tx, y - 2 * s), "TERRA ", font=f, fill=wcol)
    d.text((tx + d.textlength("TERRA ", font=f), y - 2 * s), "À VISTA", font=f, fill=c)

def header(d, alpha=1.0):
    logo(d, 72, 118, 1.0, alpha)
    f = font(22, "SemiBold", False)
    txt = "OCEANOS SISTEMAS"
    sp = 3
    total = sum(d.textlength(ch, font=f) + sp for ch in txt) - sp
    x = W - 72 - total
    for ch in txt:
        d.text((x, 124), ch, font=f, fill=mix(BG, MUTED, alpha)); x += d.textlength(ch, font=f) + sp

# ---------- rich text: *destaque* em areia ----------
def _tokens(text):
    out, hl = [], False
    for part in text.split("*"):
        for i, w in enumerate(part.split(" ")):
            if w != "":
                if i == 0 and out and part[:1] not in (" ", "") and w[0] in ".,:;?!)":
                    out.append((w, hl, True))
                else:
                    out.append((w, hl, False))
        hl = not hl
    return out

def _join(toks):
    s = ""
    for i, (w, _, ns) in enumerate(toks):
        s += ("" if (i == 0 or ns) else " ") + w
    return s

def layout(text, f, maxw):
    lines, cur = [], []
    for line_txt in text.split("\n"):
        cur = []
        for w, hl, ns in _tokens(line_txt):
            test = _join(cur + [(w, hl, ns)])
            if cur and ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(test, font=f) > maxw:
                lines.append(cur); cur = []
            if ns and cur:
                cur.append((w, hl, ns))
            else:
                cur.append((w, hl, False))
        lines.append(cur)
    return lines

def rich(d, x, y, text, size=96, maxw=W - 144, w="Bold", color=WHITE, hl=SAND, lh=1.08,
         alpha=1.0, reveal=1.0, align="left", display=True):
    """Desenha texto com destaque. reveal 0..1 revela palavra a palavra. Retorna altura."""
    f = font(size, w, display)
    lines = layout(text, f, maxw)
    nwords = sum(len(l) for l in lines)
    shown = reveal * nwords
    k = 0
    yy = y
    for l in lines:
        lw = d.textlength(_join(l), font=f)
        xx = x if align == "left" else x + (maxw - lw) / 2
        for j, (word, ishl, ns) in enumerate(l):
            if ns and j > 0:
                xx -= d.textlength(" ", font=f)
            a = clamp(shown - k) * alpha
            if a > 0:
                base = hl if ishl else color
                dy = (1 - ease_out(clamp(shown - k))) * size * 0.35
                d.text((xx, yy + dy), word, font=f, fill=mix(BG, base, a))
            xx += d.textlength(word + " ", font=f)
            k += 1
        yy += size * lh
    return yy - y

def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def pill(d, cx, y, text, size=36, fg=BG, bg=SAND, padx=40, pady=22, alpha=1.0, scale=1.0, left=None):
    f = font(int(size * scale), "Bold", False)
    tw = d.textlength(text, font=f)
    w_, h_ = tw + 2 * padx * scale, size * scale + 2 * pady * scale
    x0 = (left if left is not None else cx - w_ / 2)
    rrect(d, (x0, y, x0 + w_, y + h_), h_ / 2, fill=mix(BG, bg, alpha))
    d.text((x0 + padx * scale, y + pady * scale - size * scale * 0.12), text, font=f, fill=mix(BG, fg, alpha) if fg != BG else mix(bg, BG, alpha))
    return w_, h_

def progress_bar(d, t, total, segs=5):
    y = 1780; x0 = 72; gap = 12; sw = (W - 144 - gap * (segs - 1)) / segs
    for i in range(segs):
        p = clamp(t / total * segs - i)
        rrect(d, (x0 + i * (sw + gap), y, x0 + i * (sw + gap) + sw, y + 6), 3, fill=LINE)
        if p > 0:
            rrect(d, (x0 + i * (sw + gap), y, x0 + i * (sw + gap) + sw * p, y + 6), 3, fill=SAND)

def footnote(d, text, y=1700, alpha=1.0, size=24):
    rich(d, 72, y, text, size=size, w="Regular", color=MUTED, alpha=alpha, display=False, lh=1.35)

# ---------- video ----------
def render(path, dur, draw_fn, audio=None):
    n = int(dur * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high"]
    if audio: cmd += ["-c:a", "aac", "-b:a", "160k", "-shortest"]
    cmd += ["-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        im = draw_fn(t)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    assert p.returncode == 0, "ffmpeg falhou"

# ---------- áudio sintetizado (trilha original, sem direitos de terceiros) ----------
SR = 44100
def synth_track(path, dur, bpm=104, hits=(), chords=None, intensity=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    beat = 60 / bpm
    chords = chords or [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]  # Am F C G
    bar = beat * 4
    for i in range(int(dur / bar) + 1):
        notes = chords[i % len(chords)]
        s, e = int(i * bar * SR), min(n, int((i + 1) * bar * SR))
        if s >= n: break
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.35)
        for m in notes:
            fq = 440 * 2 ** ((m - 69) / 12)
            out[s:e] += 0.05 * env * (np.sin(2 * np.pi * fq * tt) + 0.3 * np.sin(2 * np.pi * fq * 2 * tt))
        bass = 440 * 2 ** ((notes[0] - 12 - 69) / 12)
        out[s:e] += 0.09 * env * np.sin(2 * np.pi * bass * tt)
    k = 0
    while k * beat < dur:
        s = int(k * beat * SR); L = min(int(0.35 * SR), n - s)
        tt = np.arange(L) / SR
        out[s:s + L] += 0.5 * intensity * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
        hs = int((k + 0.5) * beat * SR)
        if hs < n:
            Lh = min(int(0.05 * SR), n - hs)
            out[hs:hs + Lh] += 0.06 * intensity * np.random.randn(Lh) * np.exp(-np.arange(Lh) / SR * 80)
        k += 1
    for (ht, kind) in hits:
        s = int(ht * SR)
        if s >= n: continue
        if kind == "pop":
            L = min(int(0.12 * SR), n - s); tt = np.arange(L) / SR
            out[s:s + L] += 0.35 * np.sin(2 * np.pi * (900 + 600 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 35)
        elif kind == "buzz":
            L = min(int(0.28 * SR), n - s); tt = np.arange(L) / SR
            out[s:s + L] += 0.22 * np.sign(np.sin(2 * np.pi * 150 * tt)) * np.exp(-tt * 8) * (0.5 + 0.5 * np.sin(2 * np.pi * 20 * tt))
        elif kind == "whoosh":
            L = min(int(0.5 * SR), n - s); tt = np.arange(L) / SR
            nz = np.convolve(np.random.randn(L), np.ones(30) / 30, mode="same")
            out[s:s + L] += 0.5 * nz * np.sin(np.pi * tt / 0.5)
        elif kind == "ding":
            L = min(int(1.2 * SR), n - s); tt = np.arange(L) / SR
            for fq in (1318.5, 1975.5):
                out[s:s + L] += 0.12 * np.sin(2 * np.pi * fq * tt) * np.exp(-tt * 4)
        elif kind == "stop":  # corte seco: silencia a trilha por 0.6s
            L = min(int(0.6 * SR), n - s); out[s:s + L] *= 0.08
    fade = int(0.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
    data = (out * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes(data.tobytes())
