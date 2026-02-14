"""
EventNest - Main Views
Production-ready views for all core functionality
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.db.models import Q, Prefetch, Sum
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.db import transaction
from functools import wraps
from .forms import SignUpForm, BookingForm
from .models import (
    ServiceCategory, Service, StoreCategory, StoreItem, 
    Cart, CartItem, Order, OrderItem, Wishlist,
    UserProfile, Booking, Contact, Notification
)
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def login_required_view(view_func):
    """Custom decorator to require login for specific views"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper


# ============== HOME & LANDING ==============

def home(request):
    """Home/Landing page"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get featured items (latest 8)
    featured_items = StoreItem.objects.all()[:8]
    
    context = {
        'featured_items': featured_items,
        'services': Service.objects.all()[:3],
    }
    return render(request, 'home.html', context)


def search(request):
    """Search services and products"""
    query = request.GET.get('q', '').strip()
    
    services = Service.objects.none()
    store_items = StoreItem.objects.none()
    
    if query:
        services = Service.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        store_items = StoreItem.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'query': query,
        'services': services,
        'store_items': store_items,
    }
    return render(request, 'search_results.html', context)


# ============== AUTHENTICATION ==============

def signup_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['full_name'].split()[0]
            user.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name']
            )
            
            # Create cart
            Cart.objects.create(user=user)
            
            # Create welcome notification
            Notification.objects.create(
                user=user,
                notification_type='welcome',
                title='Welcome to EventNest! 🎉',
                message='Thank you for joining EventNest! Browse our services to plan your perfect event. We offer wedding planning, photography, catering, and much more.',
                link='/services/'
            )
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    
    context = {}
    return render(request, 'registration/login.html', context)


def logout_view(request):
    """
    User logout - Handles both GET and POST requests
    POST: Preferred method, logs out user immediately
    GET: Shows confirmation page or logs out directly (for user convenience)
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    else:
        # For GET requests, log out directly (more user-friendly)
        # This is acceptable for logout since it's not a sensitive action
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')


# ============== USER PROFILE ==============

@login_required(login_url='login')
def profile(request):
    """User profile"""
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)


# ============== SERVICES ==============

@login_required(login_url='login')
def all_services(request):
    """Browse all services"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    services = Service.objects.all()
    
    if query:
        services = services.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_id:
        services = services.filter(category_id=category_id)
    
    categories = ServiceCategory.objects.all()
    
    context = {
        'services': services,
        'categories': categories,
        'query': query,
    }
    return render(request, 'services/all_services.html', context)


@login_required(login_url='login')
def service_detail(request, service_id):
    """Service detail page"""
    service = get_object_or_404(Service, id=service_id)
    
    context = {
        'service': service,
    }
    return render(request, 'services/service_detail.html', context)


# ============== SERVICES - BOOKING ==============

@login_required(login_url='login')
def request_service_quote(request, service_id):
    """Book a service or request a quote"""
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        try:
            from datetime import datetime
            
            # Get form data
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            requirements = request.POST.get('requirements', '')
            
            # Parse date and time
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            booking_time = datetime.strptime(time_str, '%H:%M').time()
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                service_type='service',
                service_id=service.id,
                date=booking_date,
                time_slot=booking_time,
                requirements=requirements,
                total_amount=service.price,
                status='pending'
            )
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                notification_type='booking',
                title='Booking Confirmed',
                message=f'Your booking for {service.title} on {booking_date.strftime("%B %d, %Y")} at {booking_time.strftime("%I:%M %p")} has been created.',
                link=f'/my-bookings/'
            )
            
            messages.success(request, f'Booking confirmed! Check your bookings page for details.')
            return redirect('my_bookings')
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
            return redirect('service_detail', service_id=service_id)
    
    return render(request, 'services/service_detail.html', {'service': service})



@login_required(login_url='login')
def my_bookings(request):
    """View user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'core/my_bookings.html', context)


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('my_bookings')


