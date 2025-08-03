import discord
from discord.ext import commands
import config
from data_manager import DataManager

class InviteTracker:
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = DataManager()
        self.invite_cache = {}

    async def cache_invites(self):
        """Cache all current invites for tracking"""
        try:
            guild = self.bot.get_guild(config.GUILD_ID)
            if guild:
                invites = await guild.invites()
                self.invite_cache = {invite.code: invite.uses for invite in invites}
                print(f"Cached {len(self.invite_cache)} invites")
        except Exception as e:
            print(f"Error caching invites: {e}")

    async def handle_member_join(self, member: discord.Member):
        """Handle new member join - determine who invited them"""
        try:
            # Get current invites
            guild = member.guild
            current_invites = await guild.invites()
            
            # Find which invite was used
            used_invite = None
            for invite in current_invites:
                cached_uses = self.invite_cache.get(invite.code, 0)
                if invite.uses > cached_uses:
                    used_invite = invite
                    break
            
            if used_invite:
                # Update cache
                self.invite_cache[used_invite.code] = used_invite.uses
                
                # Record the invite
                await self.data_manager.add_invite(used_invite.inviter.id, member.id)
                
                print(f"Member {member} was invited by {used_invite.inviter}")
                
                # Optional: Send welcome message with inviter info
                # await self.send_welcome_message(member, used_invite.inviter)
                
            else:
                print(f"Could not determine who invited {member}")
                
        except Exception as e:
            print(f"Error handling member join: {e}")

    async def send_welcome_message(self, member: discord.Member, inviter: discord.Member):
        """Send welcome message with inviter info (optional)"""
        try:
            welcome_channel = member.guild.system_channel
            if welcome_channel:
                embed = discord.Embed(
                    title="Welcome to Bob's Discount Shack! 🎉",
                    description=f"Welcome {member.mention}! You were invited by {inviter.mention}",
                    color=config.EMBED_COLORS['success']
                )
                embed.add_field(
                    name="Getting Started",
                    value="• Use `/order` to place orders\n• Use `/ticket` for support\n• Post vouches in the vouch channel for points!",
                    inline=False
                )
                await welcome_channel.send(embed=embed)
        except Exception as e:
            print(f"Error sending welcome message: {e}")

    async def get_invite_stats(self, user_id: int) -> dict:
        """Get invite statistics for a user"""
        invite_count = self.data_manager.get_invite_count(user_id)
        
        # Get recent invites (last 30 days)
        # This would require additional tracking in the data manager
        # For now, just return the total count
        
        return {
            'total_invites': invite_count,
            'recent_invites': invite_count,  # Placeholder
            'rank': self.get_invite_rank(user_id)
        }

    def get_invite_rank(self, user_id: int) -> int:
        """Get user's rank in invite leaderboard"""
        leaderboard = self.data_manager.get_invites_leaderboard()
        for i, (user_id_str, count) in enumerate(leaderboard):
            if int(user_id_str) == user_id:
                return i + 1
        return 0  # Not in top 10 