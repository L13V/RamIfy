import os
import time
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import sys

#Set up aliases for the environment variables.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL')
PLAYING = "SCOUTING ALERT!!!"

#Format activity from .env file for use in the init.
activity = (discord.Game(name=str(PLAYING)))
loop = 0
arg1=str(sys.argv[1])
ping=str(sys.argv[2])
print(arg1)
print(ping)

#Discord Init
intents = discord.Intents.default()
client = discord.Client(intents=intents, activity=activity, status=discord.Status.online)

@client.event
async def on_ready():
    global loop
    global ping
    print(f'Logged in as {client.user}')
    print("5 second countdown for custom message.")
    print("You can stop this during the countdown (probably, I haven't tested that.)")
    time.sleep(1)
    while loop <= 5 :
        time.sleep(1)
        print(loop)
        loop=loop+1
    channel = client.get_channel(int(CHANNEL_ID))
    if ping == "True":
        await channel.send("@everyone ALERT: " + arg1)
    else:
        await channel.send("ALERT: " + arg1)
    print("This will error out. I don't want to or have the time to fix this. It's fine. Out of sight, out of mind.")
    time.sleep(5)
    quit()

client.run(DISCORD_TOKEN)