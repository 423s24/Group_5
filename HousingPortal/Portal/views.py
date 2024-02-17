from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAccountForm
from .models import UserAccount
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def dashboard(request):
    users = UserAccount.objects.all()
    per_page = 3
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'dashboard.html', {'users': users})


def index(request):
    return render(request, 'index.html')

def application(request):
    return render(request, 'forms/application/application.html')

def maintenance(request):
    return render(request, 'forms/maintenance/maintenance.html')


def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : username})


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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = 'application/application.html'


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('success_view')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')

