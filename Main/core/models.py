from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)  # Format: +880XXXXXXXXXX
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile"""
    # Skip profile creation here since it's handled in SignUpForm
    pass

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Service Categories"
        indexes = [
            models.Index(fields=['name']),
        ]

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['price']),
        ]

class EventManagement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/events/')
    event_type = models.CharField(max_length=100)  # wedding, corporate, birthday, etc.
    capacity = models.IntegerField(help_text="Maximum number of guests")
    duration = models.IntegerField(help_text="Duration in hours")
    includes_decoration = models.BooleanField(default=False)
    includes_catering = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event: {self.title}"

    def get_service_type(self):
        return 'event'

class Photography(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/photography/')
    shoot_type = models.CharField(max_length=100)  # wedding, portrait, event, etc.
    duration = models.IntegerField(help_text="Duration in hours")
    includes_editing = models.BooleanField(default=True)
    number_of_photos = models.IntegerField(help_text="Minimum number of delivered photos")
    includes_prints = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photography: {self.title}"

    def get_service_type(self):
        return 'photo'

class Catering(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per person")
    image = models.ImageField(upload_to='services/catering/')
    cuisine_type = models.CharField(max_length=100)  # Bengali, Chinese, Continental, etc.
    min_order_quantity = models.IntegerField(help_text="Minimum number of persons")
    includes_serving_staff = models.BooleanField(default=False)
    includes_setup = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Catering: {self.title}"

    def get_service_type(self):
        return 'catering'

class PrintingService(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per piece")
    image = models.ImageField(upload_to='services/printing/')
    print_type = models.CharField(max_length=100)  # invitation, business card, banner, etc.
    paper_type = models.CharField(max_length=100)
    min_order_quantity = models.IntegerField()
    includes_design = models.BooleanField(default=False)
    delivery_time = models.IntegerField(help_text="Delivery time in days")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Printing: {self.title}"

    def get_service_type(self):
        return 'printing'

class StoreCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Store Categories"
        indexes = [
            models.Index(fields=['name']),
        ]

class StoreItem(models.Model):
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='store/')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure quantity doesn't exceed stock
        if self.quantity > self.item.stock:
            self.quantity = self.item.stock
        super().save(*args, **kwargs)

    def get_total(self):
        return self.item.price * self.quantity

@receiver(pre_save, sender=CartItem)
def cart_item_pre_save(sender, instance, **kwargs):
    """Ensure cart item quantity doesn't exceed available stock and update stock"""
    try:
        if instance.pk:  # If updating existing item
            old_item = CartItem.objects.get(pk=instance.pk)
            old_quantity = old_item.quantity
            quantity_diff = instance.quantity - old_quantity
            
            if quantity_diff > 0 and quantity_diff > instance.item.stock:
                instance.quantity = old_quantity + instance.item.stock
            
            # Update stock
            instance.item.stock = max(0, instance.item.stock - quantity_diff)
            instance.item.save()
        else:  # If creating new item
            if instance.quantity > instance.item.stock:
                instance.quantity = instance.item.stock
            
            # Update stock
            instance.item.stock = max(0, instance.item.stock - instance.quantity)
            instance.item.save()
    except CartItem.DoesNotExist:
        pass

@receiver(post_delete, sender=CartItem)
def cart_item_post_delete(sender, instance, **kwargs):
    """Return stock when cart item is deleted"""
    instance.item.stock += instance.quantity
    instance.item.save()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(StoreItem, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.status == 'cancelled':
            # Return stock for cancelled orders
            for order_item in self.order_items.all():
                order_item.item.stock += order_item.quantity
                order_item.item.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    
    def save(self, *args, **kwargs):
        if self.pk is None:  # Only for new items
            # Update stock when order item is created
            self.item.stock = max(0, self.item.stock - self.quantity)
            self.item.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Return stock when order item is deleted
        self.item.stock += self.quantity
        self.item.save()
        super().delete(*args, **kwargs)
    
    def get_total(self):
        return self.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(StoreItem, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('service', 'Service'),
        ('event', 'Event Management'),
        ('photo', 'Photography'),
        ('catering', 'Catering'),
        ('printing', 'Printing Service'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    service_id = models.PositiveIntegerField()
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requirements = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service_type', 'service_id']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_service_type_display()} booking by {self.user.username}"

    def get_service(self):
        try:
            if self.service_type == 'service':
                return Service.objects.get(id=self.service_id)
            elif self.service_type == 'event':
                return EventManagement.objects.get(id=self.service_id)
            elif self.service_type == 'photo':
                return Photography.objects.get(id=self.service_id)
            elif self.service_type == 'catering':
                return Catering.objects.get(id=self.service_id)
            elif self.service_type == 'printing':
                return PrintingService.objects.get(id=self.service_id)
        except (Service.DoesNotExist, EventManagement.DoesNotExist, 
                Photography.DoesNotExist, Catering.DoesNotExist, 
                PrintingService.DoesNotExist):
            return None
        return None


class Notification(models.Model):
    """Model to store user notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('booking', 'Booking Update'),
        ('order', 'Order Update'),
        ('promo', 'Promotion'),
        ('system', 'System'),
        ('welcome', 'Welcome'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True, help_text="Optional link to related page")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Contact(models.Model):
    """Model to store contact inquiries from users"""
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('other', 'Other'),
    ]
    
    SERVICE_TYPE_CHOICES = [
        ('event', 'Event Management'),
        ('photo', 'Photography'),
        ('catering', 'Catering'),
        ('printing', 'Printing Service'),
        ('store', 'Store Item'),
        ('general', 'General Inquiry'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    preferred_contact_method = models.CharField(max_length=20, choices=CONTACT_METHOD_CHOICES, default='email')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='general')
    service_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID of the related service/item if applicable")
    service_name = models.CharField(max_length=200, blank=True, help_text="Name of the service/item being inquired about")
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('read', 'Read'), ('responded', 'Responded')], default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['service_type', 'service_id']),
        ]
    
    def __str__(self):
        return f"Contact from {self.full_name} - {self.subject}"

