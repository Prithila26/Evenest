"""
Context processors for templates.
These functions add data to the template context automatically.
"""

from django.contrib.auth.models import User
from core.models import ServiceCategory, StoreCategory, Cart, CartItem, Wishlist


def service_categories_processor(request):
    """Add service categories to template context."""
    try:
        service_categories = ServiceCategory.objects.all()
    except Exception:
        service_categories = []
    
    return {
        'service_categories': service_categories,
    }


def store_categories_processor(request):
    """Add store categories to template context."""
    try:
        store_categories = StoreCategory.objects.all()
    except Exception:
        store_categories = []
    
    return {
        'store_categories': store_categories,
    }


def cart_processor(request):
    """Add cart information to template context."""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            from django.db.models import Sum
            cart_count = cart.items.aggregate(
                total_quantity=Sum('quantity')
            )['total_quantity'] or 0
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {
        'cart_count': cart_count,
    }


def wishlist_processor(request):
    """Add wishlist information to template context."""
    wishlist_count = 0
    
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_count = wishlist.items.count()
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    
    return {
        'wishlist_count': wishlist_count,
    }
