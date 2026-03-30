from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django_otp.admin import OTPAdminSite
from .models import Profile
from products.models import Product, Category, Brand, Size
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from customers.models import Customer
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

class OTPAdmin(OTPAdminSite):
    login_template = 'login.html'
    def login(self, request, extra_context=None):
        if self.has_permission(request):
            return super().login(request, extra_context)
        
        return redirect('login') 

    def has_permission(self, request):
        # Check if the user is a superuser AND has the 'otp_verified' flag in their session
        return (request.user.is_authenticated and 
                request.user.is_superuser and 
                request.session.get('otp_verified', False))

admin_site = OTPAdmin(name='OTPAdmin')
# 1. Define how the Profile should look
class ProfileAdmin(admin.ModelAdmin):
    # This adds the columns you were missing
    list_display = ('get_username', 'get_email','phone', 'address', 'is_verified') 
    
    # This adds the search bar to the Profile page
    search_fields = ('user__username', 'user__email', 'phone')
    
    # Optional: adds a filter sidebar on the right
    list_filter = ('is_verified',)

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
try:
    admin.site.unregister(User)  # Unregister the default User admin
except admin.sites.NotRegistered:
    pass

from products.models import Product, ProductImage, ProductVariant, Size, Category, Brand, Color

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Number of empty rows to show by default
    fields = ('size', 'price', 'old_price','color', 'stock')

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','hex_code')
    search_fields = ('name','hex_code')
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.hex_code
        )
    color_preview.short_description = 'Preview'

class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "brand",
        "category",
        "get_price_range",
        "updated",
        
    )
    
    inlines = [ProductImageInline, ProductVariantInline]
   # filter_horizontal = ('sizes',)
    


    list_filter = (
        "brand",
        "category",
        "created",
    )

    search_fields = (
        "name",
        "brand__name",
        "category__name",
    )

    list_per_page = 20

    readonly_fields = ("image_preview",)
    
    # Optional: Helper to show a price range in the admin list
    def get_price_range(self, obj):
        variants = obj.variants.all()
        if variants.exists():
            prices = [v.price for v in variants]
            return f"${min(prices)} - ${max(prices)}"
        return "No variants"
    get_price_range.short_description = 'Price Range'

    def image_preview(self, obj):
        if obj.cover_image:
            from django.utils.safestring import mark_safe
            return mark_safe(f'<img src="{obj.cover_image.url}" width="50" />')
        return "No Image"

    image_preview.short_description = "Image"


class CategoryAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "category_image_preview",
        "name",
    )

    list_editable = ("name",)

    search_fields = ("name",)

    readonly_fields = ("category_image_preview",)

    def category_image_preview(self, obj):
        if obj.cat_image:
            return format_html(
                '<img src="{}" width="50" style="border-radius:6px;" />',
                obj.cat_image.url
            )
        return "No Image"
    category_image_preview.short_description = "Category Image"


class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "logo_preview",        
        "id",
        "name",
    )

    search_fields = ("name",)

    list_editable = ("name",)

    readonly_fields = ("logo_preview",)


    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="50" style="border-radius:6px;" />',
                obj.logo.url
            )
        return "No Image"

    logo_preview.short_description = "Logo"

class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "city",
        "state",
        "created",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    list_filter = (
        "city",
        "state",
        "created",
    )

    list_per_page = 20

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_product_name','quantity','price', 'variant']
    fields = ['variant', 'quantity', 'price']
    can_delete = False

    def get_product_name(self, obj):
        return obj.variant.product.name
    get_product_name.short_description = 'Product'



class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "status",
        "phone",
        "total_price",
        "created",
        "print_invoice_button"
    )
    readonly_fields = ('total_price', 'print_invoice_button')

    list_filter = (
        "status",
        "created",
    )

    fields = ('customer', 'status', 'total_price', 'print_invoice_button','phone' ,'address' ,'state', 'city', 'pincode')

    search_fields = ("customer__name", )

    inlines = [OrderItemInline]

    def print_invoice_button(self, obj):
        if obj.id:
            url = reverse('admin_order_pdf', args=[obj.id])
            return mark_safe(f'''
            <a href="{url}" class="button" 
               style="background-color: #e11d48; color: white; padding: 5px 12px; border-radius: 5px; text-decoration: none;">
               <i class="fas fa-file-pdf"></i> Download PDF
            </a>
        ''')
        return "-"

    



#class OrderItemAdmin(admin.ModelAdmin):

   # list_display = (
      #  "order",
      #  "variant",
      #  "quantity",
      #  "price",
   # )


class CartItemInline(admin.TabularInline):
    model = CartItem
    # Update these to match your new model structure
    fields = ('variant', 'quantity', 'get_price') 
    readonly_fields = ('get_price',) # 'product' and 'selected_size' were removed here
    extra = 0

    # If you want to see the price in the inline
    def get_price(self, obj):
        if obj.variant:
            return f"₹{obj.variant.price}"
        return "-"
    get_price.short_description = 'Unit Price'
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

# 2. Register them using your custom admin_site
admin_site.register(User, UserAdmin)  # Register the User model to manage users in the admin
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Size, SizeAdmin)
admin_site.register(Color, ColorAdmin)
admin_site.register(Cart, CartItemAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Brand, BrandAdmin)
admin_site.register(Order, OrderAdmin)
#admin_site.register(OrderItem, OrderItemAdmin)
admin_site.register(Customer, CustomerAdmin)