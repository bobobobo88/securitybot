# Bob's Discount Shack Discord Bot - Technical Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Modules](#core-modules)
4. [Configuration](#configuration)
5. [Data Management](#data-management)
6. [Features](#features)
7. [API Reference](#api-reference)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Bob's Discount Shack Discord Bot** is a comprehensive Discord moderation and community management bot built with `discord.py`. The bot provides auto-moderation, invite tracking, vouch watermarking, point systems, and verification management.

### Key Features
- **Auto-Moderation**: Scam link detection, invite protection, channel protection
- **Invite Tracking**: Member join/leave tracking with point management
- **Vouch System**: Image watermarking with point rewards
- **Verification System**: Auto-mute unverified users
- **Point System**: Persistent user point tracking
- **Admin Commands**: Administrative tools and monitoring

---

## 🏗️ Architecture

### Module Structure
```
securitybot/
├── main.py                 # Bot entry point and event handlers
├── config.py              # Configuration management
├── data_manager.py        # Data persistence layer
├── moderation.py          # Auto-moderation system
├── vouch_system.py        # Vouch image processing
├── invite_tracker.py      # Invite tracking system
├── verification_system.py # User verification management
├── commands.py            # Slash command definitions
├── image_processor.py     # Image watermarking
├── setup.py              # Automated setup script
├── test_bot.py           # Test suite
└── data/                 # Persistent data storage
```

### Design Patterns
- **Modular Architecture**: Each feature is isolated in its own module
- **Event-Driven**: Uses Discord's event system for real-time processing
- **Data Persistence**: JSON-based storage with async operations
- **Error Handling**: Comprehensive try-catch blocks with fallbacks

---

## 🔧 Core Modules

### 1. Main Bot (`main.py`)

**Purpose**: Central orchestrator and event handler

**Key Components**:
```python
class BobsDiscountBot(commands.Bot):
    def __init__(self):
        # Initialize all systems
        self.moderation = Moderation(self)
        self.vouch_system = VouchSystem(self)
        self.invite_tracker = InviteTracker(self)
        self.verification_system = VerificationSystem(self)
```

**Event Handlers**:
- `on_ready()`: Bot startup and command syncing
- `on_message()`: Message processing and routing
- `on_member_join()`: New member handling
- `on_member_remove()`: Member leave tracking
- `on_member_update()`: Role change monitoring
- `on_invite_create/delete()`: Invite cache management

### 2. Configuration (`config.py`)

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading with `python-dotenv`
- Robust parsing with fallback values
- Support for multiple channel IDs (comma-separated)
- Role-based permission configuration

**Configuration Variables**:
```python
# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', '1234567890123456789'))

# Channel IDs (supports multiple order channels)
ORDER_CHANNEL_IDS = [int(x.strip()) for x in os.getenv('ORDER_CHANNEL_IDS', '').split(',') if x.strip().isdigit()]

# Role IDs
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID', '1234567890123456789'))
VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID', '1234567890123456789'))
MUTED_ROLE_ID = int(os.getenv('MUTED_ROLE_ID', '1234567890123456789'))
```

### 3. Data Manager (`data_manager.py`)

**Purpose**: Persistent data storage and retrieval

**Data Files**:
- `data/points.json`: User point balances
- `data/invites.json`: Invite tracking data
- `data/cooldowns.json`: Vouch cooldown timestamps

**Key Methods**:
```python
class DataManager:
    async def add_points(self, user_id: int, points: int = 1)
    def get_points(self, user_id: int) -> int
    async def add_invite(self, inviter_id: int, invitee_id: int)
    async def remove_invite(self, inviter_id: int, invitee_id: int)
    def get_invite_count(self, user_id: int) -> int
    def is_on_cooldown(self, user_id: int) -> bool
    async def set_cooldown(self, user_id: int)
```

**Data Structure**:
```json
{
  "points": {
    "123456789": 50,
    "987654321": 25
  },
  "invites": {
    "123456789": 5,
    "relationships": {
      "987654321": "123456789"
    }
  },
  "cooldowns": {
    "123456789": "2024-01-01T12:00:00"
  }
}
```

### 4. Moderation System (`moderation.py`)

**Purpose**: Auto-moderation and channel protection

**Features**:
- **Invite Link Protection**: Bans users posting Discord invites
- **Scam Domain Blocking**: Blocks known scam domains
- **Channel Protection**: Deletes non-command messages in order/support channels

**Key Methods**:
```python
class Moderation:
    async def check_message(self, message: discord.Message)
    async def handle_order_channel(self, message: discord.Message)
    async def handle_support_channel(self, message: discord.Message)
    def has_invite_link(self, content: str) -> bool
    def has_scam_domain(self, content: str) -> bool
```

**Scam Domains**:
```python
SCAM_DOMAINS = [
    'discord.gift', 'discordapp.gift', 'discord-nitro.gift',
    'steamcommunity.com', 'steam.com', 'steampowered.com',
    'roblox.com', 'minecraft.net', 'minecraft.com'
]
```

### 5. Vouch System (`vouch_system.py`)

**Purpose**: Image watermarking and point rewards

**Features**:
- Image attachment detection
- Multi-strategy download system
- Watermark application
- Point awarding with cooldowns
- Admin role bypass
- Fallback text-based vouches

**Download Strategies**:
1. **Direct Attachment Download**: `attachment.read()`
2. **URL Download**: HTTP request with browser headers
3. **Fallback**: Text-based vouch embed

**Key Methods**:
```python
class VouchSystem:
    async def download_with_retry(self, attachment: discord.Attachment) -> BytesIO
    async def process_vouch(self, message: discord.Message)
    async def handle_vouch_channel(self, message: discord.Message)
    def is_image_attachment(self, message: discord.Message) -> bool
```

### 6. Image Processor (`image_processor.py`)

**Purpose**: Image watermarking and processing

**Features**:
- Automatic watermark creation
- Image format conversion (RGBA)
- Proportional watermark sizing
- Alpha blending for transparency

**Key Methods**:
```python
class ImageProcessor:
    def apply_watermark(self, image_data: BytesIO) -> BytesIO
    async def download_image(self, url: str) -> BytesIO
    def create_placeholder_watermark(self)
    async def process_vouch_image(self, image_url: str) -> BytesIO
```

**Watermark Placement**:
- Centered on image
- Size: 1/3 of smallest image dimension
- Alpha blending for transparency
- PNG format output

### 7. Invite Tracker (`invite_tracker.py`)

**Purpose**: Track member invites and manage join/leave events

**Features**:
- Invite cache management
- Member join tracking
- Member leave tracking with point removal
- Tracker channel notifications
- Invite statistics

**Key Methods**:
```python
class InviteTracker:
    async def cache_invites(self)
    async def handle_member_join(self, member: discord.Member)
    async def handle_member_leave(self, member: discord.Member)
    async def post_invite_tracker_message(self, member: discord.Member, inviter: discord.Member)
    async def post_member_leave_message(self, member: discord.Member, inviter_id: int, inviter_name: str)
```

**Cache Management**:
```python
self.invite_cache = {
    "invite_code": uses_count,
    "abc123": 5,
    "def456": 3
}
```

### 8. Verification System (`verification_system.py`)

**Purpose**: Auto-manage user verification status

**Features**:
- Automatic mute/unmute based on verification role
- Member scanning on startup
- Role change monitoring
- User notification system

**Key Methods**:
```python
class VerificationSystem:
    async def check_and_mute_unverified(self, member: discord.Member)
    async def scan_all_members(self)
    async def handle_member_update(self, before: discord.Member, after: discord.Member)
    async def send_mute_notification(self, member: discord.Member)
    async def send_unmute_notification(self, member: discord.Member)
```

### 9. Commands (`commands.py`)

**Purpose**: Slash command definitions and user interactions

**Available Commands**:
- `/points` - Check user point balance
- `/invites` - Check user invite count
- `/leaderboard` - View points leaderboard
- `/scan` - Admin: Scan all members for verification
- `/inviteboard` - Admin: Post invite leaderboard

**Command Structure**:
```python
class BotCommands(commands.Cog):
    @app_commands.command(name="points", description="Check your point balance")
    async def points(self, interaction: discord.Interaction)
    
    @app_commands.command(name="invites", description="Check your invite count")
    async def invites(self, interaction: discord.Interaction)
    
    @app_commands.command(name="leaderboard", description="View points leaderboard")
    async def leaderboard(self, interaction: discord.Interaction)
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)
```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here

# Channel IDs
VOUCH_CHANNEL_ID=1234567890123456789
ORDER_CHANNEL_IDS=1234567890123456789,9876543210987654321
SUPPORT_CHANNEL_ID=1234567890123456789
INVITE_TRACKER_CHANNEL_ID=1234567890123456789

# Role IDs
ADMIN_ROLE_ID=1234567890123456789
VERIFIED_ROLE_ID=1234567890123456789
MUTED_ROLE_ID=1234567890123456789

# System Configuration
POINTS_PER_VOUCH=1
VOUCH_COOLDOWN_HOURS=24
```

### Configuration Validation
The bot includes robust configuration validation:
- Type checking for numeric values
- Fallback values for missing variables
- Support for multiple channel IDs
- Error handling for invalid configurations

---

## 💾 Data Management

### File Structure
```
data/
├── points.json      # User point balances
├── invites.json     # Invite tracking data
└── cooldowns.json   # Vouch cooldown timestamps
```

### Data Persistence
- **Async Operations**: All file operations are asynchronous
- **Error Handling**: Graceful handling of file corruption
- **Automatic Creation**: Files created if missing
- **JSON Format**: Human-readable data storage

### Data Backup
- Files are automatically backed up during operations
- Atomic writes prevent data corruption
- Error recovery mechanisms

---

## 🚀 Features

### 1. Auto-Moderation
- **Invite Protection**: Bans users posting Discord invites
- **Scam Blocking**: Blocks known scam domains
- **Channel Protection**: Maintains clean order/support channels

### 2. Invite Tracking
- **Join Tracking**: Records who invited new members
- **Leave Tracking**: Removes points when members leave
- **Statistics**: Tracks invite counts and relationships
- **Notifications**: Posts to dedicated tracker channel

### 3. Vouch System
- **Image Processing**: Downloads and watermarks images
- **Point Rewards**: Awards points for successful vouches
- **Cooldown System**: Prevents spam with time limits
- **Admin Bypass**: Admins can vouch without cooldowns
- **Fallback System**: Text-based vouches if image processing fails

### 4. Verification System
- **Auto-Mute**: Mutes unverified users automatically
- **Auto-Unmute**: Unmutes users when they get verified role
- **Startup Scan**: Scans all members on bot startup
- **Role Monitoring**: Watches for role changes

### 5. Point System
- **Persistent Storage**: Points saved across bot restarts
- **Leaderboards**: Top users by points
- **Admin Commands**: Administrative point management

---

## 📚 API Reference

### Event Handlers

#### `on_ready()`
- Bot startup initialization
- Command syncing
- Status logging

#### `on_message(message)`
- Message content analysis
- Moderation checks
- Channel-specific handling
- Command processing

#### `on_member_join(member)`
- Invite tracking
- Verification status check
- Welcome message (optional)

#### `on_member_remove(member)`
- Invite point removal
- Tracker channel notification
- Relationship cleanup

#### `on_member_update(before, after)`
- Role change detection
- Verification status updates
- Mute/unmute actions

### Error Handling
- **Comprehensive Try-Catch**: All operations wrapped in error handling
- **Graceful Degradation**: Fallback systems for failed operations
- **User Feedback**: Clear error messages to users
- **Logging**: Detailed console logging for debugging

---

## 🛠️ Deployment

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Server permissions

### Installation
```bash
# Clone repository
git clone <repository_url>
cd securitybot

# Install dependencies
pip install -r requirements.txt

# Setup environment
python setup_env.py

# Configure .env file
# Edit .env with your bot token and IDs

# Run tests
python test_bot.py

# Start bot
python main.py
```

### Required Permissions
- **Manage Messages**: Delete messages in protected channels
- **Manage Roles**: Mute/unmute users
- **Ban Members**: Ban users for violations
- **Send Messages**: Post notifications and responses
- **Attach Files**: Upload watermarked images
- **Use Slash Commands**: Execute slash commands

### Server Setup
1. Create bot application in Discord Developer Portal
2. Generate bot token
3. Invite bot to server with required permissions
4. Configure channel and role IDs
5. Set up verification system roles

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Image Download Failures
**Symptoms**: 404 errors when processing vouches
**Solutions**:
- Check bot permissions
- Verify image format support
- Review download strategy logs
- Use fallback text-based vouches

#### 2. Invite Tracking Issues
**Symptoms**: Invites not being recorded
**Solutions**:
- Verify bot has invite permissions
- Check invite cache initialization
- Review member join/leave logs
- Validate invite tracker channel ID

#### 3. Configuration Errors
**Symptoms**: Bot fails to start
**Solutions**:
- Validate all environment variables
- Check ID formats (must be integers)
- Verify bot token validity
- Review permission settings

#### 4. Data Corruption
**Symptoms**: Points or invites not saving
**Solutions**:
- Check file permissions
- Validate JSON syntax
- Review async operation logs
- Restore from backup if needed

### Debug Commands
```bash
# Test configuration
python test_bot.py

# Check data files
python -c "import json; print(json.load(open('data/points.json')))"

# Validate environment
python -c "import config; print(config.BOT_TOKEN)"
```

### Logging
The bot provides comprehensive logging:
- **Console Output**: Real-time operation status
- **Error Tracking**: Detailed error messages
- **Debug Information**: Strategy attempt logs
- **User Actions**: Command and interaction logs

---

## 📝 Development Notes

### Code Style
- **PEP 8 Compliance**: Standard Python formatting
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Detailed function documentation
- **Error Handling**: Robust exception management

### Performance Considerations
- **Async Operations**: Non-blocking I/O operations
- **Memory Management**: Efficient data structures
- **File I/O**: Optimized JSON operations
- **Network Requests**: Timeout and retry mechanisms

### Security Features
- **Input Validation**: Sanitized user inputs
- **Permission Checks**: Role-based access control
- **Rate Limiting**: Cooldown systems
- **Error Sanitization**: Safe error messages

### Future Enhancements
- **Database Integration**: SQLite/PostgreSQL support
- **Web Dashboard**: Admin interface
- **Advanced Analytics**: Detailed statistics
- **Plugin System**: Modular feature extensions
- **Multi-Server Support**: Cross-server functionality

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

*Documentation generated for Bob's Discount Shack Discord Bot v1.0* 