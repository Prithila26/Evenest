from django.contrib import admin
from .models import (
    ServiceCategory, Service, StoreCategory, StoreItem, UserProfile, 
    Cart, CartItem, Order, OrderItem, Wishlist, Booking, Contact,
    EventManagement, Photography, Catering, PrintingService, Notification
)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# ============== Service Models ==============

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('cart__user__username', 'item__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('total_amount',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    search_fields = ('order__user__username', 'item__name')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'created_at')
    search_fields = ('user__username',)
    filter_horizontal = ('items',)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Number of Items'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_type', 'date', 'time_slot', 'status', 'total_amount', 'created_at')
    list_filter = ('service_type', 'status', 'date', 'created_at')
    search_fields = ('user__username', 'requirements', 'service_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# ============== Contact Model ==============

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'service_type', 'status', 'created_at')
    list_filter = ('service_type', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_read', 'mark_as_responded']
    date_hierarchy = 'created_at'
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_responded(self, request, queryset):
        queryset.update(status='responded')
    mark_as_responded.short_description = 'Mark selected as responded'


# ============== Notification Model ==============

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    date_hierarchy = 'created_at'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark selected as unread'


# ============== Service-Specific Models ==============

@admin.register(EventManagement)
class EventManagementAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'price', 'capacity')
    list_filter = ('event_type', 'created_at')
    search_fields = ('title',)

@admin.register(Photography)
class PhotographyAdmin(admin.ModelAdmin):
    list_display = ('title', 'shoot_type', 'price', 'duration')
    list_filter = ('shoot_type',)
    search_fields = ('title',)

@admin.register(Catering)
class CateringAdmin(admin.ModelAdmin):
    list_display = ('title', 'cuisine_type', 'price', 'min_order_quantity')
    list_filter = ('cuisine_type',)
    search_fields = ('title',)

@admin.register(PrintingService)
class PrintingServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'print_type', 'price', 'min_order_quantity')
    list_filter = ('print_type',)
    search_fields = ('title',)


# ============== Customize Admin Site ==============

admin.site.site_header = "EventNest Administration"
admin.site.site_title = "EventNest Admin"
admin.site.index_title = "Welcome to EventNest Admin Portal"
