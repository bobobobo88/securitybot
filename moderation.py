import re
import discord
from discord.ext import commands
import config

class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.invite_pattern = re.compile(r'discord\.gg/[a-zA-Z0-9]+')
        self.scam_domains = [
            'scam.com',
            'malicious.net',
            'fake-discord.com',
            # Add more domains as needed
        ]

    def contains_invite_link(self, content: str) -> bool:
        """Check if message contains Discord invite link"""
        return bool(self.invite_pattern.search(content))

    def contains_scam_domain(self, content: str) -> bool:
        """Check if message contains known scam domain"""
        content_lower = content.lower()
        return any(domain in content_lower for domain in self.scam_domains)

    async def handle_invite_link(self, message: discord.Message):
        """Handle invite link detection - ban user immediately"""
        try:
            # Ban the user
            await message.author.ban(reason="Posted Discord invite link")
            
            # Log the action
            print(f"Banned user {message.author} ({message.author.id}) for posting invite link")
            
            # Send notification to staff (optional)
            # You can implement this to notify staff channels
            
        except discord.Forbidden:
            print(f"Cannot ban user {message.author} - insufficient permissions")
        except Exception as e:
            print(f"Error banning user {message.author}: {e}")

    async def handle_scam_domain(self, message: discord.Message):
        """Handle scam domain detection - delete message and ban user"""
        try:
            # Delete the message
            await message.delete()
            
            # Ban the user
            await message.author.ban(reason="Posted scam/malicious domain")
            
            # Log the action
            print(f"Banned user {message.author} ({message.author.id}) for posting scam domain")
            
        except discord.Forbidden:
            print(f"Cannot ban user {message.author} - insufficient permissions")
        except Exception as e:
            print(f"Error handling scam domain for user {message.author}: {e}")

    async def handle_order_channel(self, message: discord.Message):
        """Handle order channel protection - delete ALL messages"""
        try:
            # Delete the message
            await message.delete()
            
            # Send ephemeral message to the user
            await message.author.send(
                "Please contact staff for orders and support.",
                delete_after=10
            )
            
        except discord.Forbidden:
            print(f"Cannot delete message in order channel - insufficient permissions")
        except Exception as e:
            print(f"Error handling order channel message: {e}")

    async def handle_support_channel(self, message: discord.Message):
        """Handle support channel protection - delete ALL messages"""
        try:
            # Delete the message
            await message.delete()
            
            # Send ephemeral message to the user
            await message.author.send(
                "Please contact staff for orders and support.",
                delete_after=10
            )
            
        except discord.Forbidden:
            print(f"Cannot delete message in support channel - insufficient permissions")
        except Exception as e:
            print(f"Error handling support channel message: {e}")

    async def check_message(self, message: discord.Message):
        """Main message checking function"""
        # Skip bot messages
        if message.author.bot:
            return

        # Check for invite links (server-wide)
        if self.contains_invite_link(message.content):
            await self.handle_invite_link(message)
            return

        # Check for scam domains (server-wide)
        if self.contains_scam_domain(message.content):
            await self.handle_scam_domain(message)
            return

        # Check channel-specific protections
        if message.channel.id in config.ORDER_CHANNEL_IDS:
            print(f"Message in order channel from {message.author}")
            await self.handle_order_channel(message)
        elif message.channel.id == config.SUPPORT_CHANNEL_ID:
            print(f"Message in support channel from {message.author}")
            await self.handle_support_channel(message) 