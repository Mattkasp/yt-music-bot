import ytmusicapi
from ytmusicapi import YTMusic, OAuthCredentials
#ytmusicapi.setup('broswer.json')

import os
from os import path
import requests
from dotenv import load_dotenv
import ytmusicapi.exceptions

authfile = path.join(path.dirname(__file__),'..', 'oauth.json')
load_dotenv()

test_client_id = os.getenv("YT_CLIENT_ID")
test_client_secret = os.getenv("YT_CLIENT_SECRET")


ytmusic = YTMusic(authfile, oauth_credentials=OAuthCredentials(client_id=test_client_id, client_secret=test_client_secret))

print("YTMusic API initialized")
playlistId = "PL-VgiLr5Ut0xX5efEfoUPTPC8_XH_E2U0"


def get_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    if 'youtube.com/watch?v=' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return get_video_id_from_share_link(url)
    else:
        return None
    
def add_to_playlist(playlistId, videoId):
    try:
        ytmusic.add_playlist_items(playlistId, [videoId])
    
    except ytmusicapi.exceptions.YTMusicServerError as e:
        
        print(f"YTMusicServerError: {e}. videoId: {videoId}")
        raise e
    return True


test_url = "https://music.youtube.com/watch?v=zVCzaHPSomc&list=OLAK5uy_kLsYEcEuTrC_mhxf0Kv-VqrE09Db8zr_0"
test_youtubebe_url = "https://youtu.be/i3lQxwTpBaY?si=9YU35-i0YUL-ei-3"

test_id = "4fAliEgjRac"
test_urls = ["https://youtu.be/QcxdDafgmYc?si=r0ViWSrFH1SSaouB", "https://youtu.be/i3lQxwTpBaY?si=9YU35-i0YUL-ei-3", "https://youtu.be/P6BwTGKfY44?si=PL4lUX-g7RrwGpIx", "https://youtu.be/njI-6OPsW90?si=UUiT-YaOmXSNE1fs"]


def extract_id(url_block):
    start_sequence = "\\u0026v\\"

    start_pos = url_block.find(start_sequence)
    if start_pos == -1:
        return ""
    
    # Adjust start position to the end of the start sequence
    start_pos += len(start_sequence)
    
    # Find the ending position (next backslash)
    end_pos = url_block.find("\\", start_pos)
    if end_pos == -1:
        # If no ending backslash, return the rest of the string
        return url_block[start_pos:]
    
    # Extract the part between start and end positions
    id = url_block[start_pos:end_pos]
    if id.startswith("u003d"):
        print("ID starts with u003d")
        return id[5:] #remove the first 4 characters, which should be u003d
    else:
        print("ID does not start with u003d")
        return None
    

def get_video_id_from_share_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        id_start = text.find('QcxdDafgmYc')
        start_index = text.find('originalUrl')
        #print(f"Start index: {start_index}, id_start: {id_start}")
        if start_index != -1:
            url_block = text[start_index:start_index + 200]
            #print(f"URL block: {url_block}")
            id = extract_id(url_block)
            return id



add_to_playlist(playlistId, test_id)