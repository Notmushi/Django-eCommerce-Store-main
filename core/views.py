from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Prefetch
from django.contrib import messages
from products.models import Product
from categories.models import Category
from . import cart as cart_module


def home(request):
    featured_products = Product.objects.filter(
        featured=True, available=True
    ).select_related('category')[:8]
    latest_products = Product.objects.filter(
        available=True
    ).select_related('category').order_by('-created_at')[:8]
    prefetch = Prefetch('products', queryset=Product.objects.filter(available=True).select_related('category'))
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).prefetch_related(prefetch)[:6]
    return render(request, 'pages/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    })


def cart_detail(request):
    items = cart_module.get_cart_items(request)
    total = cart_module.get_cart_total(request)
    return render(request, 'cart/cart_detail.html', {
        'cart_items': items,
        'cart_total': total,
    })


def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id, available=True)
        cart_module.add_to_cart(request, product_id, quantity)
        messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


def cart_remove(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_module.remove_from_cart(request, product_id)
        messages.info(request, f'"{product.name}" removed from cart.')
    return redirect('cart_detail')


def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        cart_module.update_cart(request, product_id, quantity)
        messages.success(request, f'"{product.name}" quantity updated.')
    return redirect('cart_detail')
