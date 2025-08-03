import discord
from discord.ext import commands
import config
from data_manager import DataManager
from image_processor import ImageProcessor

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
            data = await attachment.read()
            return BytesIO(data)
        except Exception as e:
            print(f"Error downloading attachment directly: {e}")
            raise e

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

            # Delete original message immediately
            await message.delete()

            # Process image with watermark
            try:
                print(f"Processing vouch image from {message.author}")
                
                # Try direct download first, then URL as fallback
                try:
                    print("Attempting direct attachment download...")
                    image_data = await self.download_attachment_directly(image_attachment)
                    watermarked_image = self.image_processor.apply_watermark(image_data)
                    print("Successfully processed image via direct download")
                except Exception as direct_error:
                    print(f"Direct download failed: {direct_error}")
                    print("Trying URL download as fallback...")
                    image_url = image_attachment.url
                    watermarked_image = await self.image_processor.process_vouch_image(image_url)
                    print("Successfully processed image via URL download")
                
                # Upload watermarked image
                file = discord.File(watermarked_image, filename="vouch_watermarked.png")
                
                # Send watermarked image
                await message.channel.send(
                    f"**Vouch from {message.author.mention}**",
                    file=file
                )

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
                await message.channel.send(
                    f"{message.author.mention} Error processing your image. Please try again with a different image.",
                    delete_after=10
                )

        except Exception as e:
            print(f"Error in vouch processing: {e}")

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