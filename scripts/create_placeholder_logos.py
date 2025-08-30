#!/usr/bin/env python3
"""
Create Placeholder Logos for Missing Brands
==========================================
Creates simple colored PNG placeholders for brands we couldn't download
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_logo(text, filename, bg_color, text_color, size=(100, 100)):
    """Create a simple placeholder logo with brand initials"""
    try:
        # Create image
        img = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a built-in font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 24)
            except:
                font = ImageFont.load_default()
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Save
        output_path = f"../images/{filename}"
        img.save(output_path)
        print(f"  ✅ Created {filename}")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to create {filename}: {str(e)}")
        return False

def main():
    print("🎨 Creating Placeholder Brand Logos")
    print("=" * 40)
    
    # Brand configurations with colors - only create missing ones
    placeholders = {
        "chozen-noodle.png": {"text": "CN", "bg": "#FF6B35", "fg": "white"},
        "coco-di-mama.png": {"text": "CDM", "bg": "#8B4513", "fg": "white"},
        "fresh-food-cafe.png": {"text": "FFC", "bg": "#228B22", "fg": "white"},
        "costa-drive-thru.png": {"text": "CDT", "bg": "#D4AF37", "fg": "white"},
        "spar.png": {"text": "SP", "bg": "#FF0000", "fg": "white"}
    }
    
    success_count = 0
    for filename, config in placeholders.items():
        if create_placeholder_logo(
            config["text"], 
            filename, 
            config["bg"], 
            config["fg"]
        ):
            success_count += 1
    
    print()
    print("=" * 40)
    print(f"🎉 Created {success_count}/{len(placeholders)} placeholder logos")
    print("📁 Saved to ../images/")

if __name__ == "__main__":
    main()