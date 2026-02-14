from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Service, ServiceCategory, StoreItem, StoreCategory, UserProfile, Booking, Contact
import re
from django.utils import timezone

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+880XXXXXXXXXX'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password1'
    }), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'id_password2'
    }), label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+880'):
            raise forms.ValidationError('Phone number must start with +880')
        if not re.match(r'^\+880\d{10}$', phone):
            raise forms.ValidationError('Invalid Bangladesh phone number format. Use: +880XXXXXXXXXX')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update user profile
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'full_name': self.cleaned_data['full_name'],
                    'phone': self.cleaned_data['phone'],
                    'address': self.cleaned_data['address'],
                }
            )
        return user

class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'image']

class ServiceCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = ServiceCategory
        fields = ['name', 'description']

class StoreItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=StoreCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = StoreItem
        fields = ['category', 'name', 'description', 'price', 'stock', 'image']

class StoreCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = StoreCategory
        fields = ['name', 'description']

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()
        })
    )
    time_slot = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        })
    )
    requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Any special requirements or notes...'
        })
    )

    class Meta:
        model = Booking
        fields = ['date', 'time_slot', 'requirements']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError('Cannot book for a past date.')
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        if date and time_slot:
            # Combine date and time for datetime comparison
            booking_datetime = timezone.make_aware(
                timezone.datetime.combine(date, time_slot)
            )
            if booking_datetime < timezone.now():
                raise forms.ValidationError('Cannot book for a past time.')


class ContactForm(forms.ModelForm):
    """Form for contact inquiries"""
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Full Name',
            'required': True
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'your.email@example.com',
            'required': True
        }),
        label='Email Address'
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '+880 1XXX XXX XXX',
            'type': 'tel'
        }),
        label='Phone Number (Optional)'
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'What is this about?',
            'required': True
        }),
        label='Subject'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'rows': 6,
            'placeholder': 'Tell us more about your inquiry...',
            'required': True
        }),
        label='Message / Description'
    )
    
    preferred_contact_method = forms.ChoiceField(
        choices=Contact.CONTACT_METHOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'required': True
        }),
        label='Preferred Contact Method'
    )
    
    service_type = forms.ChoiceField(
        choices=Contact.SERVICE_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'required': True
        }),
        label='Related Service'
    )
    
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'subject', 'message', 'preferred_contact_method', 'service_type']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[\d\s\+\-\(\)]{7,20}$', phone):
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email address is required.')
        return email