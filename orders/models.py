from django.db import models
from products.models import Product
from customers.models import Customer


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name="orders", null=True, blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    address=models.CharField(max_length=100, null=True, blank=True)    
    city=models.CharField(max_length=100, null=True, blank=True)
    state=models.CharField(max_length=100, null=True, blank=True)
    pincode=models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.customer:
            self.city = self.customer.city
            self.phone = self.customer.phone
            self.state = self.customer.state
            self.pincode = self.customer.pincode
            self.address = self.customer.address
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id}"
    

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    @property
    def item_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.variant.product.name} ({self.quantity})"