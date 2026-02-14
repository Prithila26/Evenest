# EvenNest Copilot Instructions

## Project Overview
EvenNest is a Django 5.2 web application for event management and commerce, featuring a service marketplace (events, photography, catering, printing) and retail store with real-time admin-client chat. Built with Django Channels for WebSocket support, Bootstrap 5 styling, and SQLite (dev) / PostgreSQL (prod).

## Architecture

### Core Models (Polymorphic Services)
The project uses **multiple service models** instead of single inheritance for flexibility:
- `Service` + `ServiceCategory` - generic services
- `EventManagement`, `Photography`, `Catering`, `PrintingService` - specific service types
- Each has `get_service_type()` method returning a string identifier ('event', 'photo', 'catering', 'printing')

**Store Models**: `StoreItem` + `StoreCategory` (separate from services)

**E-commerce**: `Cart`, `CartItem`, `Order`, `OrderItem` with **inventory tracking via signals**:
- `CartItem.pre_save` adjusts stock when quantities change
- `CartItem.post_delete` refunds stock
- `OrderItem.save/delete` handle stock management
- Stock is a **single source of truth** - avoid duplicating qty tracking elsewhere

**Chat** (under refactoring per migration 0015):
- Previous: Chat/Message/ChatSession models were removed
- Current state: Models exist in migrations but are functionally disabled
- **Do not build chat features** without first clarifying the chat strategy

**User**: `UserProfile` created via signal on User creation (enhanced with full_name, phone, address)

### Data Flow Patterns

#### Service Browsing
1. Client requests `/services/` → `service_categories_processor` caches categories (1hr)
2. Template loops `service_categories` → category links filter by ForeignKey
3. Detail pages fetch individual Service/EventManagement/etc by ID

#### Shopping Flow
1. Add to cart: checks `item.stock > 0` via `CartItem.pre_save`
2. Checkout: creates `Order` + `OrderItem` records, stock updates via signals
3. **Never manually update stock** - always use model saves/deletes

#### Future Chat Implementation
The app has WebSocket infrastructure (Channels, middleware) but chat models are currently **disabled**. Before implementing chat:
- Check migrations `0013` (Chat with admin FK) and `0015` (model removal)
- Decide: restore Chat model or use Conversation model
- Ensure WebSocket routing aligns with chosen approach
- Test AuthMiddlewareStack + WebSocketMiddleware authentication flow

### Frontend Architecture

#### Templates
- `base.html` - master layout with navbar, footer, static blocks
- `navbar_new.html` - responsive navbar with chat badge (if implemented)
- Service/Store grids use **fixed-height image containers**: 250px for grid cards, 400px for detail pages
  - CSS: `object-fit: cover` prevents distortion
  - Images are assigned via `core/management/commands/assign_product_images.py`

#### Design System (`core/static/css/style.css`)
- **Colors**: Primary #00bfff, Secondary #0056b3, Alert #ff6b6b, Success #51cf66
- **Typography**: 12px-36px scale, system fonts
- **Spacing**: 4px-48px scale using 4px increments
- **Responsive**: Mobile-first (0-767px) → Tablet (768-1023px) → Desktop (1024px+)
- No Bootstrap overrides needed - system works within Bootstrap 5

### Deployment & Configuration

#### Settings.py Key Points
- Uses environment variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `ALLOWED_HOSTS` (currently empty - fill before prod)
- Channels + Channels_Redis installed but InMemoryChannelLayer used in dev
- `DEBUG = True` in development - **set to False for production**
- SQLite for dev, use PostgreSQL + Redis for production

#### Run & Debug
```bash
cd d:\EvenNest\Main
python manage.py runserver
# Access: http://127.0.0.1:8000/

# Load seed data
python manage.py loaddata core/fixtures/initial_products.json

# Create admin
python manage.py createsuperuser
# OR use: python create_admin.py (admin2/admin123)

# Assign images to products
python manage.py assign_product_images
```

Test credentials exist in db.sqlite3: `admin2/admin123` (admin), `testclient/password123` (client)

### Key Conventions

#### Stock Management is Critical
- **Never create new CartItem/OrderItem without ORM** - signals won't trigger
- **Test stock changes** after any inventory operation
- Use `max(0, quantity)` to prevent negative stock

#### Polymorphic Services
When adding a new service type:
1. Create a model with `get_service_type()` returning a string constant
2. Add the choice to `Booking.SERVICE_CHOICES` and `Booking.get_service()` if bookings are needed
3. Update templates to iterate over all service model querysets (see `all_services.html`)

#### Permission Checks
- `@login_required` on chat/profile/checkout views
- Admins (`request.user.is_staff`) see all chats; clients see only their own
- No explicit permission decorators elsewhere - reliance on `@login_required` is intentional

#### Caching
- Service/Store categories cached for 1 hour via `cache.set()` in context processors
- **Clear cache when categories are created/deleted** - currently not automated
- Consider invalidating cache in `ServiceCategory.save()` if adding this

#### Image Handling
- All images use `ImageField(upload_to='...')` creating date-based folders
- Management command `assign_product_images.py` maps Unsplash images to products
- **Do not hardcode image paths** - always use model's image field

### Testing & Validation

#### Database Integrity
- Run `python verify_seed_data.py` to validate fixture load
- Check `db.sqlite3` tables: User, UserProfile, Service, StoreItem, Cart, Order, Booking (13+ tables)

#### Frontend Validation
- Fixed image boxes: inspect CSS `height: 250px; object-fit: cover` 
- Responsive: test at 375px (mobile), 768px (tablet), 1920px (desktop)
- No layout shift from image loading - fixed containers ensure stability

### Common Pitfalls

1. **Modifying stock directly** - use ORM saves/deletes only
2. **Adding chat features without model clarity** - migrations 0013-0015 are in flux
3. **Image paths as hardcoded strings** - always reference `model_instance.image.url`
4. **Forgetting @login_required** - chat and checkout require authentication
5. **Caching stale categories** - clear when adding new categories (currently manual)

### Documentation Files to Reference
- `PROJECT_COMPLETION_STATUS.md` - status & implementation details
- `CHAT_IMPLEMENTATION_SUMMARY.md` - WebSocket architecture (outdated post-migration 0015)
- `MODELS_AND_FIXTURE_GUIDE.md` - complete model field reference
- `SEED_DATA_SUMMARY.md` - fixture structure and data loading

---
*Last updated: December 8, 2025*  
*Django 5.2rc1 | Python 3.13 | Channels 4.x*
