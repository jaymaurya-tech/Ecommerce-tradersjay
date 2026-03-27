from django.db import models
from django.utils.text import slugify

class Brand(models.Model):

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=200)
    cat_image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50) 

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

    cover_image = models.ImageField(upload_to='products/covers/', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)
    sizes = models.ManyToManyField(Size, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.IntegerField(default=5)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount)
        return None

    def __str__(self):
        return self.name
    
    @property
    def default_size(self):
        return self.sizes.first() if self.sizes.exists() else None

class ProductImage(models.Model):
    """These are the 4-5 extra images for the details page"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
