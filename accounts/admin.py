from django.shortcuts import redirect
from django.contrib.auth.models import User
from django_otp.admin import OTPAdminSite
from .models import Profile

class OTPAdmin(OTPAdminSite):
    login_template = 'login.html'
    def login(self, request, extra_context=None):
        if self.has_permission(request):
            return super().login(request, extra_context)
        
        return redirect('login') 

    def has_permission(self, request):
        # Check if the user is a superuser AND has the 'otp_verified' flag in their session
        return (request.user.is_authenticated and 
                request.user.is_superuser and 
                request.session.get('otp_verified', False))

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(Profile)