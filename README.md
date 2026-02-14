# EventNest

A comprehensive, production-ready event management platform combining a professional services marketplace with an e-commerce store for event-related products.

## Overview

EventNest enables users to discover and book professional event services (planning, photography, catering, entertainment, etc.) while shopping for event supplies, packages, and merchandise. It's a complete platform built with Django featuring a modern dark-themed interface, secure authentication, and robust booking/order management.

## Features

### Services Marketplace
- Browse professional services across 7 categories (events, photography, catering, decorations, entertainment, transportation, venue rental)
- Service detail pages with descriptions and pricing
- Request quotes for services
- Booking system with history tracking
- 61+ pre-populated services

### E-Commerce Store
- Product catalog with 42+ items (packages, decorations, electronics, favors, supplies)
- Category filtering and search
- Shopping cart and checkout functionality
- Order history and tracking
- Invoice generation

### User Management
- Secure registration and login
- Extended user profiles with personal information
- Profile editing and preferences
- Booking and order history
- Wishlist for saving favorite items

### Advanced Features
- Real-time search across services and products
- Shopping cart management
- Secure booking system
- Admin dashboard with full CRUD operations
- Modern responsive design (mobile-first)
- Dark theme with purple accents

## Technology Stack

**Backend:**
- Django 5.2rc1
- Python 3.9+
- SQLite (development) / PostgreSQL (production)
- Channels & Daphne (WebSocket support)
- ReportLab (invoice generation)

**Frontend:**
- HTML5 with Django templating
- CSS3 with 1000+ lines of custom styling
- Bootstrap Icons 1.11.0
- Vanilla JavaScript ES6+

**Deployment:**
- Gunicorn (WSGI server)
- WhiteNoise 6.7.0 (static file serving)
- Redis (caching/async)
- Railway, Heroku, or traditional VPS ready

## Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Prithila26/Evenest.git
   cd EventNest
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
EventNest/
├── Main/
│   ├── core/                      # Main Django application
│   │   ├── models.py             # 13+ database models
│   │   ├── views.py              # 17+ view functions
│   │   ├── forms.py              # Form validation
│   │   ├── admin.py              # Admin configuration
│   │   ├── templates/            # 14+ HTML templates
│   │   ├── static/css/           # Custom styling
│   │   └── fixtures/             # Initial data
│   │
│   ├── myproject/                # Django configuration
│   │   ├── settings.py           # Project settings
│   │   ├── urls.py               # URL routing
│   │   └── wsgi.py               # WSGI config
│   │
│   ├── media/                    # User uploads
│   ├── requirements.txt          # Python dependencies
│   └── manage.py                 # Django CLI
│
├── DATABASE_GUIDE.md             # Database documentation
├── DEPLOYMENT_GUIDE.md           # Production deployment
├── QUICK_START.md                # Quick reference
└── PROJECT_SUMMARY.md            # Detailed feature overview
```

## Database Models

**User & Authentication:**
- UserProfile, Cart, CartItem, Wishlist

**Services Marketplace:**
- ServiceCategory, Service, EventManagement, Photography, Catering, PrintingService, Booking, Contact

**E-Commerce:**
- StoreCategory, StoreItem, Order, OrderItem

## API Endpoints

**Public Routes:**
- `/signup/` - User registration
- `/login/` - User login

**Authenticated Routes:**
- `/` - Home page
- `/services/` - Browse services
- `/services/<id>/quote/` - Request quote
- `/store/` - Browse products
- `/cart/` - Shopping cart
- `/checkout/` - Order checkout
- `/orders/` - Order history
- `/orders/<id>/invoice/` - Download invoice
- `/profile/` - User profile
- `/my-bookings/` - Booking history

**JSON APIs:**
- `/api/cart-count/` - Get cart count
- `/api/services-search/` - Search services
- `/api/items-search/` - Search products

## Security

✅ CSRF Protection
✅ SQL Injection Prevention (Django ORM)
✅ XSS Prevention (Template escaping)
✅ Secure Password Hashing (PBKDF2)
✅ Authentication Required (Protected endpoints)
✅ User Permission System
✅ HTTPS Ready
✅ Secure Cookies (HTTPOnly, Secure flags)

## Deployment

EventNest is production-ready and can be deployed on:

- **Railway** (Recommended) - Simple, reliable deployment
- **Heroku** - Platform-as-a-Service option
- **Traditional VPS** - Full control and customization
- **Docker** - Containerized deployment

Refer to [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

## Documentation

- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Complete feature overview and specifications
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[QUICK_START.md](./QUICK_START.md)** - Quick setup reference
- **[DATABASE_GUIDE.md](./DATABASE_GUIDE.md)** - Database structure and management

## Key Statistics

- **Models**: 13+ database models
- **Views**: 17+ view functions + 3 JSON APIs
- **Templates**: 14+ HTML templates
- **Routes**: 20+ URL patterns
- **Services**: 61+ pre-populated services
- **Products**: 42+ items ready to sell
- **Code**: 6,000+ lines of production code

## Support & Contributing

For issues, feature requests, or contributions, please visit:
https://github.com/Prohar04/EventNest

## License

This project is provided as-is for educational and commercial use. See the repository for license details.

## About

EventNest is a production-ready platform developed with Django, engineered for scalability, security, and user experience. It provides a complete solution for event service booking and product sales in one integrated platform.

**Version**: 1.0.0
**Last Updated**: December 2025
**Status**: ✅ Production Ready
