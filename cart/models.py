# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from products.models import Product # Assuming your products are in a 'shop' app

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_size = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.selected_size})"

    @property
    def item_total(self):
        return self.product.price * self.quantity

    def get_cost(self):
        return self.product.price * self.quantity