@login_required(login_url='login')
def modify_booking(request, booking_id):
    """Modify a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be modified.')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        new_date = request.POST.get('date')
        new_time = request.POST.get('time_slot')
        new_requirements = request.POST.get('requirements', '')
        
        if new_date:
            booking.date = new_date
        if new_time:
            booking.time_slot = new_time
        if new_requirements:
            booking.requirements = new_requirements
        
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been updated successfully.')
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'core/modify_booking.html', context)


# ============== STORE ==============

@login_required(login_url='login')
def all_store_items(request):
    """Browse all store items"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    items = StoreItem.objects.all()
    
    if query:
        items = items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    categories = StoreCategory.objects.all()
    
    # Get wishlist items for the user
    wishlist_items = []
    if request.user.is_authenticated:
        try:
            user_wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = list(user_wishlist.items.all())
        except Wishlist.DoesNotExist:
            pass
    
    context = {
        'items': items,
        'categories': categories,
        'query': query,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/all_items.html', context)


@login_required(login_url='login')
def store_item_detail(request, item_id):
    """Store item detail page"""
    item = get_object_or_404(StoreItem, id=item_id)
    
    # Get wishlist items for the user
    wishlist_items = []
    if request.user.is_authenticated:
        try:
            user_wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = list(user_wishlist.items.all())
        except Wishlist.DoesNotExist:
            pass
    
    context = {
        'item': item,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/item_detail.html', context)


# ============== SHOPPING CART ==============

@login_required(login_url='login')
def cart(request):
    """View shopping cart"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('item')
    total = sum(item.get_total() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
@require_POST
def add_to_cart(request, item_id):
    """Add item to cart"""
    item = get_object_or_404(StoreItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{item.name} added to cart!')
    return redirect('cart')


@login_required(login_url='login')
@require_POST
def update_cart(request, cart_item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.cart.user != request.user:
        raise Http404()
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = min(quantity, cart_item.item.stock)
        cart_item.save()
    
    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.cart.user != request.user:
        raise Http404()
    
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


# ============== CHECKOUT ==============

@login_required(login_url='login')
def checkout(request):
    """Checkout page"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all().select_related('item')
    total = sum(item.get_total() for item in cart_items)
    
    if not cart_items:
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='pending',
            shipping_address=f"{request.POST.get('address', '')}, {request.POST.get('city', '')}, {request.POST.get('zip_code', '')}"
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )
        
        # Clear cart
        cart_items.delete()
        
        # Create order notification
        Notification.objects.create(
            user=request.user,
            notification_type='order',
            title='Order Placed Successfully! 🛒',
            message=f'Your order #{order.id} for ৳{int(total)} has been placed. We will process it soon and update you on delivery.',
            link='/orders/'
        )
        
        messages.success(request, 'Order placed successfully! Thank you for your purchase.')
        return redirect('order_history')
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)


# ============== ORDER HISTORY ==============

@login_required(login_url='login')
def order_history(request):
    """View order history"""
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__item').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)


# ============== WISHLIST ==============

@login_required(login_url='login')
def wishlist(request):
    """View wishlist"""
    # Get or create user's wishlist
    user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    context = {
        'wishlist': user_wishlist,
    }
    return render(request, 'store/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, content_type, item_id):
    """Add item to wishlist"""
    # Get or create user's wishlist
    user_wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if content_type == 'storeitem':
        try:
            item = StoreItem.objects.get(id=item_id)
            user_wishlist.items.add(item)
            message = 'Added to wishlist'
        except StoreItem.DoesNotExist:
            message = 'Item not found'
    else:
        message = 'Invalid content type'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': message})
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_item_id):
    """Remove item from wishlist by item ID"""
    try:
        user_wishlist = Wishlist.objects.get(user=request.user)
        item = StoreItem.objects.get(id=wishlist_item_id)
        user_wishlist.items.remove(item)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Removed from wishlist'})
    except (Wishlist.DoesNotExist, StoreItem.DoesNotExist):
        pass
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ============== CONTACT ==============

