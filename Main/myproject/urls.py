"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', views.home, name='home'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # Auth URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # User Profile & Bookings
    path('profile/', views.profile, name='profile'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/modify/', views.modify_booking, name='modify_booking'),
    
    # Services
    path('services/', views.all_services, name='all_services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('services/<int:service_id>/quote/', views.request_service_quote, name='request_quote'),
    
    # Store
    path('store/', views.all_store_items, name='all_store_items'),
    path('store/<int:item_id>/', views.store_item_detail, name='store_item_detail'),
    
    # Shopping Cart & Checkout
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<str:content_type>/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # API endpoints
    path('api/cart-count/', views.api_cart_count, name='api_cart_count'),
    path('api/services-search/', views.api_services_search, name='api_services_search'),
    path('api/items-search/', views.api_items_search, name='api_items_search'),
    path('api/order/<int:order_id>/items/', views.api_order_items, name='api_order_items'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
