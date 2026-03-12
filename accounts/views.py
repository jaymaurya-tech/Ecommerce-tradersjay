from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import login as otp_login

# Registration View
def register(request):
    if request.method == 'POST':
        # 1. Always define your variables
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmPassword')

        # 2. Handle validation early
        if password != confirmpassword:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        # 3. Generate OTP here so it is ALWAYS defined if the code reaches here
        otp = str(random.randint(100000, 999999))
        
        # 4. Store in session (Staging)
        request.session['temp_user_data'] = {
            'username': username,
            'email': email,
            'password': password,
            'phone': phone,
            'address': address,
            'otp': otp # Save the OTP here
        }
        
        # 5. Send mail
        try:
            send_mail(
                'Verify Your Account', 
                f'Your OTP is {otp}', 
                'settings.DEFAULT_FROM_EMAIL', 
                [email], 
                fail_silently=False
            )
            return redirect('verify_otp')
        except Exception as e:
            messages.error(request, f"Could not send email: {e}")
            return render(request, 'register.html')
            
    return render(request, 'register.html')
# Login View
from django.contrib.auth import login as auth_login

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = None
        if '@' in identifier:
            user_obj = User.objects.filter(email=identifier).first()
        else:
            user_obj = User.objects.filter(username=identifier).first()

        # 1. Safely find the user without crashing on duplicates
                   
        
        if user_obj:
            # 2. Authenticate using the username found
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                if user.is_superuser:
                    request.session['pre_otp_user_id'] = user.id
                    return redirect('verify_otp')
                else:
                    auth_login(request, user)
                    return redirect('home')
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "User not found.")
            
    return render(request, 'login.html')


def logout_view(request):
    # 1. Remove custom session flags (the "mind game" variables)
    if 'otp_verified' in request.session:
        del request.session['otp_verified']
    if 'pre_otp_user_id' in request.session:
        del request.session['pre_otp_user_id']
    
    # 2. Invalidate the entire session for maximum security
    request.session.flush()
    
    # 3. Standard Django logout
    auth_logout(request)
    
    # 4. Redirect to your login page
    return redirect('login')

def verify_otp_view(request):
    # Determine the context: Are we registering a new user or logging in an Admin?
    is_admin_2fa = 'pre_otp_user_id' in request.session
    is_registration = 'temp_user_data' in request.session

    if not (is_admin_2fa or is_registration):
        messages.error(request, "Verification session expired.")
        return redirect('login')

    if request.method == 'POST':
        otp_token = request.POST.get('otp') or request.POST.get('otp_token')

        if is_admin_2fa:
            # ADMIN 2FA LOGIC
            user_id = request.session.get('pre_otp_user_id')
            user = User.objects.filter(id=user_id).first()
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first() if user else None
            
            if device and device.verify_token(otp_token):
                auth_login(request, user)
                request.session['otp_verified'] = True
                del request.session['pre_otp_user_id']
                return redirect('/owner_site_web_admin/')
            
        elif is_registration:
            # REGISTRATION LOGIC
            temp_data = request.session.get('temp_user_data')
            if otp_token == temp_data.get('otp'):
                user = User.objects.create_user(
                    username=temp_data['username'],
                    email=temp_data['email'],
                    password=temp_data['password']
                )
                Profile.objects.create(user=user, phone=temp_data['phone'], address=temp_data['address'])
                del request.session['temp_user_data']
                auth_login(request, user)
                return redirect('home')

        # If we reach here, verification failed
        messages.error(request, "Invalid code. Please try again.")
        return redirect('verify_otp') # Reload the page

    return render(request, 'verify_otp.html', {'is_admin': is_admin_2fa})

def resend_otp(request):
    temp_data = request.session.get('temp_user_data')
    if not temp_data:
        return redirect('register')
        
    # Generate new OTP
    new_otp = str(random.randint(100000, 999999))
    temp_data['otp'] = new_otp
    request.session['temp_user_data'] = temp_data
    
    # Send Email
    from django.conf import settings
    send_mail('New OTP', f'Your new OTP is {new_otp}', 
              settings.DEFAULT_FROM_EMAIL, [temp_data['email']])
    
    messages.success(request, "New OTP has been sent!")
    return redirect('verify_otp')



@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.save()
        
        # If you have a custom Profile model:
        profile = user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        messages.success(request, "Profile updated successfully!")
        
    return render(request, 'profile.html', {'user': request.user})




