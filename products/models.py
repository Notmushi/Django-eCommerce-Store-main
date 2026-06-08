from django.db import models
from django.utils.text import slugify
from categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            suffix = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base}-{suffix}'
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)
