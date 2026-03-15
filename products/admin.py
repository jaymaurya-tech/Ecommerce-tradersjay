from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Brand


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "created",
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = ("name",)