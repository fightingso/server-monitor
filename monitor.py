import os
import discord
import subprocess
from dotenv import load_dotenv

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
        message = """
            🚀 Server Monitoring Bot Activated! 🚀 \n\nHello and welcome! I'm here to assist you with real-time monitoring of your server's performance and activities. To get started, please configure your monitoring settings using the commands listed in /help.\n\nInterested in contributing to the development of this bot? Visit our GitHub repository at https://github.com/fightingso/server-monitor and see how you can help!
        """
        await channel.send(message)


@client.event
async def on_message(message):
    if message.author.bot or message.channel.id not in CHANNEL_ID:
        return
    if message.content == '/who':
        result = subprocess.run(['who'], capture_output=True, text=True)
        await message.channel.send(result.stdout)


if __name__=='__main__':
    client.run(TOKEN)
