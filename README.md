# 🏆 Hypixel BedWars Stats Bot

A Discord bot that instantly fetches and displays BedWars statistics for any Hypixel player — directly in your server.

---

## Preview

> `/bedwars gamerboy80`

```
╔══════════════════════════════╗
║  BedWars Stats · gamerboy80  ║
╠══════════════════════════════╣
║ ⭐ Level       │ 1,000       ║
║ 🗡️ Final Kills │ 132,804     ║
║ 💀 FKDR        │ 24.61       ║
║ 🏆 Wins        │ 21,450      ║
║ 📊 WLR         │ 12.38       ║
║ 🔥 Winstreak   │ 142         ║
╚══════════════════════════════╝
```

---

## Features

- **`/bedwars overall <username>`** — Overall BedWars stats
- **`/bedwars solo <username>`** — Solo stats
- **`/bedwars doubles <username>`** — Doubles stats
- **`/bedwars threes <username>`** — Threes stats
- **`/bedwars fours <username>`** — Fours stats
- **`/bedwars 4v4 <username>`** — 4v4 stats
- Displays **Level, Final Kills, FKDR, Wins, WLR, and Winstreak** for each mode
- Clean Discord embed output
- Handles players with hidden winstreaks gracefully
- Fast async requests — no lag

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
