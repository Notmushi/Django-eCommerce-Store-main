from . import cart as cart_module


def cart_count(request):
    return {'cart_count': cart_module.get_cart_count(request)}
