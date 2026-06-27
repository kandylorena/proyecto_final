from .cart import Cart


def cart_info(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        return {
            'cart_total_items': cart.get_total_items(),
            'cart_total': cart.get_total(),
        }
    return {'cart_total_items': 0, 'cart_total': 0}
