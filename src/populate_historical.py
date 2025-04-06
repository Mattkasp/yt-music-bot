api_base = "https://discord.com/api/v10"

import os
import requests
from dotenv import load_dotenv

load_dotenv()
from yt_music import add_to_playlist, get_video_id
from utils import look_for_url

auth = f"Bot {os.getenv('DISCORD_TOKEN')}"

headers = {
    'Content-Type': 'application/json',
    'Authorization': auth,
    'User-Agent': 'DiscordBot (https://discord.com/oauth2/authorize?client_id=1358501096741671202, 1.0)'
}

GUILD_ID = "1296146778080673912"
MUSIC_CHANNEL_ID = "1298321384870514859"
get_guild = f"{api_base}/guilds/{GUILD_ID}"
get_guilds_response = requests.get(get_guild, headers=headers)

def get_channels(guild_id):
    """
    Get all channels in a guild.
    """
    url = f"{api_base}/guilds/{guild_id}/channels"
    response = requests.get(url, headers=headers)
    return response.json()

def get_messages(channel_id, last_message_id=None):
    """
    Get all messages in a channel.
    """
    last_message_filter = f"&before={last_message_id}" if last_message_id else ""
    url = f"{api_base}/channels/{channel_id}/messages?limit=100{last_message_filter}"
    response = requests.get(url, headers=headers)
    return response.json()

class ChannelScraper:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.last_message_id = None
        self.urls = []
        self.failed_urls = []

    def run(self):
        while True:
            messages = get_messages(self.channel_id, self.last_message_id)
            if not messages:
                break
            self.last_message_id = messages[-1]['id']
            self.filter_messages(messages)
            if len(messages) < 100:
                print(f"Found total of {len(self.urls)} URLs.")
                break
            print(f"Fetched {len(messages)} messages.")
            print(f"Last message ID: {self.last_message_id}")
            
            
    
    def filter_messages(self, messages):
        """
        Filter messages to find YouTube URLs.
        """
        for message in messages:
            self.search_message_and_add(message)

    def search_message_and_add(self, message):
        if 'youtube.com' in message['content'] or 'youtu.be' in message['content']:
            url = look_for_url(message)
            if url:
                self.urls.append(url)
                print(f"Found URL: {url}")
                id = get_video_id(url)
                if id:
                    print(f"Found id.{id} adding to playlist")
                    playlistId = "PL-VgiLr5Ut0xX5efEfoUPTPC8_XH_E2U0"
                    try:
                        return add_to_playlist(playlistId, id)
                    except Exception as e:
                        print(f"Failed to add to playlist: {e}")
                        self.failed_urls.append(url)

if __name__ == "__main__":
    channel_id = MUSIC_CHANNEL_ID
    scraper = ChannelScraper(channel_id)
    scraper.run()
    print(f"Found total of {len(scraper.urls)} URLs.")
    
