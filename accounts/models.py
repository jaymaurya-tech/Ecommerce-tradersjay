
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True) # Store OTP here
    is_verified = models.BooleanField(default=False) # Only allow login if True

    def __str__(self):
        return self.user.username