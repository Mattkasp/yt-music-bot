
import os

import discord

from dotenv import load_dotenv
from utils import look_for_url
from yt_music import add_to_playlist, get_video_id

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_NAME = os.getenv("DISCORD_GUILD_NAME")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD_NAME:
            break
    print(f'{client.user} is connected to the guild: {guild.name} (id: {guild.id})')

@client.event
async def on_message(message: discord.Message):
    print("Message received")
    print(message.content)
    print(message.author)
    print(message.channel)
    print(f"Message in music channel?: {message.channel=='music'}")
    
    if message.author == client.user:
        return
    if message.channel.name == 'music':
        print("Message in music channel")
        if 'youtube.com' in message.content:
            print("Youtube URL found")
            url = look_for_url(message)
            if url:
                id = get_video_id(url)
                if id:
                    playlistId = "PL-VgiLr5Ut0xX5efEfoUPTPC8_XH_E2U0"
                    success = add_to_playlist(playlistId, id)
                    if success:
                        await message.channel.send("Added to playlist")
                    else:
                        await message.channel.send("Failed to add to playlist")
                else:
                    print("No video ID found")
                
            
                
client.run(TOKEN)

