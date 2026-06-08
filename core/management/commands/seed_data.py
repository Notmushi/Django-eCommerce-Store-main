from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category
from products.models import Product


categories_data = [
    {
        'name': 'T-Shirts',
        'description': 'Casual and stylish t-shirts for every occasion.',
    },
    {
        'name': 'Trousers',
        'description': 'Comfortable and trendy trousers for men and women.',
    },
    {
        'name': 'Pants',
        'description': 'A variety of pants including jeans, chinos, and more.',
    },
    {
        'name': 'Shirts',
        'description': 'Formal and casual shirts to elevate your wardrobe.',
    },
    {
        'name': 'Shoes',
        'description': 'Footwear for every step of your journey.',
    },
    {
        'name': 'Accessories',
        'description': 'Complete your look with our premium accessories.',
    },
]

products_by_category = {
    'T-Shirts': [
        ('Classic Cotton T-Shirt', 19.99, 50),
        ('Graphic Print Tee', 24.99, 40),
        ('V-Neck Slim Fit T-Shirt', 22.99, 35),
        ('Oversized Streetwear Tee', 29.99, 30),
        ('Striped Polo T-Shirt', 34.99, 25),
        ('Basic Crew Neck T-Shirt', 14.99, 100),
        ('Henley Neck T-Shirt', 27.99, 20),
        ('Athletic Dry-Fit Tee', 32.99, 45),
        ('Color Block T-Shirt', 26.99, 30),
        ('Premium Linen T-Shirt', 39.99, 15),
    ],
    'Trousers': [
        ('Chino Trousers', 49.99, 30),
        ('Formal Trousers', 59.99, 25),
        ('Cargo Trousers', 54.99, 20),
        ('Pleated Dress Trousers', 64.99, 15),
        ('Slim Fit Trousers', 44.99, 35),
        ('Wide Leg Trousers', 57.99, 20),
        ('Linen Trousers', 52.99, 25),
        ('Cropped Trousers', 47.99, 30),
        ('Tailored Trousers', 69.99, 10),
        ('Elastic Waist Trousers', 39.99, 40),
    ],
    'Pants': [
        ('Slim Fit Jeans', 44.99, 40),
        ('Straight Leg Jeans', 49.99, 35),
        ('Cargo Pants', 54.99, 25),
        ('Jogger Pants', 39.99, 30),
        ('Chino Pants', 47.99, 20),
        ('Denim Jacket Pants', 59.99, 15),
        ('Athletic Joggers', 34.99, 50),
        ('Corduroy Pants', 52.99, 20),
        ('Hiking Pants', 62.99, 15),
        ('Casual Shorts', 24.99, 60),
    ],
    'Shirts': [
        ('Classic Oxford Shirt', 44.99, 30),
        ('Slim Fit Dress Shirt', 49.99, 25),
        ('Flannel Check Shirt', 39.99, 20),
        ('Linen Casual Shirt', 54.99, 15),
        ('Denim Button-Down Shirt', 59.99, 10),
        ('Striped Business Shirt', 52.99, 20),
        ('Cuban Collar Shirt', 42.99, 25),
        ('Formal White Shirt', 47.99, 35),
        ('Hawaiian Print Shirt', 34.99, 30),
        ('Performance Polo Shirt', 44.99, 40),
    ],
    'Shoes': [
        ('Running Sneakers', 79.99, 30),
        ('Leather Loafers', 89.99, 20),
        ('Casual Canvas Shoes', 49.99, 40),
        ('Formal Oxford Shoes', 99.99, 15),
        ('High Top Sneakers', 74.99, 25),
        ('Slip-On Sneakers', 59.99, 35),
        ('Hiking Boots', 109.99, 10),
        ('Sandals', 34.99, 50),
        ('Boat Shoes', 69.99, 20),
        ('Espadrilles', 44.99, 30),
    ],
    'Accessories': [
        ('Leather Belt', 29.99, 50),
        ('Aviator Sunglasses', 39.99, 30),
        ('Classic Wrist Watch', 149.99, 15),
        ('Canvas Backpack', 54.99, 25),
        ('Silk Tie', 24.99, 40),
        ('Baseball Cap', 19.99, 60),
        ('Leather Wallet', 34.99, 35),
        ('Beanie Hat', 17.99, 45),
        ('Travel Duffle Bag', 69.99, 20),
        ('Phone Case', 14.99, 80),
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with categories and dummy products'

    def handle(self, *args, **options):
        created_categories = []

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category exists: {category.name}')
            created_categories.append(category)

        for category in created_categories:
            items = products_by_category.get(category.name, [])
            for name, price, stock in items:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'slug': slugify(name),
                        'description': f'High-quality {name.lower()} available at M Shop.',
                        'price': price,
                        'stock': stock,
                        'featured': False,
                        'available': True,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created product: {name}'))
                else:
                    self.stdout.write(f'  Product exists: {name}')

        featured_names = [
            'Classic Cotton T-Shirt', 'Slim Fit Jeans', 'Running Sneakers',
            'Chino Trousers', 'Classic Oxford Shirt', 'Leather Belt',
        ]
        Product.objects.filter(name__in=featured_names).update(featured=True)
        self.stdout.write(self.style.SUCCESS('\nMarked featured products.'))

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
