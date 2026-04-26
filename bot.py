import os
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv
from hypixel import get_uuid, get_player, parse_bedwars, parse_duels

load_dotenv()

DISCORD_TOKEN   = os.getenv("DISCORD_TOKEN")
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
GUILD_ID        = os.getenv("GUILD_ID")

if not DISCORD_TOKEN or not HYPIXEL_API_KEY:
    raise RuntimeError("Missing DISCORD_TOKEN or HYPIXEL_API_KEY in .env")

MY_GUILD = discord.Object(id=int(GUILD_ID)) if GUILD_ID else None

intents = discord.Intents.default()
client  = discord.Client(intents=intents)
tree    = app_commands.CommandTree(client)

MODE_LABELS = {
    "overall": "Overall",
    "solo":    "Solo",
    "doubles": "Doubles",
    "threes":  "Threes",
    "fours":   "Fours",
    "4v4":     "4v4",
}

DUEL_MODE_LABELS = {
    "overall":   "Overall",
    "uhc":       "UHC",
    "op":        "OP",
    "bridge":    "Bridge",
    "skywars":   "SkyWars",
    "blitz":     "Blitz",
    "nodebuff":  "NoDebuff",
    "bow":       "Bow",
    "classic":   "Classic",
    "combo":     "Combo",
    "sumo":      "Sumo",
    "boxing":    "Boxing",
    "megawalls": "MegaWalls",
}


@client.event
async def on_ready():
    if MY_GUILD:
        tree.copy_global_to(guild=MY_GUILD)
        await tree.sync(guild=MY_GUILD)
    else:
        await tree.sync()
    print(f"Logged in as {client.user}  |  Slash commands synced.", flush=True)


@tree.command(name="bedwars", description="Get BedWars stats for a Hypixel player")
@app_commands.describe(
    mode="Game mode to look up",
    player="Minecraft username",
)
@app_commands.choices(mode=[
    app_commands.Choice(name="Overall",  value="overall"),
    app_commands.Choice(name="Solo",     value="solo"),
    app_commands.Choice(name="Doubles",  value="doubles"),
    app_commands.Choice(name="Threes",   value="threes"),
    app_commands.Choice(name="Fours",    value="fours"),
    app_commands.Choice(name="4v4",      value="4v4"),
])
async def bedwars(interaction: discord.Interaction, mode: str, player: str):
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        uuid = await get_uuid(session, player)
        if uuid is None:
            await interaction.followup.send(
                f"❌ Player **{player}** was not found on Mojang. Check the spelling."
            )
            return

        player_data = await get_player(session, uuid, HYPIXEL_API_KEY)
        if player_data is None:
            await interaction.followup.send(
                f"❌ Could not fetch Hypixel data for **{player}**. "
                "They may have never logged into Hypixel."
            )
            return

    stats = parse_bedwars(player_data, mode)

    embed = discord.Embed(
        title=f"BedWars Stats [{MODE_LABELS[mode]}]  ·  {player}",
        color=0xFFAA00,
    )
    embed.add_field(name="⭐  Level",       value=str(stats["level"]),         inline=True)
    embed.add_field(name="🗡️  Final Kills", value=f"{stats['final_kills']:,}", inline=True)
    embed.add_field(name="💀  FKDR",        value=stats["fkdr"],               inline=True)
    embed.add_field(name="🏆  Wins",        value=f"{stats['wins']:,}",        inline=True)
    embed.add_field(name="📊  WLR",         value=stats["wlr"],                inline=True)
    embed.add_field(name="🔥  Winstreak",   value=stats["winstreak"],          inline=True)
    embed.set_footer(text="Hypixel API")

    await interaction.followup.send(embed=embed)


@tree.command(name="duels", description="Get Duels stats for a Hypixel player")
@app_commands.describe(
    mode="Duels game mode to look up",
    player="Minecraft username",
)
@app_commands.choices(mode=[
    app_commands.Choice(name="Overall",   value="overall"),
    app_commands.Choice(name="UHC",       value="uhc"),
    app_commands.Choice(name="OP",        value="op"),
    app_commands.Choice(name="Bridge",    value="bridge"),
    app_commands.Choice(name="SkyWars",   value="skywars"),
    app_commands.Choice(name="Blitz",     value="blitz"),
    app_commands.Choice(name="NoDebuff",  value="nodebuff"),
    app_commands.Choice(name="Bow",       value="bow"),
    app_commands.Choice(name="Classic",   value="classic"),
    app_commands.Choice(name="Combo",     value="combo"),
    app_commands.Choice(name="Sumo",      value="sumo"),
    app_commands.Choice(name="Boxing",    value="boxing"),
    app_commands.Choice(name="MegaWalls", value="megawalls"),
])
async def duels(interaction: discord.Interaction, mode: str, player: str):
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        uuid = await get_uuid(session, player)
        if uuid is None:
            await interaction.followup.send(
                f"❌ Player **{player}** was not found on Mojang. Check the spelling."
            )
            return

        player_data = await get_player(session, uuid, HYPIXEL_API_KEY)
        if player_data is None:
            await interaction.followup.send(
                f"❌ Could not fetch Hypixel data for **{player}**. "
                "They may have never logged into Hypixel."
            )
            return

    stats = parse_duels(player_data, mode)

    embed = discord.Embed(
        title=f"Duels Stats [{DUEL_MODE_LABELS[mode]}]  ·  {player}",
        color=0x00AAFF,
    )
    embed.add_field(name="🏆  Wins",      value=f"{stats['wins']:,}",   inline=True)
    embed.add_field(name="💀  Losses",    value=f"{stats['losses']:,}", inline=True)
    embed.add_field(name="📊  WLR",       value=stats["wlr"],           inline=True)
    embed.add_field(name="⚔️  Kills",     value=f"{stats['kills']:,}",  inline=True)
    embed.add_field(name="🩸  Deaths",    value=f"{stats['deaths']:,}", inline=True)
    embed.add_field(name="💢  KDR",       value=stats["kdr"],           inline=True)
    embed.add_field(name="🔥  Winstreak", value=stats["winstreak"],     inline=True)
    embed.set_footer(text="Hypixel API")

    await interaction.followup.send(embed=embed)


client.run(DISCORD_TOKEN)
