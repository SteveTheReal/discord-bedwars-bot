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
_HEADER_BOT = 66   # bottom edge of header strip
_Y0         = 84   # first panel — 18px gap below header


# BedWars prestige color by level bracket (every 100 levels)
_PRESTIGE_COLORS = [
    (170, 170, 170),  # 0-99    Iron       gray
    (255, 255, 255),  # 100-199 Iron       white
    (255, 170,   0),  # 200-299 Gold       gold
    ( 85, 255, 255),  # 300-399 Diamond    cyan
    ( 85, 255,  85),  # 400-499 Emerald    green
    ( 85, 170, 255),  # 500-599 Sapphire   blue
    (255,  85,  85),  # 600-699 Ruby       red
    (255,  85, 255),  # 700-799 Crystal    pink
    ( 85, 200, 255),  # 800-899 Opal       light blue
    (170,  85, 255),  # 900-999 Amethyst   purple
    (255, 215,   0),  # 1000+   Rainbow    gold (simplified)
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

    # Optional footer stat (centred below the grid)
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
    rows = [
        [("Level",       str(stats["level"]),          _prestige_color(stats["level"])),
         ("Final Kills", f"{stats['final_kills']:,}",  GREEN),
         ("FKDR",        stats["fkdr"],                GOLD)],
        [("Wins",        f"{stats['wins']:,}",          GREEN),
         ("WLR",         stats["wlr"],                 GOLD),
         ("Winstreak",   stats["winstreak"],            CYAN)],
    ]
    return _make(player, "BedWars", mode, BW_ACCENT, rows)


def duels_card(player: str, mode: str, stats: dict) -> io.BytesIO:
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
