from django.urls import path
from . import views

urlpatterns = [
    # ... other paths ...
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
]