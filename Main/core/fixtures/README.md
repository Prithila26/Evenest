# EventNest Seed Data Documentation

## Project Overview
EventNest is an event-management marketplace platform connecting event managers, rental stores, photography agencies, card printers, and caterers with customers. The platform also features a store for event supplies with cart, wishlist, and order functionality.

---

## 1. IDENTIFIED PRODUCT/SERVICE MODELS

Based on analysis of `/core/models.py`, the following models manage products and services:

### A. Service-Related Models (For vendors/professionals)

#### 1. **ServiceCategory** (Generic Services)
- **Fields**: `name`, `description`
- **Purpose**: Category grouping for generic services
- **Usage**: Top-level categorization for Service model

#### 2. **Service** (Generic Service Listings)
- **Fields**:
  - `category` (FK to ServiceCategory)
  - `title` (str, max 200 chars)
  - `description` (text)
  - `price` (decimal, 10 digits, 2 decimal places)
  - `image` (ImageField, uploads to `services/`)
  - `created_at`, `updated_at` (auto timestamps)
- **Purpose**: Generic service listing for miscellaneous vendor services
- **Usage**: General event services not covered by specialized models

#### 3. **EventManagement**
- **Fields**:
  - `title`, `description`, `price`, `image`
  - `event_type` (str: wedding, corporate, birthday, etc.)
  - `capacity` (int: max guests)
  - `duration` (int: hours)
  - `includes_decoration` (bool)
  - `includes_catering` (bool)
  - `created_at`, `updated_at`
- **Purpose**: Event planning and coordination packages
- **Usage**: Professional event management services

#### 4. **Photography**
- **Fields**:
  - `title`, `description`, `price`, `image`
  - `shoot_type` (str: wedding, portrait, event, etc.)
  - `duration` (int: hours)
  - `includes_editing` (bool, default True)
  - `number_of_photos` (int: minimum delivered)
  - `includes_prints` (bool)
  - `created_at`, `updated_at`
- **Purpose**: Photography and videography services
- **Usage**: Professional photography packages

#### 5. **Catering**
- **Fields**:
  - `title`, `description`, `price` (per person), `image`
  - `cuisine_type` (str: Bengali, Chinese, Continental, etc.)
  - `min_order_quantity` (int: minimum persons)
  - `includes_serving_staff` (bool)
  - `includes_setup` (bool)
  - `created_at`, `updated_at`
- **Purpose**: Catering and food services
- **Usage**: Food and beverage offerings

#### 6. **PrintingService**
- **Fields**:
  - `title`, `description`, `price` (per piece), `image`
  - `print_type` (str: invitation, business card, banner, etc.)
  - `paper_type` (str: matte, glossy, premium, etc.)
  - `min_order_quantity` (int)
  - `includes_design` (bool)
  - `delivery_time` (int: days)
  - `created_at`, `updated_at`
- **Purpose**: Printing and card design services
- **Usage**: Custom printing for events

### B. Store/Product Models (For retail items)

#### 7. **StoreCategory**
- **Fields**: `name`, `description`
- **Purpose**: Category grouping for store items
- **Usage**: Organize retail products

#### 8. **StoreItem** (Purchasable Retail Products)
- **Fields**:
  - `category` (FK to StoreCategory)
  - `name` (str, max 200 chars)
  - `description` (text)
  - `price` (decimal, 10 digits, 2 decimal places)
  - `image` (ImageField, uploads to `store/`)
  - `stock` (int, default 0)
  - `created_at`, `updated_at`
- **Purpose**: Retail products for purchase (decor, supplies, etc.)
- **Usage**: Items customers can add to cart and order

---

## 2. FIXTURE DATA SUMMARY

**File**: `core/fixtures/initial_products.json`

**Total Records**: 63 entries
- **ServiceCategories**: 4
- **StoreCategories**: 4
- **Service (Generic)**: 0 (using specialized models below)
- **EventManagement**: 6 entries (Premium wedding, Corporate, Birthday, Mehendi, Destination, Walima)
- **Photography**: 8 entries (Wedding, Pre-wedding, Birthday, Corporate, Mehendi, Videography, Maternity, Drone)
- **Catering**: 8 entries (Bengali, Continental, Biryani, Vegetarian, Appetizers, Desserts, Chinese, BBQ)
- **PrintingService**: 6 entries (Wedding cards, Business cards, Banners, Menu cards, Name tags, Brochures)
- **StoreItem**: 21 entries (Decor, Accessories, Lighting, Floral supplies)

### Key Assumptions:

1. **Currency**: All prices in **BDT (Bangladeshi Taka)** as this is a Bangladesh-based platform
2. **Image Paths**: Image filenames use underscores and follow pattern:
   - Services: `services/[service_type]_[description]_[number].jpg`
   - Store: `store/[item_type]_[descriptor]_[number].jpg`
