from django.conf import settings
from products.models import Product

CART_SESSION_KEY = 'cart'


def _get_cart(request):
    cart = request.session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {}
        request.session[CART_SESSION_KEY] = cart
    return cart


def get_cart_items(request):
    cart = _get_cart(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(
        id__in=product_ids, available=True
    ).select_related('category')
    items = []
    for product in products:
        items.append({
            'product': product,
            'quantity': cart[str(product.id)]['quantity'],
            'subtotal': product.price * cart[str(product.id)]['quantity'],
        })
    return items


def get_cart_count(request):
    cart = _get_cart(request)
    return sum(item['quantity'] for item in cart.values())


def get_cart_total(request):
    cart = _get_cart(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, available=True).only('price')
    total = sum(product.price * cart[str(product.id)]['quantity'] for product in products)
    return total


def add_to_cart(request, product_id, quantity=1):
    cart = _get_cart(request)
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] += quantity
    else:
        cart[pid] = {'quantity': quantity}
    request.session.modified = True


def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        request.session.modified = True


def update_cart(request, product_id, quantity):
    cart = _get_cart(request)
    pid = str(product_id)
    if quantity > 0:
        cart[pid] = {'quantity': quantity}
    else:
        cart.pop(pid, None)
    request.session.modified = True


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
