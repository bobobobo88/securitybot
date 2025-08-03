import os
import aiofiles
import aiohttp
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    return BytesIO(data)
                else:
                    raise Exception(f"Failed to download image: {response.status}")

    def apply_watermark(self, image_data: BytesIO) -> BytesIO:
        """Apply watermark to image"""
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
            
            # Save to BytesIO
            output = BytesIO()
            result.save(output, format='PNG', quality=95)
            output.seek(0)
            
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