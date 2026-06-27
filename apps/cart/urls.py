from django.urls import path
from .views import CartDetailView, add_to_cart, remove_from_cart, update_cart

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', update_cart, name='update_cart'),
]
