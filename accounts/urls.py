
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
    # 1. User enters email
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    # 2. Success page after sending email
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # 3. User clicks link in email, sets new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # 4. Final success page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]