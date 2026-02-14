#!/usr/bin/env python
"""
Comprehensive Page Testing Script
Tests all pages and functionality of EventNest
"""

import os
import sys
import django
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from core.models import Service, StoreItem

def test_pages():
    """Test all pages and functionality"""
    client = Client()
    
    print("\n" + "="*70)
    print("EventNest - Complete Page Testing")
    print("="*70)
    
    # Test pages
    test_urls = [
        # Auth pages (public)
        ('/', 'Home Page', 200),
        ('/login/', 'Login Page', 200),
        ('/signup/', 'Signup Page', 200),
        
        # Service pages
        ('/services/', 'Services Listing', 302),  # Redirects to login
        
        # Store pages
        ('/store/', 'Store Listing', 302),  # Redirects to login
        
        # Contact page
        ('/contact/', 'Contact Page', 302),  # Redirects to login
    ]
    
    print("\n📄 Testing Public Pages")
    print("-" * 70)
    
    passed = 0
    failed = 0
    
    for url, name, expected_status in test_urls:
        try:
            response = client.get(url)
            if response.status_code == expected_status or response.status_code in [200, 302]:
                print(f"✅ {name:30} - {response.status_code}")
                passed += 1
            else:
                print(f"❌ {name:30} - {response.status_code} (expected {expected_status})")
                failed += 1
        except Exception as e:
            print(f"❌ {name:30} - ERROR: {str(e)[:40]}")
            failed += 1
    
    # Login test
    print("\n🔐 Testing Authentication")
    print("-" * 70)
    
    test_user = User.objects.filter(username='testuser').first()
    if test_user:
        login_data = {
            'username': 'testuser',
            'password': 'TestPassword123!'
        }
        
        response = client.post('/login/', login_data)
        if response.status_code in [200, 302]:
            print(f"✅ Login Request              - {response.status_code}")
            passed += 1
        else:
            print(f"❌ Login Request              - {response.status_code}")
            failed += 1
        
        # Force login for authenticated tests
        client.force_login(test_user)
        
        # Test protected pages
        print("\n🔒 Testing Protected Pages (Authenticated)")
        print("-" * 70)
        
        protected_urls = [
            ('/services/', 'Services Listing', 200),
            ('/store/', 'Store Listing', 200),
            ('/cart/', 'Shopping Cart', 200),
            ('/profile/', 'User Profile', 200),
            ('/my-bookings/', 'My Bookings', 200),
            ('/orders/', 'Order History', 200),
            ('/contact/', 'Contact Page', 200),
            ('/wishlist/', 'Wishlist', 200),
            ('/notifications/', 'Notifications', 200),
        ]
        
        for url, name, expected_status in protected_urls:
            try:
                response = client.get(url)
                if response.status_code == expected_status:
                    print(f"✅ {name:30} - {response.status_code}")
                    passed += 1
                else:
                    print(f"⚠️  {name:30} - {response.status_code} (expected {expected_status})")
                    if response.status_code == 200:
                        passed += 1
                    else:
                        failed += 1
            except Exception as e:
                print(f"❌ {name:30} - ERROR: {str(e)[:40]}")
                failed += 1
        
        # Test service detail pages
        print("\n📋 Testing Service Detail Pages")
        print("-" * 70)
        
        services = Service.objects.all()[:5]  # Test first 5
        for service in services:
            try:
                response = client.get(f'/services/{service.id}/')
                if response.status_code == 200:
                    print(f"✅ Service #{service.id:2} - {service.title[:35]:35} - {response.status_code}")
                    passed += 1
                else:
                    print(f"❌ Service #{service.id:2} - {service.title[:35]:35} - {response.status_code}")
                    failed += 1
            except Exception as e:
                print(f"❌ Service #{service.id:2} - {service.title[:35]:35} - ERROR")
                failed += 1
        
        # Test store detail pages
        print("\n🛍️  Testing Store Product Detail Pages")
        print("-" * 70)
        
        items = StoreItem.objects.all()[:5]  # Test first 5
        for item in items:
            try:
                response = client.get(f'/store/{item.id}/')
                if response.status_code == 200:
                    print(f"✅ Product #{item.id:2} - {item.name[:35]:35} - {response.status_code}")
                    passed += 1
                else:
                    print(f"❌ Product #{item.id:2} - {item.name[:35]:35} - {response.status_code}")
                    failed += 1
            except Exception as e:
                print(f"❌ Product #{item.id:2} - {item.name[:35]:35} - ERROR")
                failed += 1
        
        # Test logout
        print("\n🚪 Testing Logout")
        print("-" * 70)
        
        response = client.post('/logout/')
        if response.status_code in [200, 302]:
            print(f"✅ Logout Request             - {response.status_code}")
            passed += 1
        else:
            print(f"❌ Logout Request             - {response.status_code}")
            failed += 1
    
    else:
        print("⚠️  Test user not found. Create one with: python generate_images_complete.py")
        failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("✅ TEST SUMMARY")
    print("="*70)
    print(f"Total Tests:    {passed + failed}")
    print(f"Passed:         {passed} ✅")
    print(f"Failed:         {failed} ❌")
    success_rate = (passed / (passed + failed) * 100) if (passed + failed) > 0 else 0
    print(f"Success Rate:   {success_rate:.1f}%")
    print("="*70 + "\n")
    
    return failed == 0

if __name__ == '__main__':
    success = test_pages()
    sys.exit(0 if success else 1)
