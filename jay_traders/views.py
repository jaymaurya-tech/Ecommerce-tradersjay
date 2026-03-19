from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product, Brand, Category
def home(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'brands': brands,
        'categories': categories
    }
    return render(request, "index.html", context)

