from django.shortcuts import render, HttpResponse

# Create your views here.
def dashboard(request):
    return HttpResponse("dashboard test")