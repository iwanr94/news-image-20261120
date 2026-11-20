#!/usr/bin/env python3
"""Render entry.png: 1024x1024 newspaper-style summary of world news, 20 Nov 2026.
Pure Pillow (no numpy). Text is measured and asserted to fit inside its panel.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40

CREAM      = (239, 233, 222)
CARD       = (251, 248, 241)
INK        = (23, 24, 28)
INK_SOFT   = (74, 76, 84)
MUTED      = (116, 112, 104)
ACCENT     = (165, 18, 27)      # deep red
NAVY       = (22, 50, 79)
GOLD       = (176, 122, 30)
HAIR       = (208, 199, 183)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B  = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R  = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_M  = "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(d, trial, font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked(d, xy, text, font, fill, track=2):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + track


def tracked_w(d, text, font, track=2):
    return sum(tw(d, c, font) for c in text) + track * (len(text) - 1)


def panel(d, box, kicker, headline, body, accent=ACCENT, fg=INK,
          lead=False, hl_size=None, bd_size=14):
    """Draw a card. Raises if any text would overflow the card."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=CARD, outline=HAIR, width=1)
    d.rectangle((x0 + 1, y0 + 1, x0 + 5, y1 - 1), fill=accent)

    pad = 16
    ix0, ix1 = x0 + pad, x1 - pad
    iw = ix1 - ix0
    y = y0 + 14

    kf = F(SANS_B, 11)
    tracked(d, (ix0, y), kicker.upper(), kf, accent, track=1)
    y += 19

    hs = hl_size or (19 if not lead else 36)
    hf = F(SERIF_B if lead else SANS_B, hs)
    lines = wrap(d, headline, hf, iw)
    lh = int(hs * 1.24)
    for ln in lines:
        d.text((ix0, y), ln, font=hf, fill=fg)
        y += lh
    y += 4

    if body:
        bf = F(SANS_R, bd_size)
        blh = int(bd_size * 1.44)
        blines = wrap(d, body, bf, iw)
        for ln in blines:
            d.text((ix0, y), ln, font=bf, fill=INK_SOFT)
            y += blh

    if y > y1 - 6:
        raise ValueError(
            "overflow in panel %r: used=%d box_h=%d" % (kicker, y - y0, y1 - y0))
    return y


