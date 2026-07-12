# Importing all packages
import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import random
from typing import Optional

# Tokens
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Intents
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Prefix for the bot : "!"
bot = commands.Bot(command_prefix='!', intents=intents)

# Variables
GUILD_ID = discord.Object(id=1525756075301933106)

# Events
@bot.event
async def on_ready():
    print(f"Logged in the server as {bot.user.name}")
    try:
        guild = discord.Object(id=1525756075301933106)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"{len(synced)} commands are sync to guild number : {guild}")

    except Exception as e:
        print(f"Error syncing commands: {e}")

# Modules
def generate_sqawk():
    while True:
        sqwak = "".join(random.choice("01234567") for _ in range(4))

        if sqwak not in ["7500", "7600", "7700"]:
            return sqwak
        
# / Commands
@bot.tree.command(name="acars", description="Generate a ACARS", guild=GUILD_ID)
@app_commands.describe(
    callsign="Aircraft callsign following the ICAO format",
    equipment="Aircraft type",
    departure="4-letter ICAO departure airport (e.g., MDPC)",
    destination="4-letter ICAO destination airport (e.g., LCLK)",
    altitude="Crusing Flight Level, having only 3 numbers (e.g., 190)",
    depfrq="Departure control frequency (e.g., 119.9)",
    sid="Standard Instrument Departure name (Radar Vectors is accepted)",
    remarks="Optional additional clearance remarks",
    sqwak="Optional custom squawk code (generates automatically if empty)"
)

async def acars(interaction: discord.Interaction, callsign: str, equipment: str, departure: str, destination: str, altitude: int, depfrq: float, sid: str, remarks: Optional[str] = None, sqwak: Optional[str] = None):

    # Variables

    if sqwak is None: 
        sqwak = generate_sqawk()

    identifier = random.randint(100, 900)

    embed = discord.Embed(
        title=f"PDC Generator - {callsign}",
        description=" ",
        color=0x506caf
    )

    pdc_content = f"""ACARS: PDC | CALLSIGN: {callsign} | EQUIPMENT : {equipment} |
DEPARTURE: {departure} | DESTINATION: {destination} |
ROUTE: {departure}.{sid}..{destination} |
ALTITUDE: FL{altitude} | TRANSPONDER: {sqwak} | REMARKS: {remarks} |
CLEARED: {sid} | EXP FL{altitude} 2 MIN AFT DP, DPFRQ: {depfrq}
IDENTIFIER: {identifier}A"""


    embed.add_field(
        name="Pre-departure Clearance",
        value=f"```\n{pdc_content}\n```",
        inline=False
    )

    embed.set_footer(
        text="Bot made by Yuker | ACARS 2026"
    )
    await interaction.response.send_message(embed=embed)

# Run the discord bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)


# callsign 
#     equipment
#     departure 
#     destination 
#     altitude 
#     depfrq
#     SID

#  print(f"ACARS: PDC | CALLSIGN: {callsign} | EQUIPMENT: {equipment} |")
#  print(f"DEPARTURE: {departure} | DESTINATION: {destination} |")
#  print(f"ROUTE: {departure}.{route}..{destination} |")
#  print(f"ALTITUDE: {formatted_exp} | TRANSPONDER: {transponder} | REMARKS:")
#  print(f"CLEARED {route} EXP {formatted_alt} 2 MIN AFT DP, DPFRQ {depfrq}")
#  print(f"IDENTIFIER: {identifier}A")