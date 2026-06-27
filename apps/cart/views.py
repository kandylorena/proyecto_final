from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.catalog.models import Product
from .cart import Cart


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_items'] = cart.get_items()
        context['cart_total'] = cart.get_total()
        return context


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        messages.error(request, 'La cantidad debe ser al menos 1.')
        return redirect('catalog:product_detail', pk=product_id)
    if quantity > product.stock:
        messages.error(request, f'Stock insuficiente. Solo hay {product.stock} disponibles.')
        return redirect('catalog:product_detail', pk=product_id)
    cart = Cart(request)
    cart.add(product, quantity)
    messages.success(request, f'"{product.name}" añadido al carrito.')
    return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('cart:cart_detail')


@login_required
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 0))
    cart = Cart(request)
    if quantity > 0:
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            messages.error(request, f'Stock insuficiente. Solo hay {product.stock} disponibles.')
            return redirect('cart:cart_detail')
    cart.update(product_id, quantity)
    messages.success(request, 'Carrito actualizado.')
    return redirect('cart:cart_detail')
