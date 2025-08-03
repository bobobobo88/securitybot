import discord
from discord import app_commands
from discord.ext import commands
import config
from data_manager import DataManager

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = DataManager()

    @app_commands.command(name="points", description="Check your current point balance")
    async def points(self, interaction: discord.Interaction):
        """Check user's point balance"""
        try:
            points = self.data_manager.get_points(interaction.user.id)
            
            embed = discord.Embed(
                title="💰 Point Balance",
                description=f"You have **{points}** points from vouches",
                color=config.EMBED_COLORS['success']
            )
            
            # Add leaderboard info
            leaderboard = self.data_manager.get_points_leaderboard(5)
            if leaderboard:
                leaderboard_text = ""
                for i, (user_id, count) in enumerate(leaderboard):
                    user = self.bot.get_user(int(user_id))
                    username = user.name if user else f"User {user_id}"
                    leaderboard_text += f"{i+1}. {username}: {count} points\n"
                
                embed.add_field(
                    name="🏆 Top 5 Leaderboard",
                    value=leaderboard_text,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            print(f"Error in points command: {e}")
            await interaction.response.send_message(
                "Error retrieving points. Please try again.",
                ephemeral=True
            )

    @app_commands.command(name="invites", description="Check your invite count")
    async def invites(self, interaction: discord.Interaction):
        """Check user's invite count"""
        try:
            invite_count = self.data_manager.get_invite_count(interaction.user.id)
            
            embed = discord.Embed(
                title="📨 Invite Statistics",
                description=f"You have invited **{invite_count}** members to the server",
                color=config.EMBED_COLORS['info']
            )
            
            # Add leaderboard info
            leaderboard = self.data_manager.get_invites_leaderboard(5)
            if leaderboard:
                leaderboard_text = ""
                for i, (user_id, count) in enumerate(leaderboard):
                    user = self.bot.get_user(int(user_id))
                    username = user.name if user else f"User {user_id}"
                    leaderboard_text += f"{i+1}. {username}: {count} invites\n"
                
                embed.add_field(
                    name="🏆 Top 5 Inviters",
                    value=leaderboard_text,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            print(f"Error in invites command: {e}")
            await interaction.response.send_message(
                "Error retrieving invite count. Please try again.",
                ephemeral=True
            )



    @app_commands.command(name="inviteboard", description="Display invite leaderboard in tracker channel (Admin only)")
    async def inviteboard(self, interaction: discord.Interaction):
        """Display invite leaderboard in the tracker channel"""
        try:
            # Check if user has admin role
            has_admin_role = any(role.id == config.ADMIN_ROLE_ID for role in interaction.user.roles)
            if not has_admin_role:
                await interaction.response.send_message(
                    "You don't have permission to use this command.",
                    ephemeral=True
                )
                return

            # Check if tracker channel is configured
            if not config.INVITE_TRACKER_CHANNEL_ID:
                await interaction.response.send_message(
                    "Invite tracker channel not configured. Set INVITE_TRACKER_CHANNEL_ID in .env",
                    ephemeral=True
                )
                return

            channel = self.bot.get_channel(config.INVITE_TRACKER_CHANNEL_ID)
            if not channel:
                await interaction.response.send_message(
                    "Invite tracker channel not found. Check the channel ID.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "Posting invite leaderboard to tracker channel...",
                ephemeral=True
            )

            # Get leaderboard
            leaderboard = self.data_manager.get_invites_leaderboard(10)
            
            if not leaderboard:
                embed = discord.Embed(
                    title="📊 Invite Leaderboard",
                    description="No invites tracked yet!",
                    color=config.EMBED_COLORS['info']
                )
            else:
                embed = discord.Embed(
                    title="📊 Invite Leaderboard",
                    description="Top 10 members by invites",
                    color=config.EMBED_COLORS['success']
                )
                
                leaderboard_text = ""
                for i, (user_id, invites) in enumerate(leaderboard):
                    user = self.bot.get_user(int(user_id))
                    username = user.name if user else f"User {user_id}"
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                    leaderboard_text += f"{medal} {username}: {invites} invites\n"
                
                embed.add_field(
                    name="🏆 Rankings",
                    value=leaderboard_text,
                    inline=False
                )
            
            embed.timestamp = discord.utils.utcnow()
            await channel.send(embed=embed)
            
            await interaction.followup.send(
                "Invite leaderboard posted!",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Error in inviteboard command: {e}")
            await interaction.response.send_message(
                "Error posting invite leaderboard. Please try again.",
                ephemeral=True
            )

    @app_commands.command(name="scan", description="Scan all members for verification status (Admin only)")
    async def scan_members(self, interaction: discord.Interaction):
        """Scan all members and mute unverified ones"""
        try:
            # Check if user has admin role
            has_admin_role = any(role.id == config.ADMIN_ROLE_ID for role in interaction.user.roles)
            if not has_admin_role:
                await interaction.response.send_message(
                    "You don't have permission to use this command.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "Scanning all members for verification status... This may take a moment.",
                ephemeral=True
            )

            # Import verification system
            from verification_system import VerificationSystem
            verification_system = VerificationSystem(self.bot)
            
            # Scan all members
            await verification_system.scan_all_members()
            
            await interaction.followup.send(
                "Member scan complete! Check console for details.",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Error in scan command: {e}")
            await interaction.response.send_message(
                "Error scanning members. Please try again.",
                ephemeral=True
            )

    @app_commands.command(name="leaderboard", description="View points leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        """Show points leaderboard"""
        try:
            leaderboard = self.data_manager.get_points_leaderboard(10)
            
            if not leaderboard:
                embed = discord.Embed(
                    title="🏆 Points Leaderboard",
                    description="No points earned yet!",
                    color=config.EMBED_COLORS['info']
                )
            else:
                embed = discord.Embed(
                    title="🏆 Points Leaderboard",
                    description="Top 10 members by points",
                    color=config.EMBED_COLORS['success']
                )
                
                leaderboard_text = ""
                for i, (user_id, points) in enumerate(leaderboard):
                    user = self.bot.get_user(int(user_id))
                    username = user.name if user else f"User {user_id}"
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                    leaderboard_text += f"{medal} {username}: {points} points\n"
                
                embed.add_field(
                    name="Rankings",
                    value=leaderboard_text,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(f"Error in leaderboard command: {e}")
            await interaction.response.send_message(
                "Error retrieving leaderboard. Please try again.",
                ephemeral=True
            ) 