3. **Service Models**: Used specialized models (EventManagement, Photography, Catering, PrintingService) instead of generic Service model
4. **Pricing**:
   - Event Management: 35,000 - 350,000 BDT
   - Photography: 12,000 - 65,000 BDT
   - Catering: 250 - 850 BDT per person
   - Printing: 3 - 50 BDT per piece
   - Store Items: 450 - 8,500 BDT
5. **Stock Levels**: StoreItems have realistic stock quantities (12-150 pieces)
6. **Timestamps**: All created/updated timestamps set to 2025-12-07 for consistency

---

## 3. HOW TO LOAD THE DATA

### Step 1: Verify Fixture File Location
The fixture file should be at:
```
E:\EvenNest\Main\core\fixtures\initial_products.json
```

### Step 2: Load the Fixture
Run the following command in your Django project root:

```bash
python manage.py loaddata initial_products.json
```

### Step 3: Verify Loading
After loading, you should see:
```
Installed X object(s) from 1 fixture(s)
```

### Step 4: Check in Admin
1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with: **admin / admin123**
3. Navigate to:
   - **Service Categories** → Should see 4 categories
   - **Event Management** → Should see 6 entries
   - **Photography** → Should see 8 entries
   - **Catering** → Should see 8 entries
   - **Printing Service** → Should see 6 entries
   - **Store Categories** → Should see 4 categories
   - **Store Items** → Should see 21 entries

---

## 4. IMAGE SETUP

The fixture references image files but doesn't create them. To display images properly:

### Option A: Upload Images Manually (Through Admin)
1. Go to each model's admin page
2. Edit each entry
3. Upload actual images
4. Save

### Option B: Copy Image Files (Recommended)
1. Place image files in the appropriate folders:
   - `media/services/` (for Service, EventManagement, Photography, Catering, PrintingService)
   - `media/store/` (for StoreItem)
2. Use filenames exactly as in the fixture:
   - Example: `media/services/wedding_premium_coordination_01.jpg`
   - Example: `media/store/crystal_centerpiece_led_01.jpg`

### Option C: Create Placeholder Images
Use online placeholder services or generate dummy images and rename them to match fixture filenames.

---

## 5. FIXTURE STRUCTURE DETAILS

### Example Service Entry (EventManagement):
```json
{
  "model": "core.eventmanagement",
  "pk": 1,
  "fields": {
    "title": "Premium Wedding Coordination Package",
    "description": "Complete wedding planning and coordination...",
    "price": "250000.00",
    "image": "services/wedding_premium_coordination_01.jpg",
    "event_type": "Wedding",
    "capacity": 500,
    "duration": 8,
    "includes_decoration": true,
    "includes_catering": false,
    "created_at": "2025-12-07T10:00:00Z",
    "updated_at": "2025-12-07T10:00:00Z"
  }
}
```

### Example Store Item Entry:
```json
{
  "model": "core.storeitem",
  "pk": 1,
  "fields": {
    "category": 1,
    "name": "Crystal Glass Table Centerpiece with LED Base",
    "description": "Elegant crystal glass centerpiece...",
    "price": "2500.00",
    "image": "store/crystal_centerpiece_led_01.jpg",
    "stock": 25,
    "created_at": "2025-12-07T10:00:00Z",
    "updated_at": "2025-12-07T10:00:00Z"
  }
}
```

---

## 6. TROUBLESHOOTING

### Issue: "No such table" error
**Solution**: Run migrations first
```bash
python manage.py migrate
```

### Issue: Image not displaying
**Solution**: 
1. Ensure media files exist at the specified path
2. Check `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`
3. Upload images manually through admin interface

### Issue: Fixture not found
**Solution**: Ensure file is in correct path:
```
core/fixtures/initial_products.json
```
(not `Core/fixtures/` or other variations)

### Issue: Duplicate key errors
**Solution**: 
- Delete `db.sqlite3` and re-run migrations, then loaddata
- Or manually delete conflicting entries in admin

---

## 7. CUSTOMIZATION

To modify the seed data:

1. **Edit JSON**: Open `initial_products.json` in any text editor
2. **Change values**: Update prices, descriptions, titles, etc.
3. **Add entries**: Duplicate an existing entry, change `pk` (primary key) to new unique number
4. **Reload**: 
   ```bash
   python manage.py loaddata initial_products.json
   ```

---

## 8. NEXT STEPS

After loading data:

1. **Upload Images**: Add actual product/service images to media folders
2. **Create Users/Vendors**: Add vendor accounts for contact/booking features
3. **Test Functionality**: Browse products on frontend, test cart, booking system
4. **Customize Data**: Adjust prices, descriptions, and availability per business needs

---

**Created**: 2025-12-07  
**Version**: 1.0  
**Platform**: EventNest Django Project
