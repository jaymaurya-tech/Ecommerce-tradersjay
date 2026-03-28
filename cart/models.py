# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from products.models import Product # Assuming your products are in a 'shop' app

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.item_total for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, null=True, blank=True) # Link to the specific variant
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'variant')  # Ensure one entry per variant in the cart

    def __str__(self):
        if self.variant:
            product_name = self.variant.product.name if self.variant.product else "Unknown Product"
            size_name = self.variant.size if self.variant.size else "Unknown Size"
            return f"{product_name} ({size_name})"
        return f"CartItem {self.id}"

    @property
    def item_total(self):
        if self.variant:
            return self.variant.price * self.quantity
        return 0

    def get_cost(self):
        if self.variant:
            return self.item_total
      