from django.db import models


class Customer(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100, null=True)

    state = models.CharField(max_length=100, null=True)

    pincode = models.CharField(max_length=10, null=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name