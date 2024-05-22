import os
import asyncio
import discord
from dotenv import load_dotenv
from bot_modules import reply, login_report

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("Token not found. Please set the DISCORD_BOT_TOKEN environment variable.")

CHANNEL_ID = os.getenv('CHANNEL_ID').split(", ")
if CHANNEL_ID is None:
    raise ValueError("CHANNEL_ID not found. Please set the CHANNEL_ID environment variable.")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for channel in CHANNEL_ID:
        channel = client.get_channel(int(channel))
        message = "🚀 **Server Monitor Activated!** 🚀"
        await channel.send(message)

    while True:
        await login_report(client, CHANNEL_ID)
        await asyncio.sleep(1)


@client.event
async def on_message(message):
    if message.author.bot or str(message.channel.id) not in CHANNEL_ID:
        return
    await reply(message)


if __name__=='__main__':
    client.run(TOKEN)
