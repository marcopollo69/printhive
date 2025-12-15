# PROJECT_OVERVIEW.md
## PrintHive Kenya - Django Web Application

**Status**: Development Complete | All Features Functional  
**Last Updated**: December 2025

---

## Project Summary

**Purpose**: A custom branding and printing business website that enables customers in Nairobi to browse services, view product examples with pricing, and submit quote requests with design file uploads.

**Core User Journey**:  
Browse services (T-shirts, mugs, decals, etc.) → View featured products with pricing → Use pricing calculator for estimates → Submit quote request via contact form (with optional design upload) → Receive confirmation and auto-reply email.

---

## Technology Stack & Dependencies

### Backend
- **Django**: 4.2+ (Python web framework)
- **Python**: 3.x
- **SQLite**: Default database (development)
- **Pillow**: 10.0+ (Image processing for uploads)

### Frontend
- **Tailwind CSS**: 3.x via CDN (Utility-first CSS framework)
- **Feather Icons**: Icon library via CDN
- **Vanilla JavaScript**: No framework (handles modals, form validation, pricing calculator)

### Third-Party Services
- **Email Backend**: Django console backend (development) - ready for SMTP configuration in production
- **Media Storage**: Local filesystem (`media/` directory)

---

## Project Structure

```
print_hive_project/
├── core/                          # Main Django app
│   ├── models.py                  # Data models (4 models)
│   ├── views.py                   # View functions (4 views)
│   ├── urls.py                    # URL routing for core app
│   ├── forms.py                   # Customer inquiry form with validation
│   ├── admin.py                   # Django admin customizations
│   ├── migrations/                # Database schema migrations
│   ├── static/core/               # App-specific static files
│   │   ├── css/styles.css         # Custom CSS (minimal)
│   │   ├── js/main.js             # Frontend JavaScript
│   │   └── img/                   # Static images (logo, hero)
│   └── templates/core/            # HTML templates
│       ├── index.html             # Homepage
│       ├── service_detail.html    # Service category page
│       └── inquiry_success.html   # Form success page
├── templates/base.html            # Base template (inherited by all)
├── media/                         # User-uploaded files
│   ├── products/                  # Product images
│   └── specifications/            # Customer design files
├── print_hive_project/            # Project settings directory
│   ├── settings.py                # Configuration
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py                    # WSGI entry point
├── db.sqlite3                     # SQLite database
├── manage.py                      # Django management script
└── requirements.txt               # Python dependencies
```

---

## Data Models (core/models.py)

### 1. ServiceCategory
**Purpose**: Represents categories of printing/branding services offered (T-Shirts, Mugs, Decals, etc.)

**Key Fields**:
- `name` (CharField): Service name  
- `slug` (SlugField): URL-friendly identifier (auto-generated)
- `description` (TextField): Service details
- `icon_class` (CharField): Feather icon name for display
- `is_active` (BooleanField): Visibility toggle

**Relationships**: Has many `ProductExample` objects via reverse ForeignKey (`products`)

---

### 2. ProductExample
**Purpose**: Example products/packages with pricing displayed on website for customer reference

**Key Fields**:
- `title` (CharField): Product name
- `starting_price` (DecimalField): Display price
- `unit_price` (DecimalField): For pricing calculator (nullable)
- `min_quantity` (PositiveIntegerField): Minimum order quantity
- `image` (ImageField): Product photo (uploads to `media/products/`)
- `is_featured` (BooleanField): Show on homepage if True

**Relationships**:  
- `category` (ForeignKey → `ServiceCategory`): Parent service category

---

### 3. CustomerInquiry
**Purpose**: Stores customer contact form submissions with status tracking for CRM

**Key Fields**:
- `name`, `phone`, `email` (CharField/EmailField): Contact details
- `message` (TextField): Customer's inquiry
- `status` (CharField): Workflow state (new, contacted, quoted, closed)
- `submitted_on` (DateTimeField): Timestamp

**Relationships**:  
- `service_needed` (ForeignKey → `ServiceCategory`, nullable): Selected service
- Has one `QuoteRequest` object via reverse OneToOne (`quote`)

**Special Property**:  
- `whatsapp_link`: Generates WhatsApp URL with pre-filled message for quick follow-up

---

### 4. QuoteRequest
**Purpose**: Quote metadata linked to customer inquiry, stores design files and admin notes

**Key Fields**:
- `specifications_file` (FileField): Customer's design upload
- `estimated_price` (DecimalField): Admin-entered quote amount
- `notes` (TextField): Internal notes
- `follow_up_date` (DateField): Reminder date

