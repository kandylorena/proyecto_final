from decimal import Decimal
from django.conf import settings

from apps.catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price),
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        for product in products:
            pid = str(product.id)
            item = {
                'product': product,
                'quantity': self.cart[pid]['quantity'],
                'price': Decimal(self.cart[pid]['price']),
                'subtotal': Decimal(self.cart[pid]['price']) * self.cart[pid]['quantity'],
            }
            items.append(item)
        return items

    def get_total(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True
