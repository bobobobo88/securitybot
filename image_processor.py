import os
import aiofiles
import aiohttp
import asyncio
from PIL import Image, ImageEnhance
from io import BytesIO
import config

class ImageProcessor:
    def __init__(self):
        self.watermark_path = config.WATERMARK_PATH
        self.ensure_watermark_exists()

    def ensure_watermark_exists(self):
        """Ensure watermark file exists, create placeholder if not"""
        if not os.path.exists(self.watermark_path):
            os.makedirs(os.path.dirname(self.watermark_path), exist_ok=True)
            # Create a simple placeholder watermark
            self.create_placeholder_watermark()

    def create_placeholder_watermark(self):
        """Create a simple placeholder watermark"""
        try:
            # Create a simple text-based watermark
            img = Image.new('RGBA', (400, 200), (0, 0, 0, 0))
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(img)
            # Use default font
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            text = "Stream Plug"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
            
            # Draw text with outline
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
            
            img.save(self.watermark_path, 'PNG')
            print(f"Created placeholder watermark at {self.watermark_path}")
        except Exception as e:
            print(f"Error creating placeholder watermark: {e}")

    async def download_image(self, url: str) -> BytesIO:
        """Download image from URL"""
        print(f"Attempting to download image from: {url}")
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=30) as response:
                    print(f"Download response status: {response.status}")
                    print(f"Response headers: {dict(response.headers)}")
                    
                    if response.status == 200:
                        data = await response.read()
                        print(f"Successfully downloaded {len(data)} bytes")
                        return BytesIO(data)
                    else:
                        error_text = await response.text()
                        print(f"Error response: {error_text}")
                        raise Exception(f"Failed to download image: {response.status} - {error_text}")
            except aiohttp.ClientError as e:
                print(f"Network error downloading image: {e}")
                raise Exception(f"Network error: {e}")
            except asyncio.TimeoutError:
                print("Timeout downloading image")
                raise Exception("Timeout downloading image")
            except Exception as e:
                print(f"Unexpected error downloading image: {e}")
                raise e

    def apply_watermark(self, image_data: BytesIO) -> BytesIO:
        """Apply watermark to image with size optimization"""
        try:
            # Open the main image
            main_image = Image.open(image_data)
            
            # Convert to RGBA if necessary
            if main_image.mode != 'RGBA':
                main_image = main_image.convert('RGBA')
            
            # Load watermark
            watermark = Image.open(self.watermark_path)
            
            # Resize watermark to be proportional to main image
            watermark_size = min(main_image.width, main_image.height) // 3
            watermark = watermark.resize((watermark_size, watermark_size), Image.Resampling.LANCZOS)
            
            # Calculate position (center)
            x = (main_image.width - watermark.width) // 2
            y = (main_image.height - watermark.height) // 2
            
            # Create a copy of the main image
            result = main_image.copy()
            
            # Paste watermark with alpha blending
            result.paste(watermark, (x, y), watermark)
            
            # Optimize image size for Discord (max 8MB, target under 5MB)
            output = BytesIO()
            
            # Try different quality settings to get optimal file size
            quality_settings = [85, 75, 65, 55]
            max_size_bytes = 5 * 1024 * 1024  # 5MB target
            
            for quality in quality_settings:
                output.seek(0)
                output.truncate(0)
                
                # Save with current quality
                result.save(output, format='JPEG', quality=quality, optimize=True)
                output.seek(0)
                
                # Check file size
                current_size = len(output.getvalue())
                print(f"Image size with quality {quality}: {current_size / 1024 / 1024:.2f}MB")
                
                if current_size <= max_size_bytes:
                    print(f"Image optimized successfully: {current_size / 1024 / 1024:.2f}MB")
                    break
                
                # If still too large, try resizing the image
                if quality == quality_settings[-1]:  # Last quality setting
                    print("Image still too large, resizing...")
                    # Resize image to reduce file size
                    scale_factor = 0.8
                    new_width = int(result.width * scale_factor)
                    new_height = int(result.height * scale_factor)
                    result = result.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Try saving again with highest quality
                    output.seek(0)
                    output.truncate(0)
                    result.save(output, format='JPEG', quality=85, optimize=True)
                    output.seek(0)
                    final_size = len(output.getvalue())
                    print(f"Resized image size: {final_size / 1024 / 1024:.2f}MB")
            
            return output
            
        except Exception as e:
            print(f"Error applying watermark: {e}")
            # Return original image if watermarking fails
            image_data.seek(0)
            return image_data

    async def process_vouch_image(self, image_url: str) -> BytesIO:
        """Process a vouch image: download, watermark, and return"""
        try:
            # Download the image
            image_data = await self.download_image(image_url)
            
            # Apply watermark
            watermarked_image = self.apply_watermark(image_data)
            
            return watermarked_image
            
        except Exception as e:
            print(f"Error processing vouch image: {e}")
            raise e 