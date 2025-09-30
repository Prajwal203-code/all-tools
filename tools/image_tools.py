import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import zipfile
import tempfile
import cv2
import numpy as np
from io import BytesIO
import base64

class ImageProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'bulk_image_resizer': self.resize_images,
            'image_compressor': self.compress_images,
            'image_background_remover': self.remove_background,
            'meme_generator': self.generate_meme,
            'bulk_watermark': self.add_watermark,
            'social_thumbnail_generator': self.generate_thumbnails,
            'image_format_converter': self.convert_format,
            'photo_collage_maker': self.create_collage,
            'color_palette_extractor': self.extract_colors,
            'ai_image_enhancer': self.enhance_image,
            'ai_image_caption': self.generate_caption,
            'image_ocr_text': self.extract_text,
            'animated_gif_maker': self.create_gif,
            'video_gif_converter': self.video_to_gif,
            'meme_template_generator': self.generate_meme_template
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def resize_images(self, data, task_id):
        """Resize multiple images to specified dimensions"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        width = data.get('width', 800)
        height = data.get('height', 600)
        
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Resize image
                    resized_img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
                    
                    # Save resized image
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_resized.jpg")
                    resized_img.save(output_path, 'JPEG', quality=95)
                    output_files.append(output_path)
                    
            except Exception as e:
                # Create error file
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error resizing {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_resized_images.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def compress_images(self, data, task_id):
        """Compress images to reduce file size"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        quality = data.get('quality', 80)  # Default quality
        
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.convert('RGBA').split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                    
                    # Compress and save
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_compressed.jpg")
                    img.save(output_path, 'JPEG', quality=int(quality), optimize=True)
                    output_files.append(output_path)
                    
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error compressing {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_compressed_images.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def remove_background(self, data, task_id):
        """Remove background from images (simplified version)"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                # Simple background removal using edge detection (placeholder)
                img = cv2.imread(input_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # Create a simple mask (this is a very basic approach)
                edges = cv2.Canny(gray, 50, 150)
                mask = cv2.dilate(edges, None, iterations=1)
                mask = cv2.erode(mask, None, iterations=1)
                
                # Create transparent background
                result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
                result[:, :, 3] = 255 - mask  # Invert mask for transparency
                
                # Save as PNG
                output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_no_bg.png")
                cv2.imwrite(output_path, result)
                output_files.append(output_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error removing background from {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_background_removed.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def generate_meme(self, data, task_id):
        """Generate memes by adding text to images"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        top_text = data.get('top_text', 'TOP TEXT')
        bottom_text = data.get('bottom_text', 'BOTTOM TEXT')
        
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Resize to standard meme size
                    img = img.resize((800, 600), Image.Resampling.LANCZOS)
                    draw = ImageDraw.Draw(img)
                    
                    # Try to load a font, fallback to default
                    try:
                        font_size = 50
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add top text
                    if top_text:
                        bbox = draw.textbbox((0, 0), top_text, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        x = (img.width - text_width) // 2
                        y = 20
                        
                        # Add outline
                        for dx in [-2, -1, 0, 1, 2]:
                            for dy in [-2, -1, 0, 1, 2]:
                                if dx != 0 or dy != 0:
                                    draw.text((x + dx, y + dy), top_text, font=font, fill='black')
                        
                        # Add main text
                        draw.text((x, y), top_text, font=font, fill='white')
                    
                    # Add bottom text
                    if bottom_text:
                        bbox = draw.textbbox((0, 0), bottom_text, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        x = (img.width - text_width) // 2
                        y = img.height - text_height - 20
                        
                        # Add outline
                        for dx in [-2, -1, 0, 1, 2]:
                            for dy in [-2, -1, 0, 1, 2]:
                                if dx != 0 or dy != 0:
                                    draw.text((x + dx, y + dy), bottom_text, font=font, fill='black')
                        
                        # Add main text
                        draw.text((x, y), bottom_text, font=font, fill='white')
                    
                    # Save meme
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_meme.jpg")
                    img.save(output_path, 'JPEG', quality=95)
                    output_files.append(output_path)
                    
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error creating meme from {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_memes.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def add_watermark(self, data, task_id):
        """Add watermark to multiple images"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        watermark_text = data.get('watermark_text', 'WATERMARK')
        
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Create watermark
                    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    draw = ImageDraw.Draw(watermark)
                    
                    # Try to load font
                    try:
                        font_size = min(img.width, img.height) // 20
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # Position watermark
                    bbox = draw.textbbox((0, 0), watermark_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = img.width - text_width - 20
                    y = img.height - text_height - 20
                    
                    # Add watermark text with transparency
                    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
                    
                    # Composite watermark onto image
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    watermarked = Image.alpha_composite(img, watermark)
                    
                    # Convert back to RGB for JPEG
                    if watermarked.mode == 'RGBA':
                        rgb_img = Image.new('RGB', watermarked.size, (255, 255, 255))
                        rgb_img.paste(watermarked, mask=watermarked.split()[-1])
                        watermarked = rgb_img
                    
                    # Save watermarked image
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_watermarked.jpg")
                    watermarked.save(output_path, 'JPEG', quality=95)
                    output_files.append(output_path)
                    
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error adding watermark to {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_watermarked_images.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def generate_thumbnails(self, data, task_id):
        """Generate social media thumbnails"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        platform = data.get('platform', 'instagram')  # instagram, twitter, facebook, youtube
        
        # Platform dimensions
        dimensions = {
            'instagram': (1080, 1080),
            'twitter': (1200, 675),
            'facebook': (1200, 630),
            'youtube': (1280, 720)
        }
        
        size = dimensions.get(platform, (1080, 1080))
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Create thumbnail with proper aspect ratio
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                    
                    # Create background and center image
                    background = Image.new('RGB', size, (255, 255, 255))
                    x = (size[0] - img.width) // 2
                    y = (size[1] - img.height) // 2
                    background.paste(img, (x, y))
                    
                    # Save thumbnail
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_{platform}_thumbnail.jpg")
                    background.save(output_path, 'JPEG', quality=95)
                    output_files.append(output_path)
                    
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error creating thumbnail for {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_{platform}_thumbnails.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    def convert_format(self, data, task_id):
        """Convert images between different formats"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        target_format = data.get('format', 'JPEG').upper()
        
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                with Image.open(input_path) as img:
                    # Convert format
                    if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                        # Convert to RGB for JPEG
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.convert('RGBA').split()[-1] if img.mode == 'RGBA' else None)
                        img = rgb_img
                    
                    # Determine file extension
                    ext_map = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'GIF': '.gif'}
                    ext = ext_map.get(target_format, '.jpg')
                    
                    # Save converted image
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_converted{ext}")
                    
                    if target_format == 'JPEG':
                        img.save(output_path, target_format, quality=95)
                    else:
                        img.save(output_path, target_format)
                    
                    output_files.append(output_path)
                    
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP for output
        zip_path = os.path.join(self.output_dir, f"{task_id}_converted_to_{target_format.lower()}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)
        
        self.update_progress(task_id, 100)
        return {'output_path': zip_path, 'filename': os.path.basename(zip_path)}
    
    # Simplified implementations for remaining methods
    def create_collage(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_collage.jpg")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_colors(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_color_palette.txt")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def enhance_image(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_enhanced.jpg")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_caption(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_captions.txt")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_text(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_extracted_text.txt")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def create_gif(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_animated.gif")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def video_to_gif(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_video_to_gif.gif")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_meme_template(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_meme_template.jpg")
        # Simplified implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}