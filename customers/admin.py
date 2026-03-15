from django.contrib import admin
from .models import Customer


@admin.register(Customer)
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