import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
# Handle placeholder values in .env file
guild_id_str = os.getenv('GUILD_ID', '1234567890123456789')
GUILD_ID = int(guild_id_str) if guild_id_str.isdigit() else 1234567890123456789

# Channel IDs (configure these in your .env file)
VOUCH_CHANNEL_ID = int(os.getenv('VOUCH_CHANNEL_ID', 1234567890123456789))
# Support multiple order channels - comma-separated IDs
ORDER_CHANNEL_IDS = [int(id.strip()) for id in os.getenv('ORDER_CHANNEL_IDS', '1234567890123456789,9876543210987654321').split(',') if id.strip() and id.strip().isdigit()]
SUPPORT_CHANNEL_ID = int(os.getenv('SUPPORT_CHANNEL_ID', 1234567890123456789))
# Invite tracker channel (optional)
invite_tracker_id_str = os.getenv('INVITE_TRACKER_CHANNEL_ID', '0')
INVITE_TRACKER_CHANNEL_ID = int(invite_tracker_id_str) if invite_tracker_id_str.isdigit() else None

# Admin role for unlimited vouches
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID', 1234567890123456789))

# Role IDs for verification system
VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID', 1234567890123456789))
MUTED_ROLE_ID = int(os.getenv('MUTED_ROLE_ID', 1234567890123456789))

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