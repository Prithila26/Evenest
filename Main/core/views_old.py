from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.db.models import Q, Prefetch, Sum
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db import transaction
from django.http import JsonResponse
from .forms import SignUpForm, ServiceForm, ServiceCategoryForm, StoreItemForm, StoreCategoryForm, BookingForm
from .models import (
    ServiceCategory, Service, StoreCategory, StoreItem, 
    Cart, CartItem, Order, OrderItem, Wishlist,
    UserProfile, EventManagement, Photography, Catering, PrintingService, Booking
)
from django.utils import timezone

def service_categories_processor(request):
    """Context processor to provide service categories to all templates"""
    categories = cache.get('service_categories')
    if categories is None:
        categories = ServiceCategory.objects.all()
        cache.set('service_categories', categories, 3600)  # Cache for 1 hour
    return {'service_categories': categories}

def store_categories_processor(request):
    """Context processor to provide store categories to all templates"""
    categories = cache.get('store_categories')
    if categories is None:
        categories = StoreCategory.objects.all().order_by('name')
        cache.set('store_categories', categories, 3600)  # Cache for 1 hour
    return {'store_categories': categories}

def cart_processor(request):
    """Context processor to provide cart data to all templates - optimized"""
    if request.user.is_authenticated:
        try:
            # Use select_related for faster queries
            cart = Cart.objects.select_related('user').prefetch_related('items__item').filter(user=request.user).first()
            if cart is None:
                cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get total items efficiently
            from django.db.models import Sum
            total_items = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
            
            return {
                'user_cart': cart,
                'cart_total': cart.get_total(),
                'cart_item_count': total_items
            }
        except:
            return {
                'user_cart': None,
                'cart_total': 0,
                'cart_item_count': 0
            }
    return {
        'user_cart': None,
        'cart_total': 0,
        'cart_item_count': 0
    }

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to EvenNest.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.profile.full_name}!')
            return redirect('home')
        else:
            error = 'Invalid username or password. Please try again.'
    return render(request, 'registration/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@cache_page(60 * 15)  # Cache for 15 minutes
@login_required
def home(request):
    # Remove cache for store items to get fresh stock counts
    services = Service.objects.select_related('category').all()[:6]
    store_items = StoreItem.objects.select_related('category').all()[:6]
    
    # Get user's wishlist items
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_items = list(wishlist.items.values_list('id', flat=True))
    
    context = {
        'services': services,
        'store_items': store_items,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'home.html', context)

@cache_page(60 * 15)
def service_category_view(request, category_name):
    display_name = category_name.replace('-', ' ').title()
    category = get_object_or_404(ServiceCategory, name=display_name)
    services = Service.objects.select_related('category').filter(category=category)
    
    context = {
        'category': category,
        'services': services,
    }
    return render(request, 'services/category.html', context)

@cache_page(60 * 15)
def store_category_view(request, category_name):
    display_name = category_name.replace('-', ' ').title()
    category = get_object_or_404(StoreCategory, name=display_name)
    items = StoreItem.objects.select_related('category').filter(category=category)
    
    # Get user's wishlist items if authenticated
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_items = wishlist.items.values_list('id', flat=True)
    
    context = {
        'category': category,
        'items': items,
        'wishlist_items': wishlist_items
    }
    return render(request, 'store/category.html', context)

@login_required
def personal_info(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            profile.full_name = form.cleaned_data['full_name']
            profile.phone = form.cleaned_data['phone']
            profile.address = form.cleaned_data['address']
            profile.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('personal_info')
    else:
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'full_name': profile.full_name,
            'phone': profile.phone,
            'address': profile.address,
        }
        form = SignUpForm(initial=initial_data, instance=request.user)
        del form.fields['password1']
        del form.fields['password2']
    
    return render(request, 'registration/personal_info.html', {
        'form': form,
        'profile': profile
    })

def search(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    services = Service.objects.select_related('category').all()
    store_items = StoreItem.objects.select_related('category').all()
    
    if query:
        services = services.filter(Q(title__icontains=query) | Q(description__icontains=query))
        store_items = store_items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if min_price:
        try:
            min_price = float(min_price)
            services = services.filter(price__gte(min_price))
            store_items = store_items.filter(price__gte(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            services = services.filter(price__lte(max_price))
            store_items = store_items.filter(price__lte(max_price))
        except ValueError:
            pass
    
    # Get user's wishlist items
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_items = wishlist.items.values_list('id', flat=True)
    
    context = {
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'services': services,
        'store_items': store_items,
        'wishlist_items': wishlist_items
    }
    return render(request, 'search_results.html', context)

def all_services_view(request):
    services = Service.objects.all()
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        services = services.filter(price__gte(float(min_price)))
    if max_price:
        services = services.filter(price__lte(float(max_price)))
    
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    elif sort_by == 'name':
        services = services.order_by('title')
    
    categories = ServiceCategory.objects.all()
    
    context = {
        'services': services,
        'categories': categories,
        'title': 'All Services',
        'current_category': category_id,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort_by
    }
    return render(request, 'services/all_services.html', context)

def all_store_items_view(request):
    store_items = StoreItem.objects.all()
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        store_items = store_items.filter(category_id=category_id)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        store_items = store_items.filter(price__gte=float(min_price))
    if max_price:
        store_items = store_items.filter(price__lte=float(max_price))
    
    # Stock filter
    in_stock = request.GET.get('in_stock')
    if in_stock:
        store_items = store_items.filter(stock__gt(0))
    
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        store_items = store_items.order_by('price')
    elif sort_by == 'price_high':
        store_items = store_items.order_by('-price')
    elif sort_by == 'name':
        store_items = store_items.order_by('name')
    
    categories = StoreCategory.objects.all()
    
    context = {
        'items': store_items,
        'categories': categories,
        'title': 'All Store Items',
        'current_category': category_id,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort_by,
        'in_stock': in_stock
    }
    return render(request, 'store/all_items.html', context)

def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Determine service type based on the category name
    service_type = None
    category_name = service.category.name.lower()
    if 'event' in category_name:
        service_type = 'event'
    elif 'photo' in category_name:
        service_type = 'photo'
    elif 'cater' in category_name:
        service_type = 'catering'
    elif 'print' in category_name:
        service_type = 'printing'
    
    context = {
        'service': service,
        'service_type': service_type
    }
    return render(request, 'services/service_detail.html', context)

def store_item_detail_view(request, item_id):
    item = get_object_or_404(StoreItem, id=item_id)
    context = {
        'item': item
    }
    return render(request, 'store/item_detail.html', context)

@require_POST
@login_required
def add_to_cart(request, item_id):
    """Add an item to cart with proper stock management"""
    try:
        with transaction.atomic():
            # Get fresh item instance with lock for update
            item = StoreItem.objects.select_for_update().get(id=item_id)
            
            if item.stock < 1:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Sorry, this item is out of stock.',
                        'current_stock': item.stock
                    })
                messages.warning(request, 'Sorry, this item is out of stock.')
                return redirect(request.META.get('HTTP_REFERER', 'home'))
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
            
            if not created:
                if cart_item.quantity + 1 > item.stock:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Sorry, only {item.stock} items available in stock.',
                            'current_stock': item.stock
                        })
                    messages.warning(request, f'Sorry, only {item.stock} items available in stock.')
                    return redirect(request.META.get('HTTP_REFERER', 'home'))
                cart_item.quantity += 1
                cart_item.save()
            
            # Update stock count for real-time display
            item.refresh_from_db()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f'{item.name} added to cart.',
                    'current_stock': item.stock,
                    'cart_count': cart.items.aggregate(total=Sum('quantity'))['total'] or 0
                })
            messages.success(request, f'{item.name} added to cart.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
            
    except StoreItem.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Item not found.'
            })
        messages.error(request, 'Item not found.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            })
        messages.error(request, 'An error occurred. Please try again.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    try:
        cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.warning(request, 'Item was already removed from cart.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_count
        })
    
    return redirect('cart_detail')

@require_POST
@login_required
def update_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > cart_item.item.stock:
        messages.warning(request, 'Sorry, not enough items in stock.')
        quantity = cart_item.item.stock
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Verify stock availability before creating order
                stock_issues = []
                for cart_item in cart.items.all():
                    # Get fresh stock count from database with lock
                    store_item = StoreItem.objects.select_for_update().get(id=cart_item.item.id)
                    if cart_item.quantity > store_item.stock:
                        stock_issues.append(f'{store_item.name} only has {store_item.stock} items in stock.')
                
                if stock_issues:
                    messages.error(request, 'Stock issues: ' + '; '.join(stock_issues))
                    return redirect('cart_detail')

                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.get_total(),
                    shipping_address=request.user.profile.address,
                    status='pending'
                )
                
                # Create order items and update stock
                for cart_item in cart.items.select_related('item'):
                    store_item = StoreItem.objects.select_for_update().get(id=cart_item.item.id)
                    
                    OrderItem.objects.create(
                        order=order,
                        item=store_item,
                        quantity=cart_item.quantity,
                        price=store_item.price
                    )
                    
                    # Update stock
                    store_item.stock -= cart_item.quantity
                    store_item.save()
                
                # Clear the cart
                cart.items.all().delete()
                
                messages.success(request, 'Order placed successfully! You can track your order in the Order History.')
                
                # Redirect to order history page which will show the newly placed order
                return redirect('order_history')
                
        except Exception as e:
            messages.error(request, 'An error occurred while processing your order. Please try again.')
            return redirect('cart_detail')
    
    return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    # Use select_related and prefetch_related to optimize queries
    orders = Order.objects.select_related('user').prefetch_related(
        Prefetch(
            'order_items',
            queryset=OrderItem.objects.select_related('item', 'item__category')
        )
    ).filter(user=request.user).order_by('-created_at')
    
    # Get user's wishlist items for easy checking
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_items = wishlist.items.values_list('id', flat=True)
    
    return render(request, 'store/order_history.html', {
        'orders': orders,
        'wishlist_items': wishlist_items
    })

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