**Relationships**:  
- `inquiry` (OneToOneField → `CustomerInquiry`): Parent inquiry

---

## Core Views & URL Patterns

| View Function | URL Pattern | Purpose |
|--------------|-------------|---------|
| `index()` | `/` | Renders homepage with active services and featured products (up to 6). Passes empty `CustomerInquiryForm` for contact section. |
| `service_detail(slug)` | `/service/<slug>/` | Displays details of a specific `ServiceCategory` and all its associated products. Slug is auto-generated from service name. |
| `submit_inquiry()` | `/inquiry/submit/` | Handles POST request from contact form. Validates form, creates `CustomerInquiry` and `QuoteRequest`, uploads design file, sends 2 emails (admin notification + customer auto-reply), redirects to success page. |
| `inquiry_success()` | `/inquiry/success/` | Simple success confirmation page with WhatsApp contact link. |

---

## Template Architecture

### Inheritance Chain
```
base.html (shared layout: header, footer, Tailwind config)
  ├── index.html (homepage)
  ├── service_detail.html (service category page)
  └── inquiry_success.html (success page)
```

### Key Templates

**[base.html](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/base.html)** (Project root templates/)
- Defines site-wide structure: navigation, footer, Tailwind configuration
- Loads Feather Icons, Google Fonts (Montserrat, Open Sans)
- Contains mobile menu toggle
- Declares `{% block content %}` for child templates

**[index.html](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/core/index.html)** (core/templates/core/)
- Hero section with logo and call-to-action
- Services grid (loops `{% for service in services %}`)
- Featured products section with pricing and "Quick Estimate" buttons
- Contact form with CSRF protection (loops `{% for field in form %}`)
- Pricing calculator modal (JavaScript-controlled)

**[service_detail.html](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/core/service_detail.html)**
- Service header with icon and description
- Product grid for category's products
- Each product has "Quick Estimate" button linked to JS modal

**[inquiry_success.html](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/core/inquiry_success.html)**
- Confirmation message with checkmarks
- Next steps instructions
- Direct WhatsApp contact link

### Important Template Tags & Filters
- `{% static 'core/...' %}`: Load static files (images, CSS, JS)
- `{% csrf_token %}`: CSRF protection for forms
- `{{ product.starting_price|floatformat:0 }}`: Format prices without decimals
- `{{ product.description|truncatewords:10 }}`: Limit description length
- `{% if product.image %}`: Conditional rendering

---

## Static Assets & Frontend

### Styling
**Primary Framework**: Tailwind CSS 3.x (via CDN)
- Configured in `base.html` with custom theme colors:
  - Primary: `#000000` (Black)
  - Accent: `#F1C40F` (Gold/Yellow)

