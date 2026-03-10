from django.contrib import admin
from accounts.admin import admin_site
from .models import Product, Brand

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'brand')
    list_filter = ('brand',)
    search_fields = ('name',)

admin_site.register(Brand, site=admin_site)