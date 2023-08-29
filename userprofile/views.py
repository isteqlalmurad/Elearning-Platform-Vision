
# Create your views here.
# views.py
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from userprofile.models import UserProfile
from .forms import CustomUserCreationForm
from django.contrib import messages

from django.shortcuts import render


def landing(request):
    return render(request, 'userprofile/landing.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Handle the additional fields here
            profile = UserProfile(
                user=user, dob=form.cleaned_data['dob'], likes=form.cleaned_data['likes'], image=form.cleaned_data['image'])
            print(request.FILES)
            profile.save()
            logger.info(
                f"New-User {user.username} has successfuly been created.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'userprofile/register.html', {'form': form})


logger = logging.getLogger(__name__)


def user_login(request):
    # user = None  # Initialization to prevent UnboundLocalError
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info(f"User {user.username} logged in successfully.")
                return redirect('home')
            else:
                messages.error(request, 'Account is disabled.')
                logger.warning(
                    f"Attempt to login with disabled account: {user.username}")
        else:
            messages.error(request, 'Invalid login details.')
            logger.warning(f"Invalid login attempt with username: {username}")
    return render(request, 'userprofile/login.html')


def user_logout(request):
    # Logging the logout
    logger.info(f"User {request.user.username} logged out.")
    logout(request)
    # messages.success(request, 'Logged out successfully.') might use it later for notification
    return redirect('landing')
