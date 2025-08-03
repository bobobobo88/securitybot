# Bob's Discount Shack Discord Bot

A comprehensive auto-moderation Discord bot designed specifically for Bob's Discount Shack, a marketplace server selling discounted services and money-making methods.

## Features

### 🔒 Auto-Moderation System
- **Invite Link Protection**: Automatically bans users who post Discord invite links anywhere in the server
- **Scam Domain Blocking**: Deletes messages and bans users who post known malicious domains
- **Channel Protection**: Maintains clean order and support channels by deleting all messages
- **Verification System**: Automatically mutes users without the verified role

### 🖼️ Vouch Watermarking System
- **Image Processing**: Automatically downloads, watermarks, and reposts images in the vouch channel
- **Stream Plug Logo**: Applies transparent Stream Plug logo overlay to all vouch images
- **Point Rewards**: Awards 1 point per successful vouch with 5-hour cooldown
- **Cooldown Enforcement**: Prevents spam by enforcing time limits between vouch submissions
- **Admin Bypass**: Admin role can post unlimited vouches without cooldown restrictions

### 📊 Point & Invite Tracking
- **Point System**: Persistent point balance tracking for all users
- **Invite Tracking**: Monitors who invited each new member
- **Leaderboards**: Display top users by points and invites
- **Statistics**: Detailed tracking and reporting

### 🎫 Support System
- **Channel Protection**: Maintains clean order and support channels by deleting all messages
- **Ephemeral Messages**: Sends private reminders to users about proper channel usage

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Discord Server with proper permissions

### 2. Installation

1. **Clone or download the bot files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**:
   - Run: `python setup_env.py` (or copy `env_example.txt` to `.env`)
   - Fill in your bot token and channel IDs

4. **Configure channels**:
   - Create channels for vouches, orders, and support
   - Update the channel IDs in your `.env` file

5. **Set up bot permissions**:
   - Give the bot the following permissions:
     - Read Messages
     - Send Messages
     - Manage Messages
     - Ban Members
     - Attach Files
     - Embed Links
     - Use Slash Commands
     - Manage Channels

### 3. Running the Bot

```bash
python main.py
```

## Configuration

### Environment Variables (.env file)

```env
# Bot Configuration
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here

# Channel IDs
VOUCH_CHANNEL_ID=1234567890123456789
# Multiple order channels - comma-separated IDs
ORDER_CHANNEL_IDS=1234567890123456789,9876543210987654321
SUPPORT_CHANNEL_ID=1234567890123456789
# Invite tracker channel (optional - set to 0 to disable)
INVITE_TRACKER_CHANNEL_ID=1234567890123456789

# Admin role for unlimited vouches
ADMIN_ROLE_ID=1234567890123456789

# Role IDs for verification system
VERIFIED_ROLE_ID=1234567890123456789
MUTED_ROLE_ID=1234567890123456789
```

### Channel Setup

1. **Vouch Channel**: Where users post success screenshots
2. **Order Channels**: Protected channels where all messages are deleted (supports multiple channels)
3. **Support Channel**: Protected channel where all messages are deleted

## Commands

### Slash Commands

- `/points` - Check your current point balance
- `/invites` - Check your invite count
- `/leaderboard` - View points leaderboard
- `/scan` - Scan all members for verification status (Admin only)
- `/inviteboard` - Display invite leaderboard in tracker channel (Admin only)

## Features in Detail

### Auto-Moderation

**Invite Link Protection**:
- Detects Discord invite links using regex pattern
- Immediately bans users (no warnings)
- Server-wide protection

**Channel Protection**:
- Order channel: Only `/order` commands allowed
- Support channel: Only `/ticket` commands allowed
- All other messages are deleted with helpful reminders

### Vouch System

**Image Processing Workflow**:
1. User posts image in vouch channel
2. Bot downloads original image
3. Deletes original message immediately
4. Applies Stream Plug watermark overlay
5. Reposts watermarked version
6. Awards points to user

**Watermark Specifications**:
- Transparent Stream Plug logo
- Centered position
- Semi-transparent overlay
- Proportional sizing

**Point System**:
- 1 point per successful vouch
- 5-hour cooldown between submissions
- Persistent storage
- No point decay

### Invite Tracking

**Core Functionality**:
- Tracks which user invited each new member
- Maintains invite count per user
- Displays invite leaderboard
- Basic statistics and counts

**Data Storage**:
- User ID → Invite count mapping
- Inviter → Invitee relationships
- Join timestamps

## File Structure

```
securitybot/
├── main.py              # Main bot file
├── config.py            # Configuration settings
├── data_manager.py      # Data persistence
├── moderation.py        # Auto-moderation system
├── vouch_system.py      # Vouch watermarking
├── invite_tracker.py    # Invite tracking
├── commands.py          # Slash commands
├── image_processor.py   # Image processing
├── requirements.txt     # Dependencies
├── README.md           # This file
└── data/               # Data storage directory
    ├── points.json
    ├── invites.json
    └── cooldowns.json
```

## Permissions Required

The bot needs the following permissions:
- **Read Messages**: To monitor all channels
- **Send Messages**: To send responses and notifications
- **Manage Messages**: To delete inappropriate messages
- **Ban Members**: To ban users who violate rules
- **Attach Files**: To upload watermarked images
- **Embed Links**: To send rich embeds
- **Use Slash Commands**: To register and use slash commands
- **Manage Channels**: To create ticket channels

## Troubleshooting

### Common Issues

1. **Bot not responding**:
   - Check bot token in `.env` file
   - Ensure bot has proper permissions
   - Verify bot is online

2. **Commands not working**:
   - Check if commands are synced (should show in console)
   - Ensure bot has "Use Slash Commands" permission
   - Verify channel IDs are correct

3. **Image watermarking not working**:
   - Check if `assets/watermark.png` exists
   - Ensure bot has "Attach Files" permission
   - Check internet connection for image downloads

4. **Invite tracking not working**:
   - Ensure bot has "Manage Server" permission
   - Check if invites are being cached properly
   - Verify guild ID is correct

### Logs

The bot provides console output for:
- Bot startup and connection
- Command usage
- Moderation actions
- Error messages
- Invite tracking events

## Development

### Adding New Features

1. **New Commands**: Add to `commands.py`
2. **New Moderation Rules**: Add to `moderation.py`
3. **New Data Storage**: Extend `data_manager.py`
4. **New Image Processing**: Extend `image_processor.py`

### Testing

Test the bot in a development server before deploying to production:
1. Create a test Discord server
2. Set up test channels
3. Configure bot for test environment
4. Test all features thoroughly

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review console logs for error messages
3. Verify all configuration is correct
4. Test in a development environment first

## License

This bot is designed specifically for Bob's Discount Shack. Please ensure compliance with Discord's Terms of Service and your server's rules. 