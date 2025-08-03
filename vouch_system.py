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

    async def process_vouch(self, message: discord.Message):
        """Process a vouch image - watermark and award points"""
        try:
            # Check if user is on cooldown
            if self.data_manager.is_on_cooldown(message.author.id):
                remaining = self.data_manager.get_cooldown_remaining(message.author.id)
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention} Please wait {hours}h {minutes}m before posting another vouch.",
                    delete_after=10
                )
                return

            # Get image URL
            image_url = self.get_image_url(message)
            if not image_url:
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
                watermarked_image = await self.image_processor.process_vouch_image(image_url)
                
                # Upload watermarked image
                file = discord.File(watermarked_image, filename="vouch_watermarked.png")
                
                # Send watermarked image
                await message.channel.send(
                    f"**Vouch from {message.author.mention}**",
                    file=file
                )

                # Award points
                await self.data_manager.add_points(message.author.id, config.POINTS_PER_VOUCH)
                await self.data_manager.set_cooldown(message.author.id)

                # Send confirmation
                points = self.data_manager.get_points(message.author.id)
                await message.channel.send(
                    f"Thanks for posting success {message.author.mention}! You now have {points} point(s). 💰",
                    delete_after=10
                )

            except Exception as e:
                print(f"Error processing vouch image: {e}")
                await message.channel.send(
                    f"{message.author.mention} Error processing your image. Please try again.",
                    delete_after=10
                )

        except Exception as e:
            print(f"Error in vouch processing: {e}")

    async def handle_vouch_channel(self, message: discord.Message):
        """Handle messages in vouch channel"""
        # Only process messages with image attachments
        if self.is_image_attachment(message):
            await self.process_vouch(message)
        else:
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