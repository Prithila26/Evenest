# Bangladesh Content Localization Guide

## Overview
EventNest has been successfully localized for Bangladesh with:
- ✅ All descriptions updated with Bangladesh context
- ✅ Pricing converted to Bangladesh Taka (BDT)
- ✅ References to major Bangladesh cities (Dhaka, Chittagong, Sylhet)
- ✅ Bengali traditions and ceremonies mentioned
- ✅ Placeholder images ready for replacement

---

## 📍 Localization Details

### Cities Referenced
- **Dhaka** - Capital city, primary event hub
- **Chittagong** - Second-largest city, coastal events
- **Sylhet** - Third major city, special events
- **Cox's Bazar** - Tourism and destination events

### Bengali Traditions Mentioned
- **Mehendi** - Pre-wedding celebration
- **Sangeet** - Music and singing ceremony
- **Shadi** - Wedding ceremony
- **Bengali Sweets** - Rasgulla, Sandesh, Kheer
- **Regional Cuisines** - Ilish (Hilsa fish), Biryani, curries

### Currency
- All prices converted to **Bangladesh Taka (BDT)**
- Typical conversions:
  - ৳ 900 ≈ $10 USD
  - ৳ 15,000 ≈ $180 USD (Starter Package)
  - ৳ 75,000 ≈ $900 USD (Luxury Package)

---

## 🖼️ Image Replacement Guide

### Service Images to Update (30 images)
Located in: `media/services/`

| Filename | Service | Description |
|----------|---------|-------------|
| event_planning_bd.jpg | Full Event Planning | Event planning setup, consultation, decoration |
| wedding_planning_bd.jpg | Wedding Planning | Traditional Bengali wedding ceremony |
| corporate_event_bd.jpg | Corporate Event | IT park, corporate gathering, team building |
| birthday_party_bd.jpg | Birthday Party | Colorful celebration, decorations, cake |
| coordination_bd.jpg | Day-Of Coordination | Event coordinator managing event |
| photography_bd.jpg | Professional Photography | Photographer with camera, events |
| videography_bd.jpg | Videography Services | Video camera, cinematography |
| drone_bd.jpg | Drone Photography | Aerial shots, drone over venue |
| catering_buffet_bd.jpg | Buffet Catering | Food spread, buffet table, Bangladeshi cuisine |
| catering_plated_bd.jpg | Plated Dinner | Elegant plated dishes, formal dining |
| cocktail_bd.jpg | Cocktail Party | Drinks, appetizers, party atmosphere |
| dessert_bd.jpg | Dessert & Cake Service | Bengali sweets, cakes, desserts |
| bar_service_bd.jpg | Bar Service | Professional bar setup, bartender |
| decoration_wedding_bd.jpg | Wedding Decoration | Elaborate decorations, flower arrangements |
| flowers_bd.jpg | Floral Arrangements | Fresh flowers, Bengal gardening |
| balloons_bd.jpg | Balloon Decoration | Balloon arches, colorful balloons |
| lighting_bd.jpg | Lighting Design | Ambient lights, LED setup, illumination |
| stage_backdrop_bd.jpg | Stage & Backdrop Setup | Stage design, photo backdrop, traditional motifs |
| dj_bd.jpg | DJ Service | DJ booth, mixing, entertainment |
| liveband_bd.jpg | Live Band | Musicians performing, traditional/modern music |
| mc_bd.jpg | MC/Host Services | Host announcing, engaging crowd |
| entertainment_bd.jpg | Entertainment Package | Dancers, performers, entertainment |
| photobooth_bd.jpg | Photo Booth | Photo booth with props, guests taking photos |
| transport_luxury_bd.jpg | Bride & Groom Transport | Luxury car, decorated vehicle, bride & groom |
| transport_guests_bd.jpg | Guest Transportation | Coach, shuttle, guests boarding |
| valet_bd.jpg | Parking Valet Service | Valet attendants, parking area |
| banquet_hall_bd.jpg | Banquet Hall Rental | Grand hall, seating arrangement, capacity |
| garden_venue_bd.jpg | Outdoor Garden Venue | Garden setting, outdoor setup, natural backdrop |
| rooftop_bd.jpg | Rooftop Venue | Rooftop view, Dhaka skyline, sunset |
| venue_setup_bd.jpg | Venue Decoration Setup | Transformation, before-after, setup process |

### Store Product Images to Update (21 images)
Located in: `media/store/`

| Filename | Product | Description |
|----------|---------|-------------|
| package_starter.jpg | Starter Event Package | Package contents display |
| package_premium.jpg | Premium Event Package | Luxury items, premium display |
| package_luxury.jpg | Luxury Event Package | Complete luxury package showcase |
| balloons.jpg | Balloon Arch Kit | Assembled balloon arch |
| lights.jpg | Fairy Light String | String lights arranged |
| flowers.jpg | Floral Garland | Flower garland display |
| centerpieces.jpg | Table Centerpiece Set | Table center decorations |
| backdrop.jpg | Backdrop Stand with Drapes | Assembled backdrop stand |
| speaker.jpg | Portable Bluetooth Speaker | Speaker product photo |
| projector.jpg | LED Projector | Projector on stand |
| microphone.jpg | Wireless Microphone Set | Microphone and receiver |
| lightshow.jpg | Party Light Show Equipment | Light system setup |
| favors_personalized.jpg | Personalized Party Favors | Custom favor items |
| gift_boxes.jpg | Luxury Gift Box Set | Elegant gift boxes |
| candles.jpg | Candle Favor Set | Scented candles |
| matchbooks.jpg | Custom Matchbooks | Printed matchbooks display |
| invitations.jpg | Invitation Card Pack | Cards and envelopes |
| napkins.jpg | Napkins & Tableware Set | Table settings display |
| plates_cups.jpg | Party Plates & Cups Combo | Disposable tableware |
| confetti.jpg | Confetti & Streamers Pack | Colorful confetti, streamers |
| wrapping_paper.jpg | Gift Wrapping Paper Pack | Paper rolls display |

