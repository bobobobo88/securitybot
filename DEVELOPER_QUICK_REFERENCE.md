# Developer Quick Reference Guide

## 🚀 Quick Start

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
python setup_env.py

# Test configuration
python test_bot.py

# Run bot
python main.py
```

### Key Files
- `main.py` - Bot entry point and event handlers
- `config.py` - Configuration management
- `data_manager.py` - Data persistence
- `moderation.py` - Auto-moderation
- `vouch_system.py` - Image processing
- `invite_tracker.py` - Invite tracking
- `verification_system.py` - User verification
- `commands.py` - Slash commands

## 🔧 Common Tasks

### Adding a New Command
```python
# In commands.py
@app_commands.command(name="newcommand", description="Description")
async def newcommand(self, interaction: discord.Interaction):
    # Command logic here
    await interaction.response.send_message("Response")
```

### Adding a New Event Handler
```python
# In main.py
async def on_new_event(self, event_data):
    # Event handling logic
    pass
```

### Adding Data Storage
```python
# In data_manager.py
async def add_new_data(self, user_id: int, data: str):
    user_id_str = str(user_id)
    self.new_data[user_id_str] = data
    await self.save_json(self.new_data_file, self.new_data)
```

### Adding Configuration
```python
# In config.py
NEW_CONFIG = os.getenv('NEW_CONFIG', 'default_value')

# In .env
NEW_CONFIG=your_value_here
```

## 📊 Data Structures

### Points System
```json
{
  "123456789": 50,
  "987654321": 25
}
```

### Invite Tracking
```json
{
  "123456789": 5,
  "relationships": {
    "987654321": "123456789"
  }
}
```

### Cooldowns
```json
{
  "123456789": "2024-01-01T12:00:00"
}
```

## 🛠️ Debugging

### Common Issues
1. **Image Download Fails**: Check bot permissions and download strategy
2. **Invites Not Tracking**: Verify invite cache and permissions
3. **Configuration Errors**: Validate all environment variables
4. **Data Not Saving**: Check file permissions and JSON syntax

### Debug Commands
```bash
# Test all components
python test_bot.py

# Check data files
python -c "import json; print(json.load(open('data/points.json')))"

# Validate config
python -c "import config; print(config.BOT_TOKEN)"
```

### Logging
- All modules include comprehensive logging
- Check console output for detailed error messages
- Debug information shows strategy attempts and data flow

## 🔄 Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Test changes
python test_bot.py

# Commit changes
git add .
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature
```

### 2. Testing
```bash
# Run test suite
python test_bot.py

# Test specific component
python -c "from data_manager import DataManager; dm = DataManager(); print(dm.get_points(123))"
```

### 3. Deployment
```bash
# Update dependencies
pip install -r requirements.txt

# Test configuration
python test_bot.py

# Start bot
python main.py
```

## 📝 Code Standards

### Python Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Handle exceptions properly

### Discord.py Patterns
```python
# Event handlers
async def on_event(self, data):
    try:
        # Event logic
        pass
    except Exception as e:
        print(f"Error in event: {e}")

# Commands
@app_commands.command()
async def command(self, interaction: discord.Interaction):
    try:
        # Command logic
        await interaction.response.send_message("Response")
    except Exception as e:
        await interaction.response.send_message("Error occurred", ephemeral=True)
```

### Async Patterns
```python
# File operations
async def save_data(self):
    async with aiofiles.open(filepath, 'w') as f:
        await f.write(json.dumps(data, indent=2))

# HTTP requests
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.read()
```

## 🔧 Configuration Reference

### Required Environment Variables
```env
BOT_TOKEN=your_bot_token
GUILD_ID=your_guild_id
VOUCH_CHANNEL_ID=channel_id
ORDER_CHANNEL_IDS=id1,id2,id3
SUPPORT_CHANNEL_ID=channel_id
INVITE_TRACKER_CHANNEL_ID=channel_id
ADMIN_ROLE_ID=role_id
VERIFIED_ROLE_ID=role_id
MUTED_ROLE_ID=role_id
```

### Optional Configuration
```env
POINTS_PER_VOUCH=1
VOUCH_COOLDOWN_HOURS=24
```

## 🚨 Error Handling

### Best Practices
1. **Always wrap async operations in try-catch**
2. **Provide fallback mechanisms**
3. **Log errors with context**
4. **Give user-friendly error messages**

### Example Error Handling
```python
async def process_data(self, data):
    try:
        # Process data
        result = await self.complex_operation(data)
        return result
    except SpecificError as e:
        print(f"Specific error: {e}")
        # Fallback logic
        return self.fallback_method(data)
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Generic fallback
        return None
```

## 📚 Useful Resources

### Discord.py Documentation
- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)

### Python Resources
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

### Project Files
- `DOCUMENTATION.md` - Comprehensive documentation
- `README.md` - User guide
- `QUICKSTART.md` - Quick setup guide
- `test_bot.py` - Test suite

## 🔄 Update Checklist

When updating the bot:

1. **Test Configuration**
   - Run `python test_bot.py`
   - Verify all environment variables

2. **Test Features**
   - Test vouch system with image upload
   - Test invite tracking with member join/leave
   - Test moderation with various messages
   - Test verification system

3. **Check Data Integrity**
   - Verify data files are readable
   - Check JSON syntax
   - Validate data structures

4. **Update Documentation**
   - Update relevant documentation
   - Add new configuration options
   - Document new features

5. **Deploy Safely**
   - Backup current data
   - Test in staging if possible
   - Monitor logs after deployment

---

*Quick Reference Guide for Bob's Discount Shack Discord Bot* 