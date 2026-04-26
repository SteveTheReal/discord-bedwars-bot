import os
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv
from hypixel import get_uuid, get_player, parse_bedwars

load_dotenv()

DISCORD_TOKEN   = os.getenv("DISCORD_TOKEN")
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")

if not DISCORD_TOKEN or not HYPIXEL_API_KEY:
    raise RuntimeError("Missing DISCORD_TOKEN or HYPIXEL_API_KEY in .env")

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


@client.event
async def on_ready():
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
async def bedwars(interaction: discord.Interaction, mode: app_commands.Choice[str], player: str):
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

    stats = parse_bedwars(player_data, mode.value)

    embed = discord.Embed(
        title=f"BedWars Stats [{mode.name}]  ·  {player}",
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


client.run(DISCORD_TOKEN)
