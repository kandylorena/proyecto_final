from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from apps.cart.cart import Cart
from .models import Order, OrderItem


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@login_required
def checkout(request):
    cart = Cart(request)
    items = cart.get_items()
    if not items:
        messages.error(request, 'El carrito está vacío.')
        return redirect('cart:cart_detail')

    with transaction.atomic():
        total = cart.get_total()
        order = Order.objects.create(user=request.user, total=total)

        for item in items:
            product = item['product']
            if item['quantity'] > product.stock:
                messages.error(
                    request,
                    f'Stock insuficiente para "{product.name}". Solo hay {product.stock} disponibles.',
                )
                return redirect('cart:cart_detail')

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item['quantity'],
                price_snapshot=item['price'],
            )

            product.stock -= item['quantity']
            product.save()

        cart.clear()

    messages.success(request, '¡Compra confirmada exitosamente!')
    return redirect('orders:order_detail', pk=order.id)
