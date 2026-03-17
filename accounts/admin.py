from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django_otp.admin import OTPAdminSite
from .models import Profile
from products.models import Product, Category, Brand
from orders.models import Order, OrderItem
from customers.models import Customer
from django.utils.html import format_html

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



class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "created",
        "updated",
        "discount_price",
    )

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


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" style="border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image"


class CategoryAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "name",
    )

    search_fields = ("name",)


class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "logo_preview",        
        "id",
        "name",
    )

    search_fields = ("name",)

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
    extra = 1



class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "status",
        "total_price",
        "created",
    )

    list_filter = (
        "status",
        "created",
    )

    search_fields = ("customer__name", )

    inlines = [OrderItemInline]



class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )
 
# 2. Register them using your custom admin_site
admin_site.register(User, UserAdmin)  # Register the User model to manage users in the admin
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Brand, BrandAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderItem, OrderItemAdmin)
admin_site.register(Customer, CustomerAdmin)