**Custom CSS**: [styles.css](file:///home/marco/Desktop/PrintHive/print_hive_project/core/static/core/css/styles.css)
- Minimal custom styles
- `.hero-gradient`: Black gradient background
- Product image container with `object-contain` to prevent cropping

### JavaScript
**File**: [main.js](file:///home/marco/Desktop/PrintHive/print_hive_project/core/static/core/js/main.js)

**Responsibilities**:
1. **Mobile Menu**: Toggles hamburger menu on small screens
2. **Smooth Scrolling**: Handles anchor link navigation
3. **Pricing Calculator Modal**:
   - Opens when "Quick Estimate" button clicked
   - Populates with product data (`data-title`, `data-unit-price`, `data-min-qty`)
   - Calculates total with volume discounts (5% at 50+ units, 10% at 200+)
   - Enforces minimum quantity
4. **Phone Validation**: Client-side Kenyan phone number validation (`^(\+254|0)[17]\d{8}$`)
5. **Feather Icons**: Initializes icon library on page load

### Images/Media
- **Static Images**: `/core/static/core/img/` (logo.png, branding-products.jpg)
- **Uploaded Product Images**: `media/products/` (via Django FileField)
- **Customer Design Files**: `media/specifications/` (attached to QuoteRequest)

---

## Key Features & How They Work

### 1. Dynamic Service/Product Display

**Data Flow**: `Model` → `View` → `Template`

1. **Model**: `ServiceCategory` and `ProductExample` store data
2. **View** ([views.py:9-20](file:///home/marco/Desktop/PrintHive/print_hive_project/core/views.py#L9-L20)):
   ```python
   services = ServiceCategory.objects.filter(is_active=True)
   products = ProductExample.objects.filter(is_active=True, is_featured=True)[:6]
   ```
3. **Template** (index.html):
   ```django
   {% for product in products %}
     <h3>{{ product.title }}</h3>
     <p>Starting at KSh {{ product.starting_price|floatformat:0 }}</p>
   {% endfor %}
   ```

**Critical**: Template variables must stay on single line to render correctly (Django parser issue when split across lines).

---

### 2. Quote Request Pipeline

**User Journey**: Form Fill → Submit → Email Notifications → Database Save → Redirect

**Step-by-Step**:
1. **User fills form** on homepage (name, phone, email, service, message, optional file upload)
2. **Browser sends POST** to `/inquiry/submit/`
3. **View validates** `CustomerInquiryForm` ([forms.py](file:///home/marco/Desktop/PrintHive/print_hive_project/core/forms.py))
   - Phone regex: `^(\+254|0)[17]\d{8}$` (Kenyan format)
   - Email validation, required fields
4. **Database operations**:
   ```python
   inquiry = form.save()  # Creates CustomerInquiry
   quote = QuoteRequest.objects.create(inquiry=inquiry)  # Links QuoteRequest
   quote.specifications_file = request.FILES['design_file']  # Saves upload
   ```
5. **Email notifications** ([views.py:52-101](file:///home/marco/Desktop/PrintHive/print_hive_project/core/views.py#L52-L101)):
   - **Admin email**: "New Inquiry from {name}" with inquiry details + admin link
   - **Customer auto-reply**: "Thank you for contacting PrintHive Kenya"
6. **Redirect** to `/inquiry/success/`

**Email Config** (development):
- Backend: `django.core.mail.backends.console.EmailBackend` (prints to terminal)
- From: `studioprinthive@gmail.com`

---

### 3. Pricing Calculator (Client-Side)

**Technology**: Pure JavaScript (no framework)

**Trigger**: Click "Quick Estimate" button on product card

**Logic** ([main.js:86-105](file:///home/marco/Desktop/PrintHive/print_hive_project/core/static/core/js/main.js#L86-L105)):
```javascript
// Get product data from button
const unitPrice = parseFloat(button.dataset.unitPrice);
const minQty = parseInt(button.dataset.minQty);

// Calculate with volume discounts
let price = unitPrice;
if (qty >= 200) price *= 0.90;  // 10% off
else if (qty >= 50) price *= 0.95;  // 5% off

const total = qty * price;
```

**UI**:
- Modal overlay with product title
- Quantity input (enforces minimum)
- Real-time total calculation (formatted as "KSh 1,500")
- Close on outside click or ESC key

---

## Environment & Configuration

### Critical Settings ([settings.py](file:///home/marco/Desktop/PrintHive/print_hive_project/print_hive_project/settings.py))

**For Production Deployment, Update**:
```python
# Line 26
DEBUG = False  # CRITICAL: Disable debug mode

# Line 28
ALLOWED_HOSTS = ['printhive.co.ke', 'www.printhive.co.ke']  # Add domain

# Database (lines 79-86) - Switch to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'printhive_db',
        'USER': 'printhive_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static/Media Files (lines 121-127)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collectstatic
MEDIA_ROOT = BASE_DIR / 'media'  # Already configured

# Email (lines 132-134) - Configure SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'studioprinthive@gmail.com'
EMAIL_HOST_PASSWORD = 'app_password_here'
DEFAULT_FROM_EMAIL = 'studioprinthive@gmail.com'

# Security (add lines)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Current Development Settings**:
- `DEBUG = True`
- `ALLOWED_HOSTS = []` (allows localhost)
- `DATABASE = SQLite` (db.sqlite3)
- `EMAIL_BACKEND = console` (prints emails to terminal)

---

## "Getting Started" Checklist

### Prerequisites
- Python 3.8+ installed
- Git (if cloning from repository)

### Setup Commands
```bash
# 1. Clone repository (if applicable)
git clone <repository-url>
cd print_hive_project

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create admin superuser
python manage.py createsuperuser
# Username: admin
# Password: (choose secure password)

# 6. Load sample data (optional - for demonstration)
python manage.py shell
>>> from core.models import ServiceCategory, ProductExample
>>> # Create services and products via shell or admin panel

# 7. Run development server
python manage.py runserver

# 8. Access application
# Homepage: http://127.0.0.1:8000/
# Admin Panel: http://127.0.0.1:8000/admin/
```

### First-Time Setup
1. Log into admin panel (`/admin/`)
2. Create 6 service categories (T-Shirts, Mugs, Pens, Jerseys, Decals, Corporate Gifts)
3. Add product examples with images
4. Mark 3-6 products as "featured" to display on homepage
5. Test contact form submission
6. Check terminal for email output (development mode)

---

## Admin Panel Features

### Customizations ([admin.py](file:///home/marco/Desktop/PrintHive/print_hive_project/core/admin.py))

**ServiceCategory Admin**:
- List view shows name, slug, order, active status
- Inline editing for order
- Slug auto-generated from name
- Search by name/description

**ProductExample Admin**:
- List view shows title, category, price, featured, active
- Editable list columns: is_featured, is_active
- Filter by category, featured, active
- Search by title/description
- Image upload interface

**CustomerInquiry Admin**:
- List view shows name, phone, service, status, date
- Editable status directly in list
- Filter by status, service, date
- Search by name/phone/email
- Custom action: "Send WhatsApp Message" (opens WhatsApp link)
- Inline `QuoteRequest` for editing quote details within inquiry

**QuoteRequest Admin**:
- Typically edited inline within CustomerInquiry
- Fields: specifications file, estimated price, notes, follow-up date
- Auto-timestamps (created_at, updated_at)

---

## Database Schema Summary

```
ServiceCategory (1) ──< (∞) ProductExample
     │
     └──< (∞) CustomerInquiry (1) ──< (1) QuoteRequest
```

**Relationships**:
- One `ServiceCategory` has many `ProductExample` objects
- One `ServiceCategory` has many `CustomerInquiry` objects (via service_needed)
- One `CustomerInquiry` has exactly one `QuoteRequest`

---

## Common Workflows

### Adding a New Service
1. Admin → Service Categories → Add Service Category
2. Fill: name, description, icon_class (Feather icon name), order
3. Slug auto-generates on save
4. Add related products via ProductExample

### Processing Customer Inquiry
1. Check email notification (terminal in dev, inbox in prod)
2. Admin → Customer Inquiries → Click inquiry
3. Review message, check attached design file
4. Update status to "Contacted"
5. Fill out quote details (estimated price, notes)
6. Click "WhatsApp" action to follow up
7. Mark status "Quote Sent" → "Closed"

### Updating Product Pricing
1. Admin → Product Examples → Select product
2. Edit `starting_price` (display price)
3. Edit `unit_price` (calculator price)
4. Update `min_quantity` if needed
5. Save

---

## Deployment Considerations

### Pre-Deployment Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to production database (PostgreSQL recommended)
- [ ] Configure real SMTP email backend
- [ ] Set up static file serving (`collectstatic`)
- [ ] Configure media file serving (nginx/Apache or cloud storage)
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set secure cookie flags
- [ ] Generate new `SECRET_KEY`
- [ ] Set up backup strategy for database
- [ ] Configure logging

### Recommended Stack
- **Web Server**: Nginx or Apache
- **WSGI Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL
- **Static/Media**: Cloud storage (AWS S3, Cloudinary) or local with nginx
- **Email**: SMTP provider (Gmail, SendGrid, Mailgun)
- **Hosting**: VPS (DigitalOcean, Linode) or PaaS (Heroku, Railway)

---

## Maintenance Notes

### Regular Tasks
- Monitor customer inquiries daily
- Upload new product images regularly
- Update pricing as needed
- Review and respond to quotes within 24-48 hours

### Known Issues & Solutions
- **Template syntax error**: If `{% endif %}` tags break across lines, prices won't display. Fix: Keep Django template variables on single lines.
- **Image cropping**: Use `object-contain` CSS property, not `object-cover`, to show full product images.

### Contact Information
- **Admin Email**: studioprinthive@gmail.com
- **Admin Phone**: +254 746 336 276
- **WhatsApp**: +254 782 070 228

---

## Version History

**v1.0** (December 2025)
- Initial production-ready release
- 4 data models, 4 views
- Pricing calculator with volume discounts
- Email notifications
- File upload support
- Mobile-responsive design
- Admin panel customizations

---

## Quick Reference Links

- [Models](file:///home/marco/Desktop/PrintHive/print_hive_project/core/models.py)
- [Views](file:///home/marco/Desktop/PrintHive/print_hive_project/core/views.py)
- [Forms](file:///home/marco/Desktop/PrintHive/print_hive_project/core/forms.py)
- [URLs](file:///home/marco/Desktop/PrintHive/print_hive_project/core/urls.py)  
- [Admin](file:///home/marco/Desktop/PrintHive/print_hive_project/core/admin.py)
- [Settings](file:///home/marco/Desktop/PrintHive/print_hive_project/print_hive_project/settings.py)
- [Main JavaScript](file:///home/marco/Desktop/PrintHive/print_hive_project/core/static/core/js/main.js)
- [Base Template](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/base.html)
- [Homepage Template](file:///home/marco/Desktop/PrintHive/print_hive_project/core/templates/core/index.html)

---

**End of Document**
