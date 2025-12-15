# Django SQLite to MySQL Migration Guide
## PrintHive Kenya - Database Migration for PythonAnywhere

---

## Phase 1: Local Preparation & Package Installation

### Step 1.1: Install MySQL Client

**For Ubuntu/Debian Linux:**
```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

# Install mysqlclient
pip install mysqlclient
```

**For macOS:**
```bash
brew install mysql pkg-config
pip install mysqlclient
```

**For Windows:**
```bash
pip install mysqlclient
```

**Fallback Option (if mysqlclient fails):**
```bash
pip install pymysql
```

If using pymysql, add this to `print_hive_project/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Step 1.2: Update Requirements
```bash
cd /home/marco/Desktop/PrintHive/print_hive_project
echo "mysqlclient>=2.1.0" >> requirements.txt
```

Or manually add to `requirements.txt`:
```
django>=4.2
pillow>=10.0
mysqlclient>=2.1.0
```

---

## Phase 2: Create MySQL Database

### Step 2.1: Install MySQL Server (if not installed)
```bash
# Ubuntu/Debian
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure installation
sudo mysql_secure_installation
```

### Step 2.2: Access MySQL
```bash
sudo mysql -u root -p
```

### Step 2.3: Create Database & User
Execute these SQL commands in MySQL:
```sql
-- Create the database
CREATE DATABASE print_hive_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create dedicated user (use a strong password!)
CREATE USER 'printhive_user'@'localhost' IDENTIFIED BY 'YourStrongPassword123!';

-- Grant full privileges
GRANT ALL PRIVILEGES ON print_hive_db.* TO 'printhive_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT User, Host FROM mysql.user;

-- Exit
EXIT;
```

**Test Connection:**
```bash
mysql -u printhive_user -p print_hive_db
# Enter password when prompted
```

---

## Phase 3: Update Django Settings

### Step 3.1: Backup Current Settings
```bash
cp print_hive_project/settings.py print_hive_project/settings_backup.py
```

### Step 3.2: Update DATABASES Configuration

Open `print_hive_project/settings.py` and **replace** the DATABASES section:

**BEFORE (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**AFTER (MySQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'print_hive_db',
        'USER': 'printhive_user',
        'PASSWORD': 'YourStrongPassword123!',  # Use your actual password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

> ⚠️ **Security Note**: For production, use environment variables:
> ```python
> import os
> 'PASSWORD': os.environ.get('DB_PASSWORD'),
> ```

---

## Phase 4: Data Migration (Dump & Load)

### Step 4.1: Export Data from SQLite

**IMPORTANT**: Do this BEFORE changing settings.py!

```bash
cd /home/marco/Desktop/PrintHive/print_hive_project

# Full backup with exclusions to prevent integrity errors
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude=contenttypes \
    --exclude=auth.Permission \
    --indent=2 \
    > db_backup.json
```

**Verify the backup:**
```bash
head -50 db_backup.json  # Check it looks like valid JSON
wc -l db_backup.json     # Should have many lines
```

### Step 4.2: Apply New Schema to MySQL

After updating settings.py to MySQL:

```bash
# Test database connection
python manage.py check

# Create fresh migrations (usually not needed)
python manage.py makemigrations

# Apply all migrations to create tables in MySQL
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying core.0001_initial... OK
  ...
```

### Step 4.3: Load Data into MySQL

```bash
python manage.py loaddata db_backup.json
```

**If you get errors**, try loading in stages:
```bash
# Load auth users first
python manage.py loaddata db_backup.json --app auth

# Then load core app data
python manage.py loaddata db_backup.json --app core
```

**Alternative: Fresh Start (if loaddata fails)**
```bash
# Just migrate and manually recreate data via admin
python manage.py migrate
python manage.py createsuperuser
# Then seed data via admin or management command
```

---

## Phase 5: Post-Migration Verification

### Step 5.1: Test Django Server
```bash
python manage.py runserver
```

**Verify these work:**
- [ ] Homepage: http://127.0.0.1:8000/
- [ ] Admin Panel: http://127.0.0.1:8000/admin/
- [ ] Service Categories load
- [ ] Product Examples display with prices
- [ ] Contact form submits successfully
- [ ] Quick Estimate calculator works

### Step 5.2: Check Database Tables
```bash
mysql -u printhive_user -p print_hive_db

