from django.urls import path
from .views import OrderListView, OrderDetailView, checkout

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('checkout/', checkout, name='checkout'),
]
