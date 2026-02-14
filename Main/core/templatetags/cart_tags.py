from django import template
from django.db.models import Sum
from core.models import Cart

register = template.Library()

@register.simple_tag
def cart_item_count(user):
    """Returns the total number of items in the user's cart, including quantities"""
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            total = cart.items.aggregate(total=Sum('quantity'))['total']
            return total or 0
    return 0

@register.filter
def get_wishlist_status(item, user):
    """Check if an item is in user's wishlist"""
    if user.is_authenticated:
        return user.wishlist_set.filter(items=item).exists()
    return False

@register.filter
def smart_image_url(image):
    """Returns the correct URL for an image - handles both file uploads and external URLs"""
    if not image:
        return ''
    # Check if it's an external URL
    if hasattr(image, 'name') and image.name.startswith('http'):
        return image.name
    # Otherwise return the normal URL
    try:
        return image.url
    except:
        return ''