def big_stat(d, box, value, label, accent=ACCENT):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=CARD, outline=HAIR, width=1)
    d.rectangle((x0 + 1, y0 + 1, x1 - 1, y0 + 4), fill=accent)
    vf = F(SANS_B, 34)
    vw = tw(d, value, vf)
    d.text(((x0 + x1 - vw) / 2, y0 + 14), value, font=vf, fill=accent)
    lf = F(SANS_M, 11)
    for i, ln in enumerate(wrap(d, label, lf, (x1 - x0) - 20)):
        lw = tw(d, ln, lf)
        d.text(((x0 + x1 - lw) / 2, y0 + 58 + i * 15), ln, font=lf, fill=MUTED)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---------- outer frame ----------
    d.rectangle((0, 0, W - 1, H - 1), outline=INK, width=0)
    d.rectangle((10, 10, W - 11, H - 11), outline=INK, width=2)
    d.rectangle((17, 17, W - 18, H - 18), outline=HAIR, width=1)

    # ---------- masthead ----------
    kf = F(SANS_B, 11)
    kicker = "RINGKASAN BERITA DUNIA"
    kw = tracked_w(d, kicker, kf, 2.6)
    tracked(d, (M, 34), kicker, kf, ACCENT, track=2)
    ed = "EDISI PAGI  ·  WIB"
    d.text((W - M - tw(d, ed, F(SANS_M, 11)), 36), ed, font=F(SANS_M, 11), fill=MUTED)

    d.text((M - 3, 48), "BERITA DUNIA", font=F(SERIF_B, 62), fill=INK)

    # date: unmistakable, in a red bar
    d.rectangle((M, 126, W - M, 174), fill=ACCENT)
    datef = F(SANS_B, 30)
    d.text((M + 18, 137), "Jumat, 20 November 2026", font=datef, fill=(255, 250, 244))
    tag = "8 PERISTIWA PILIHAN"
    d.text((W - M - 18 - tw(d, tag, F(SANS_B, 12)), 149), tag,
           font=F(SANS_B, 12), fill=(255, 214, 208))
    d.rectangle((M, 178, W - M, 181), fill=INK)

    # ---------- lead story (ICJ) ----------
    lead_box = (M, 190, 616, 470)
    # headline block is drawn manually so the stat chip can sit beside the dek
    x0, y0, x1, y1 = lead_box
    d.rounded_rectangle(lead_box, radius=10, fill=CARD, outline=HAIR, width=1)
    d.rectangle((x0 + 1, y0 + 1, x0 + 6, y1 - 1), fill=ACCENT)

    ix = x0 + 20
    iw = (x1 - 20) - ix
    tracked(d, (ix, y0 + 15), "UTAMA  ·  MAHKAMAH INTERNASIONAL", F(SANS_B, 11),
            ACCENT, track=1)

    hf = F(SERIF_B, 44)
    hlines = wrap(d, "ICJ Nyatakan Myanmar Bersalah Genosida", hf, iw)
    y = y0 + 36
    for ln in hlines:
        d.text((ix, y), ln, font=hf, fill=INK)
        y += 53
    y += 6
    d.rectangle((ix, y, ix + 54, y + 3), fill=GOLD)
    y += 14

    df = F(SERIF_R, 19)
    dek = ("Kasus Rohingya: putusan 9-6 — untuk pertama kalinya pengadilan itu "
           "menyatakan sebuah negara bersalah atas genosida.")
    for ln in wrap(d, dek, df, 360):
        d.text((ix, y), ln, font=df, fill=INK_SOFT)
        y += 27

    if y > y1 - 10:
        raise ValueError("lead dek overflow: %d" % (y - y0))

    # stat chip inside the lead card
    chip = (440, y0 + 206, 608, y0 + 206 + 60)
    d.rounded_rectangle(chip, radius=8, fill=(243, 232, 230), outline=(226, 200, 197))
    vf = F(SANS_B, 40)
    d.text((chip[0] + 12, chip[1] + 4), "9-6", font=vf, fill=ACCENT)
    lab_x = chip[0] + 86
    for i, (t, fnt, col) in enumerate((("suara hakim", F(SANS_M, 12), INK_SOFT),
                                       ("ICJ, Den Haag", F(SANS_R, 11), MUTED))):
        if lab_x + tw(d, t, fnt) > chip[2] - 8:
            raise ValueError("chip label overflow: %s" % t)
        d.text((lab_x, chip[1] + 14 + i * 18), t, font=fnt, fill=col)

    # ---------- right rail: second-lead ----------
    panel(d, (628, 190, W - M, 470), "Diplomasi  ·  KTT Shenzhen",
          "Trump, Xi & Putin Bertemu Tiga Pihak Pertama Kali",
          "Deklarasi damai bersama usai pertemuan sekitar 70 menit. Hasilnya "
          "lebih sempit dari harapan: tidak ada terobosan soal Ukraina, Iran, "
          "maupun program nuklir.",
          accent=NAVY, hl_size=25, bd_size=15)

    # small caption block at the foot of the rail card
    cap_y = 414
    d.rectangle((644, cap_y, W - M - 16, cap_y + 1), fill=HAIR)
    for i, ln in enumerate(("Shenzhen, Tiongkok  ·  KTT trilateral pertama",
                            "Hasil di bawah ekspektasi pasar dan sekutu")):
        d.text((644, cap_y + 12 + i * 17), ln, font=F(SANS_M, 11), fill=MUTED)

    # ---------- lower grid: 3 rows x 2 cols ----------
    lx = [M, 512]
    lw = 502 - M
    rx = [512, W - M]
    rows = [(486, 596), (604, 714), (722, 832)]

    panel(d, (lx[0], rows[0][0], lx[1], rows[0][1]), "Timur Tengah  ·  Riyadh",
          "Rudal Houthi Hantam Menara PIF",
          "Serangan mengenai menara dana kekayaan Saudi di distrik finansial Riyadh.",
          hl_size=18, bd_size=13)

    panel(d, (rx[0], rows[0][0], rx[1], rows[0][1]), "Pasar  ·  Wall Street",
          "Anthropic Melonjak 17% di Debut Nasdaq",
          "Ditutup ~$97 dari harga IPO $83. Bursa AS turun hari ke-5, Nikkei -4,8%.",
          accent=NAVY, hl_size=18, bd_size=13)

    panel(d, (lx[0], rows[1][0], lx[1], rows[1][1]), "Eropa Timur  ·  Ukraina",
          "Rusia Serang Kyiv; Jembatan Kerch Dihantam",
          "8 tewas dan 28 luka di Kyiv. Ukraina menyerang Jembatan Kerch untuk "
          "ketiga kalinya pekan ini.",
          hl_size=18, bd_size=13)

    panel(d, (rx[0], rows[1][0], rx[1], rows[1][1]), "Teknologi  ·  GTA 6",
          "GTA 6 Tembus Penjualan $2,3 Miliar",
          "Peluncuran langsung mencatat rekor pendapatan untuk sebuah peluncuran gim.",
          hl_size=18, bd_size=13)

    panel(d, (lx[0], rows[2][0], lx[1], rows[2][1]), "Kesehatan  ·  Kenya",
          "Pasien Ebola Terakhir Dipulangkan",
          "37 hari setelah kasus pertama dilaporkan, Kenya tidak lagi merawat "
          "pasien Ebola.",
          hl_size=18, bd_size=13)

    panel(d, (rx[0], rows[2][0], rx[1], rows[2][1]), "Ekonomi & Politik  ·  Dunia",
          "Utang Global Mendekati 100% PDB",
          "IMF memperingatkan beban utang publik dunia. Senat AS menolak "
          "resolusi perang Iran 51-48.",
          hl_size=18, bd_size=13)

    # ---------- footer ----------
    d.rectangle((M, 850, W - M, 852), fill=INK)
    ff = F(SANS_M, 12)
    d.text((M, 864), "Sumber: laporan kantor berita internasional, 20 November 2026",
           font=ff, fill=INK_SOFT)
    right = "BERITA DUNIA  ·  1024 x 1024"
    d.text((W - M - tw(d, right, ff), 864), right, font=ff, fill=MUTED)

    # thin double rule at very bottom
    d.rectangle((M, 890, W - M, 891), fill=HAIR)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
