import discord
from discord.ext import commands
import asyncio
import config
from moderation import Moderation
from vouch_system import VouchSystem
from invite_tracker import InviteTracker
from commands import BotCommands

class BobsDiscountBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        
        # Initialize systems
        self.moderation = Moderation(self)
        self.vouch_system = VouchSystem(self)
        self.invite_tracker = InviteTracker(self)
        
    async def setup_hook(self):
        """Setup hook for bot initialization"""
        # Add command cog
        await self.add_cog(BotCommands(self))
        
        # Cache invites for tracking
        await self.invite_tracker.cache_invites()
        
        print("Bot setup complete!")

    async def on_ready(self):
        """Bot ready event"""
        print(f"Logged in as {self.user}")
        print(f"Bot ID: {self.user.id}")
        print(f"Connected to {len(self.guilds)} guild(s)")
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        """Handle all incoming messages"""
        # Skip bot messages
        if message.author.bot:
            return

        # Process commands first
        await self.process_commands(message)

        # Handle moderation
        await self.moderation.check_message(message)

        # Handle vouch channel
        if message.channel.id == config.VOUCH_CHANNEL_ID:
            await self.vouch_system.handle_vouch_channel(message)

    async def on_member_join(self, member):
        """Handle new member joins for invite tracking"""
        await self.invite_tracker.handle_member_join(member)

    async def on_invite_create(self, invite):
        """Handle new invite creation"""
        # Update invite cache
        self.invite_tracker.invite_cache[invite.code] = invite.uses
        print(f"New invite created: {invite.code} by {invite.inviter}")

    async def on_invite_delete(self, invite):
        """Handle invite deletion"""
        # Remove from cache
        if invite.code in self.invite_tracker.invite_cache:
            del self.invite_tracker.invite_cache[invite.code]
        print(f"Invite deleted: {invite.code}")

async def main():
    """Main function to run the bot"""
    bot = BobsDiscountBot()
    
    try:
        await bot.start(config.BOT_TOKEN)
    except discord.LoginFailure:
        print("Invalid bot token. Please check your .env file.")
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 