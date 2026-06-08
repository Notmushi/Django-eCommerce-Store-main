# M Shop — Django Ecommerce

A modern ecommerce platform built with Django 6 and Bootstrap 5.

## Features

- User authentication (register, login, logout, profile)
- Product catalog with categories
- Shopping cart (session-based)
- Checkout system with order tracking
- Featured & latest product showcases
- Django admin with image previews, custom filters, and inline management
- Fully responsive Bootstrap 5 design

## Requirements

- Python 3.12+
- pip

## Setup Instructions

### 1. Clone the repository

```
git clone <repo-url>
cd ecommerce
```

### 2. Create a virtual environment

```
python -m venv venv
```

Activate it:

- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
```

To generate a secure key:

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run migrations

```
python manage.py migrate
```

### 6. Create a superuser (for admin access)

```
python manage.py createsuperuser
```

### 7. Run the development server

```
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

### 8. Admin panel

Navigate to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

## Project Structure

```
ecommerce/
├── accounts/          # User authentication app
├── categories/        # Category management
├── core/              # Home, cart logic, context processors
├── ecommerce/         # Project settings & URLs
├── orders/            # Checkout & order management
├── products/          # Product catalog
├── static/            # CSS, JS, images
├── templates/         # HTML templates
│   ├── accounts/
│   ├── cart/
│   ├── categories/
│   ├── includes/      # Reusable template partials
│   ├── orders/
│   ├── pages/
│   ├── partials/      # Header, footer
│   └── products/
└── media/             # User-uploaded files (created on first upload)
```
