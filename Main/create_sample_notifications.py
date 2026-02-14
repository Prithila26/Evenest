#!/usr/bin/env python
"""
Script to create sample notifications for existing users
This ensures users see meaningful notifications in the navbar dropdown
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from core.models import Notification, Order, Booking

print("\n" + "="*60)
print("Creating Sample Notifications for All Users")
print("="*60)

# Sample notifications to create
sample_notifications = [
    {
        'notification_type': 'welcome',
        'title': 'Welcome to EventNest! 🎉',
        'message': 'Thank you for being part of EventNest! Explore our wide range of services for your next event - weddings, corporate events, birthdays, and more.',
        'link': '/services/'
    },
    {
        'notification_type': 'promo',
        'title': 'Special Discount - 20% Off! 🎁',
        'message': 'Get 20% off on all Photography packages this month! Use code: EVENTPIC20. Valid until end of December 2025.',
        'link': '/services/'
    },
    {
        'notification_type': 'system',
        'title': 'Profile Complete Your Profile',
        'message': 'Add your phone number and address to your profile for faster checkout and better service coordination.',
        'link': '/profile/'
    },
]

users = User.objects.all()
notifications_created = 0

for user in users:
    # Check if user already has notifications
    existing_count = Notification.objects.filter(user=user).count()
    
    if existing_count == 0:
        # Create sample notifications for this user
        for notif_data in sample_notifications:
            Notification.objects.create(
                user=user,
                notification_type=notif_data['notification_type'],
                title=notif_data['title'],
                message=notif_data['message'],
                link=notif_data['link'],
                is_read=False
            )
            notifications_created += 1
        print(f"✅ Created {len(sample_notifications)} notifications for: {user.username}")
    else:
        print(f"⏭️  Skipped {user.username} (already has {existing_count} notifications)")

    # If user has orders, create order notification
    orders = Order.objects.filter(user=user).order_by('-created_at')[:1]
    for order in orders:
        existing = Notification.objects.filter(
            user=user,
            notification_type='order',
            title__contains=str(order.id)
        ).exists()
        
        if not existing:
            Notification.objects.create(
                user=user,
                notification_type='order',
                title=f'Order #{order.id} Confirmed ✅',
                message=f'Your order for ৳{int(order.total_amount)} has been confirmed and is being processed.',
                link='/orders/',
                is_read=True  # Mark as read since it's historical
            )
            notifications_created += 1
            print(f"  📦 Added order notification for order #{order.id}")

    # If user has bookings, create booking notification
    bookings = Booking.objects.filter(user=user).order_by('-created_at')[:1]
    for booking in bookings:
        existing = Notification.objects.filter(
            user=user,
            notification_type='booking',
            message__contains=str(booking.id)
        ).exists()
        
        if not existing:
            Notification.objects.create(
                user=user,
                notification_type='booking',
                title=f'Booking Confirmed! 📅',
                message=f'Your {booking.get_service_type_display()} booking for {booking.date.strftime("%d %b %Y")} has been confirmed.',
                link='/my-bookings/',
                is_read=True
            )
            notifications_created += 1
            print(f"  📅 Added booking notification for booking #{booking.id}")

print("\n" + "="*60)
print(f"✅ Created {notifications_created} notifications across {users.count()} users")
print("="*60 + "\n")
