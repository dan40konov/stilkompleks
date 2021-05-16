from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .decorators import not_authenticated_user
from django.contrib.auth.models import Group
from . decorators import admin_only

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'dashboard.html')

@not_authenticated_user
def user_register(request):
    
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, "Account Created Succesfully For  " + username)
            return redirect('home')

    return render(request, 'register.html', {'form': form })

@not_authenticated_user
def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, "User logged in as " + username)
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Login not possible")
    return render(request, 'login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='user_login')
@admin_only
def admin_page(request):
    return render(request, 'admin.html')
