from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.db.models import Q

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

def search_products(request):
    query = request.GET.get('q', '').strip()# Get the 'q' parameter from the URL
    results = []

    if query:
        # This searches for the query in Name, Description, Brand, or Category
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {
        'query': query,
        'products': results
    })