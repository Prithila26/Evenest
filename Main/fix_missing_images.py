#!/usr/bin/env python
"""Check for missing images and create them"""

import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Service, StoreItem
from PIL import Image, ImageDraw, ImageFont

def create_image_for_item(title, category, filename, width=800, height=600, price=None):
    """Create a professional placeholder image"""
    try:
        # Create image with gradient
        img = Image.new('RGB', (width, height), color=(30, 60, 114))
        draw = ImageDraw.Draw(img)
        
        # Add gradient
        for i in range(height):
            ratio = i / height
            r = int(30 + (42 - 30) * ratio)
            g = int(60 + (82 - 60) * ratio)
            b = int(114 + (152 - 114) * ratio)
            draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
        
        # Load font
        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_small = ImageFont.truetype("arial.ttf", 32)
        except:
            font_large = font_small = ImageFont.load_default()
        
        # Draw title
        y_pos = 150
        title_words = title.split()
        for i in range(0, len(title_words), 3):
            line = ' '.join(title_words[i:i+3])
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_pos), line, fill=(255, 255, 255), font=font_large)
            y_pos += 60
        
        # Draw category
        bbox = draw.textbbox((0, 0), category, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_pos + 40), category, fill=(200, 200, 200), font=font_small)
        
        # Draw price if provided
        if price:
            price_text = f"BDT {price}"
            bbox = draw.textbbox((0, 0), price_text, font=font_small)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_pos + 100), price_text, fill=(100, 200, 100), font=font_small)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img.save(filename)
        return True
    except Exception as e:
        print(f"Error creating {filename}: {e}")
        return False

print("\n" + "="*70)
print("CHECKING AND FIXING MISSING IMAGES")
print("="*70)

# Check services
print("\n📋 SERVICES")
print("-"*70)
services = Service.objects.all()
service_missing = 0
for service in services:
    if not service.image or not service.image.name:
        # Create image
        filename = f"media/services/{service.title.lower().replace(' ', '_').replace('&', 'and').replace('(', '').replace(')', '')}_service.jpg"
        if create_image_for_item(service.title, service.category.name, filename):
            # Update in DB
            rel_path = filename.replace('media/', '')
            service.image = rel_path
            service.save()
            print(f"✅ Created: {service.title}")
            service_missing += 1
        else:
            print(f"❌ Failed: {service.title}")
    else:
        path = f"media/{service.image.name}"
        if not os.path.exists(path):
            print(f"⚠️  Missing file: {service.title} -> {service.image.name}")
            service_missing += 1
        else:
            print(f"✓ OK: {service.title}")

# Check store items
print("\n📦 STORE ITEMS")
print("-"*70)
items = StoreItem.objects.all()
item_missing = 0
for item in items:
    if not item.image or not item.image.name:
        # Create image
        filename = f"media/store/{item.name.lower().replace(' ', '_').replace('&', 'and').replace('(', '').replace(')', '')}_product.jpg"
        if create_image_for_item(item.name, item.category.name, filename, price=item.price):
            # Update in DB
            rel_path = filename.replace('media/', '')
            item.image = rel_path
            item.save()
            print(f"✅ Created: {item.name}")
            item_missing += 1
        else:
            print(f"❌ Failed: {item.name}")
    else:
        path = f"media/{item.image.name}"
        if not os.path.exists(path):
            print(f"⚠️  Missing file: {item.name} -> {item.image.name}")
            item_missing += 1
        else:
            print(f"✓ OK: {item.name}")

print("\n" + "="*70)
print(f"✅ SUMMARY: {service_missing} services + {item_missing} items fixed")
print("="*70 + "\n")
