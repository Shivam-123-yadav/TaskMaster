from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser

# ... (previous views remain same: register_view, login_view, logout_view)

@login_required
def profile_view(request):
    """
    Display user profile with statistics
    """
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def settings_view(request):
    """
    Settings page with multiple tabs
    """
    if request.method == 'POST':
        user = request.user
        
        # Handle Profile Update
        if 'first_name' in request.POST:
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.bio = request.POST.get('bio', '')
            user.phone = request.POST.get('phone', '')
            
            # Handle avatar upload
            if request.FILES.get('avatar'):
                user.avatar = request.FILES['avatar']
            
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')
        
        # Handle Account Settings Update
        elif 'username' in request.POST:
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            
            # Check if username is already taken
            if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, 'Username already taken!')
            # Check if email is already taken
            elif CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, 'Email already in use!')
            else:
                user.username = new_username
                user.email = new_email
                user.save()
                messages.success(request, 'Account settings updated successfully!')
            
            return redirect('settings')
        
        # Handle Password Change
        elif 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Verify current password
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect!')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match!')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long!')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Password changed successfully!')
            
            return redirect('settings')
    
    return render(request, 'accounts/settings.html')


@login_required
def update_profile_view(request):
    """
    Handle profile updates via AJAX or form submission
    """
    if request.method == 'POST':
        user = request.user
        
        # Update profile fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.phone = request.POST.get('phone', user.phone)
        
        # Handle file upload
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')