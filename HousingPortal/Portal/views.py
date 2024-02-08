from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def application(request):
    return render(request, 'forms/application/application.html')

def maintenance(request):
    return render(request, 'forms/maintenance/maintenance.html')

def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : user_profile})