# In MySQL shell:
SHOW TABLES;
SELECT COUNT(*) FROM core_servicecategory;
SELECT COUNT(*) FROM core_productexample;
SELECT COUNT(*) FROM core_customerinquiry;
EXIT;
```

### Step 5.3: Media Files (IMPORTANT!)

> ⚠️ **Media files are NOT in the database!**

The `media/` directory contains:
- `media/products/` - Product images
- `media/specifications/` - Customer design uploads

**These must be copied manually to PythonAnywhere:**
```bash
# On local machine, compress media folder
cd /home/marco/Desktop/PrintHive/print_hive_project
tar -czvf media_backup.tar.gz media/

# Upload media_backup.tar.gz to PythonAnywhere
# Then extract on server:
tar -xzvf media_backup.tar.gz
```

### Step 5.4: Create Superuser (if needed)
```bash
python manage.py createsuperuser
# Username: admin
# Email: studioprinthive@gmail.com
# Password: (choose secure password)
```

---

## PythonAnywhere-Specific Configuration

### Database Setup on PythonAnywhere

1. Go to **Databases** tab in PythonAnywhere dashboard
2. Set a MySQL password (note it down!)
3. Create database: `yourusername$print_hive_db`
4. Database host: `yourusername.mysql.pythonanywhere-services.com`

### Update settings.py for PythonAnywhere
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$print_hive_db',
        'USER': 'yourusername',
        'PASSWORD': 'your_pythonanywhere_mysql_password',
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Static & Media Files on PythonAnywhere
```python
# Add to settings.py
STATIC_ROOT = '/home/yourusername/printhive/staticfiles/'
MEDIA_ROOT = '/home/yourusername/printhive/media/'
```

Run collectstatic:
```bash
python manage.py collectstatic
```

---

## Quick Reference: Complete Command Sequence

```bash
# 1. Backup data (while still using SQLite)
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.Permission \
    --indent=2 > db_backup.json

# 2. Backup media files
tar -czvf media_backup.tar.gz media/

# 3. Install MySQL client
pip install mysqlclient

# 4. Create MySQL database (in MySQL shell)
# CREATE DATABASE print_hive_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 5. Update settings.py with MySQL config

# 6. Apply migrations to MySQL
python manage.py migrate

# 7. Load data into MySQL
python manage.py loaddata db_backup.json

# 8. Create superuser if needed
python manage.py createsuperuser

# 9. Test
python manage.py runserver
```

---

## Troubleshooting

### Error: "Access denied for user"
- Verify username/password in settings.py
- Check user privileges: `SHOW GRANTS FOR 'printhive_user'@'localhost';`

### Error: "Unknown database"
- Verify database exists: `SHOW DATABASES;`
- Database name is case-sensitive on Linux

### Error: "mysqlclient installation failed"
- Use pymysql fallback (see Phase 1.1)
- On Ubuntu: `sudo apt-get install python3-dev default-libmysqlclient-dev`

### Error: "loaddata IntegrityError"
- Re-export with `--natural-foreign --natural-primary`
- Try loading without auth data, then create new superuser

### Error: "Incorrect string value" (Unicode)
- Ensure database uses `utf8mb4`: 
  ```sql
  ALTER DATABASE print_hive_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

---

## Rollback Plan

If migration fails and you need to revert:

```bash
# Restore SQLite settings
cp print_hive_project/settings_backup.py print_hive_project/settings.py

# Verify SQLite still works
python manage.py runserver
```

Your original `db.sqlite3` file is untouched during this process.

---

**End of Migration Guide**
