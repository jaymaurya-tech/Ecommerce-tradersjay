from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_detail(request, id):
    # Fetch the product by ID
    product = get_object_or_404(Product, id=id)
    
    # The 'images' variable is available because of 'related_name=images' in the model
    # We fetch them here just to be explicit, though you can also loop in the template
    gallery_images = product.images.all() 
    
    context = {
        'product': product,
        'gallery_images': gallery_images,
    }
    return render(request, 'product_detail.html', context)