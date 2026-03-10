
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Built-in Login
    path('login/',views.login_view, name='login'),
    # Built-in Logout
    path('logout/',views.logout_view, name='logout'),
    # Custom Registration View
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('profile/', views.profile_view, name='profile'),
]