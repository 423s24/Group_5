
from django.urls import path
from .views import index, application, maintenance, user_login, add_user_account, success_view

urlpatterns = [
    path('', index, name='index'),
    path('forms/application', application, name='application'),
    path('forms/maintenance', maintenance, name='maintenance'),
    path('login/', user_login, name='login'),
    path('add_user_account/', add_user_account, name='add_user_account'),
    path('success/', success_view, name='success_view'),
]