@login_required(login_url='login')
def contact(request):
    """Contact form"""
    if request.method == 'POST':
        contact = Contact.objects.create(
            full_name=request.POST.get('full_name', ''),
            email=request.POST.get('email', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
            preferred_contact_method=request.POST.get('contact_method', 'email'),
            user=request.user if request.user.is_authenticated else None
        )
        messages.success(request, 'Your message has been sent! We will contact you soon.')
        return redirect('home')
    
    return render(request, 'core/contact.html')


# ============== API ENDPOINTS (JSON) ==============

@login_required(login_url='login')
def api_cart_count(request):
    """Get cart item count via AJAX"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return JsonResponse({'count': count})
    except Cart.DoesNotExist:
        return JsonResponse({'count': 0})


def api_services_search(request):
    """Search services via AJAX"""
    query = request.GET.get('q', '')
    services = Service.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )[:10].values('id', 'title', 'price')
    
    return JsonResponse(list(services), safe=False)


def api_items_search(request):
    """Search store items via AJAX"""
    query = request.GET.get('q', '')
    items = StoreItem.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:10].values('id', 'name', 'price')
    
    return JsonResponse(list(items), safe=False)


# ============== NOTIFICATIONS ==============

@login_required(login_url='login')
def notifications(request):
    """View all notifications"""
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'core/notifications.html', context)


@login_required(login_url='login')
def api_notifications(request):
    """Get notifications via AJAX for navbar dropdown"""
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    notifications_list = []
    for n in user_notifications:
        notifications_list.append({
            'id': n.id,
            'title': n.title,
            'message': n.message[:100] + '...' if len(n.message) > 100 else n.message,
            'type': n.notification_type,
            'link': n.link or '',
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%d %b %Y, %I:%M %p'),
        })
    
    return JsonResponse({
        'notifications': notifications_list,
        'unread_count': unread_count,
    })


@login_required(login_url='login')
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)


@login_required(login_url='login')
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})


def create_notification(user, notification_type, title, message, link=None):
    """Helper function to create notifications"""
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )


# ============== API - ORDER REORDER ==============

@login_required(login_url='login')
def api_order_items(request, order_id):
    """Get items from an order for reordering"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        items = []
        
        for order_item in order.order_items.all():
            items.append({
                'id': order_item.item.id,
                'name': order_item.item.name,
                'quantity': order_item.quantity,
                'price': str(order_item.price),
            })
        
        return JsonResponse({
            'success': True,
            'items': items,
            'order_id': order.id,
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Order not found'
        }, status=404)


# ============== INVOICE ==============

@login_required(login_url='login')
def download_invoice(request, order_id):
    """Download invoice as PDF"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('order_history')
    
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from datetime import datetime
        from django.http import FileResponse
        
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=12,
            alignment=1  # Center
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#666666'),
            spaceAfter=6
        )
        
        # Title
        elements.append(Paragraph("INVOICE", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Order info
        order_info = [
            [f"Invoice #: {order.id}", f"Date: {order.created_at.strftime('%B %d, %Y')}"],
            [f"Status: {order.get_status_display()}", f"Amount: ৳{order.total_amount:,.2f}"],
        ]
        
        info_table = Table(order_info, colWidths=[3*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Customer info
        elements.append(Paragraph("Bill To:", styles['Heading3']))
        customer_info = f"{order.user.get_full_name() or order.user.username}<br/>{order.shipping_address}"
        elements.append(Paragraph(customer_info, header_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Items table
        elements.append(Paragraph("Order Items", styles['Heading3']))
        
        item_data = [
            ['Product', 'Quantity', 'Price', 'Total'],
        ]
        
        for order_item in order.order_items.all():
            item_data.append([
                order_item.item.name[:30],
                str(order_item.quantity),
                f"৳{order_item.price:,.2f}",
                f"৳{order_item.get_total():,.2f}",
            ])
        
        # Add total row
        item_data.append([
            '',
            '',
            'Total:',
            f"৳{order.total_amount:,.2f}",
        ])
        
        items_table = Table(item_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7C3AED')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F3E8FF')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F9F5FF')]),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1  # Center
        )
        elements.append(Paragraph(
            "Thank you for your order! <br/>EventNest - Event Management Platform",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Return as file download
        response = FileResponse(buffer, as_attachment=True, filename=f'Invoice_{order.id}.pdf', content_type='application/pdf')
        return response
    
    except ImportError:
        # Fallback if reportlab not installed - return JSON with order data
        return JsonResponse({
            'error': 'PDF generation library not available',
            'order_id': order.id,
            'total': str(order.total_amount),
            'items': [
                {
                    'name': item.item.name,
                    'qty': item.quantity,
                    'price': str(item.price),
                    'total': str(item.get_total()),
                }
                for item in order.order_items.all()
            ]
        })


# ============== ERROR HANDLERS ==============

def handler404(request, exception):
    """404 error handler"""
    return render(request, '404.html', status=404)


def handler500(request):
    """500 error handler"""
    return render(request, '500.html', status=500)