---

## 📷 Image Sources Recommended

### For Bangladesh Event Photos
1. **Local Photographers**
   - Dhaka-based event photographers
   - Wedding photography studios
   - Portfolio photographers

2. **Stock Photo Sites with Bangladesh Content**
   - Unsplash (search: "Bangladesh events")
   - Pexels (search: "Asian events")
   - Pixabay (search: "celebration")
   - Shutterstock/Getty Images

3. **Local Content**
   - DhanmondiRentals.com
   - Local vendor photos
   - Community photographer networks

4. **Image Specifications**
   - **Resolution**: 1920x1080px minimum (Full HD)
   - **Format**: JPG or PNG
   - **File Size**: 200-500KB optimal
   - **Aspect Ratio**: 16:9 or 4:3
   - **Colors**: Vibrant, warm, inviting

---

## 🔧 How to Update Images

### Option 1: Manual Image Upload
```bash
# Replace placeholder with actual image
1. Find image in media/services/ or media/store/
2. Delete placeholder file
3. Replace with your Bangladesh-sourced image
4. Keep the exact filename
5. Clear browser cache to see updates
```

### Option 2: Batch Update Script
Create and run this script:
```python
from pathlib import Path
import shutil

# Copy your Bangladesh images to media folders
source_images = Path('path/to/your/images')
services_dest = Path('media/services')
store_dest = Path('media/store')

# Copy service images
for img in source_images.glob('*_bd.jpg'):
    shutil.copy(img, services_dest / img.name)

# Copy store images
for img in source_images.glob('*.jpg'):
    shutil.copy(img, store_dest / img.name)
```

### Option 3: Update Database
```python
# Update Service images
from core.models import Service
service = Service.objects.get(title='Full Event Planning')
service.image = 'services/your_new_image.jpg'
service.save()
```

---

## 📋 Updated Service Descriptions Sample

### Before
"Complete event planning and coordination services"

### After
"Complete event planning and coordination services across Dhaka, Chittagong, and Sylhet. Expert handling of traditional Bengali ceremonies, modern celebrations, and cultural events."

### Before
"Buffet setup for 50 people"

### After
"Authentic Bengali buffet catering featuring traditional Dhaka cuisine, regional specialties, and international options. Includes Ilish, Biryani, curries, and sweets from renowned Bangladesh caterers."

---

## 💰 Updated Pricing (BDT)

### Service Pricing
- Small Services: ৳600 - ৳3,000
- Medium Services: ৳3,600 - ৳9,000
- Premium Services: ৳12,000 - ৳75,000

### Product Pricing
- Basic Items: ৳900 - ৳2,400
- Standard Items: ৳3,000 - ৳6,000
- Premium Items: ৳9,000 - ৳75,000

---

## 🎯 Testing the Updates

### View Updated Content
1. **Services Page**: `/services/` - See Bengali descriptions
2. **Store Page**: `/store/` - See BDT prices
3. **Service Details**: Click any service to see full description
4. **Product Details**: Click any product to see price in BDT

### Database Verification
```bash
# Check services updated
python manage.py shell
from core.models import Service
service = Service.objects.first()
print(service.title)
print(service.description)  # Should mention Dhaka/Chittagong
```

---

## 📱 What Changed

### For Users
1. **Descriptions** now mention Bangladeshi cities and traditions
2. **Prices** displayed in Bangladeshi Taka (৳)
3. **Cultural References** to Bengali ceremonies and cuisines
4. **Placeholder Images** ready for authentic Bengali photos

### For Admin
1. All 61 services updated with Bangladesh context
2. All 42 products updated with BDT pricing
3. 51 image placeholders created and ready
4. Ready for production deployment in Bangladesh

---

## 🚀 Next Steps

1. **Collect Images** from Bangladesh photographers/vendors
2. **Replace Placeholders** with actual images
3. **Test Locally** to ensure images display correctly
4. **Deploy** to production server
5. **Monitor** site performance and user feedback

---

## 📞 Support

For image updates or content changes:
1. Check actual image dimensions and formats
2. Ensure filenames match exactly
3. Clear browser cache after updates
4. Restart Django server if needed
5. Test on mobile devices

---

## 📊 Content Statistics

| Item | Count | Status |
|------|-------|--------|
| Services | 61 | ✅ Updated |
| Service Images | 30 | 📋 Placeholder |
| Store Products | 42 | ✅ Updated |
| Product Images | 21 | 📋 Placeholder |
| Price Currency | BDT | ✅ Updated |
| Descriptions | 83 | ✅ Localized |

---

**Created**: December 10, 2025  
**Status**: Bangladesh localization complete  
**Next Phase**: Image replacement and production deployment  
**Repository**: https://github.com/Prohar04/EventNest
