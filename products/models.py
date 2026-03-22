from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.IntegerField(default=5)
    
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount)
        return None

    def __str__(self):
        return self.name