@require_POST
@login_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(StoreItem, id=item_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if item in wishlist.items.all():
        wishlist.items.remove(item)
        message = f"{item.name} removed from wishlist."
        is_in_wishlist = False
    else:
        wishlist.items.add(item)
        message = f"{item.name} added to wishlist."
        is_in_wishlist = True
    
    messages.success(request, message)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': message,
            'is_in_wishlist': is_in_wishlist
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def create_booking(request, service_type, service_id):
    try:
        # Get the original service first
        service = get_object_or_404(Service, id=service_id)
        
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.service_type = service_type
                booking.service_id = service_id
                booking.total_amount = service.price
                booking.save()
                
                messages.success(request, 'Booking created successfully! We will contact you soon.')
                return redirect('booking_list')
        else:
            form = BookingForm()

        return render(request, 'core/booking_form.html', {
            'form': form,
            'service': service
        })
    except Service.DoesNotExist:
        messages.error(request, 'Service not found.')
        return redirect('all_services')

@login_required
def booking_list(request):
    # Get bookings with prefetched services for efficiency
    bookings = (Booking.objects
                .filter(user=request.user)
                .select_related('user')
                .order_by('-created_at'))
    
    # Pass to template with success message if redirected from create_booking
    return render(request, 'core/booking_list.html', {
        'bookings': bookings,
        'title': 'My Bookings'  # This will show in the browser tab
    })


def contact_provider(request):
    """View to handle contact provider inquiries - optimized with error handling"""
    from .forms import ContactForm
    
    # Get pre-fill data from query parameters
    service_type = request.GET.get('service_type', 'general')
    service_id = request.GET.get('service_id', '')
    service_name = request.GET.get('service_name', '')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = form.save(commit=False)
                
                # If user is authenticated, link them to the contact
                if request.user.is_authenticated:
                    contact.user = request.user
                    # Pre-fill name and email from user profile if not provided
                    if not contact.full_name:
                        try:
                            if hasattr(request.user, 'profile') and request.user.profile.full_name:
                                contact.full_name = request.user.profile.full_name
                            else:
                                contact.full_name = request.user.get_full_name() or request.user.username
                        except:
                            contact.full_name = request.user.username
                    
                    if not contact.phone and hasattr(request.user, 'profile'):
                        try:
                            contact.phone = request.user.profile.phone or ''
                        except:
                            contact.phone = ''
                
                # Set service info if provided
                if service_id:
                    contact.service_id = int(service_id) if service_id.isdigit() else None
                if service_name:
                    contact.service_name = service_name[:200]  # Limit to field max length
                
                contact.save()
                
                messages.success(
                    request,
                    'Thank you! Your inquiry has been submitted successfully. We will get back to you shortly.'
                )
                return redirect('contact_success')
            except Exception as e:
                messages.error(request, f'An error occurred while submitting your form. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        initial_data = {
            'service_type': service_type,
        }
        
        # Pre-fill user data if authenticated
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'profile'):
                    initial_data['full_name'] = request.user.profile.full_name or request.user.get_full_name()
                    initial_data['phone'] = request.user.profile.phone or ''
                else:
                    initial_data['full_name'] = request.user.get_full_name() or request.user.username
            except:
                initial_data['full_name'] = request.user.username
            
            initial_data['email'] = request.user.email
        
        form = ContactForm(initial=initial_data)
    
    context = {
        'form': form,
        'service_type': service_type,
        'service_name': service_name,
        'service_id': service_id,
    }
    
    return render(request, 'core/contact_provider.html', context)


def contact_success(request):
    """Success page after contact form submission"""
    return render(request, 'core/contact_success.html')
