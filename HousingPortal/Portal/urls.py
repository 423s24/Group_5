
from django.urls import path
from .views import index, application, maintenance

urlpatterns = [
    path('', index, name='index'),
    path('forms/', application, name='application'),
    path('forms/', maintenance, name='maintenance'),
]