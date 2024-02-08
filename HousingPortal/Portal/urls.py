
from django.urls import path
from .views import index, application, maintenance

urlpatterns = [
    path('', index, name='index'),
    path('forms/application', application, name='application'),
    path('forms/maintenance', maintenance, name='maintenance'),
]