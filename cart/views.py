from itertools import product

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from customers.models import Customer
from .models import Cart, CartItem
from products.models import Product, ProductVariant

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
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')  # Get the selected variant ID from the form

    # Find the specific variant the user wants
    if variant_id:
        variant = get_object_or_404(ProductVariant, product=product, id=variant_id)
    else:
        # Fallback to the first available variant (default)
        variant = product.variants.first()
        if not variant:
            return redirect('product_detail', pk=product_id) # Or handle "Out of Stock"

    # Use the variant to find/create the cart item
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, variant=variant)

    if not item_created:
        # Optional: Check if quantity exceeds variant.stock before incrementing
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_detail')

    
@login_required
def cart_update(request, variant_id):
    cart = get_object_or_404(Cart, user=request.user)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    # Get the size from the POST request
   # selected_size = request.POST.get('size')
    #if not selected_size: selected_size = None
    
    # 1. Look for the item. Filter is safer than get.
    cart_item = CartItem.objects.filter(
        cart=cart, 
        variant=variant, 
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
def cart_remove(request, variant_id):
    cart = get_object_or_404(Cart, user=request.user)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart_item = get_object_or_404(CartItem, cart=cart, variant=variant)
    cart_item.delete()
    
    return redirect('cart_detail')

@login_required
def cart_view(request):
    # Fetch cart items and "select_related" to optimize database hits
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('variant', 'variant__product')
    
    subtotal = 0
    for item in cart_items:
        # Price comes from the variant!
        item.item_total = item.variant.price * item.quantity
        subtotal += item.item_total
    
    discount = subtotal * 0.10
    total = subtotal - discount
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'shipping_progress': min((subtotal / 50) * 100, 100),
        'free_shipping_unlocked': subtotal >= 50,
        'amount_to_free_shipping': max(50 - subtotal, 0)
    }
    return render(request, 'cart.html', context)

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    # Check if cart is empty before allowing checkout
    if not cart_items.exists():
        return redirect('cart_detail')

    subtotal = cart.get_total_price()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'checkout.html', context)



from orders.models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from orders.utils import render_to_pdf

@login_required
def process_order(request):
    if request.method == 'POST':
        # 1. Get the cart and check if it's empty
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            return redirect('cart_detail')

        # 2. Extract details from the Checkout Form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        # You can also capture 'payment_method' here if needed

        # 3. Find or Update/Create Customer by email
        # We use update_or_create to ensure the Customer has the latest info from the form
        customer, created = Customer.objects.update_or_create(
            email=request.user.email,
            defaults={
                'name': f"{first_name} {last_name}",
                'phone': phone,
                'address': address,
                'city': city,
            }
        )

        # 4. Create the Order
        # This links the order to the Customer object we just found/created
        order = Order.objects.create(
            customer=customer,
            total_price=cart.get_total_price(),
            status="pending"
        )

        # 5. Move Cart Items to Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                price=item.variant.price  # Capture the price at the moment of purchase
            )

        # 6. Clear the User's Cart
        cart_items.delete()

        # 7. Redirect to the success page with the Order ID
        return redirect('order_success', order_id=order.id)

    # If it's a GET request, just send them back to checkout
    return redirect('checkout')

@login_required
def order_success(request, order_id):
    # Fetch the specific order for this user
    order = get_object_or_404(Order, id=order_id)
    
    # Passing the data your order_success.html expects:
    context = {
        'order': order,
        'order_items': order.items.all(), # This uses the related_name="items"
        'total_price': order.total_price,
    }
    return render(request, 'order_success.html', context)

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = {
        'order': order,
        'order_items': order.items.all(), # Ensure this matches your related_name
        'total_price': order.total_price,
    }
    
    pdf = render_to_pdf('invoice_pdf.html', data)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{order.id}.pdf"
        content = f"inline; filename={filename}" # 'inline' opens in browser, 'attachment' downloads
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF", status=400)