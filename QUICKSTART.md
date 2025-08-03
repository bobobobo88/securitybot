# Quick Start Guide

Get Bob's Discount Shack Discord Bot running in 5 minutes!

## 🚀 Quick Setup

### 1. Run Setup Script
```bash
python setup.py
```

### 2. Configure Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Copy the token
5. Edit `.env` file and replace `your_bot_token_here` with your token

### 3. Get Channel IDs
1. Enable Developer Mode in Discord (User Settings > Advanced)
2. Right-click on your channels and "Copy ID"
3. Update the channel IDs in `.env` file:
   - `VOUCH_CHANNEL_ID` - Where users post vouches
   - `ORDER_CHANNEL_IDS` - Where `/order` commands are used (comma-separated for multiple channels)
   - `SUPPORT_CHANNEL_ID` - Where `/ticket` commands are used

### 4. Invite Bot to Server
1. Go to OAuth2 > URL Generator in Discord Developer Portal
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - Read Messages
   - Send Messages
   - Manage Messages
   - Ban Members
   - Attach Files
   - Embed Links
   - Use Slash Commands
   - Manage Channels
4. Copy the generated URL and open it
5. Select your server and authorize

### 5. Run the Bot
```bash
python main.py
```

## ✅ Test Features

### Test Auto-Moderation
1. Post a Discord invite link anywhere → User should be banned
2. Post any message in order channel → Should be deleted with reminder
3. Post any message in support channel → Should be deleted with reminder

### Test Vouch System
1. Post an image in vouch channel → Should be watermarked and reposted
2. Check points with `/points` command
3. Try posting again within 5 hours → Should be blocked

### Test Commands
- `/points` - Check your points
- `/invites` - Check your invites
- `/ticket` - Create support ticket
- `/leaderboard` - View leaderboard

## 🔧 Troubleshooting

### Bot not responding?
- Check bot token in `.env`
- Ensure bot is online
- Verify bot has proper permissions

### Commands not working?
- Check console for "Synced X command(s)" message
- Ensure bot has "Use Slash Commands" permission
- Try restarting the bot

### Image watermarking not working?
- Check bot has "Attach Files" permission
- Verify internet connection
- Check console for error messages

## 📋 Required Permissions

Make sure your bot has these permissions:
- ✅ Read Messages
- ✅ Send Messages  
- ✅ Manage Messages
- ✅ Ban Members
- ✅ Attach Files
- ✅ Embed Links
- ✅ Use Slash Commands
- ✅ Manage Channels

## 🎯 Next Steps

1. **Customize watermark**: Replace `assets/watermark.png` with your logo
2. **Add scam domains**: Edit `moderation.py` to add more blocked domains
3. **Configure point rewards**: Modify point thresholds in `config.py`
4. **Set up roles**: Create roles for different point levels

## 📞 Support

If you need help:
1. Check the main README.md for detailed documentation
2. Review console output for error messages
3. Verify all configuration is correct
4. Test in a development server first

---

**Ready to go!** Your bot should now be protecting your server and managing vouches automatically. 