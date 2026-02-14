"""
EventNest Template Generator
Generates all production-ready templates for the platform
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'core', 'templates')

# Ensure directories exist
os.makedirs(os.path.join(TEMPLATES_DIR, 'services'), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'store'), exist_ok=True)
os.makedirs(os.path.join(TEMPLATES_DIR, 'registration'), exist_ok=True)

TEMPLATES = {
    'home.html': '''{% extends 'base.html' %}

{% block title %}Home - EventNest{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="hero">
    <div class="container">
        <div class="hero-content">
            <h1>Discover, Create & Manage Events Effortlessly</h1>
            <p>Your complete platform for event management, professional services, and premium merchandise.</p>
            <div class="hero-buttons">
                <a href="{% url 'all_services' %}" class="btn btn-primary">
                    <i class="bi bi-sparkles"></i> Explore Services
                </a>
                <a href="{% url 'all_store_items' %}" class="btn btn-secondary">
                    <i class="bi bi-shop"></i> Browse Store
                </a>
            </div>
        </div>
    </div>
</div>

<!-- Featured Services Section -->
<section class="section">
    <div class="container">
        <div class="section-title">
            <h2>Our Premium Services</h2>
            <p class="section-subtitle">Professional event services tailored to your needs</p>
        </div>
        
        <div class="grid grid-3">
            <div class="service-card">
                <div class="card-image-container">
                    <img src="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=400&h=250&fit=crop" alt="Event Planning">
                </div>
                <div class="card-body">
                    <div class="card-badge">Popular</div>
                    <h3 class="card-title">Event Planning</h3>
                    <p class="card-description">Complete event coordination and management from planning to execution.</p>
                    <a href="{% url 'all_services' %}" class="btn btn-primary" style="width: 100%; justify-content: center;">
                        View Services
                    </a>
                </div>
            </div>

            <div class="service-card">
                <div class="card-image-container">
                    <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=250&fit=crop" alt="Photography">
                </div>
                <div class="card-body">
                    <div class="card-badge">Professional</div>
                    <h3 class="card-title">Photography</h3>
                    <p class="card-description">Professional photographers capturing your special moments.</p>
                    <a href="{% url 'all_services' %}" class="btn btn-primary" style="width: 100%; justify-content: center;">
                        View Services
                    </a>
                </div>
            </div>

            <div class="service-card">
                <div class="card-image-container">
                    <img src="https://images.unsplash.com/photo-1555939594-58d7cb561404?w=400&h=250&fit=crop" alt="Catering">
                </div>
                <div class="card-body">
                    <div class="card-badge">Delicious</div>
                    <h3 class="card-title">Catering</h3>
                    <p class="card-description">Gourmet catering services for events of all sizes.</p>
                    <a href="{% url 'all_services' %}" class="btn btn-primary" style="width: 100%; justify-content: center;">
                        View Services
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Featured Products Section -->
<section class="section" style="background: rgba(99, 102, 241, 0.05);">
    <div class="container">
        <div class="section-title">
            <h2>Featured Products</h2>
            <p class="section-subtitle">Curated merchandise and event packages</p>
        </div>
        
        {% if featured_items %}
        <div class="grid grid-4">
            {% for item in featured_items %}
            <div class="product-card">
                <div class="card-image-container">
                    <img src="{{ item.image.url }}" alt="{{ item.name }}">
                </div>
                <div class="card-body">
                    <h3 class="card-title">{{ item.name }}</h3>
                    <p class="card-description">{{ item.description|truncatewords:15 }}</p>
                    <div class="card-footer">
                        <div class="card-price">${{ item.price }}</div>
                        <a href="{% url 'store_item_detail' item.id %}" class="btn btn-primary btn-small">
                            View
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <p>No products available at the moment.</p>
        </div>
        {% endif %}

        <div style="text-align: center; margin-top: var(--spacing-3xl);">
            <a href="{% url 'all_store_items' %}" class="btn btn-primary">
                <i class="bi bi-arrow-right"></i> Explore Full Store
            </a>
        </div>
    </div>
</section>

<!-- Why Choose EventNest Section -->
<section class="section">
    <div class="container">
        <div class="section-title">
            <h2>Why Choose EventNest?</h2>
            <p class="section-subtitle">Everything you need for a successful event</p>
        </div>
        
        <div class="grid grid-4">
            <div class="card">
                <div style="text-align: center; padding: var(--spacing-xl) 0;">
                    <div style="font-size: 3rem; color: var(--primary); margin-bottom: var(--spacing-md);">
                        <i class="bi bi-shield-check"></i>
                    </div>
                    <h4 style="margin-bottom: var(--spacing-md);">100% Verified</h4>
                    <p>All service providers and products are verified for quality.</p>
                </div>
            </div>

            <div class="card">
                <div style="text-align: center; padding: var(--spacing-xl) 0;">
                    <div style="font-size: 3rem; color: var(--accent-blue); margin-bottom: var(--spacing-md);">
                        <i class="bi bi-lightning-fill"></i>
                    </div>
                    <h4 style="margin-bottom: var(--spacing-md);">Fast & Easy</h4>
                    <p>Quick booking and seamless checkout process.</p>
                </div>
            </div>

            <div class="card">
                <div style="text-align: center; padding: var(--spacing-xl) 0;">
                    <div style="font-size: 3rem; color: var(--accent-teal); margin-bottom: var(--spacing-md);">
                        <i class="bi bi-headset"></i>
                    </div>
                    <h4 style="margin-bottom: var(--spacing-md);">24/7 Support</h4>
                    <p>Our dedicated support team is always ready to help.</p>
                </div>
            </div>

            <div class="card">
                <div style="text-align: center; padding: var(--spacing-xl) 0;">
                    <div style="font-size: 3rem; color: var(--accent-pink); margin-bottom: var(--spacing-md);">
                        <i class="bi bi-award"></i>
                    </div>
                    <h4 style="margin-bottom: var(--spacing-md);">Best Quality</h4>
                    <p>Premium services and products for exceptional events.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="section" style="background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%); color: white;">
    <div class="container" style="text-align: center;">
        <h2 style="color: white; margin-bottom: var(--spacing-xl);">Ready to Create Your Perfect Event?</h2>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: var(--spacing-2xl); font-size: 1.1rem;">
            Join thousands of customers who have made their events unforgettable with EventNest.
        </p>
        <a href="{% url 'all_services' %}" class="btn btn-secondary">
            Start Planning Today
        </a>
    </div>
</section>
{% endblock %}
''',

    'services/all_services.html': '''{% extends 'base.html' %}

{% block title %}Services - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-xl);">Professional Event Services</h1>
        
        <!-- Search & Filter -->
        <div class="search-bar">
            <div class="search-input-group">
                <i class="bi bi-search search-icon"></i>
                <input type="text" placeholder="Search services..." id="searchInput">
            </div>
        </div>

        <!-- Services Grid -->
        <div class="grid grid-3">
            {% for service in services %}
            <div class="service-card">
                <div class="card-image-container">
                    <img src="{{ service.image.url }}" alt="{{ service.title }}">
                </div>
                <div class="card-body">
                    <h3 class="card-title">{{ service.title }}</h3>
                    <p class="card-description">{{ service.description|truncatewords:20 }}</p>
                    <div class="card-meta">
                        <div class="card-meta-item">
                            <i class="bi bi-tag"></i>
                            {{ service.category.name }}
                        </div>
                        <div class="card-meta-item">
                            <i class="bi bi-star"></i>
                            4.8 (120 reviews)
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="card-price">${{ service.price }}</div>
                        <a href="{% url 'service_detail' service.id %}" class="btn btn-primary btn-small">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="empty-state" style="grid-column: 1 / -1;">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p>No services available at the moment.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<script>
    // Simple search functionality
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.service-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
</script>
{% endblock %}
''',

    'services/service_detail.html': '''{% extends 'base.html' %}

{% block title %}{{ service.title }} - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div class="flex" style="gap: var(--spacing-2xl); margin-bottom: var(--spacing-3xl);">
            <!-- Image -->
            <div style="flex: 1; min-width: 0;">
                <img src="{{ service.image.url }}" alt="{{ service.title }}" style="width: 100%; border-radius: var(--radius-xl); object-fit: cover; height: 400px;">
            </div>

            <!-- Details -->
            <div style="flex: 1;">
                <div class="card-badge">{{ service.category.name }}</div>
                <h1 style="margin-top: var(--spacing-md);">{{ service.title }}</h1>
                
                <div class="flex" style="gap: var(--spacing-lg); margin: var(--spacing-xl) 0; align-items: center;">
                    <div>
                        <div style="font-size: 2rem; color: var(--primary); font-weight: 700;">${{ service.price }}</div>
                        <p style="color: var(--text-tertiary);">Starting from</p>
                    </div>
                    <div style="border-left: 2px solid var(--bg-tertiary); padding-left: var(--spacing-lg);">
                        <div class="flex" style="gap: var(--spacing-sm); align-items: center;">
                            <i class="bi bi-star-fill" style="color: var(--warning); font-size: 1.2rem;"></i>
                            <span style="font-weight: 600;">4.8 out of 5</span>
                        </div>
                        <p style="color: var(--text-tertiary); font-size: 0.9rem;">Based on 120+ reviews</p>
                    </div>
                </div>

                <div style="background: var(--bg-secondary); padding: var(--spacing-lg); border-radius: var(--radius-lg); margin-bottom: var(--spacing-xl);">
                    <h4 style="margin-bottom: var(--spacing-md);">What's Included:</h4>
                    <ul style="list-style: none; display: flex; flex-direction: column; gap: var(--spacing-sm);">
                        <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-sm);"></i>Professional team</li>
                        <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-sm);"></i>Full support</li>
                        <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-sm);"></i>Premium quality</li>
                    </ul>
                </div>

                <a href="{% url 'contact' %}" class="btn btn-primary" style="width: 100%; justify-content: center; padding: var(--spacing-lg);">
                    <i class="bi bi-chat-dots"></i> Request a Quote
                </a>
            </div>
        </div>

        <!-- Description -->
        <div class="card">
            <h3>About This Service</h3>
            <p>{{ service.description }}</p>
            
            <h4 style="margin-top: var(--spacing-xl);">Key Features</h4>
            <div class="grid grid-2">
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-check"></i> Quality Assured
                    </h5>
                    <p>All our services meet the highest industry standards.</p>
                </div>
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-check"></i> Customizable
                    </h5>
                    <p>Packages can be tailored to your specific needs.</p>
                </div>
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-check"></i> On-Time Delivery
                    </h5>
                    <p>We guarantee punctual and reliable service delivery.</p>
                </div>
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-check"></i> Expert Team
                    </h5>
                    <p>Experienced professionals dedicated to your success.</p>
                </div>
            </div>
        </div>

        <!-- Reviews -->
        <div class="card" style="margin-top: var(--spacing-2xl);">
            <h3>Customer Reviews</h3>
            <div style="display: flex; flex-direction: column; gap: var(--spacing-xl); margin-top: var(--spacing-xl);">
                <div style="padding: var(--spacing-lg); background: var(--bg-secondary); border-radius: var(--radius-lg);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: var(--spacing-md);">
                        <div>
                            <p style="font-weight: 600; margin-bottom: var(--spacing-xs);">John Doe</p>
                            <div style="display: flex; gap: var(--spacing-xs);">
                                {% for i in "12345" %}
                                <i class="bi bi-star-fill" style="color: var(--warning);"></i>
                                {% endfor %}
                            </div>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-tertiary);">2 weeks ago</p>
                    </div>
                    <p>"Absolutely fantastic service! Would recommend to anyone."</p>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''',

    'store/all_items.html': '''{% extends 'base.html' %}

{% block title %}Store - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-xl);">EventNest Store</h1>
        
        <!-- Search & Filter -->
        <div class="search-bar">
            <div class="search-input-group">
                <i class="bi bi-search search-icon"></i>
                <form method="get" style="width: 100%;">
                    <input type="text" name="q" placeholder="Search products..." value="{{ request.GET.q }}" style="width: 100%;">
                </form>
            </div>
        </div>

        <!-- Categories Filter -->
        <div class="filters">
            <a href="{% url 'all_store_items' %}" class="filter-btn {% if not request.GET.category %}active{% endif %}">
                All Categories
            </a>
            {% for category in categories %}
            <a href="?category={{ category.id }}" class="filter-btn {% if request.GET.category == category.id|stringformat:'s' %}active{% endif %}">
                {{ category.name }}
            </a>
            {% endfor %}
        </div>

        <!-- Products Grid -->
        <div class="grid grid-4">
            {% for item in items %}
            <div class="product-card">
                <div class="card-image-container">
                    <img src="{{ item.image.url }}" alt="{{ item.name }}">
                </div>
                <div class="card-body">
                    <p style="font-size: 0.85rem; color: var(--text-tertiary); margin-bottom: var(--spacing-sm);">
                        {{ item.category.name }}
                    </p>
                    <h3 class="card-title">{{ item.name }}</h3>
                    <p class="card-description">{{ item.description|truncatewords:15 }}</p>
                    <div class="flex" style="gap: var(--spacing-sm); color: var(--success); font-size: 0.9rem; margin: var(--spacing-md) 0;">
                        {% if item.stock > 0 %}
                            <i class="bi bi-check-circle"></i>
                            <span>{{ item.stock }} in stock</span>
                        {% else %}
                            <i class="bi bi-exclamation-circle" style="color: var(--warning);"></i>
                            <span>Out of stock</span>
                        {% endif %}
                    </div>
                    <div class="card-footer">
                        <div class="card-price">${{ item.price }}</div>
                        <a href="{% url 'store_item_detail' item.id %}" class="btn btn-primary btn-small">
                            View
                        </a>
                    </div>
                </div>
            </div>
            {% empty %}
            <div class="empty-state" style="grid-column: 1 / -1;">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p>No products found.</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
''',

    'store/item_detail.html': '''{% extends 'base.html' %}

{% block title %}{{ item.name }} - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div class="flex" style="gap: var(--spacing-2xl); margin-bottom: var(--spacing-3xl);">
            <!-- Image -->
            <div style="flex: 1; min-width: 0;">
                <img src="{{ item.image.url }}" alt="{{ item.name }}" style="width: 100%; border-radius: var(--radius-xl); object-fit: cover; height: 400px;">
            </div>

            <!-- Details -->
            <div style="flex: 1;">
                <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-md);">
                    <i class="bi bi-tag"></i> {{ item.category.name }}
                </p>
                <h1>{{ item.name }}</h1>
                
                <div style="margin: var(--spacing-xl) 0;">
                    <div style="font-size: 2.5rem; color: var(--primary); font-weight: 700; margin-bottom: var(--spacing-md);">
                        ${{ item.price }}
                    </div>
                    <div class="flex" style="gap: var(--spacing-md); align-items: center;">
                        <div class="flex" style="gap: var(--spacing-xs);">
                            {% for i in "12345" %}
                            <i class="bi bi-star-fill" style="color: var(--warning);"></i>
                            {% endfor %}
                        </div>
                        <p style="color: var(--text-tertiary);">(95 reviews)</p>
                    </div>
                </div>

                <div style="background: var(--bg-secondary); padding: var(--spacing-lg); border-radius: var(--radius-lg); margin-bottom: var(--spacing-xl);">
                    <div class="flex" style="gap: var(--spacing-md); align-items: center;">
                        <div>
                            {% if item.stock > 0 %}
                            <p style="color: var(--success); font-weight: 600;">
                                <i class="bi bi-check-circle-fill"></i> In Stock
                            </p>
                            <p style="font-size: 0.9rem; color: var(--text-tertiary);">Only {{ item.stock }} left!</p>
                            {% else %}
                            <p style="color: var(--error); font-weight: 600;">
                                <i class="bi bi-x-circle-fill"></i> Out of Stock
                            </p>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <form method="post" action="{% url 'add_to_cart' item.id %}" style="display: flex; gap: var(--spacing-md);">
                    {% csrf_token %}
                    <input type="number" name="quantity" value="1" min="1" max="{{ item.stock }}" style="width: 100px;">
                    <button type="submit" class="btn btn-primary" {% if item.stock == 0 %}disabled{% endif %} style="flex: 1;">
                        <i class="bi bi-bag-plus"></i> Add to Cart
                    </button>
                </form>
            </div>
        </div>

        <!-- Description -->
        <div class="card">
            <h3>Product Details</h3>
            <p>{{ item.description }}</p>
            
            <h4 style="margin-top: var(--spacing-xl); margin-bottom: var(--spacing-md);">Features</h4>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: var(--spacing-md);">
                <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-md);"></i>High-quality materials</li>
                <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-md);"></i>Durable and long-lasting</li>
                <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-md);"></i>Free shipping on orders over $50</li>
                <li><i class="bi bi-check-circle-fill" style="color: var(--success); margin-right: var(--spacing-md);"></i>30-day money-back guarantee</li>
            </ul>
        </div>

        <!-- Shipping Info -->
        <div class="card" style="margin-top: var(--spacing-2xl);">
            <h3>Shipping & Returns</h3>
            <div class="grid grid-2">
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-truck"></i> Free Shipping
                    </h5>
                    <p>On orders over $50. Standard delivery 3-5 business days.</p>
                </div>
                <div>
                    <h5 style="color: var(--primary); margin-bottom: var(--spacing-sm);">
                        <i class="bi bi-arrow-repeat"></i> Easy Returns
                    </h5>
                    <p>30-day return policy. No questions asked.</p>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''',

    'store/cart.html': '''{% extends 'base.html' %}

{% block title %}Shopping Cart - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-2xl);">Shopping Cart</h1>

        {% if cart_items %}
        <div class="grid" style="grid-template-columns: 1fr 350px; gap: var(--spacing-2xl);">
            <!-- Cart Items -->
            <div>
                <div class="card">
                    {% for cart_item in cart_items %}
                    <div style="display: flex; gap: var(--spacing-lg); padding: var(--spacing-lg); border-bottom: 1px solid var(--bg-tertiary); align-items: start;">
                        {% if cart_item.item.image %}
                        <img src="{{ cart_item.item.image.url }}" alt="{{ cart_item.item.name }}" style="width: 120px; height: 120px; border-radius: var(--radius-lg); object-fit: cover;">
                        {% endif %}
                        <div style="flex: 1;">
                            <h4 style="margin-bottom: var(--spacing-sm);">{{ cart_item.item.name }}</h4>
                            <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-md);">{{ cart_item.item.category.name }}</p>
                            
                            <form method="post" action="{% url 'update_cart' cart_item.id %}" style="margin-bottom: var(--spacing-md);">
                                {% csrf_token %}
                                <div class="flex" style="gap: var(--spacing-sm); align-items: center;">
                                    <label>Qty:</label>
                                    <input type="number" name="quantity" value="{{ cart_item.quantity }}" min="1" max="{{ cart_item.item.stock }}" style="width: 70px;">
                                    <button type="submit" class="btn btn-small btn-ghost">Update</button>
                                </div>
                            </form>

                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <p style="font-weight: 600; font-size: 1.1rem; color: var(--primary);">
                                    ${{ cart_item.get_total }}
                                </p>
                                <a href="{% url 'remove_from_cart' cart_item.id %}" class="btn btn-small" style="color: var(--error); background: rgba(239, 68, 68, 0.1);">
                                    <i class="bi bi-trash"></i> Remove
                                </a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Order Summary -->
            <div>
                <div class="card">
                    <h4 style="margin-bottom: var(--spacing-lg);">Order Summary</h4>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: var(--spacing-md);">
                        <p>Subtotal</p>
                        <p style="font-weight: 600;">${{ total }}</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: var(--spacing-md);">
                        <p>Shipping</p>
                        <p style="font-weight: 600;">Free</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding-top: var(--spacing-lg); border-top: 1px solid var(--bg-tertiary); margin-bottom: var(--spacing-xl);">
                        <p style="font-weight: 600; font-size: 1.1rem;">Total</p>
                        <p style="font-weight: 600; font-size: 1.1rem; color: var(--primary);">${{ total }}</p>
                    </div>

                    <a href="{% url 'checkout' %}" class="btn btn-primary" style="width: 100%; justify-content: center;">
                        <i class="bi bi-credit-card"></i> Proceed to Checkout
                    </a>
                    <a href="{% url 'all_store_items' %}" class="btn btn-ghost" style="width: 100%; justify-content: center; margin-top: var(--spacing-md);">
                        Continue Shopping
                    </a>
                </div>
            </div>
        </div>
        {% else %}
        <div class="card">
            <div class="empty-state">
                <i class="bi bi-bag" style="font-size: 4rem; margin-bottom: var(--spacing-lg);"></i>
                <h3>Your cart is empty</h3>
                <p style="margin-bottom: var(--spacing-xl);">Start adding items to get started!</p>
                <a href="{% url 'all_store_items' %}" class="btn btn-primary">
                    <i class="bi bi-shop"></i> Continue Shopping
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</section>
{% endblock %}
''',

    'registration/login.html': '''{% extends 'base.html' %}

{% block title %}Login - EventNest{% endblock %}

{% block content %}
<section class="section" style="display: flex; align-items: center; justify-content: center; min-height: 600px;">
    <div class="card" style="max-width: 450px; width: 100%;">
        <div style="text-align: center; margin-bottom: var(--spacing-2xl);">
            <h1 style="font-size: 2rem; margin-bottom: var(--spacing-md);">Welcome Back</h1>
            <p style="color: var(--text-secondary);">Sign in to your EventNest account</p>
        </div>

        <form method="post" style="display: flex; flex-direction: column; gap: var(--spacing-lg);">
            {% csrf_token %}

            {% if form.non_field_errors %}
            <div class="alert alert-error">
                {% for error in form.non_field_errors %}
                <p>{{ error }}</p>
                {% endfor %}
            </div>
            {% endif %}

            <div class="form-group">
                <label for="{{ form.username.id_for_label }}">Email or Username</label>
                {{ form.username }}
                {% if form.username.errors %}
                <div class="form-error">{{ form.username.errors.0 }}</div>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="{{ form.password.id_for_label }}">Password</label>
                {{ form.password }}
                {% if form.password.errors %}
                <div class="form-error">{{ form.password.errors.0 }}</div>
                {% endif %}
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%; padding: var(--spacing-lg);">
                Sign In
            </button>
        </form>

        <div style="text-align: center; margin-top: var(--spacing-2xl); padding-top: var(--spacing-xl); border-top: 1px solid var(--bg-tertiary);">
            <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">Don't have an account?</p>
            <a href="{% url 'signup' %}" class="btn btn-ghost" style="width: 100%; justify-content: center;">
                Create Account
            </a>
        </div>
    </div>
</section>
{% endblock %}
''',

    'registration/signup.html': '''{% extends 'base.html' %}

{% block title %}Sign Up - EventNest{% endblock %}

{% block content %}
<section class="section" style="display: flex; align-items: center; justify-content: center; min-height: 600px;">
    <div class="card" style="max-width: 500px; width: 100%;">
        <div style="text-align: center; margin-bottom: var(--spacing-2xl);">
            <h1 style="font-size: 2rem; margin-bottom: var(--spacing-md);">Create Account</h1>
            <p style="color: var(--text-secondary);">Join EventNest and start managing events</p>
        </div>

        <form method="post" style="display: flex; flex-direction: column; gap: var(--spacing-lg);">
            {% csrf_token %}

            {% if form.non_field_errors %}
            <div class="alert alert-error">
                {% for error in form.non_field_errors %}
                <p>{{ error }}</p>
                {% endfor %}
            </div>
            {% endif %}

            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="full_name" placeholder="John Doe" required>
            </div>

            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" placeholder="john@example.com" required>
            </div>

            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="johndoe" required>
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="••••••••" required>
            </div>

            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" name="password_confirm" placeholder="••••••••" required>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%; padding: var(--spacing-lg);">
                Create Account
            </button>
        </form>

        <div style="text-align: center; margin-top: var(--spacing-2xl); padding-top: var(--spacing-xl); border-top: 1px solid var(--bg-tertiary);">
            <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">Already have an account?</p>
            <a href="{% url 'login' %}" class="btn btn-ghost" style="width: 100%; justify-content: center;">
                Sign In
            </a>
        </div>
    </div>
</section>
{% endblock %}
''',
}

def create_templates():
    """Create all template files"""
    for filename, content in TEMPLATES.items():
        filepath = os.path.join(TEMPLATES_DIR, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Created {filename}")

if __name__ == '__main__':
    create_templates()
    print("\n✓ All templates created successfully!")
