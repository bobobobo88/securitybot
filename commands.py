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

    @app_commands.command(name="ticket", description="Create a support ticket")
    async def ticket(self, interaction: discord.Interaction):
        """Create a support ticket"""
        try:
            # Check if user is in support channel
            if interaction.channel_id != config.SUPPORT_CHANNEL_ID:
                await interaction.response.send_message(
                    "Please use this command in the support channel.",
                    ephemeral=True
                )
                return

            # Create ticket channel
            guild = interaction.guild
            category = guild.get_channel(config.SUPPORT_CHANNEL_ID).category
            
            # Create ticket channel name
            ticket_name = f"ticket-{interaction.user.name}"
            
            # Check if ticket already exists
            existing_channel = discord.utils.get(guild.channels, name=ticket_name)
            if existing_channel:
                await interaction.response.send_message(
                    f"You already have an open ticket: {existing_channel.mention}",
                    ephemeral=True
                )
                return

            # Create ticket channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }
            
            ticket_channel = await guild.create_text_channel(
                name=ticket_name,
                category=category,
                overwrites=overwrites
            )
            
            # Send welcome message
            embed = discord.Embed(
                title="🎫 Support Ticket Created",
                description=f"Welcome {interaction.user.mention}! A staff member will assist you shortly.",
                color=config.EMBED_COLORS['success']
            )
            embed.add_field(
                name="What to include:",
                value="• Your order details\n• Screenshots if needed\n• Specific issue description",
                inline=False
            )
            
            await ticket_channel.send(embed=embed)
            
            await interaction.response.send_message(
                f"Ticket created! {ticket_channel.mention}",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Error creating ticket: {e}")
            await interaction.response.send_message(
                "Error creating ticket. Please try again or contact staff.",
                ephemeral=True
            )

    @app_commands.command(name="order", description="Place an order")
    async def order(self, interaction: discord.Interaction):
        """Place an order (placeholder command)"""
        try:
            # Check if user is in order channel
            if interaction.channel_id not in config.ORDER_CHANNEL_IDS:
                await interaction.response.send_message(
                    "Please use this command in an order channel.",
                    ephemeral=True
                )
                return

            embed = discord.Embed(
                title="🛒 Order System",
                description="Order functionality coming soon!",
                color=config.EMBED_COLORS['info']
            )
            embed.add_field(
                name="Available Services",
                value="• Uber Eats\n• IPTV\n• Money-making methods\n• More coming soon!",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            print(f"Error in order command: {e}")
            await interaction.response.send_message(
                "Error processing order. Please try again.",
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