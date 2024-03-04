
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('forms/application', views.application, name='application'),
    path('forms/maintenance', views.maintenance, name='maintenance'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.payment, name='payment'),
    path('support/', views.support, name='support'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete_user, name='delete'),
    path('createbuilding/', views.add_building, name='createbuilding'),
    path('building/<int:building_id>', views.building_info, name='building_info')
    #path('success/', views.success_view, name='success_view'),
    #path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]