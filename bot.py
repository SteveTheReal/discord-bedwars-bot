import os
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv
from hypixel import get_uuid, get_player, parse_bedwars

load_dotenv()

DISCORD_TOKEN    = os.getenv("DISCORD_TOKEN")
HYPIXEL_API_KEY  = os.getenv("HYPIXEL_API_KEY")

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


async def fetch_and_reply(interaction: discord.Interaction, player: str, mode: str):
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
    label = MODE_LABELS[mode]

    embed = discord.Embed(
        title=f"BedWars Stats [{label}]  ·  {player}",
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


class BedwarsGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="bedwars", description="Get BedWars stats for a Hypixel player")

    @app_commands.command(name="overall", description="Overall BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def overall(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "overall")

    @app_commands.command(name="solo", description="Solo BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def solo(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "solo")

    @app_commands.command(name="doubles", description="Doubles BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def doubles(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "doubles")

    @app_commands.command(name="threes", description="Threes BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def threes(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "threes")

    @app_commands.command(name="fours", description="Fours BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def fours(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "fours")

    @app_commands.command(name="4v4", description="4v4 BedWars stats")
    @app_commands.describe(player="Minecraft username")
    async def fourvfour(self, interaction: discord.Interaction, player: str):
        await fetch_and_reply(interaction, player, "4v4")


tree.add_command(BedwarsGroup())


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}  |  Slash commands synced.", flush=True)


client.run(DISCORD_TOKEN)
