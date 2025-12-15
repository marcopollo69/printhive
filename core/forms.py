from django import forms
from django.core.validators import RegexValidator
from .models import CustomerInquiry, ServiceCategory


class CustomerInquiryForm(forms.ModelForm):
    """Form for customer inquiries with Kenyan phone validation."""
    
    phone_regex = RegexValidator(
        regex=r'^(\+254|0)[17]\d{8}$',
        message="Enter a valid Kenyan phone number (e.g., 0712345678 or +254712345678)"
    )
    
    phone = forms.CharField(
        validators=[phone_regex],
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': '0712 345 678'
        })
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'you@example.com'
        })
    )
    
    company = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Your company (optional)'
        })
    )
    
    service_needed = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.filter(is_active=True),
        required=False,
        empty_label="Select a service (optional)",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'rows': 4,
            'placeholder': 'Tell us about your project...'
        })
    )
    
    design_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'accept': '.pdf,.png,.jpg,.jpeg,.ai,.psd,.svg'
        }),
        help_text="Upload your logo or design files (optional)"
    )

    class Meta:
        model = CustomerInquiry
        fields = ['name', 'phone', 'email', 'company', 'service_needed', 'message']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        # Normalize phone number format
        phone = phone.replace(' ', '').replace('-', '')
        return phone
