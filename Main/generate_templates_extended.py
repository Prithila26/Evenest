"""
Generate remaining templates for EventNest
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'core', 'templates')

os.makedirs(os.path.join(TEMPLATES_DIR, 'core'), exist_ok=True)

TEMPLATES = {
    'store/checkout.html': '''{% extends 'base.html' %}

{% block title %}Checkout - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-2xl);">Complete Your Order</h1>

        <div class="grid" style="grid-template-columns: 1fr 350px; gap: var(--spacing-2xl);">
            <!-- Checkout Form -->
            <form method="post" style="display: flex; flex-direction: column; gap: var(--spacing-xl);">
                {% csrf_token %}

                <!-- Shipping Info -->
                <div class="card">
                    <h3 style="margin-bottom: var(--spacing-lg);">Shipping Address</h3>
                    
                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" name="full_name" value="{{ request.user.first_name }}" required>
                    </div>

                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email" value="{{ request.user.email }}" required>
                    </div>

                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" name="address" placeholder="123 Main Street" required>
                    </div>

                    <div class="grid grid-2">
                        <div class="form-group">
                            <label>City</label>
                            <input type="text" name="city" required>
                        </div>
                        <div class="form-group">
                            <label>ZIP Code</label>
                            <input type="text" name="zip_code" required>
                        </div>
                    </div>
                </div>

                <!-- Payment Info -->
                <div class="card">
                    <h3 style="margin-bottom: var(--spacing-lg);">Payment Method</h3>
                    
                    <div style="padding: var(--spacing-lg); background: var(--bg-secondary); border-radius: var(--radius-lg); margin-bottom: var(--spacing-lg);">
                        <div style="display: flex; align-items: center; gap: var(--spacing-md);">
                            <input type="radio" name="payment_method" value="card" id="card" checked>
                            <label for="card" style="margin: 0; cursor: pointer;">
                                <i class="bi bi-credit-card"></i> Credit/Debit Card
                            </label>
                        </div>
                    </div>

                    <p style="color: var(--text-tertiary); font-size: 0.9rem; margin-bottom: var(--spacing-lg);">
                        Demo mode: Use card <strong>4111 1111 1111 1111</strong>
                    </p>

                    <div class="form-group">
                        <label>Card Number</label>
                        <input type="text" placeholder="1234 5678 9012 3456" maxlength="19" required>
                    </div>

                    <div class="grid grid-2">
                        <div class="form-group">
                            <label>MM/YY</label>
                            <input type="text" placeholder="12/25" maxlength="5" required>
                        </div>
                        <div class="form-group">
                            <label>CVV</label>
                            <input type="text" placeholder="123" maxlength="3" required>
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%; padding: var(--spacing-lg);">
                    <i class="bi bi-check-circle"></i> Complete Order
                </button>
            </form>

            <!-- Order Summary -->
            <div>
                <div class="card" style="position: sticky; top: 100px;">
                    <h4 style="margin-bottom: var(--spacing-lg);">Order Summary</h4>
                    
                    <div style="padding-bottom: var(--spacing-lg); border-bottom: 1px solid var(--bg-tertiary); margin-bottom: var(--spacing-lg);">
                        {% for item in cart_items %}
                        <div style="display: flex; justify-content: space-between; margin-bottom: var(--spacing-sm);">
                            <p style="color: var(--text-secondary);">{{ item.item.name }} x{{ item.quantity }}</p>
                            <p style="font-weight: 600;">${{ item.get_total }}</p>
                        </div>
                        {% endfor %}
                    </div>

                    <div style="display: flex; justify-content: space-between; margin-bottom: var(--spacing-md);">
                        <p>Subtotal</p>
                        <p style="font-weight: 600;">${{ total }}</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: var(--spacing-xl);">
                        <p>Shipping</p>
                        <p style="font-weight: 600; color: var(--success);">Free</p>
                    </div>

                    <div style="display: flex; justify-content: space-between; padding-top: var(--spacing-lg); border-top: 2px solid var(--primary);">
                        <p style="font-weight: 600; font-size: 1.1rem;">Total</p>
                        <p style="font-weight: 600; font-size: 1.1rem; color: var(--primary);">${{ total }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''',

    'core/profile.html': '''{% extends 'base.html' %}

{% block title %}My Profile - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-2xl);">My Profile</h1>

        <div class="grid" style="grid-template-columns: 300px 1fr; gap: var(--spacing-2xl);">
            <!-- Sidebar -->
            <div>
                <div class="card">
                    <div style="text-align: center; margin-bottom: var(--spacing-lg);">
                        <div style="width: 120px; height: 120px; background: var(--primary); border-radius: 50%; margin: 0 auto var(--spacing-lg); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
                            <i class="bi bi-person-fill"></i>
                        </div>
                        <h3>{{ request.user.first_name }} {{ request.user.last_name }}</h3>
                        <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-lg);">{{ request.user.email }}</p>
                    </div>

                    <div style="border-top: 1px solid var(--bg-tertiary); padding-top: var(--spacing-lg);">
                        <a href="{% url 'my_bookings' %}" class="btn btn-ghost" style="width: 100%; justify-content: flex-start;">
                            <i class="bi bi-calendar-check"></i> My Bookings
                        </a>
                        <a href="{% url 'order_history' %}" class="btn btn-ghost" style="width: 100%; justify-content: flex-start; margin-top: var(--spacing-sm);">
                            <i class="bi bi-receipt"></i> My Orders
                        </a>
                        <a href="{% url 'logout' %}" class="btn btn-ghost" style="width: 100%; justify-content: flex-start; margin-top: var(--spacing-sm); color: var(--error);">
                            <i class="bi bi-box-arrow-right"></i> Logout
                        </a>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div>
                <div class="card">
                    <h3 style="margin-bottom: var(--spacing-xl);">Personal Information</h3>

                    <form method="post" style="display: flex; flex-direction: column; gap: var(--spacing-lg);">
                        {% csrf_token %}

                        <div class="grid grid-2">
                            <div class="form-group">
                                <label>First Name</label>
                                <input type="text" name="first_name" value="{{ request.user.first_name }}" required>
                            </div>
                            <div class="form-group">
                                <label>Last Name</label>
                                <input type="text" name="last_name" value="{{ request.user.last_name }}" required>
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" value="{{ request.user.email }}" disabled>
                        </div>

                        <div class="form-group">
                            <label>Phone</label>
                            <input type="tel" name="phone" value="{{ request.user.profile.phone }}" placeholder="+1 (555) 000-0000">
                        </div>

                        <div class="form-group">
                            <label>Address</label>
                            <textarea name="address" rows="3" placeholder="123 Main Street, City, State 12345">{{ request.user.profile.address }}</textarea>
                        </div>

                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check"></i> Save Changes
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''',

    'core/my_bookings.html': '''{% extends 'base.html' %}

{% block title %}My Bookings - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-2xl);">My Bookings</h1>

        {% if bookings %}
        <div style="display: flex; flex-direction: column; gap: var(--spacing-xl);">
            {% for booking in bookings %}
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div class="flex" style="align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-sm);">
                            <h3>{{ booking.get_service_type_display }} - ID #{{ booking.id }}</h3>
                            <span class="badge {% if booking.status == 'confirmed' %}badge-success{% else %}badge-warning{% endif %}">
                                {{ booking.get_status_display }}
                            </span>
                        </div>
                        <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-calendar"></i> {{ booking.date }} at {{ booking.time_slot }}
                        </p>
                        <p style="color: var(--text-secondary);">Total: <strong style="color: var(--primary); font-size: 1.1rem;">${{ booking.total_amount }}</strong></p>
                    </div>
                    <div>
                        <button class="btn btn-secondary" style="margin-bottom: var(--spacing-sm);">
                            <i class="bi bi-pencil"></i> Modify
                        </button>
                        <button class="btn btn-ghost" style="color: var(--error);">
                            <i class="bi bi-x"></i> Cancel
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="card">
            <div class="empty-state">
                <i class="bi bi-calendar" style="font-size: 4rem; margin-bottom: var(--spacing-lg);"></i>
                <h3>No bookings yet</h3>
                <p style="margin-bottom: var(--spacing-xl);">Start booking services to see them here!</p>
                <a href="{% url 'all_services' %}" class="btn btn-primary">
                    <i class="bi bi-stars"></i> Browse Services
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</section>
{% endblock %}
''',

    'store/order_history.html': '''{% extends 'base.html' %}

{% block title %}Order History - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <h1 style="margin-bottom: var(--spacing-2xl);">Order History</h1>

        {% if orders %}
        <div style="display: flex; flex-direction: column; gap: var(--spacing-xl);">
            {% for order in orders %}
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start; padding-bottom: var(--spacing-lg); border-bottom: 1px solid var(--bg-tertiary); margin-bottom: var(--spacing-lg);">
                    <div>
                        <h3 style="margin-bottom: var(--spacing-sm);">Order #{{ order.id }}</h3>
                        <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-calendar"></i> {{ order.created_at|date:"F d, Y" }}
                        </p>
                        <span class="badge {% if order.status == 'delivered' %}badge-success{% elif order.status == 'shipped' %}badge-primary{% else %}badge-warning{% endif %}">
                            {{ order.get_status_display }}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: var(--text-tertiary); margin-bottom: var(--spacing-sm);">Total</p>
                        <p style="font-weight: 600; font-size: 1.3rem; color: var(--primary);">${{ order.total_amount }}</p>
                    </div>
                </div>

                <div>
                    {% for item in order.order_items.all %}
                    <div style="display: flex; gap: var(--spacing-lg); margin-bottom: var(--spacing-md); padding-bottom: var(--spacing-md); border-bottom: 1px solid var(--bg-tertiary);">
                        {% if item.item.image %}
                        <img src="{{ item.item.image.url }}" alt="{{ item.item.name }}" style="width: 80px; height: 80px; border-radius: var(--radius-lg); object-fit: cover;">
                        {% endif %}
                        <div style="flex: 1;">
                            <h4>{{ item.item.name }}</h4>
                            <p style="color: var(--text-tertiary);">Qty: {{ item.quantity }}</p>
                        </div>
                        <p style="font-weight: 600; color: var(--primary);">${{ item.get_total }}</p>
                    </div>
                    {% endfor %}
                </div>

                <div style="display: flex; gap: var(--spacing-md); margin-top: var(--spacing-lg);">
                    <button class="btn btn-secondary">
                        <i class="bi bi-download"></i> Download Invoice
                    </button>
                    <button class="btn btn-ghost">
                        <i class="bi bi-arrow-repeat"></i> Reorder
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="card">
            <div class="empty-state">
                <i class="bi bi-receipt" style="font-size: 4rem; margin-bottom: var(--spacing-lg);"></i>
                <h3>No orders yet</h3>
                <p style="margin-bottom: var(--spacing-xl);">Start shopping to see your orders here!</p>
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

    'core/contact.html': '''{% extends 'base.html' %}

{% block title %}Contact Us - EventNest{% endblock %}

{% block content %}
<section class="section">
    <div class="container">
        <div class="section-title">
            <h1>Get In Touch</h1>
            <p class="section-subtitle">Have a question? We're here to help! Reach out to us anytime.</p>
        </div>

        <div class="grid grid-2">
            <!-- Contact Form -->
            <div class="card">
                <h3 style="margin-bottom: var(--spacing-lg);">Send us a Message</h3>

                <form method="post" style="display: flex; flex-direction: column; gap: var(--spacing-lg);">
                    {% csrf_token %}

                    <div class="form-group">
                        <label>Full Name</label>
                        <input type="text" name="full_name" value="{{ request.user.first_name }}" placeholder="John Doe" required>
                    </div>

                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email" value="{{ request.user.email }}" placeholder="john@example.com" required>
                    </div>

                    <div class="form-group">
                        <label>Subject</label>
                        <input type="text" name="subject" placeholder="How can we help?" required>
                    </div>

                    <div class="form-group">
                        <label>Message</label>
                        <textarea name="message" rows="6" placeholder="Tell us more about your inquiry..." required></textarea>
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        <i class="bi bi-send"></i> Send Message
                    </button>
                </form>
            </div>

            <!-- Contact Info -->
            <div>
                <div class="card">
                    <h3 style="margin-bottom: var(--spacing-2xl);">Contact Information</h3>

                    <div style="margin-bottom: var(--spacing-xl);">
                        <h5 style="color: var(--primary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-geo-alt"></i> Address
                        </h5>
                        <p>123 Event Street<br>New York, NY 10001<br>United States</p>
                    </div>

                    <div style="margin-bottom: var(--spacing-xl);">
                        <h5 style="color: var(--primary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-telephone"></i> Phone
                        </h5>
                        <p><a href="tel:+1234567890" style="text-decoration: none;">+1 (234) 567-890</a></p>
                    </div>

                    <div style="margin-bottom: var(--spacing-xl);">
                        <h5 style="color: var(--primary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-envelope"></i> Email
                        </h5>
                        <p><a href="mailto:info@eventnest.com" style="text-decoration: none;">info@eventnest.com</a></p>
                    </div>

                    <div style="margin-bottom: var(--spacing-xl);">
                        <h5 style="color: var(--primary); margin-bottom: var(--spacing-md);">
                            <i class="bi bi-clock"></i> Business Hours
                        </h5>
                        <p>Monday - Friday: 9:00 AM - 6:00 PM<br>Saturday: 10:00 AM - 4:00 PM<br>Sunday: Closed</p>
                    </div>

                    <div style="padding-top: var(--spacing-lg); border-top: 1px solid var(--bg-tertiary);">
                        <h5 style="color: var(--primary); margin-bottom: var(--spacing-md);">Follow Us</h5>
                        <div class="flex" style="gap: var(--spacing-md);">
                            <a href="#"><i class="bi bi-facebook" style="font-size: 1.5rem;"></i></a>
                            <a href="#"><i class="bi bi-twitter" style="font-size: 1.5rem;"></i></a>
                            <a href="#"><i class="bi bi-instagram" style="font-size: 1.5rem;"></i></a>
                            <a href="#"><i class="bi bi-linkedin" style="font-size: 1.5rem;"></i></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''',
}

for filename, content in TEMPLATES.items():
    filepath = os.path.join(TEMPLATES_DIR, filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ Created {filename}")

print("\n✓ All remaining templates created!")
