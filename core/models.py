from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    """Abstract class to ensure only one instance of a model exists."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"There can be only one {self.__class__.__name__} instance")
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj



class ServiceCategory(models.Model):
    """Category of printing/branding services offered."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=50,
        help_text="Feather icon name (e.g., 'shirt', 'coffee', 'truck')"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductExample(models.Model):
    """Example products/packages with pricing."""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price per unit for calculator"
    )
    min_quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'starting_price']

    def __str__(self):
        return f"{self.title} - KSh {self.starting_price}"


class CustomerInquiry(models.Model):
    """Customer contact/inquiry submissions."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quote Sent'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    company = models.CharField(max_length=150, blank=True)
    service_needed = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries'
    )
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    class Meta:
        verbose_name_plural = "Customer Inquiries"
        ordering = ['-submitted_on']

    def __str__(self):
        return f"{self.name} - {self.submitted_on.strftime('%Y-%m-%d')}"

    @property
    def whatsapp_link(self):
        """Generate WhatsApp link with pre-filled message."""
        phone = self.phone.replace(' ', '').replace('-', '')
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]
        message = f"Hello {self.name}, thank you for your inquiry about PrintHive services. We'd love to discuss your project!"
        return f"https://wa.me/{phone}?text={message}"


class QuoteRequest(models.Model):
    """Quote details linked to a customer inquiry."""
    inquiry = models.OneToOneField(
        CustomerInquiry,
        on_delete=models.CASCADE,
        related_name='quote'
    )
    specifications_file = models.FileField(
        upload_to='specifications/',
        null=True,
        blank=True,
        help_text="Customer's design files or specifications"
    )
    estimated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote for {self.inquiry.name}"


class PricingTier(models.Model):
    """Global volume discount tiers."""
    min_quantity = models.PositiveIntegerField(unique=True, help_text="Minimum quantity to trigger this discount")
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Discount percentage (e.g., 5.00 for 5%)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-min_quantity']

    def __str__(self):
        return f"{self.min_quantity}+ units: {self.discount_percentage}% off"


class SiteConfiguration(SingletonModel):
    """Global site settings (Logo, Contact Info)."""
    site_name = models.CharField(max_length=100, default="PrintHive Kenya")
    logo = models.ImageField(upload_to='site/', help_text="Main website logo")
    phone_contact = models.CharField(max_length=20, default="+254 746 336 276", help_text="Primary contact phone")
    whatsapp_number = models.CharField(max_length=20, default="+254746336276", help_text="Number for WhatsApp links (no spaces/+)")
    email_contact = models.EmailField(default="studioprinthive@gmail.com")
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"


class SocialMediaLink(models.Model):
    """Social media links for footer."""
    name = models.CharField(max_length=50, help_text="e.g., Facebook, Instagram")
    url = models.URLField()
    icon_class = models.CharField(max_length=50, help_text="Feather icon name (e.g., facebook, instagram)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class CarouselImage(models.Model):
    """Hero section carousel images."""
    title = models.CharField(max_length=100, blank=True, help_text="Alt text for the image")
    image = models.ImageField(upload_to='carousel/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Slide {self.id}"
