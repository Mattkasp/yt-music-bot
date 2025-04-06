import discord
def look_for_url(message: discord.Message | dict) -> str:
    """
    Check if the message contains a YouTube URL.
    """
    if isinstance(message, discord.Message):
        content = message.content

    if isinstance(message, dict):
        content = message['content']
    if 'youtube.com' in content or 'youtu.be' in content:
        split_message =  content.split()
        for word in split_message:
            if 'youtube.com' in word or 'youtu.be' in word:
                url = word
                break
        else:
            url = content
        return url
    else:
        return None