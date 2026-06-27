from django.db import models
from django.contrib.auth.models import User

from apps.catalog.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('completed', 'Completada'),
            ('cancelled', 'Cancelada'),
        ],
        default='pending',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Orden #{self.id} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'
