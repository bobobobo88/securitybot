import discord
from discord.ext import commands
import config
from data_manager import DataManager
from image_processor import ImageProcessor
from io import BytesIO

class VouchSystem:
    def __init__(self, bot):
        self.bot = bot
        self.data_manager = DataManager()
        self.image_processor = ImageProcessor()

    def is_image_attachment(self, message: discord.Message) -> bool:
        """Check if message contains image attachment"""
        if not message.attachments:
            return False
        
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                return True
        return False

    def get_image_url(self, message: discord.Message) -> str:
        """Get the first image URL from message attachments"""
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                return attachment.url
        return None

    async def download_attachment_directly(self, attachment: discord.Attachment) -> BytesIO:
        """Download attachment directly without using URL"""
        try:
            print(f"Downloading attachment directly: {attachment.filename}, {attachment.size} bytes")
            data = await attachment.read()
            print(f"Successfully downloaded {len(data)} bytes")
            return BytesIO(data)
        except Exception as e:
            print(f"Error downloading attachment directly: {e}")
            raise e

    async def download_with_retry(self, attachment: discord.Attachment) -> BytesIO:
        """Download attachment with simple retry strategy"""
        # Try direct download first (this was working before)
        try:
            print("Attempting direct attachment download...")
            data = await attachment.read()
            print(f"Successfully downloaded {len(data)} bytes")
            return BytesIO(data)
        except Exception as e1:
            print(f"Direct download failed: {e1}")
            
            # Fallback: Try URL download with basic headers
            try:
                print("Trying URL download as fallback...")
                import aiohttp
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url, headers=headers, timeout=30) as response:
                        if response.status == 200:
                            data = await response.read()
                            print(f"URL download successful: {len(data)} bytes")
                            return BytesIO(data)
                        else:
                            raise Exception(f"HTTP {response.status}")
            except Exception as e2:
                print(f"URL download failed: {e2}")
                raise Exception(f"All download methods failed. Last error: {e2}")

    async def process_vouch(self, message: discord.Message):
        """Process a vouch image - watermark and award points"""
        try:
            # Check if user has admin role (bypass cooldown)
            has_admin_role = any(role.id == config.ADMIN_ROLE_ID for role in message.author.roles)
            
            # Check if user is on cooldown (skip for admins)
            if not has_admin_role and self.data_manager.is_on_cooldown(message.author.id):
                remaining = self.data_manager.get_cooldown_remaining(message.author.id)
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} Please wait {hours}h {minutes}m before posting another vouch.",
                    delete_after=10
                )
                return

            # Get image attachment
            image_attachment = None
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    image_attachment = attachment
                    break
            
            if not image_attachment:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} Please attach an image with your vouch.",
                    delete_after=10
                )
                return

            # Process image with watermark FIRST (before deleting message)
            try:
                print(f"Processing vouch image from {message.author}")
                print(f"Attachment info: {image_attachment.filename}, {image_attachment.content_type}, {image_attachment.size} bytes")
                
                # Use retry strategy to download image
                image_data = await self.download_with_retry(image_attachment)
                watermarked_image = self.image_processor.apply_watermark(image_data)
                print("Successfully processed image with watermark")
                
                # Check final image size
                watermarked_image.seek(0)
                final_size = len(watermarked_image.getvalue())
                print(f"Final watermarked image size: {final_size / 1024 / 1024:.2f}MB")
                
                # NOW delete the original message
                await message.delete()
                
                # Upload watermarked image (now JPEG format for better compression)
                file = discord.File(watermarked_image, filename="vouch_watermarked.jpg")
                
                # Send watermarked image with size-aware error handling
                try:
                    await message.channel.send(
                        f"**Vouch from {message.author.mention}**",
                        file=file
                    )
                    print("Successfully uploaded watermarked image")
                    
                except discord.HTTPException as e:
                    if "413" in str(e) or "Payload Too Large" in str(e) or "40005" in str(e):
                        print(f"Image still too large after optimization: {e}")
                        print(f"Final size was: {final_size / 1024 / 1024:.2f}MB")
                        # Fall back to text-based vouch with image info
                        await self.send_fallback_vouch(message, image_attachment, final_size)
                    else:
                        print(f"Other Discord upload error: {e}")
                        # Try fallback for any upload error
                        await self.send_fallback_vouch(message, image_attachment, final_size)

                # Award points
                await self.data_manager.add_points(message.author.id, config.POINTS_PER_VOUCH)
                
                # Set cooldown only for non-admin users
                if not has_admin_role:
                    await self.data_manager.set_cooldown(message.author.id)

                # Send confirmation
                points = self.data_manager.get_points(message.author.id)
                await message.channel.send(
                    f"Thanks for posting success {message.author.mention}! You now have {points} point(s). 💰",
                    delete_after=10
                )

            except Exception as e:
                print(f"Error processing vouch image: {e}")
                print(f"Attachment info: {image_attachment.filename}, {image_attachment.content_type}, {image_attachment.size} bytes")
                
                # Fallback: Create a comprehensive text-based vouch
                await self.send_fallback_vouch(message, image_attachment, 0)
                
                # Award points even with fallback
                await self.data_manager.add_points(message.author.id, config.POINTS_PER_VOUCH)
                
                # Set cooldown only for non-admin users
                if not has_admin_role:
                    await self.data_manager.set_cooldown(message.author.id)
                
                # Send confirmation
                points = self.data_manager.get_points(message.author.id)
                await message.channel.send(
                    f"Thanks for posting success {message.author.mention}! You now have {points} point(s). 💰",
                    delete_after=10
                )

        except Exception as e:
            print(f"Error in vouch processing: {e}")

    async def send_fallback_vouch(self, message: discord.Message, attachment: discord.Attachment, processed_size: int):
        """Send a fallback text-based vouch when image upload fails"""
        try:
            print("Sending fallback text-based vouch...")
            
            # Create a comprehensive embed
            embed = discord.Embed(
                title="📸 Vouch from " + message.author.display_name,
                description=f"**{message.author.mention}** posted a vouch!",
                color=config.EMBED_COLORS['success']
            )
            
            # Add file information
            embed.add_field(
                name="📎 Original File",
                value=f"`{attachment.filename}` ({attachment.size:,} bytes)",
                inline=False
            )
            
            if processed_size > 0:
                embed.add_field(
                    name="🖼️ Processed Size",
                    value=f"`{processed_size:,} bytes` ({processed_size / 1024 / 1024:.2f}MB)",
                    inline=False
                )
            
            # Add file type info
            embed.add_field(
                name="📋 File Type",
                value=f"`{attachment.content_type}`",
                inline=True
            )
            
            # Add timestamp
            embed.timestamp = discord.utils.utcnow()
            
            # Set thumbnail
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            # Add footer with processing note
            embed.set_footer(text="Image processed with watermark but too large for Discord upload")
            
            await message.channel.send(embed=embed)
            print("Fallback vouch sent successfully")
            
        except Exception as e:
            print(f"Error sending fallback vouch: {e}")
            # Ultimate fallback - just send a simple message
            await message.channel.send(
                f"📸 **Vouch from {message.author.mention}**\n"
                f"File: `{attachment.filename}` ({attachment.size:,} bytes)\n"
                f"*Image processed but too large for upload*"
            )

    async def handle_vouch_channel(self, message: discord.Message):
        """Handle messages in vouch channel"""
        print(f"Vouch channel message detected from {message.author}: {len(message.attachments)} attachments")
        
        # Only process messages with image attachments
        if self.is_image_attachment(message):
            print(f"Processing vouch image from {message.author}")
            await self.process_vouch(message)
        else:
            print(f"Deleting non-image message from {message.author}")
            # Delete non-image messages
            try:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} Please attach an image with your vouch.",
                    delete_after=10
                )
            except discord.Forbidden:
                print(f"Cannot delete message in vouch channel - insufficient permissions")
            except Exception as e:
                print(f"Error handling vouch channel message: {e}") 