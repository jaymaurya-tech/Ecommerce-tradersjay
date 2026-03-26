from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

@login_required
def cart_detail(request):
    # Get or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.get_total_price()
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def cart_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size')
    
    # Check if item already exists in cart to increment quantity
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, selected_size=size)
    
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart_detail')

    
@login_required
def cart_update(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    # Get the size from the POST request
    selected_size = request.POST.get('size')
    if not selected_size: selected_size = None
    
    # 1. Look for the item. Filter is safer than get.
    cart_item = CartItem.objects.filter(
        cart=cart, 
        product=product, 
        selected_size=selected_size # Ensure this field name matches your Model!
    ).first()

    if request.method == 'POST':
        # 2. Safety Check: If the item wasn't found, redirect back to cart
        if not cart_item:
            return redirect('cart_detail')

        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity > 0:
                cart_item.save()
            else:
                cart_item.delete()
                
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    
    return redirect('cart_detail')

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.item_total =item.product.price * item.quantity
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    discount = subtotal * 0.10
    total = subtotal - discount
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,

        'shipping_progress': min((subtotal / 50) * 100, 100), # Progress bar %
        'free_shipping_unlocked': subtotal >= 50,
        'amount_to_free_shipping': max(50 - subtotal, 0)
    }
    return render(request, 'cart.html', context)