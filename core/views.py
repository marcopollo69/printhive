from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ServiceCategory, ProductExample, CustomerInquiry, QuoteRequest, PricingTier, CarouselImage
from .forms import CustomerInquiryForm


def index(request):
    """Home page with services and featured products."""
    services = ServiceCategory.objects.filter(is_active=True)
    products = ProductExample.objects.filter(is_active=True, is_featured=True)[:6]
    carousel_slides = CarouselImage.objects.filter(is_active=True)
    form = CustomerInquiryForm()
    
    pricing_tiers = PricingTier.objects.filter(is_active=True)
    
    context = {
        'services': services,
        'products': products,
        'carousel_slides': carousel_slides,
        'pricing_tiers': pricing_tiers,
        'form': form,
    }
    return render(request, 'core/index.html', context)


def service_detail(request, slug):
    """Detail page for a service category."""
    service = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    products = service.products.filter(is_active=True)
    
    pricing_tiers = PricingTier.objects.filter(is_active=True)
    
    context = {
        'service': service,
        'products': products,
        'pricing_tiers': pricing_tiers,
    }
    return render(request, 'core/service_detail.html', context)


def submit_inquiry(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        form = CustomerInquiryForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the inquiry
            inquiry = form.save()
            
            # Create associated quote request
            quote = QuoteRequest.objects.create(inquiry=inquiry)
            
            # Handle file upload if present
            if 'design_file' in request.FILES:
                quote.specifications_file = request.FILES['design_file']
                quote.save()
            
            # Send notification email to admin
            try:
                send_mail(
                    subject=f'New Inquiry from {inquiry.name}',
                    message=f'''
New inquiry received on PrintHive Kenya:

Name: {inquiry.name}
Phone: {inquiry.phone}
Email: {inquiry.email}
Company: {inquiry.company or 'N/A'}
Service: {inquiry.service_needed or 'Not specified'}

Message:
{inquiry.message}

---
View in admin: /admin/core/customerinquiry/{inquiry.id}/change/
WhatsApp: {inquiry.whatsapp_link}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass  # Don't fail if email doesn't work
            
            # Send auto-reply to customer
            try:
                send_mail(
                    subject='Thank you for contacting PrintHive Kenya!',
                    message=f'''
Dear {inquiry.name},

Thank you for reaching out to PrintHive Kenya! We have received your inquiry and our team will get back to you within 24 hours.

Your inquiry details:
- Service: {inquiry.service_needed or 'General inquiry'}
- Message: {inquiry.message[:200]}{'...' if len(inquiry.message) > 200 else ''}

If you need immediate assistance, please call us at +254 700 123 456 or message us on WhatsApp.

Best regards,
The PrintHive Kenya Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            return redirect('core:inquiry_success')
        else:
            # Form has errors, return to index with errors
            services = ServiceCategory.objects.filter(is_active=True)
            products = ProductExample.objects.filter(is_active=True, is_featured=True)[:6]
            pricing_tiers = PricingTier.objects.filter(is_active=True)
            context = {
                'services': services,
                'products': products,
                'pricing_tiers': pricing_tiers,
                'form': form,
                'form_errors': True,
            }
            return render(request, 'core/index.html', context)
    
    return redirect('core:index')


def inquiry_success(request):
    """Success page after form submission."""
    return render(request, 'core/inquiry_success.html')


def calculate_price(request):
    """API endpoint to calculate price based on quantity and product."""
    product_id = request.GET.get('product_id')
    qty = int(request.GET.get('qty', 1))
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
        
    product = get_object_or_404(ProductExample, id=product_id)
    
    # Use unit_price if set, otherwise starting_price (though starting_price is usually for display)
    # The model says unit_price is "Price per unit for calculator"
    base_price = product.unit_price if product.unit_price else product.starting_price
    
    # Get active pricing tiers
    tiers = PricingTier.objects.filter(is_active=True).order_by('-min_quantity')
    
    discount_percentage = Decimal('0.00')
    for tier in tiers:
        if qty >= tier.min_quantity:
            discount_percentage = tier.discount_percentage
            break
            
    # Calculate total
    multiplier = (Decimal('100.00') - discount_percentage) / Decimal('100.00')
    final_unit_price = base_price * multiplier
    total_price = final_unit_price * qty
    
    return JsonResponse({
        'total_price': float(total_price),
        'unit_price': float(final_unit_price),
        'base_unit_price': float(base_price),
        'discount_percentage': float(discount_percentage),
        'qty': qty
    })


def products(request):
    """View to display all featured products with filtering."""
    categories = ServiceCategory.objects.filter(is_active=True)
    products = ProductExample.objects.filter(is_active=True, is_featured=True)
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'core/products.html', context)
