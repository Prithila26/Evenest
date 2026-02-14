#!/usr/bin/env python
"""
EventNest - Final QA Checklist
Comprehensive verification of all fixes and requirements
"""

import os
import sys
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from core.models import Service, StoreItem, Notification, ServiceCategory, StoreCategory, Order, Booking, Contact

def run_qa_checklist():
    """Run comprehensive QA checklist"""
    
    print("\n" + "="*70)
    print("🔍 EVENTNEST - FINAL QA CHECKLIST")
    print("="*70)
    
    passed = 0
    failed = 0
    
    # A. Authentication Tests
    print("\n📋 A. AUTHENTICATION FLOWS")
    print("-"*70)
    
    client = Client()
    
    # Test 1: Login page accessible
    response = client.get('/login/')
    if response.status_code == 200:
        print("✅ Login page accessible")
        passed += 1
    else:
        print(f"❌ Login page - {response.status_code}")
        failed += 1
    
    # Test 2: Signup page accessible
    response = client.get('/signup/')
    if response.status_code == 200:
        print("✅ Signup page accessible")
        passed += 1
    else:
        print(f"❌ Signup page - {response.status_code}")
        failed += 1
    
    # Test 3: Login works
    test_user = User.objects.filter(username='testuser').first()
    if test_user:
        response = client.post('/login/', {'username': 'testuser', 'password': 'TestPassword123!'})
        if response.status_code == 302:
            print("✅ Login works with redirect")
            passed += 1
        else:
            print(f"❌ Login failed - {response.status_code}")
            failed += 1
    else:
        print("⚠️  Test user not found - skipping login test")
    
    # Test 4: Logout works (both GET and POST)
    client.force_login(test_user)
    response = client.post('/logout/')
    if response.status_code == 302:
        print("✅ Logout via POST works")
        passed += 1
    else:
        print(f"❌ Logout POST failed - {response.status_code}")
        failed += 1
    
    response = client.get('/logout/')
    if response.status_code == 302:
        print("✅ Logout via GET works (redirects)")
        passed += 1
    else:
        print(f"❌ Logout GET failed - {response.status_code}")
        failed += 1
    
    # Test 5: Protected pages redirect when not logged in
    client.logout()
    response = client.get('/services/')
    if response.status_code == 302:
        print("✅ Protected pages redirect to login")
        passed += 1
    else:
        print(f"❌ Protected pages not redirecting - {response.status_code}")
        failed += 1
    
    # B. Page Tests
    print("\n📋 B. PAGE FUNCTIONALITY")
    print("-"*70)
    
    client.force_login(test_user)
    
    pages = [
        ('/services/', 'Services listing'),
        ('/store/', 'Store listing'),
        ('/cart/', 'Shopping cart'),
        ('/profile/', 'User profile'),
        ('/my-bookings/', 'My bookings'),
        ('/orders/', 'Order history'),
        ('/contact/', 'Contact page'),
        ('/wishlist/', 'Wishlist'),
        ('/notifications/', 'Notifications'),
    ]
    
    for url, name in pages:
        response = client.get(url)
        if response.status_code == 200:
            print(f"✅ {name}")
            passed += 1
        else:
            print(f"❌ {name} - {response.status_code}")
            failed += 1
    
    # C. Data Consistency Tests
    print("\n📋 C. DATA CONSISTENCY (BANGLADESH)")
    print("-"*70)
    
    # Test services have prices
    services = Service.objects.all()
    all_have_prices = all(s.price > 0 for s in services)
    if all_have_prices:
        print(f"✅ All {services.count()} services have prices")
        passed += 1
    else:
        print(f"❌ Some services missing prices")
        failed += 1
    
    # Test store items have prices
    items = StoreItem.objects.all()
    all_items_have_prices = all(i.price > 0 for i in items)
    if all_items_have_prices:
        print(f"✅ All {items.count()} store items have prices")
        passed += 1
    else:
        print(f"❌ Some items missing prices")
        failed += 1
    
    # Test images exist
    services_with_images = sum(1 for s in services if s.image)
    if services_with_images == services.count():
        print(f"✅ All {services.count()} services have images")
        passed += 1
    else:
        print(f"⚠️  {services.count() - services_with_images} services missing images")
        failed += 1
    
    items_with_images = sum(1 for i in items if i.image)
    if items_with_images == items.count():
        print(f"✅ All {items.count()} store items have images")
        passed += 1
    else:
        print(f"⚠️  {items.count() - items_with_images} items missing images")
        failed += 1
    
    # D. Notification System
    print("\n📋 D. NOTIFICATION SYSTEM")
    print("-"*70)
    
    notifications = Notification.objects.all()
    if notifications.count() > 0:
        print(f"✅ {notifications.count()} notifications exist")
        passed += 1
    else:
        print("❌ No notifications found")
        failed += 1
    
    # Test notification API
    response = client.get('/api/notifications/')
    if response.status_code == 200:
        print("✅ Notification API works")
        passed += 1
    else:
        print(f"❌ Notification API failed - {response.status_code}")
        failed += 1
    
    # E. Admin Panel
    print("\n📋 E. ADMIN PANEL")
    print("-"*70)
    
    admin = User.objects.filter(is_superuser=True).first()
    if admin:
        admin_client = Client()
        admin_client.force_login(admin)
        
        response = admin_client.get('/admin/')
        if response.status_code == 200:
            print("✅ Admin panel accessible for superuser")
            passed += 1
        else:
            print(f"❌ Admin panel failed - {response.status_code}")
            failed += 1
        
        # Test regular user can't access
        regular_client = Client()
        regular_client.force_login(test_user)
        response = regular_client.get('/admin/')
        if response.status_code == 302:
            print("✅ Admin panel blocked for regular users")
            passed += 1
        else:
            print(f"❌ Admin panel not secured - {response.status_code}")
            failed += 1
    else:
        print("⚠️  No admin user found")
        failed += 1
    
    # F. Database Stats
    print("\n📋 F. DATABASE STATISTICS")
    print("-"*70)
    print(f"   Users: {User.objects.count()}")
    print(f"   Services: {Service.objects.count()}")
    print(f"   Store Items: {StoreItem.objects.count()}")
    print(f"   Service Categories: {ServiceCategory.objects.count()}")
    print(f"   Store Categories: {StoreCategory.objects.count()}")
    print(f"   Notifications: {Notification.objects.count()}")
    print(f"   Orders: {Order.objects.count()}")
    print(f"   Bookings: {Booking.objects.count()}")
    print(f"   Contact Inquiries: {Contact.objects.count()}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 QA CHECKLIST SUMMARY")
    print("="*70)
    print(f"Total Checks:   {passed + failed}")
    print(f"Passed:         {passed} ✅")
    print(f"Failed:         {failed} ❌")
    success_rate = (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
    print(f"Success Rate:   {success_rate:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL CHECKS PASSED! EventNest is ready for production.")
    else:
        print(f"\n⚠️  {failed} checks failed. Please review and fix.")
    
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == '__main__':
    success = run_qa_checklist()
    sys.exit(0 if success else 1)
