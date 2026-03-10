from django.contrib.auth.models import User
from django_otp.admin import OTPAdminSite
from django_otp.admin import OTPAdminAuthenticationForm
from .models import Profile

class OTPAdmin(OTPAdminSite):
    # This forces Django to use the form that includes the OTP field
    login_form = OTPAdminAuthenticationForm

admin_site = OTPAdmin(name='OTPAdmin')

# Register your models
admin_site.register(Profile)
if not hasattr(User, 'is_verified'):
    def is_verified(self):
        return getattr(self, 'otp_device', None) is not None
    User.is_verified = is_verified