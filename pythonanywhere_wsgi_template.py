# /var/www/YourUsername_pythonanywhere_com_wsgi.py
#
# IMPORTANT: This is a TEMPLATE for your PythonAnywhere WSGI configuration.
# Copy this content to your actual WSGI file on PythonAnywhere and replace
# all instances of 'YourUsername' with your actual PythonAnywhere username.
#
# To find your WSGI file:
# 1. Go to the Web tab on PythonAnywhere
# 2. Look for the "WSGI configuration file" link in the Code section
# 3. Click it to edit, then paste this content

import os
import sys

# ==============================================================================
# PATH CONFIGURATION
# ==============================================================================

# Add your project directory to the Python path
# Replace 'YourUsername' with your actual PythonAnywhere username
path = '/home/YourUsername/print_hive_project'
if path not in sys.path:
    sys.path.insert(0, path)

# ==============================================================================
# ENVIRONMENT VARIABLES
# ==============================================================================

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'print_hive_project.settings'
os.environ['DJANGO_ENV'] = 'production'
os.environ['DJANGO_DEBUG'] = 'False'

# Generate a new secret key for production! Use:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
os.environ['DJANGO_SECRET_KEY'] = 'REPLACE-WITH-A-SECURE-SECRET-KEY'

# ==============================================================================
# DATABASE CONFIGURATION
# Replace these values with your actual PythonAnywhere MySQL credentials
# ==============================================================================

os.environ['DB_NAME'] = 'YourUsername$printhive'
os.environ['DB_USER'] = 'YourUsername'
os.environ['DB_PASSWORD'] = 'YOUR_MYSQL_PASSWORD_HERE'
os.environ['DB_HOST'] = 'YourUsername.mysql.pythonanywhere-services.com'

# ==============================================================================
# EMAIL CONFIGURATION (Optional - for sending emails)
# ==============================================================================

# For Gmail, you need to:
# 1. Enable 2-Factor Authentication on your Google account
# 2. Generate an "App Password" at https://myaccount.google.com/apppasswords
# 3. Use that App Password here (not your regular Gmail password)

# os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
# os.environ['EMAIL_PORT'] = '587'
# os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'
# os.environ['EMAIL_HOST_PASSWORD'] = 'your-16-character-app-password'

# ==============================================================================
# WSGI APPLICATION
# ==============================================================================

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
