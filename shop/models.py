from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount = models.IntegerField(default=0) # Percentage
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name