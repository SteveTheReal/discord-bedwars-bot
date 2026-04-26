import aiohttp

MOJANG_URL = "https://api.mojang.com/users/profiles/minecraft/"
HYPIXEL_URL = "https://api.hypixel.net/player"

# Maps mode name -> Hypixel stat key prefix
MODE_PREFIXES = {
    "overall": "",
    "solo":    "eight_one_",
    "doubles": "eight_two_",
    "threes":  "four_three_",
    "fours":   "four_four_",
    "4v4":     "two_four_",
}


async def get_uuid(session: aiohttp.ClientSession, username: str) -> str | None:
    async with session.get(f"{MOJANG_URL}{username}") as resp:
        if resp.status == 200:
            data = await resp.json(content_type=None)
            return data.get("id")
        return None


async def get_player(session: aiohttp.ClientSession, uuid: str, api_key: str) -> dict | None:
    params = {"key": api_key, "uuid": uuid}
    async with session.get(HYPIXEL_URL, params=params) as resp:
        if resp.status != 200:
            return None
        data = await resp.json(content_type=None)
        if data.get("success") and data.get("player"):
            return data["player"]
        return None


def _ratio(a: int, b: int) -> str:
    if b == 0:
        return "∞"
    return f"{a / b:.2f}"


DUEL_MODE_PREFIXES = {
    "overall":  "",
    "uhc":      "UHC_DUEL_",
    "op":       "OP_DUEL_",
    "bridge":   "BRIDGE_DUEL_",
    "skywars":  "SW_DUEL_",
    "blitz":    "BLITZ_DUEL_",
    "nodebuff": "NO_DEBUFF_DUEL_",
    "bow":      "BOW_DUEL_",
    "classic":  "CLASSIC_DUEL_",
    "combo":    "COMBO_DUEL_",
    "sumo":     "SUMO_DUEL_",
    "boxing":   "BOXING_DUEL_",
    "megawalls": "MW_DUEL_",
}


def parse_bedwars(player: dict, mode: str = "overall") -> dict:
    bw = player.get("stats", {}).get("Bedwars", {})
    achievements = player.get("achievements", {})
    prefix = MODE_PREFIXES.get(mode, "")

    final_kills  = bw.get(f"{prefix}final_kills_bedwars", 0)
    final_deaths = bw.get(f"{prefix}final_deaths_bedwars", 0)
    wins         = bw.get(f"{prefix}wins_bedwars", 0)
    losses       = bw.get(f"{prefix}losses_bedwars", 0)
    winstreak    = bw.get("winstreak" if mode == "overall" else f"{prefix}winstreak")

    return {
        "level":        achievements.get("bedwars_level", 0),
        "final_kills":  final_kills,
        "final_deaths": final_deaths,
        "fkdr":         _ratio(final_kills, final_deaths),
        "wins":         wins,
        "losses":       losses,
        "wlr":          _ratio(wins, losses),
        "winstreak":    f"{winstreak:,}" if winstreak is not None else "Hidden",
    }


def parse_duels(player: dict, mode: str = "overall") -> dict:
    duels  = player.get("stats", {}).get("Duels", {})
    prefix = DUEL_MODE_PREFIXES.get(mode, "")

    wins      = duels.get(f"{prefix}wins", 0)
    losses    = duels.get(f"{prefix}losses", 0)
    kills     = duels.get(f"{prefix}kills", 0)
    deaths    = duels.get(f"{prefix}deaths", 0)
    ws_key    = "current_winstreak" if mode == "overall" else f"{prefix}current_winstreak"
    winstreak = duels.get(ws_key)

    return {
        "wins":      wins,
        "losses":    losses,
        "wlr":       _ratio(wins, losses),
        "kills":     kills,
        "deaths":    deaths,
        "kdr":       _ratio(kills, deaths),
        "winstreak": f"{winstreak:,}" if winstreak is not None else "Hidden",
    }
