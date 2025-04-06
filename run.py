from src.main import client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


if __name__ == "__main__":
    client.run(TOKEN)