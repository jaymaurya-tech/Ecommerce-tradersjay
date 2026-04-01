from django.db import models


from django.conf import settings # Add this import

class Customer(models.Model):
    # Link to the built-in User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='customer_profile',
        null=True, 
        blank=True
    )
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