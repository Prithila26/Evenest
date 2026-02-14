"""
Populate EventNest database with sample services and store items
Run with: python manage.py shell < populate_data.py
Or: python populate_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from core.models import (
    ServiceCategory, Service, StoreCategory, StoreItem
)
from django.utils import timezone


def populate_services():
    """Add sample services to database"""
    
    # Create service categories
    categories_data = [
        ('Events', 'Event planning and management'),
        ('Photography', 'Professional photography services'),
        ('Catering', 'Food and beverage services'),
        ('Decorations', 'Venue decoration and styling'),
        ('Entertainment', 'Entertainment and performers'),
        ('Transportation', 'Transportation and logistics'),
        ('Venue', 'Venue rental and setup'),
    ]
    
    categories = {}
    for name, desc in categories_data:
        cat, created = ServiceCategory.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        categories[name] = cat
        print(f"{'Created' if created else 'Found'} category: {name}")
    
    # Create services
    services_data = [
        # Events
        ('Events', [
            {'title': 'Full Event Planning', 'description': 'Complete event planning and coordination services', 'price': 5000.00},
            {'title': 'Day-Of Coordination', 'description': 'Professional coordinator for your event day', 'price': 1500.00},
            {'title': 'Wedding Planning', 'description': 'Specialized wedding planning services', 'price': 8000.00},
            {'title': 'Corporate Event Planning', 'description': 'Professional corporate event planning', 'price': 3500.00},
            {'title': 'Birthday Party Planning', 'description': 'Custom birthday party planning and execution', 'price': 1200.00},
        ]),
        # Photography
        ('Photography', [
            {'title': 'Professional Photography Package', 'description': '8-hour photography coverage with 500+ edited photos', 'price': 2500.00},
            {'title': 'Videography Services', 'description': '4K video coverage with professional editing', 'price': 3500.00},
            {'title': 'Drone Photography', 'description': 'Aerial photography and videography services', 'price': 1500.00},
            {'title': 'Pre-Event Photo Session', 'description': 'Pre-wedding or engagement photoshoot', 'price': 800.00},
            {'title': 'Photo Album & Printing', 'description': 'Professional album design and printing', 'price': 600.00},
        ]),
        # Catering
        ('Catering', [
            {'title': 'Buffet Catering (50 guests)', 'description': 'Complete buffet setup for 50 people', 'price': 2500.00},
            {'title': 'Plated Dinner Service', 'description': 'Full plated dinner service with staff', 'price': 4500.00},
            {'title': 'Cocktail Party Catering', 'description': 'Appetizers and drinks for cocktail party', 'price': 1800.00},
            {'title': 'Dessert & Cake Service', 'description': 'Custom desserts and cake service', 'price': 800.00},
            {'title': 'Bar Service', 'description': 'Full bar setup with bartender', 'price': 1200.00},
        ]),
        # Decorations
        ('Decorations', [
            {'title': 'Wedding Decoration Package', 'description': 'Complete wedding venue decoration', 'price': 3000.00},
            {'title': 'Floral Arrangements', 'description': 'Custom floral designs and arrangements', 'price': 1500.00},
            {'title': 'Balloon Decoration', 'description': 'Balloon arches, garlands, and installations', 'price': 800.00},
            {'title': 'Lighting Design', 'description': 'Professional ambient and decorative lighting', 'price': 2000.00},
            {'title': 'Stage & Backdrop Setup', 'description': 'Professional stage and photo backdrop setup', 'price': 1200.00},
        ]),
        # Entertainment
        ('Entertainment', [
            {'title': 'DJ Service', 'description': 'Professional DJ with sound system', 'price': 1500.00},
            {'title': 'Live Band', 'description': 'Live music performance with 4-piece band', 'price': 3500.00},
            {'title': 'MC/Host Services', 'description': 'Professional event host and MC', 'price': 800.00},
            {'title': 'Entertainment Package', 'description': 'DJ, MC, and special entertainment', 'price': 2500.00},
            {'title': 'Photo Booth', 'description': 'Interactive photo booth with props', 'price': 600.00},
        ]),
        # Transportation
        ('Transportation', [
            {'title': 'Bride & Groom Transport', 'description': 'Luxury car for bride and groom', 'price': 800.00},
            {'title': 'Guest Transportation', 'description': 'Coach or shuttle service for guests', 'price': 1500.00},
            {'title': 'Parking Valet Service', 'description': 'Professional valet parking services', 'price': 600.00},
        ]),
        # Venue
        ('Venue', [
            {'title': 'Banquet Hall Rental', 'description': 'Spacious banquet hall for 200+ guests', 'price': 5000.00},
            {'title': 'Outdoor Garden Venue', 'description': 'Beautiful outdoor garden setup', 'price': 3000.00},
            {'title': 'Rooftop Venue', 'description': 'Modern rooftop venue with city views', 'price': 4000.00},
            {'title': 'Venue Decoration Setup', 'description': 'Complete venue setup and decoration', 'price': 2500.00},
        ]),
    ]
    
    for category_name, services_list in services_data:
        category = categories.get(category_name)
        if not category:
            continue
        
        for service_info in services_list:
            service, created = Service.objects.get_or_create(
                title=service_info['title'],
                defaults={
                    'category': category,
                    'description': service_info['description'],
                    'price': service_info['price'],
                }
            )
            print(f"{'Created' if created else 'Found'} service: {service.title}")
    
    print(f"\nTotal services: {Service.objects.count()}")


def populate_store_items():
    """Add sample store items to database"""
    
    # Create store categories
    categories_data = [
        ('Packages', 'Event packages and bundles'),
        ('Decorations', 'Decoration items and supplies'),
        ('Electronics', 'Audio and visual equipment'),
        ('Favors', 'Party favors and gifts'),
        ('Supplies', 'Event supplies'),
    ]
    
    categories = {}
    for name, desc in categories_data:
        cat, created = StoreCategory.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        categories[name] = cat
        print(f"{'Created' if created else 'Found'} category: {name}")
    
    # Create store items
    items_data = [
        # Packages
        ('Packages', [
            {
                'title': 'Starter Event Package',
                'description': 'Includes 50 invitations, decorations, and supplies',
                'price': 500.00,
                'stock': 50,
            },
            {
                'title': 'Premium Event Package',
                'description': 'Complete package with decorations, invitations, and favors for 100 guests',
                'price': 1200.00,
                'stock': 30,
            },
            {
                'title': 'Luxury Event Package',
                'description': 'Full event package with premium decorations and supplies',
                'price': 2500.00,
                'stock': 20,
            },
        ]),
        # Decorations
        ('Decorations', [
            {
                'title': 'Balloon Arch Kit',
                'description': '50 balloons with arch frame and decorations',
                'price': 150.00,
                'stock': 100,
            },
            {
                'title': 'Fairy Light String',
                'description': '20 meters LED fairy lights for decorations',
                'price': 80.00,
                'stock': 150,
            },
            {
                'title': 'Floral Garland',
                'description': 'Artificial flower garland for venue decoration',
                'price': 120.00,
                'stock': 75,
            },
            {
                'title': 'Table Centerpiece Set',
                'description': 'Set of 10 elegant table centerpieces',
                'price': 300.00,
                'stock': 50,
            },
            {
                'title': 'Backdrop Stand with Drapes',
                'description': 'Professional backdrop stand with premium drapes',
                'price': 400.00,
                'stock': 30,
            },
        ]),
        # Electronics
        ('Electronics', [
            {
                'title': 'Portable Bluetooth Speaker',
                'description': '360-degree sound quality portable speaker',
                'price': 120.00,
                'stock': 80,
            },
            {
                'title': 'LED Projector',
                'description': '1080p LED projector for presentations',
                'price': 350.00,
                'stock': 25,
            },
            {
                'title': 'Wireless Microphone Set',
                'description': 'Set of 2 wireless microphones with receiver',
                'price': 200.00,
                'stock': 40,
            },
            {
                'title': 'Party Light Show Equipment',
                'description': 'RGB laser light show system',
                'price': 500.00,
                'stock': 15,
            },
        ]),
        # Favors
        ('Favors', [
            {
                'title': 'Personalized Party Favors (Pack of 20)',
                'description': 'Customizable party favors for guests',
                'price': 100.00,
                'stock': 200,
            },
            {
                'title': 'Luxury Gift Box Set (10 pcs)',
                'description': 'Elegant gift boxes with packaging',
                'price': 150.00,
                'stock': 100,
            },
            {
                'title': 'Candle Favor Set (20 pcs)',
                'description': 'Scented candles as guest favors',
                'price': 120.00,
                'stock': 80,
            },
            {
                'title': 'Custom Matchbooks (100 pcs)',
                'description': 'Custom printed matchbooks',
                'price': 80.00,
                'stock': 120,
            },
        ]),
        # Supplies
        ('Supplies', [
            {
                'title': 'Invitation Card Pack (50)',
                'description': 'Premium invitation cards with envelopes',
                'price': 80.00,
                'stock': 200,
            },
            {
                'title': 'Napkins & Tableware Set',
                'description': 'Complete set of premium napkins and utensils',
                'price': 60.00,
                'stock': 150,
            },
            {
                'title': 'Party Plates & Cups Combo',
                'description': '100-piece set of disposable plates and cups',
                'price': 50.00,
                'stock': 250,
            },
            {
                'title': 'Confetti & Streamers Pack',
                'description': 'Mixed confetti and streamers for decorations',
                'price': 30.00,
                'stock': 300,
            },
            {
                'title': 'Gift Wrapping Paper Pack',
                'description': 'Assorted gift wrapping paper rolls',
                'price': 40.00,
                'stock': 200,
            },
        ]),
    ]
    
    for category_name, items_list in items_data:
        category = categories.get(category_name)
        if not category:
            continue
        
        for item_info in items_list:
            item, created = StoreItem.objects.get_or_create(
                name=item_info['title'],
                defaults={
                    'category': category,
                    'description': item_info['description'],
                    'price': item_info['price'],
                    'stock': item_info['stock'],
                }
            )
            print(f"{'Created' if created else 'Found'} item: {item.name}")
    
    print(f"\nTotal store items: {StoreItem.objects.count()}")


if __name__ == '__main__':
    print("=" * 60)
    print("Populating EventNest Database")
    print("=" * 60)
    
    print("\n--- Adding Services ---")
    populate_services()
    
    print("\n--- Adding Store Items ---")
    populate_store_items()
    
    print("\n" + "=" * 60)
    print("Database population complete!")
    print("=" * 60)
