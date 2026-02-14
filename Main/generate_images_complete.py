#!/usr/bin/env python
"""
Complete Image Generation and Page Testing Script
Generates images for all services and products that match their descriptions
"""

import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from core.models import Service, StoreItem, UserProfile, Cart

def create_placeholder_image(text, filename, width=800, height=600):
    """Create a beautiful placeholder image with text"""
    try:
        # Create image with gradient
        img = Image.new('RGB', (width, height), color=(30, 60, 114))
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect with colored rectangles
        for i in range(height):
            ratio = i / height
            r = int(30 + (42 - 30) * ratio)
            g = int(60 + (82 - 60) * ratio)
            b = int(114 + (152 - 114) * ratio)
            draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
        
        # Try to use a nice font, fallback to default
        try:
            font_size = 40
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(current_line) > 4:  # Max 4 words per line
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text
        y = (height - len(lines) * 50) // 2
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += 50
        
        # Save image
        img.save(filename)
        return True
    except Exception as e:
        print(f"Error creating image {filename}: {e}")
        return False

def generate_service_images():
    """Generate images for all services"""
    print("\n📸 Generating Service Images")
    print("-" * 60)
    
    media_path = Path('media/services')
    media_path.mkdir(parents=True, exist_ok=True)
    
    services = Service.objects.all()
    created_count = 0
    
    for service in services:
        if not service.image or not service.image.name:
            # Create a descriptive filename
            filename = media_path / f"{service.title.lower().replace(' ', '_')}_service.jpg"
            
            # Create image with service title and category
            text = f"{service.title}\n{service.category.name}"
            
            if create_placeholder_image(text, str(filename)):
                # Update service with image
                relative_path = f"services/{filename.name}"
                service.image = relative_path
                service.save()
                created_count += 1
                print(f"✓ Created: {service.title}")
    
    return created_count

def generate_store_images():
    """Generate images for all store items"""
    print("\n📦 Generating Store Product Images")
    print("-" * 60)
    
    media_path = Path('media/store')
    media_path.mkdir(parents=True, exist_ok=True)
    
    items = StoreItem.objects.all()
    created_count = 0
    
    for item in items:
        if not item.image or not item.image.name:
            # Create a descriptive filename
            filename = media_path / f"{item.name.lower().replace(' ', '_')}_product.jpg"
            
            # Create image with item name and category
            text = f"{item.name}\n{item.category.name}\nBDT {item.price}"
            
            if create_placeholder_image(text, str(filename)):
                # Update item with image
                relative_path = f"store/{filename.name}"
                item.image = relative_path
                item.save()
                created_count += 1
                print(f"✓ Created: {item.name}")
    
    return created_count

def create_test_user():
    """Create a test user for testing"""
    print("\n👤 Creating Test User")
    print("-" * 60)
    
    username = 'testuser'
    if User.objects.filter(username=username).exists():
        print(f"✓ Test user '{username}' already exists")
        return User.objects.get(username=username)
    
    user = User.objects.create_user(
        username=username,
        email='test@example.com',
        password='TestPassword123!'
    )
    
    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': 'Test User',
            'phone': '+8801700000000',
            'address': 'Dhaka, Bangladesh'
        }
    )
    
    Cart.objects.get_or_create(user=user)
    
    print(f"✓ Test user created: {username}")
    return user

def main():
    print("\n" + "="*60)
    print("EventNest - Complete Image & Page Setup")
    print("="*60)
    
    # Generate images
    service_images = generate_service_images()
    store_images = generate_store_images()
    
    # Create test user
    test_user = create_test_user()
    
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  • Service images created/updated: {service_images}")
    print(f"  • Store product images created/updated: {store_images}")
    print(f"  • Test user: testuser / TestPassword123!")
    print(f"\n🌐 Access the platform at: http://127.0.0.1:8000/")
    print(f"\n📝 Pages to test:")
    print(f"  1. http://127.0.0.1:8000/login/ - Login page")
    print(f"  2. http://127.0.0.1:8000/signup/ - Signup page")
    print(f"  3. http://127.0.0.1:8000/services/ - Services listing")
    print(f"  4. http://127.0.0.1:8000/store/ - Store listing")
    print(f"  5. http://127.0.0.1:8000/services/1/ - Service detail")
    print(f"  6. http://127.0.0.1:8000/store/1/ - Product detail")
    print(f"  7. http://127.0.0.1:8000/cart/ - Shopping cart")
    print(f"  8. http://127.0.0.1:8000/profile/ - User profile")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
