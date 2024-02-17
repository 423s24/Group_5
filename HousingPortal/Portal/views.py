from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAccountForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def application(request):
    return render(request, 'forms/application/application.html')

def maintenance(request):
    return render(request, 'forms/maintenance/maintenance.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login/login.html')

def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : user_profile})


def add_user_account(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_view')
    else:
        form = UserAccountForm()

    return render(request, 'add_user_account.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')


