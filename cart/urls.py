from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:variant_id>/', views.cart_update, name='cart_update'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success')
]