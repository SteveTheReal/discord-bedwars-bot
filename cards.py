from PIL import Image, ImageDraw, ImageFont
import io

_FONTS = "C:/Windows/Fonts/"


def _f(name: str, size: int) -> ImageFont.FreeTypeFont:
    for fn in (name, "arialbd.ttf", "segoeuib.ttf"):
        try:
            return ImageFont.truetype(_FONTS + fn, size)
        except OSError:
            continue
    return ImageFont.load_default()


# Palette
BG    = (14, 14, 26)
PANEL = (24, 24, 44)
WHITE = (235, 235, 250)
GRAY  = (110, 115, 145)
GREEN = (78,  212, 112)
RED   = (212,  82,  82)
GOLD  = (255, 192,  48)
CYAN  = (68,  172, 255)

BW_ACCENT = (255, 163,   0)
DU_ACCENT = (  0, 158, 255)

_W          = 620
_PAD        = 12
_COLS       = 3
_PH         = 80
_PW         = (_W - _PAD * (_COLS + 1)) // _COLS
_HEADER_BOT = 66
_Y0         = 84


# Full BedWars prestige color table — one entry per 100-level bracket
_PRESTIGE_COLORS = [
    # idx  levels      prestige         colour
    (170, 170, 170),  # 0    0-99     Iron             gray
    (255, 255, 255),  # 1    100-199  Iron             white
    (255, 170,   0),  # 2    200-299  Gold             gold
    ( 85, 255, 255),  # 3    300-399  Diamond          aqua
    ( 85, 255,  85),  # 4    400-499  Emerald          green
    ( 85, 85,  255),  # 5    500-599  Sapphire         blue
    (255,  85,  85),  # 6    600-699  Ruby             red
    (255,  85, 255),  # 7    700-799  Crystal          pink
    ( 85, 210, 255),  # 8    800-899  Opal             light blue
    (170,  85, 255),  # 9    900-999  Amethyst         purple
    (255, 215,   0),  # 10   1000-1099 Rainbow         gold (rainbow simplified)
    (200, 200, 200),  # 11   1100-1199 Iron Prime      silver
    (255, 200,  40),  # 12   1200-1299 Gold Prime      bright gold
    ( 50, 225, 225),  # 13   1300-1399 Diamond Prime   bright aqua
    ( 50, 225,  50),  # 14   1400-1499 Emerald Prime   bright green
    ( 50, 100, 255),  # 15   1500-1599 Sapphire Prime  bright blue
    (225,  50,  50),  # 16   1600-1699 Ruby Prime      bright red
    (225,  50, 225),  # 17   1700-1799 Crystal Prime   bright pink
    ( 50, 200, 245),  # 18   1800-1899 Opal Prime      sky blue
    (155,  50, 230),  # 19   1900-1999 Amethyst Prime  deep purple
    (215, 225, 235),  # 20   2000-2099 Mirror          silver-white
    (255, 245, 140),  # 21   2100-2199 Light           pale yellow
    (255, 150,  95),  # 22   2200-2299 Dawn            orange-pink
    (150,  70, 180),  # 23   2300-2399 Dusk            violet
    (140, 215, 255),  # 24   2400-2499 Air             sky blue
    ( 70, 205, 160),  # 25   2500-2599 Wind            teal
    (120,  70, 220),  # 26   2600-2699 Nebula          indigo
    (255, 235,  50),  # 27   2700-2799 Thunder         yellow
    (105, 155,  70),  # 28   2800-2899 Earth           olive
    ( 50, 140, 255),  # 29   2900-2999 Water           ocean blue
    (255,  85,  30),  # 30   3000+     Fire            orange-red
]


def _prestige_color(level: int) -> tuple:
    return _PRESTIGE_COLORS[min(level // 100, len(_PRESTIGE_COLORS) - 1)]


def _make(player: str, game: str, mode: str, accent: tuple,
          rows: list, footer: tuple | None = None) -> io.BytesIO:

    n_rows = len(rows)
    h = _Y0 + n_rows * (_PH + _PAD) + (48 if footer else 20) + 8

    img  = Image.new("RGB", (_W, h), BG)
    draw = ImageDraw.Draw(img)

    f_title = _f("segoeuib.ttf", 19)
    f_lbl   = _f("segoeuib.ttf", 11)
    f_val   = _f("ariblk.ttf",   34)
    f_foot  = _f("arialbd.ttf",  16)

    # Top accent bar
    draw.rectangle([0, 0, _W, 5], fill=accent)

    # Header strip
    draw.rectangle([0, 5, _W, _HEADER_BOT], fill=(20, 20, 36))
    draw.text((_W // 2, (_HEADER_BOT + 5) // 2),
              f"{game}  [{mode}]  ·  {player}",
              font=f_title, fill=WHITE, anchor="mm")

    # Stat panels
    for r, row in enumerate(rows):
        for c, (lbl, val, color) in enumerate(row):
            x = _PAD + c * (_PW + _PAD)
            y = _Y0 + r * (_PH + _PAD)
            draw.rounded_rectangle([x, y, x + _PW, y + _PH], radius=8, fill=PANEL)
            draw.text((x + _PW // 2, y + 15), lbl, font=f_lbl, fill=GRAY,  anchor="mt")
            draw.text((x + _PW // 2, y + 52), val, font=f_val, fill=color, anchor="mm")

    # Optional footer stat
    if footer:
        lbl, val, color = footer
        fy = _Y0 + n_rows * (_PH + _PAD) + 24
        draw.text((_W // 2, fy),
                  f"{lbl}:  {val}", font=f_foot, fill=color, anchor="mm")

    # Bottom accent bar
    draw.rectangle([0, h - 5, _W, h], fill=accent)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def bedwars_card(player: str, mode: str, stats: dict) -> io.BytesIO:
    # Column colours: col 0 = GREEN, col 1 = GOLD, col 2 = CYAN
    # Level is the one exception — it uses the prestige colour.
    rows = [
        [("Level",       str(stats["level"]),          _prestige_color(stats["level"])),
         ("Final Kills", f"{stats['final_kills']:,}",  GOLD),
         ("FKDR",        stats["fkdr"],                CYAN)],
        [("Wins",        f"{stats['wins']:,}",          GREEN),
         ("WLR",         stats["wlr"],                 GOLD),
         ("Winstreak",   stats["winstreak"],            CYAN)],
    ]
    return _make(player, "BedWars", mode, BW_ACCENT, rows)


def duels_card(player: str, mode: str, stats: dict) -> io.BytesIO:
    # Column colours: col 0 = GREEN, col 1 = RED, col 2 = GOLD
    rows = [
        [("Wins",   f"{stats['wins']:,}",   GREEN),
         ("Losses", f"{stats['losses']:,}", RED),
         ("WLR",    stats["wlr"],           GOLD)],
        [("Kills",  f"{stats['kills']:,}",  GREEN),
         ("Deaths", f"{stats['deaths']:,}", RED),
         ("KDR",    stats["kdr"],           GOLD)],
    ]
    return _make(player, "Duels", mode, DU_ACCENT, rows,
                 footer=("Winstreak", stats["winstreak"], CYAN))
