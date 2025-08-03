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
        """Download attachment with multiple retry strategies"""
        # Strategy 1: Direct download
        try:
            print("Strategy 1: Direct attachment download")
            return await self.download_attachment_directly(attachment)
        except Exception as e1:
            print(f"Strategy 1 failed: {e1}")
            
            # Strategy 2: URL download with different headers
            try:
                print("Strategy 2: URL download with browser headers")
                import aiohttp
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://discord.com/',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url, headers=headers, timeout=30) as response:
                        if response.status == 200:
                            data = await response.read()
                            print(f"Strategy 2 successful: {len(data)} bytes")
                            return BytesIO(data)
                        else:
                            raise Exception(f"HTTP {response.status}")
            except Exception as e2:
                print(f"Strategy 2 failed: {e2}")
                
                # Strategy 3: Try with different URL format
                try:
                    print("Strategy 3: Alternative URL format")
                    # Try without query parameters
                    base_url = attachment.url.split('?')[0]
                    async with aiohttp.ClientSession() as session:
                        async with session.get(base_url, headers=headers, timeout=30) as response:
                            if response.status == 200:
                                data = await response.read()
                                print(f"Strategy 3 successful: {len(data)} bytes")
                                return BytesIO(data)
                            else:
                                raise Exception(f"HTTP {response.status}")
                except Exception as e3:
                    print(f"Strategy 3 failed: {e3}")
                    
                    # Strategy 4: Try with different CDN endpoints
                    try:
                        print("Strategy 4: Alternative CDN endpoints")
                        # Try different Discord CDN endpoints
                        cdn_urls = [
                            attachment.url.replace('cdn.discordapp.com', 'media.discordapp.net'),
                            attachment.url.replace('cdn.discordapp.com', 'images-ext-1.discordapp.net'),
                            attachment.url.replace('cdn.discordapp.com', 'images-ext-2.discordapp.net'),
                        ]
                        
                        for cdn_url in cdn_urls:
                            try:
                                print(f"Trying CDN URL: {cdn_url}")
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(cdn_url, headers=headers, timeout=30) as response:
                                        if response.status == 200:
                                            data = await response.read()
                                            print(f"Strategy 4 successful: {len(data)} bytes")
                                            return BytesIO(data)
                            except Exception as cdn_error:
                                print(f"CDN URL failed: {cdn_error}")
                                continue
                        
                        raise Exception("All CDN endpoints failed")
                    except Exception as e4:
                        print(f"Strategy 4 failed: {e4}")
                        
                        # Strategy 5: Try with session cookies and more aggressive headers
                        try:
                            print("Strategy 5: Aggressive browser simulation")
                            aggressive_headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'Accept-Language': 'en-US,en;q=0.9',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Referer': 'https://discord.com/channels/@me',
                                'DNT': '1',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                                'Sec-Fetch-Dest': 'image',
                                'Sec-Fetch-Mode': 'no-cors',
                                'Sec-Fetch-Site': 'same-site',
                                'Cache-Control': 'no-cache',
                                'Pragma': 'no-cache'
                            }
                            
                            async with aiohttp.ClientSession() as session:
                                async with session.get(attachment.url, headers=aggressive_headers, timeout=30) as response:
                                    if response.status == 200:
                                        data = await response.read()
                                        print(f"Strategy 5 successful: {len(data)} bytes")
                                        return BytesIO(data)
                                    else:
                                        raise Exception(f"HTTP {response.status}")
                        except Exception as e5:
                            print(f"Strategy 5 failed: {e5}")
                            
                            # Strategy 6: Try using bot's HTTP session
                            try:
                                print("Strategy 6: Using bot's HTTP session")
                                # Use the bot's own HTTP session which might have different permissions
                                async with self.bot.http.session.get(attachment.url, timeout=30) as response:
                                    if response.status == 200:
                                        data = await response.read()
                                        print(f"Strategy 6 successful: {len(data)} bytes")
                                        return BytesIO(data)
                                    else:
                                        raise Exception(f"HTTP {response.status}")
                            except Exception as e6:
                                print(f"Strategy 6 failed: {e6}")
                                
                                # Strategy 7: Try with different URL parameters
                                try:
                                    print("Strategy 7: Modified URL parameters")
                                    # Try adding different parameters to the URL
                                    base_url = attachment.url.split('?')[0]
                                    modified_urls = [
                                        f"{base_url}?size=4096",
                                        f"{base_url}?size=2048", 
                                        f"{base_url}?size=1024",
                                        f"{base_url}?format=webp",
                                        f"{base_url}?format=png"
                                    ]
                                    
                                    for modified_url in modified_urls:
                                        try:
                                            print(f"Trying modified URL: {modified_url}")
                                            async with aiohttp.ClientSession() as session:
                                                async with session.get(modified_url, headers=headers, timeout=30) as response:
                                                    if response.status == 200:
                                                        data = await response.read()
                                                        print(f"Strategy 7 successful: {len(data)} bytes")
                                                        return BytesIO(data)
                                        except Exception as url_error:
                                            print(f"Modified URL failed: {url_error}")
                                            continue
                                    
                                    raise Exception("All modified URLs failed")
                                except Exception as e7:
                                    print(f"Strategy 7 failed: {e7}")
                                    raise Exception(f"All download strategies failed. Last error: {e7}")

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
                
                # Use retry strategy to download image
                image_data = await self.download_with_retry(image_attachment)
                watermarked_image = self.image_processor.apply_watermark(image_data)
                print("Successfully processed image with watermark")
                
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
                
                # Fallback: Create a simple text-based vouch
                try:
                    print("Attempting fallback text-based vouch...")
                    embed = discord.Embed(
                        title="📸 Vouch from " + message.author.display_name,
                        description=f"**{message.author.mention}** posted a vouch!",
                        color=config.EMBED_COLORS['success']
                    )
                    embed.add_field(
                        name="📎 Original File",
                        value=f"`{image_attachment.filename}` ({image_attachment.size:,} bytes)",
                        inline=False
                    )
                    embed.set_thumbnail(url=message.author.display_avatar.url)
                    embed.timestamp = discord.utils.utcnow()
                    
                    await message.channel.send(embed=embed)
                    
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
                    
                except Exception as fallback_error:
                    print(f"Fallback also failed: {fallback_error}")
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