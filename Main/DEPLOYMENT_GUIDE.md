# EventNest Deployment Guide

> **Production-ready deployment instructions for EventNest**

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Vercel Deployment](#vercel-deployment)
3. [Railway Deployment](#railway-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Security Hardening](#security-hardening)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] No console errors in development
- [ ] Static files collecting properly
- [ ] Environment variables configured
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured
- [ ] SECRET_KEY is secret and strong

### Database
- [ ] Migrations applied
- [ ] Data backup created
- [ ] Database indices optimized
- [ ] Superuser created

### Assets
- [ ] Static files collected
- [ ] Media files organized
- [ ] CSS/JS minified
- [ ] Images optimized

### Security
- [ ] HTTPS enabled
- [ ] CSRF protection enabled
- [ ] Security headers set
- [ ] Rate limiting configured
- [ ] Input validation complete

---

## Vercel Deployment

Vercel is **NOT recommended** for Django applications as it doesn't support traditional Python processes. Use Railway or Heroku instead.

---

## Railway Deployment

Railway.app is an excellent choice for Django deployments.

### Step 1: Prepare Your Project

1. **Ensure requirements.txt is updated**
   ```bash
   pip freeze > requirements.txt
   ```

2. **Create a Procfile**
   ```
   release: python manage.py migrate
   web: gunicorn myproject.wsgi
   ```

3. **Add gunicorn to requirements.txt**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

4. **Update settings.py for production**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-railway-url.railway.app']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

### Step 2: Connect to Railway

1. Install Railway CLI
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway
   ```bash
   railway login
   ```

3. Create a new Railway project
   ```bash
   railway init
   ```

### Step 3: Configure Environment Variables

In Railway dashboard, add:
```
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
DATABASE_URL=your-postgres-url
ALLOWED_HOSTS=your-railway-url.railway.app
```

### Step 4: Connect Database

1. In Railway dashboard, add PostgreSQL service
2. Copy the DATABASE_URL
3. Update your settings.py to use DATABASE_URL

### Step 5: Deploy

```bash
railway up
```

---

## Heroku Deployment

### Step 1: Setup Heroku

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

### Step 2: Prepare Project

1. **Create Procfile** (if not exists)
   ```
   release: python manage.py migrate
   web: gunicorn myproject.wsgi
   ```

2. **Create runtime.txt**
   ```
   python-3.11.7
   ```

3. **Install production dependencies**
   ```bash
   pip install gunicorn whitenoise dj-database-url psycopg2-binary
   pip freeze > requirements.txt
   ```

### Step 3: Update Settings

```python
# settings.py
import dj_database_url
import os

DEBUG = False

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Allowed hosts
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'www.your-app-name.herokuapp.com']

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}
```

### Step 4: Add Add-ons

```bash
# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis (optional, for caching)
heroku addons:create heroku-redis:premium-0
```

### Step 5: Configure Environment Variables

```bash
heroku config:set DEBUG=False
heroku config:set DJANGO_SECRET_KEY=your-secret-key-here
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

### Step 6: Deploy

```bash
git push heroku main
```

### Step 7: Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic
```

### Step 8: View Logs

```bash
heroku logs --tail
```

---

## Environment Configuration

### Create .env file (for local development)

```env
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (optional)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Stripe (optional)
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
```

### Load .env in settings.py

```python
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```

---

## Database Setup

### PostgreSQL (Recommended for Production)

1. **Install psycopg2**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update settings.py**
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default='postgresql://user:password@localhost:5432/eventnest'
       )
   }
   ```

3. **Create database**
   ```bash
   createdb eventnest
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

### Database Backups

#### PostgreSQL Backup
```bash
pg_dump eventnest > backup.sql
```

#### Restore from Backup
```bash
psql eventnest < backup.sql
```

#### Automated Backups (Heroku)
```bash
heroku pg:backups:schedule DATABASE_URL --at '02:00 UTC'
```

---

## Security Hardening

### 1. Update settings.py for Production

```python
# SECURITY SETTINGS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", 'cdn.jsdelivr.net'),
    'style-src': ("'self'", 'cdn.jsdelivr.net'),
    'img-src': ("'self'", 'data:', 'https:'),
}
```

### 2. Setup HTTPS

- Use Let's Encrypt with Certbot
- Or use Heroku's automatic HTTPS
- Or CloudFlare for free SSL

### 3. Database Security

```python
# Use environment variables for credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### 4. API Rate Limiting

```bash
pip install django-ratelimit
```

### 5. Firewall Rules

Configure your server firewall:
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block all other ports
sudo ufw default deny incoming
```

---

## Monitoring & Maintenance

### Setup Error Tracking

#### With Sentry
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=False
)
```

### Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Health Checks

Create a health check endpoint:

```python
# views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now()
    })

# urls.py
path('health/', health_check, name='health_check'),
```

### Scheduled Tasks (Celery)

Setup Celery for background tasks:

```bash
pip install celery redis
```

```python
# celery.py
from celery import Celery

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

---

## Post-Deployment Checklist

- [ ] Test all features
- [ ] Check admin panel works
- [ ] Verify static files loading
- [ ] Test media file uploads
- [ ] Check email sending
- [ ] Monitor error logs
- [ ] Test database backups
- [ ] Verify SSL/HTTPS working
- [ ] Test on mobile devices
- [ ] Monitor performance

---

## Troubleshooting

### Database Connection Error

```bash
# Check DATABASE_URL format
heroku config:get DATABASE_URL

# Test connection
python manage.py dbshell
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
heroku run python manage.py collectstatic
```

### Permission Denied Errors

```bash
# Check file permissions
ls -la /path/to/project

# Fix permissions
chmod -R 755 media/
chmod -R 755 staticfiles/
```

### Memory Issues

```bash
# Upgrade dyno size (Heroku)
heroku ps:type web=standard-2x

# Monitor memory usage
heroku ps
```

---

## Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- Heroku Django: https://devcenter.heroku.com/articles/getting-started-with-python
- Railway Documentation: https://docs.railway.app/
- Security: https://docs.djangoproject.com/en/stable/topics/security/

---

**Last Updated**: December 2024
**Version**: 1.0.0
