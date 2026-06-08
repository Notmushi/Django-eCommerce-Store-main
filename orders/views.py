from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.cart import get_cart_items, get_cart_total, clear_cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout_view(request):
    cart_items = get_cart_items(request)
    cart_total = get_cart_total(request)

    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                total=cart_total,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['product'].price,
                    quantity=item['quantity'],
                )
            clear_cart(request)
            messages.success(request, 'Order placed successfully!')
            return redirect('order_summary', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def order_summary_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_summary.html', {
        'order': order,
    })
