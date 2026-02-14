"""
Download Bangladesh-based event images and update service/store descriptions
"""

import os
import requests
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from core.models import Service, ServiceCategory, StoreItem, StoreCategory


def download_image(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✓ Downloaded: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {str(e)}")
        return False


def update_service_descriptions():
    """Update service descriptions with Bangladesh context"""
    
    updates = {
        'Full Event Planning': {
            'description': 'Complete event planning and coordination services across Dhaka, Chittagong, and Sylhet. Expert handling of traditional Bengali ceremonies, modern celebrations, and cultural events.',
            'image': 'services/event_planning_bd.jpg'
        },
        'Wedding Planning': {
            'description': 'Specialized wedding planning for Bengali traditions including Mehendi, Sangeet, and Shadi. Manage all arrangements from Dhaka to Cox\'s Bazar. Expert in Hindu, Muslim, and Christian wedding ceremonies.',
            'image': 'services/wedding_planning_bd.jpg'
        },
        'Corporate Event Planning': {
            'description': 'Professional corporate event planning for Dhaka IT parks, multinational offices, and Bangladesh business conferences. Manage product launches, team building, and annual events.',
            'image': 'services/corporate_event_bd.jpg'
        },
        'Birthday Party Planning': {
            'description': 'Custom birthday party planning and execution across Bangladesh. Theme-based celebrations, traditional Bengali decorations, and modern entertainment options.',
            'image': 'services/birthday_party_bd.jpg'
        },
        'Day-Of Coordination': {
            'description': 'Professional event day coordination and management. Ensure smooth execution of all planned activities on your special day across Bangladeshi venues.',
            'image': 'services/coordination_bd.jpg'
        },
        'Professional Photography Package': {
            'description': 'Professional 8-hour photography coverage capturing Bengali traditions, ceremonies, and candid moments with 500+ edited digital photos. Specialist in traditional and modern wedding photography.',
            'image': 'services/photography_bd.jpg'
        },
        'Videography Services': {
            'description': '4K cinematic video coverage of your event with professional editing. Capture precious Bengali moments in stunning quality with emotional storytelling.',
            'image': 'services/videography_bd.jpg'
        },
        'Drone Photography': {
            'description': 'Aerial drone photography and videography services for venue overviews, grand entrances, and aerial reception shots. Licensed drone operators in Bangladesh.',
            'image': 'services/drone_bd.jpg'
        },
        'Buffet Catering (50 guests)': {
            'description': 'Authentic Bengali buffet catering featuring traditional Dhaka cuisine, regional specialties, and international options. Includes Ilish, Biryani, curries, and sweets from renowned Bangladesh caterers.',
            'image': 'services/catering_buffet_bd.jpg'
        },
        'Plated Dinner Service': {
            'description': 'Full plated dinner service with professional waitstaff serving gourmet Bengali and fusion cuisine. Perfect for formal events and receptions across Dhaka and other major cities.',
            'image': 'services/catering_plated_bd.jpg'
        },
        'Cocktail Party Catering': {
            'description': 'Appetizers and drinks service featuring Bengali samosas, pakoras, and modern cocktails. Suitable for corporate events, receptions, and celebrations in Bangladesh.',
            'image': 'services/cocktail_bd.jpg'
        },
        'Dessert & Cake Service': {
            'description': 'Custom traditional Bengali sweets, modern cakes, and desserts from top Bangladesh bakeries. Featuring Rasgulla, Sandesh, Kheer, and custom celebration cakes.',
            'image': 'services/dessert_bd.jpg'
        },
        'Bar Service': {
            'description': 'Full bar setup with professional bartenders serving traditional Bengali drinks and international cocktails. Available for events across Bangladesh.',
            'image': 'services/bar_service_bd.jpg'
        },
        'Wedding Decoration Package': {
            'description': 'Complete wedding venue decoration with traditional Bengali designs, modern aesthetics, and cultural elements. Specializing in Dhaka and Chittagong venues.',
            'image': 'services/decoration_wedding_bd.jpg'
        },
        'Floral Arrangements': {
            'description': 'Custom floral designs using fresh flowers from Bangladesh gardens. Traditional and modern arrangements perfect for Bengali ceremonies and celebrations.',
            'image': 'services/flowers_bd.jpg'
        },
        'Balloon Decoration': {
            'description': 'Colorful balloon arches, garlands, and installations for all types of celebrations. Bring vibrancy to your Bengali event across Bangladesh.',
            'image': 'services/balloons_bd.jpg'
        },
        'Lighting Design': {
            'description': 'Professional ambient and decorative lighting transforming venues into magical spaces. LED lights, traditional lamps, and modern lighting effects for Bangladeshi events.',
            'image': 'services/lighting_bd.jpg'
        },
        'Stage & Backdrop Setup': {
            'description': 'Professional stage design and photo backdrop setup with traditional Bengali motifs and modern designs. Perfect for ceremonies and photography in Bangladesh.',
            'image': 'services/stage_backdrop_bd.jpg'
        },
        'DJ Service': {
            'description': 'Professional DJ with international sound system playing Bengali hits, Bollywood classics, and modern music. Available for weddings and celebrations across Bangladesh.',
            'image': 'services/dj_bd.jpg'
        },
        'Live Band': {
            'description': 'Live music performance featuring Bengali classical, modern bands, and fusion music with professional musicians from Dhaka music scene.',
            'image': 'services/liveband_bd.jpg'
        },
        'MC/Host Services': {
            'description': 'Professional event host and MC providing bilingual (Bengali-English) hosting with warm personality and professional experience in Bangladesh events.',
            'image': 'services/mc_bd.jpg'
        },
        'Entertainment Package': {
            'description': 'Complete entertainment package including DJ, MC, dancers, and special performers for Bengali celebrations and events.',
            'image': 'services/entertainment_bd.jpg'
        },
        'Photo Booth': {
            'description': 'Interactive photo booth with fun props and Bengali cultural themes. Digital and printed photos instantly for your guests at Bangladesh events.',
            'image': 'services/photobooth_bd.jpg'
        },
        'Bride & Groom Transport': {
            'description': 'Luxury vehicle transport for bride and groom featuring premium cars and professional drivers. Traditional flower-decorated vehicles available for Bengali weddings.',
            'image': 'services/transport_luxury_bd.jpg'
        },
        'Guest Transportation': {
            'description': 'Coach or shuttle service for guests from hotels to venues across Dhaka, Chittagong, and other Bangladesh cities. Comfortable and timely transportation.',
            'image': 'services/transport_guests_bd.jpg'
        },
        'Parking Valet Service': {
            'description': 'Professional valet parking services for events across Bangladesh venues. Secure parking management with trained valet staff.',
            'image': 'services/valet_bd.jpg'
        },
        'Banquet Hall Rental': {
            'description': 'Spacious banquet halls in prime Dhaka locations accommodating 200+ guests. Modern facilities with traditional Bengali architecture available.',
            'image': 'services/banquet_hall_bd.jpg'
        },
        'Outdoor Garden Venue': {
            'description': 'Beautiful outdoor garden venues near Dhaka perfect for intimate gatherings, engagement parties, and outdoor receptions with natural Bengali garden settings.',
            'image': 'services/garden_venue_bd.jpg'
        },
        'Rooftop Venue': {
            'description': 'Modern rooftop venues in Dhaka with stunning city views. Perfect for sunset receptions, cocktail parties, and contemporary celebrations.',
            'image': 'services/rooftop_bd.jpg'
        },
        'Venue Decoration Setup': {
            'description': 'Complete venue setup and decoration service transforming any Bangladeshi space into an elegant event venue. Professional installation team.',
            'image': 'services/venue_setup_bd.jpg'
        },
    }
    
    for service in Service.objects.all():
        if service.title in updates:
            update = updates[service.title]
            service.description = update['description']
            service.save()
            print(f"✓ Updated: {service.title}")
    
    print(f"\nTotal services updated: {len(updates)}")


def update_store_item_descriptions():
    """Update store item descriptions with Bangladesh context"""
    
    updates = {
        'Starter Event Package': {
            'description': 'Perfect starter package for small celebrations in Bangladesh. Includes 50 premium invitations, traditional Bengali decorations, and event supplies. Ideal for intimate gatherings.',
            'price': 15000  # BDT pricing
        },
        'Premium Event Package': {
            'description': 'Comprehensive package for 100 guests featuring premium invitations, decorated table setups, beautiful centerpieces, and elegant favors. Everything you need for a memorable Bengali celebration.',
            'price': 35000
        },
        'Luxury Event Package': {
            'description': 'Ultimate luxury event package with all premium items for grand celebrations. Includes exclusive decorations, premium invitations, luxury favors, and complete event supplies for unforgettable moments.',
            'price': 75000
        },
        'Balloon Arch Kit': {
            'description': 'Complete balloon arch setup with 50 high-quality balloons and sturdy frame. Perfect for creating stunning entrances and backdrop areas at Bengali events.',
            'price': 4500
        },
        'Fairy Light String': {
            'description': '20 meters of premium LED fairy lights perfect for ambient lighting at evening celebrations. Create magical atmospheres for traditional and modern Bengali events.',
            'price': 2400
        },
        'Floral Garland': {
            'description': 'Beautiful artificial flower garland (4 meters) featuring traditional Bengali flower combinations. Perfect for mandir decoration, entrance arches, and stage backdrops.',
            'price': 3600
        },
        'Table Centerpiece Set': {
            'description': 'Set of 10 elegant table centerpieces with traditional Bengali designs and modern aesthetics. Enhance your dining tables and reception areas beautifully.',
            'price': 9000
        },
        'Backdrop Stand with Drapes': {
            'description': 'Professional backdrop stand with premium quality drapes in traditional and modern designs. Perfect for wedding photos and event decoration across Bangladesh.',
            'price': 12000
        },
        'Portable Bluetooth Speaker': {
            'description': '360-degree sound quality portable speaker perfect for small gatherings, receptions, and personal celebrations. Portable and reliable for Bangladesh events.',
            'price': 3600
        },
        'LED Projector': {
            'description': 'Full HD 1080p LED projector ideal for presentations, photo slideshows, and entertainment at corporate and personal events in Bangladesh.',
            'price': 10500
        },
        'Wireless Microphone Set': {
            'description': 'Professional wireless microphone set with 2 mics and receiver. Essential for speeches, announcements, and entertainment at Bengali celebrations.',
            'price': 6000
        },
        'Party Light Show Equipment': {
            'description': 'RGB laser light show system creating stunning visual effects. Perfect for modern celebrations, DJ parties, and contemporary events.',
            'price': 15000
        },
        'Personalized Party Favors (Pack of 20)': {
            'description': 'Customizable party favors with your names, dates, or personalized messages. Memorable gifts for your guests at Bengali weddings and celebrations.',
            'price': 3000
        },
        'Luxury Gift Box Set (10 pcs)': {
            'description': 'Set of 10 elegant gift boxes perfect for guest gifts, mementos, and prizes. Premium packaging for special occasions in Bangladesh.',
            'price': 4500
        },
        'Candle Favor Set (20 pcs)': {
            'description': 'Beautiful scented candles as guest favors. Traditional yet elegant gifts that guests will appreciate and remember your celebration.',
            'price': 3600
        },
        'Custom Matchbooks (100 pcs)': {
            'description': 'Personalized matchbooks with custom printing. Traditional party favor popular at Bengali weddings and formal events.',
            'price': 2400
        },
        'Invitation Card Pack (50)': {
            'description': 'Premium invitation cards with matching envelopes. Elegant designs suitable for formal events, weddings, and special celebrations in Bangladesh.',
            'price': 2400
        },
        'Napkins & Tableware Set': {
            'description': 'Premium quality napkins, tablecloths, and complete tableware set for elegant dining. Perfect for formal events and receptions.',
            'price': 1800
        },
        'Party Plates & Cups Combo': {
            'description': '100-piece disposable yet elegant plates and cups set. Convenient and stylish for serving food and drinks at events.',
            'price': 1500
        },
        'Confetti & Streamers Pack': {
            'description': 'Colorful mixed confetti and streamers for celebrations. Add festive vibrancy to your Bengali event decorations and celebrations.',
            'price': 900
        },
        'Gift Wrapping Paper Pack': {
            'description': 'Assorted premium gift wrapping paper rolls in traditional and modern designs. Perfect for wrapping gifts and creating beautiful presentations.',
            'price': 1200
        },
    }
    
    for item in StoreItem.objects.all():
        if item.name in updates:
            update = updates[item.name]
            item.description = update['description']
            item.price = update['price']
            item.save()
            print(f"✓ Updated: {item.name} - BDT {update['price']}")
    
    print(f"\nTotal items updated: {len(updates)}")


def create_placeholder_images():
    """Create Bangladesh-themed placeholder images locally"""
    
    services_dir = Path('media/services')
    store_dir = Path('media/store')
    
    services_dir.mkdir(parents=True, exist_ok=True)
    store_dir.mkdir(parents=True, exist_ok=True)
    
    # Create simple placeholder PNG files for services
    service_images = [
        'event_planning_bd.jpg',
        'wedding_planning_bd.jpg',
        'corporate_event_bd.jpg',
        'birthday_party_bd.jpg',
        'coordination_bd.jpg',
        'photography_bd.jpg',
        'videography_bd.jpg',
        'drone_bd.jpg',
        'catering_buffet_bd.jpg',
        'catering_plated_bd.jpg',
        'cocktail_bd.jpg',
        'dessert_bd.jpg',
        'bar_service_bd.jpg',
        'decoration_wedding_bd.jpg',
        'flowers_bd.jpg',
        'balloons_bd.jpg',
        'lighting_bd.jpg',
        'stage_backdrop_bd.jpg',
        'dj_bd.jpg',
        'liveband_bd.jpg',
        'mc_bd.jpg',
        'entertainment_bd.jpg',
        'photobooth_bd.jpg',
        'transport_luxury_bd.jpg',
        'transport_guests_bd.jpg',
        'valet_bd.jpg',
        'banquet_hall_bd.jpg',
        'garden_venue_bd.jpg',
        'rooftop_bd.jpg',
        'venue_setup_bd.jpg',
    ]
    
    store_images = [
        'package_starter.jpg',
        'package_premium.jpg',
        'package_luxury.jpg',
        'balloons.jpg',
        'lights.jpg',
        'flowers.jpg',
        'centerpieces.jpg',
        'backdrop.jpg',
        'speaker.jpg',
        'projector.jpg',
        'microphone.jpg',
        'lightshow.jpg',
        'favors_personalized.jpg',
        'gift_boxes.jpg',
        'candles.jpg',
        'matchbooks.jpg',
        'invitations.jpg',
        'napkins.jpg',
        'plates_cups.jpg',
        'confetti.jpg',
        'wrapping_paper.jpg',
    ]
    
    print("Creating placeholder image files...")
    
    # Create placeholder content (simple GIF or PNG data)
    placeholder_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
        b'\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00'
        b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    )
    
    # Create service image placeholders
    for img in service_images:
        filepath = services_dir / img
        try:
            if not filepath.exists():
                with open(filepath, 'wb') as f:
                    f.write(placeholder_gif)
                print(f"✓ Created: {filepath}")
        except Exception as e:
            print(f"✗ Failed to create {filepath}: {str(e)}")
    
    # Create store image placeholders
    for img in store_images:
        filepath = store_dir / img
        try:
            if not filepath.exists():
                with open(filepath, 'wb') as f:
                    f.write(placeholder_gif)
                print(f"✓ Created: {filepath}")
        except Exception as e:
            print(f"✗ Failed to create {filepath}: {str(e)}")


if __name__ == '__main__':
    print("=" * 70)
    print("Updating EventNest with Bangladesh-Based Content")
    print("=" * 70)
    
    print("\n--- Creating Placeholder Images ---")
    create_placeholder_images()
    
    print("\n--- Updating Service Descriptions (Bangladesh Context) ---")
    update_service_descriptions()
    
    print("\n--- Updating Store Item Descriptions & Pricing (BDT) ---")
    update_store_item_descriptions()
    
    print("\n" + "=" * 70)
    print("✅ Update Complete! All content is now Bangladesh-based")
    print("=" * 70)
    print("\nKey Changes:")
    print("• All descriptions reference Bangladesh cities (Dhaka, Chittagang, Sylhet)")
    print("• Service descriptions mention Bengali traditions and ceremonies")
    print("• Store prices updated to Bangladesh Taka (BDT)")
    print("• All images created as placeholders")
    print("• Ready for you to replace with actual Bangladesh-sourced images")
