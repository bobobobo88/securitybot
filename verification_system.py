import discord
from discord.ext import commands
import config

class VerificationSystem:
    def __init__(self, bot):
        self.bot = bot

    async def check_and_mute_unverified(self, member: discord.Member):
        """Check if member has verified role, mute if not"""
        try:
            # Check if member has verified role
            has_verified_role = any(role.id == config.VERIFIED_ROLE_ID for role in member.roles)
            
            # Check if member already has muted role
            has_muted_role = any(role.id == config.MUTED_ROLE_ID for role in member.roles)
            
            if not has_verified_role and not has_muted_role:
                # Add muted role
                muted_role = member.guild.get_role(config.MUTED_ROLE_ID)
                if muted_role:
                    await member.add_roles(muted_role, reason="Auto-muted: No verified role")
                    print(f"Auto-muted {member} ({member.id}) - No verified role")
                    
                    # Send DM to user
                    try:
                        embed = discord.Embed(
                            title="🔇 You have been muted",
                            description="You have been automatically muted because you don't have the verified role.",
                            color=config.EMBED_COLORS['warning']
                        )
                        embed.add_field(
                            name="How to get verified:",
                            value="Contact a staff member to get the verified role.",
                            inline=False
                        )
                        await member.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send DM to {member} - DMs closed")
                    except Exception as e:
                        print(f"Error sending DM to {member}: {e}")
                else:
                    print(f"Error: Muted role not found (ID: {config.MUTED_ROLE_ID})")
            
            elif has_verified_role and has_muted_role:
                # Remove muted role if they have verified role
                muted_role = member.guild.get_role(config.MUTED_ROLE_ID)
                if muted_role:
                    await member.remove_roles(muted_role, reason="Auto-unmuted: Has verified role")
                    print(f"Auto-unmuted {member} ({member.id}) - Has verified role")
                    
                    # Send DM to user
                    try:
                        embed = discord.Embed(
                            title="🔊 You have been unmuted",
                            description="You have been automatically unmuted because you now have the verified role.",
                            color=config.EMBED_COLORS['success']
                        )
                        await member.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send DM to {member} - DMs closed")
                    except Exception as e:
                        print(f"Error sending DM to {member}: {e}")
                        
        except Exception as e:
            print(f"Error checking/muting member {member}: {e}")

    async def scan_all_members(self):
        """Scan all members in the guild and mute unverified ones"""
        try:
            if self.bot.guilds:
                guild = self.bot.guilds[0]
                print(f"Scanning {len(guild.members)} members for verification status...")
                
                muted_count = 0
                unmuted_count = 0
                
                for member in guild.members:
                    if not member.bot:  # Skip bots
                        # Check if member has verified role
                        has_verified_role = any(role.id == config.VERIFIED_ROLE_ID for role in member.roles)
                        has_muted_role = any(role.id == config.MUTED_ROLE_ID for role in member.roles)
                        
                        if not has_verified_role and not has_muted_role:
                            # Add muted role
                            muted_role = guild.get_role(config.MUTED_ROLE_ID)
                            if muted_role:
                                await member.add_roles(muted_role, reason="Auto-muted: No verified role")
                                muted_count += 1
                                print(f"Muted {member} ({member.id})")
                        
                        elif has_verified_role and has_muted_role:
                            # Remove muted role
                            muted_role = guild.get_role(config.MUTED_ROLE_ID)
                            if muted_role:
                                await member.remove_roles(muted_role, reason="Auto-unmuted: Has verified role")
                                unmuted_count += 1
                                print(f"Unmuted {member} ({member.id})")
                
                print(f"Scan complete: {muted_count} members muted, {unmuted_count} members unmuted")
                
        except Exception as e:
            print(f"Error scanning members: {e}")

    async def handle_member_update(self, before: discord.Member, after: discord.Member):
        """Handle member role updates"""
        try:
            # Check if verified role was added or removed
            before_verified = any(role.id == config.VERIFIED_ROLE_ID for role in before.roles)
            after_verified = any(role.id == config.VERIFIED_ROLE_ID for role in after.roles)
            
            if not before_verified and after_verified:
                # Member got verified role - unmute them
                muted_role = after.guild.get_role(config.MUTED_ROLE_ID)
                if muted_role and muted_role in after.roles:
                    await after.remove_roles(muted_role, reason="Auto-unmuted: Got verified role")
                    print(f"Auto-unmuted {after} ({after.id}) - Got verified role")
                    
                    # Send DM
                    try:
                        embed = discord.Embed(
                            title="🔊 You have been unmuted",
                            description="You have been automatically unmuted because you now have the verified role.",
                            color=config.EMBED_COLORS['success']
                        )
                        await after.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send DM to {after} - DMs closed")
                    except Exception as e:
                        print(f"Error sending DM to {after}: {e}")
            
            elif before_verified and not after_verified:
                # Member lost verified role - mute them
                muted_role = after.guild.get_role(config.MUTED_ROLE_ID)
                if muted_role and muted_role not in after.roles:
                    await after.add_roles(muted_role, reason="Auto-muted: Lost verified role")
                    print(f"Auto-muted {after} ({after.id}) - Lost verified role")
                    
                    # Send DM
                    try:
                        embed = discord.Embed(
                            title="🔇 You have been muted",
                            description="You have been automatically muted because you lost the verified role.",
                            color=config.EMBED_COLORS['warning']
                        )
                        embed.add_field(
                            name="How to get verified:",
                            value="Contact a staff member to get the verified role.",
                            inline=False
                        )
                        await after.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send DM to {after} - DMs closed")
                    except Exception as e:
                        print(f"Error sending DM to {after}: {e}")
                        
        except Exception as e:
            print(f"Error handling member update: {e}") 