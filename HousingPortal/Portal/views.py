from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, AuthForm
from .models import UserAccount
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def support(request):
    return render(request, 'support.html')

@login_required(login_url="/login")
def dashboard(request):
    users = UserAccount.objects.all()
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'dashboard.html', {'users': users})

@login_required(login_url="/login")
def application(request):
    return render(request, 'forms/application/application.html')

@login_required(login_url="/login")
def maintenance(request):
    return render(request, 'forms/maintenance/maintenance.html')

def payment(request):
    return render(request, 'payment.html')

@login_required(login_url="/login")
def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : username})

# Views for user accounts and authentication
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                request.session.set_expiry(1800) # Set session expiry to 30 minutes
                return redirect('/')
        else:
            form = RegisterForm()
        
        return render(request, 'registration/signup.html', {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = AuthForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(1800) # Set session expiry to 30 minutes
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/dashboard')
        else:
            form = AuthForm(request)
        return render(request, 'registration/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')

# Views for errors
def handler_404(request, exception):
    return render(request, '404.html', status=404)