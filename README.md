# 🏆 Hypixel Stats Bot

A Discord bot that instantly fetches and displays BedWars and Duels statistics for any Hypixel player — directly in your server.

---

## Preview

**BedWars** — `/bedwars Overall gamerboy80`

```
╔══════════════════════════════════════╗
║  BedWars Stats [Overall] · gamerboy80 ║
╠══════════════════════════════════════╣
║ ⭐ Level       │ 1,000               ║
║ 🗡️ Final Kills │ 132,804             ║
║ 💀 FKDR        │ 24.61               ║
║ 🏆 Wins        │ 21,450              ║
║ 📊 WLR         │ 12.38               ║
║ 🔥 Winstreak   │ 142                 ║
╚══════════════════════════════════════╝
```

**Duels** — `/duels UHC gamerboy80`

```
╔══════════════════════════════════════╗
║  Duels Stats [UHC] · gamerboy80      ║
╠══════════════════════════════════════╣
║ 🏆 Wins        │ 3,241               ║
║ 💀 Losses      │ 812                 ║
║ 📊 WLR         │ 3.99                ║
║ ⚔️ Kills       │ 9,104               ║
║ 🩸 Deaths      │ 2,190               ║
║ 💢 KDR         │ 4.16                ║
║ 🔥 Winstreak   │ 28                  ║
╚══════════════════════════════════════╝
```

---

## Commands

### `/bedwars <mode> <username>`
Look up BedWars stats for any player. Pick a mode from the dropdown, then enter the username.

| Mode | Description |
|------|-------------|
| Overall | Combined stats across all modes |
| Solo | Solo (1v1v1v1v1v1v1v1) |
| Doubles | Doubles (2v2v2v2) |
| Threes | Threes (3v3v3v3) |
| Fours | Fours (4v4v4v4) |
| 4v4 | 4v4 |

**Stats shown:** Level, Final Kills, FKDR, Wins, WLR, Winstreak

---

### `/duels <mode> <username>`
Look up Duels stats for any player. Pick a mode from the dropdown, then enter the username.

| Mode | Description |
|------|-------------|
| Overall | Combined stats across all modes |
| UHC | UHC Duels |
| OP | OP Duels |
| Bridge | Bridge Duels |
| SkyWars | SkyWars Duels |
| Blitz | Blitz Duels |
| NoDebuff | NoDebuff Duels |
| Bow | Bow Duels |
| Classic | Classic Duels |
| Combo | Combo Duels |
| Sumo | Sumo Duels |
| Boxing | Boxing Duels |
| MegaWalls | MegaWalls Duels |

**Stats shown:** Wins, Losses, WLR, Kills, Deaths, KDR, Winstreak

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/SteveTheReal/discord-bedwars-bot.git
cd discord-bedwars-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API keys

Copy `.env.example` to a new file called `.env` and fill in your keys:

```
DISCORD_TOKEN=your_discord_bot_token
HYPIXEL_API_KEY=your_hypixel_api_key
```

- **Discord token** — Create a bot at [discord.com/developers/applications](https://discord.com/developers/applications)
- **Hypixel API key** — Apply for a permanent key at [developer.hypixel.net](https://developer.hypixel.net)

### 4. Run the bot
```bash
python bot.py
```
Or on Windows, double-click `run.bat`.

---

## Tech Stack

- [discord.py](https://github.com/Rapptz/discord.py) — Discord API wrapper
- [aiohttp](https://docs.aiohttp.org/) — Async HTTP requests
- [Hypixel Public API](https://api.hypixel.net/) — Player stats
- [Mojang API](https://api.mojang.com/) — Username → UUID resolution

---

## License

MIT — do whatever you want with it.
