# PythonAnywhere Deployment Guide

**GitHub:** `github.com/Notmushi/Django-eCommerce-Store-main.git`

---

## 1. Initial Setup (one-time)

### 1.1 Create a PythonAnywhere account
- Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (free "Beginner" plan works)

### 1.2 Open a Bash console
- Go to **Consoles** → **Start a new Bash console**

### 1.3 Clone the repository
```bash
git clone https://github.com/Notmushi/Django-eCommerce-Store-main.git
cd Django-eCommerce-Store-main
```

### 1.4 Create and activate a virtual environment
```bash
mkvirtualenv --python=3.10 ecommerce-env
pip install -r requirements.txt
```

### 1.5 Create the `.env` file
```bash
nano .env
```
Paste:
```
SECRET_KEY=<generate a new secret key>
DEBUG=False
ALLOWED_HOSTS=.pythonanywhere.com,localhost,127.0.0.1
```
Generate a key with Python:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 1.6 Run migrations & collect static
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 1.7 Create a superuser (optional)
```bash
python manage.py createsuperuser
```

---

## 2. Configure the WSGI file

### 2.1 Open the WSGI configuration
- Go to **Web** → click on your web app URL
- Under **Code**, click the **WSGI configuration file** link

### 2.2 Replace its contents
```python
import os
import sys

# Add your project directory to sys.path
path = '/home/<your-username>/Django-eCommerce-Store-main'
if path not in sys.path:
    sys.path.append(path)

# Point to your virtualenv site-packages
# (find the actual path by running in Bash: 'pip -V' or 'which python')
# Usually: /home/<your-username>/.virtualenvs/ecommerce-env/lib/python3.10/site-packages

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce.settings'

# Load .env variables
from decouple import config
os.environ['SECRET_KEY'] = config('SECRET_KEY')
os.environ['DEBUG'] = config('DEBUG', default='False')
os.environ['ALLOWED_HOSTS'] = config('ALLOWED_HOSTS')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> Replace `<your-username>` with your PythonAnywhere username (find it with `whoami` in Bash).

### 2.3 Configure the virtualenv path in Web tab
- Under **Virtualenv**, enter: `/home/<your-username>/.virtualenvs/ecommerce-env`

### 2.4 Configure static & media files

Under **Static files**:
| URL | Directory |
|-----|-----------|
| `/static/` | `/home/<your-username>/Django-eCommerce-Store-main/staticfiles` |
| `/media/` | `/home/<your-username>/Django-eCommerce-Store-main/media` |

### 2.5 Reload the web app
- Click the green **Reload** button

Your site should now be live at `https://<your-username>.pythonanywhere.com`

---

## 3. Deploying Code Changes (routine updates)

Every time you push changes to GitHub and want them live:

### 3.1 Open a Bash console
```bash
cd ~/Django-eCommerce-Store-main
git pull origin main
```

### 3.2 Activate virtualenv & install any new dependencies
```bash
workon ecommerce-env
pip install -r requirements.txt   # if requirements changed
```

### 3.3 Run migrations (if models changed)
```bash
python manage.py migrate
```

### 3.4 Collect static files (if static files changed)
```bash
python manage.py collectstatic --noinput
```

### 3.5 Reload the web app
```bash
# Option A: from the Web tab (click Reload)
# Option B: using the PA API (if set up):
# touch /var/www/<your-username>_pythonanywhere_com_wsgi.py
```

---

## 4. Updating only the WSGI file

If you only need to tweak the WSGI file:

1. Go to **Web** → click **WSGI configuration file**
2. Make your edits
3. Click **Save**
4. Click **Reload**

Or from the command line:
```bash
nano /var/www/<your-username>_pythonanywhere_com_wsgi.py
# edit, save (Ctrl+X, Y, Enter), then reload via Web tab
```

---

## 5. Troubleshooting

| Problem | Solution |
|---------|----------|
| **500 Internal Server Error** | Check **Web → Error log** |
| **Static files not loading** | Verify static file mappings in Web tab; re-run `collectstatic` |
| **ModuleNotFoundError** | Ensure virtualenv path is set correctly in the Web tab |
| **Database errors** | Run `python manage.py migrate` |
| **"Invalid HTTP_HOST"** | Make sure `.pythonanywhere.com` is in `ALLOWED_HOSTS` |
| **.env not working** | WSGI reads `.env` from the project root — double-check the path |
