# EventNest Login/Logout - Quick Start Guide

## ✅ Status: Fully Operational

Login and logout functionality is now working properly with comprehensive error handling, validation, and security features.

---

## How to Test Login/Logout

### 1. **Create a Test Account**
```bash
cd D:\EventNest\Main
python manage.py shell
```

```python
from django.contrib.auth.models import User
from core.models import UserProfile, Cart

# Create user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='TestPassword123!'
)

# Create profile
UserProfile.objects.create(
    user=user,
    full_name='Test User',
    phone='+880XXXXXXXXXX',
    address='Dhaka, Bangladesh'
)

# Create cart
Cart.objects.create(user=user)

# Exit shell
exit()
```

### 2. **Test in Browser**
Start the server:
```bash
cd D:\EventNest\Main
python manage.py runserver 127.0.0.1:8000
```

Visit: `http://127.0.0.1:8000/`

#### **Login Steps:**
1. Click "Login" button in navbar (top right)
2. Enter username: `testuser`
3. Enter password: `TestPassword123!`
4. Click "Sign In"
5. ✅ Should redirect to home page (logged in state)

#### **Verify Authentication:**
1. Click "Services" in navbar
2. Should see all services page (requires authentication)
3. Click user dropdown (top right)
4. Should show profile and logout options

#### **Logout Steps:**
1. Click user profile dropdown (top right)
2. Click "Logout"
3. ✅ Should redirect to home (logged out state)
4. Click "Services" again
5. Should redirect to login page (no access)

---

## Run Automated Tests

```bash
cd D:\EventNest\Main
python test_authentication.py
```

Expected output shows ✅ for all tests:
- ✅ User signup
- ✅ Login with correct credentials
- ✅ Authenticated user access
- ✅ Logout functionality
- ✅ Unauthenticated redirect
- ✅ Login rejection for wrong password

---

## What Was Fixed

### ✅ Login View
- Added proper input validation
- Better error messages
- Handles missing username/password

### ✅ Logout View
- Only accepts POST requests (security)
- Properly destroys session
- Displays success message

### ✅ Login Template
- Fixed form rendering
- Proper message display
- CSRF token protection

### ✅ Image Handling
- Fixed missing image errors
- Shows placeholder when image unavailable
- Services and store pages render correctly

### ✅ Authentication Decorators
- `@login_required` on all protected pages
- Redirects to login for unauthorized users
- Works on services, store, profile, bookings, etc.

---

## Test Credentials

**Test Account 1:**
- Username: `testuser`
- Password: `TestPassword123!`
- Email: `test@example.com`

**Bangladesh Format Phone:**
- Format: `+880XXXXXXXXXX`
- Example: `+8801700000000`

---

## Security Features Enabled

✅ **Session Management**
- Secure session cookies
- Database-backed sessions
- 7-day session timeout

✅ **CSRF Protection**
- All forms have CSRF tokens
- POST-only logout (prevents accidental logout)

✅ **Password Security**
- PBKDF2 hashing
- Django's built-in validation
- Password confirmation on signup

✅ **Route Protection**
- `@login_required` on all main pages
- Automatic redirect to login
- Prevents unauthorized access

---

## Common Issues & Solutions

### "Invalid username or password"
- Check username is exactly correct
- Verify password matches exactly
- Create new user if needed

### Logout button not working
- Make sure using navbar logout (not direct URL)
- Check browser has cookies enabled
- Clear cache and cookies if needed

### Can't access services page when not logged in
- This is correct behavior! (Page protected)
- Login first, then try again
- See message redirecting to login

### Password reset needed
- Currently manual reset only
- Contact admin for password reset
- Or delete and recreate user account

---

## Next Steps (Optional)

1. **Signup Form Enhancement**
   - Currently requires manual user creation for testing
   - Signup form can be improved with better validation

2. **Password Reset**
   - Add forgot password functionality
   - Email-based password recovery

3. **Two-Factor Authentication**
   - Additional security layer
   - SMS or email verification

4. **Social Login**
   - Google/Facebook OAuth
   - Optional convenience feature

---

## File Changes Summary

**Modified Files:**
- `core/views.py` - Fixed login/logout views
- `core/templates/registration/login.html` - Fixed form rendering
- `core/templates/registration/signup.html` - Rewrote with all fields
- `core/templates/services/all_services.html` - Fixed image display
- `core/templates/store/all_items.html` - Fixed image display
- `myproject/settings.py` - Added testserver to ALLOWED_HOSTS

**New Files:**
- `test_authentication.py` - Authentication test suite
- `AUTHENTICATION_FIX_REPORT.md` - Detailed fix documentation

---

## Command Reference

```bash
# Start server
python manage.py runserver 127.0.0.1:8000

# Create test user
python manage.py shell
# Then use create_user code above

# Run tests
python test_authentication.py

# View current users
python manage.py shell
from django.contrib.auth.models import User
User.objects.all()
```

---

## Support

For issues or questions:
1. Check `AUTHENTICATION_FIX_REPORT.md` for detailed information
2. Review test results in `test_authentication.py`
3. Check browser console for JavaScript errors
4. Verify server is running on `http://127.0.0.1:8000/`

---

**Status**: ✅ **Authentication Fully Operational**  
**Version**: 1.0  
**Last Updated**: December 10, 2025  
**Repository**: https://github.com/Prohar04/EventNest
