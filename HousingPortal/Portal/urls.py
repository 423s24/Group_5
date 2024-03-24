
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # Page URLs
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/requests/', views.maintenance_requests, name='maintenance_requests'),
    path('dashboard/requests/<int:request_id>', views.request_info, name='request_info'),
    #TODO path('dashboard/users/', views.users, name='users'),
    path('dashboard/users/<str:username>/', views.view_user, name='view_user'),
    #TODO dashboard/users/create
    #TODO path('dashboard/buildings/', views.dashboard, name='dashboard'),
    path('dashboard/buildings/<int:building_id>', views.building_info, name='building_info'),
    path('dashboard/buildings/create/', views.add_building, name='createbuilding'),
    path('support/', views.support, name='support'),
    path('profile/', views.profile, name='profile'),

    # Authenticaiton URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Functionality URLs
    path('delete/', views.delete, name='delete'),
    
    path('forms/maintenance', views.maintenance, name='maintenance'),
    path('createbuilding/', views.add_building, name='createbuilding'),
    path('building/<int:building_id>', views.building_info, name='building_info'),
    path('request/<int:request_id>', views.request_info, name='request_info'),
    path('request/<int:request_id>/add_note', views.add_note, name='add_note'),
    path('request/edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('request/delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('request/<int:request_id>/edit_request', views.edit_request, name='edit_request'),
    #path('success/', views.success_view, name='success_view'),
    #path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_comp.html'), name='password_reset_complete'),
]