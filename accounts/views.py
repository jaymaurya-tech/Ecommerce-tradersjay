from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. Safely find the user without crashing on duplicates
        user_obj = User.objects.filter(email=email).first()
        
        if user_obj:
            # 2. Authenticate using the username found
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "User not found.")
            
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login') # Redirect back to login page

def verify_otp_view(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        temp_data = request.session.get('temp_user_data')
        
        # 1. Check if session data even exists
        if not temp_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        # 2. Check if OTP matches
        if user_otp == temp_data['otp']:
            # Create user
            user = User.objects.create_user(
                username=temp_data['username'],
                email=temp_data['email'],
                password=temp_data['password']
            )
            user.is_active = True
            user.save()
            
            # Create profile
            Profile.objects.create(
                user=user, 
                phone=temp_data['phone'], 
                address=temp_data['address']
            )
            
            # Clean session
            del request.session['temp_user_data']
            
            # Log the user in
            login(request, user)
            
            # 3. Force the redirect
            return redirect('home') 
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
            return render(request, 'verify_otp.html')
            
    return render(request, 'verify_otp.html')

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