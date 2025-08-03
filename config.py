import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# Channel IDs (configure these in your .env file)
VOUCH_CHANNEL_ID = int(os.getenv('VOUCH_CHANNEL_ID', 0))
ORDER_CHANNEL_ID = int(os.getenv('ORDER_CHANNEL_ID', 0))
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', 0))

# Cooldown Settings
VOUCH_COOLDOWN_HOURS = 5

# Point System
POINTS_PER_VOUCH = 1

# File Paths
WATERMARK_PATH = "assets/watermark.png"
DATA_DIR = "data"

# Colors for embeds
EMBED_COLORS = {
    'success': 0x00ff00,
    'error': 0xff0000,
    'info': 0x0099ff,
    'warning': 0xffff00
} 