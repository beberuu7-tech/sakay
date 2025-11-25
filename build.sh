#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create default superuser (only if it doesn't exist)
python manage.py create_default_superuser
```

### Add Environment Variables in Render:

Go to your Render dashboard → Environment tab → Add:
```
DJANGO_SUPERUSER_USERNAME = youradminname
DJANGO_SUPERUSER_EMAIL = youremail@example.com
DJANGO_SUPERUSER_PASSWORD = YourSecurePassword123!