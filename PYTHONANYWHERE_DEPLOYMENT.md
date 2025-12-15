# PrintHive - PythonAnywhere Deployment Guide

This guide will help you deploy PrintHive to PythonAnywhere.

## Prerequisites Completed ✅

The following files have been prepared for deployment:
- `requirements.txt` - Contains Django, mysqlclient, and Pillow
- `settings.py` - Updated with production settings and PythonAnywhere support
- `staticfiles/` - Collected static files (130 files)

---

## Phase 2: PythonAnywhere Setup

### Step 1: Create an Account
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com) (free tier works)
2. Open the Dashboard and go to the **Consoles** tab
3. Start a new **Bash console**

### Step 2: Upload Your Code
In the Bash console:
```bash
# Option A: Clone via Git (recommended)
git clone <your-repository-url>

# Option B: Upload manually via the 'Files' tab
```

### Step 3: Create Virtual Environment
```bash
cd print_hive_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Phase 3: Configure the Web App

### Step 4: Set Up the Web App
1. Go to the **Web** tab in dashboard
2. Click "**Add a new web app**"
3. Choose "**Manual configuration**" (not Django)
4. Select **Python 3.10** or your development version

### Step 5: Configure Virtual Environment
In the Web tab > Virtualenv section, enter:
```
/home/YourUsername/printhive/venv
```

### Step 6: Edit WSGI File
Click the WSGI file link and replace all contents with:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/YourUsername/printhive'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'print_hive_project.settings'
os.environ['DJANGO_ENV'] = 'production'
os.environ['DJANGO_DEBUG'] = 'False'

# Database credentials (set these!)
os.environ['DB_NAME'] = 'YourUsername$printhive'
os.environ['DB_USER'] = 'YourUsername'
os.environ['DB_PASSWORD'] = 'YourMySQLPassword'
os.environ['DB_HOST'] = 'YourUsername.mysql.pythonanywhere-services.com'

# Optional: Set a secure secret key
os.environ['DJANGO_SECRET_KEY'] = 'your-secure-secret-key-here'

# Load the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANT: Replace `YourUsername` with your actual PythonAnywhere username!**

---

## Phase 4: Set Up MySQL Database

### Step 7: Create MySQL Database
1. Go to the **Databases** tab
2. Set a MySQL password (remember it!)
3. Create a new database: `YourUsername$printhive`

### Step 8: Update WSGI File
Update the database credentials in the WSGI file with the password you just set.

### Step 9: Run Migrations
In the Bash console (with venv activated):
```bash
cd /home/YourUsername/printhive
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

---

## Phase 5: Configure Static & Media Files

### Step 10: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 11: Configure Static File Mappings
In the **Web** tab > Static files section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YourUsername/printhive/staticfiles` |
| `/media/` | `/home/YourUsername/printhive/media` |

### Step 12: Create Media Directory
```bash
mkdir -p /home/YourUsername/printhive/media
```

---

## Phase 6: Final Launch

### Step 13: Update ALLOWED_HOSTS
Make sure to update `settings.py` with your actual PythonAnywhere domain:
```python
ALLOWED_HOSTS = [
    'YourUsername.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]
```

### Step 14: Reload Web App
Click the big green **Reload** button on the Web tab.

### Step 15: Verify Deployment
- Visit: `https://YourUsername.pythonanywhere.com`
- Test admin: `https://YourUsername.pythonanywhere.com/admin`

---

## Post-Deployment Tasks

### Email Configuration
For production email, add to WSGI file:
```python
os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'
```
Note: For Gmail, you need an "App Password" (not your regular password).

### Database Backup
Use the **Schedule** tab to set up regular MySQL dumps:
```bash
mysqldump -u YourUsername -h YourUsername.mysql.pythonanywhere-services.com \
    'YourUsername$printhive' > /home/YourUsername/backups/db_backup_$(date +%Y%m%d).sql
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| White screen/500 error | Check error log in Web tab |
| Static files not loading | Verify static file mappings in Web tab |
| Database connection error | Double-check DB credentials in WSGI file |
| Admin works but site errors | Check ALLOWED_HOSTS includes your domain |
| Import errors | Verify virtualenv path is correct |

---

## Quick Reference

- **Your site URL**: `https://YourUsername.pythonanywhere.com`
- **Admin URL**: `https://YourUsername.pythonanywhere.com/admin`
- **Error logs**: Web tab > Log files section
- **Bash console**: Consoles tab > Bash
- **MySQL console**: Databases tab > Start a console

---

*Generated for PrintHive Project - December 2025*
