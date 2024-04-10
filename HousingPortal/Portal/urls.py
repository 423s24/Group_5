
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # Page URLs
    path('', views.home, name='home'),
    path('support/', views.support, name='support'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/requests/', views.maintenance_requests, name='maintenance_requests'),
    path('dashboard/requests/saved', views.saved_requests, name='saved_requests'),
    path('dashboard/requests/<int:request_id>', views.request_info, name='request_info'),
    path('dashboard/users/', views.users, name='users'),
    path('dashboard/users/<str:username>/', views.view_user, name='view_user'),
    #TODO dashboard/users/create
    path('dashboard/buildings/', views.buildings, name='buildings'),
    path('dashboard/buildings/<int:building_id>', views.building_info, name='building_info'),
    path('dashboard/buildings/create/', views.add_building, name='createbuilding'),
    path('search/', views.advanced_search, name='search'),
   
    # Authenticaiton URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_comp.html'), name='password_reset_complete'),

    # Functionality URLs
    path('delete/', views.delete, name='delete'),
    path('toggle_save/<int:request_id>', views.toggle_save, name='toggle_save'),
    path('check_username/', views.check_username, name='check_username'),
    
    # TODO Change urls below to new site structure
    path('forms/maintenance', views.maintenance, name='maintenance'),
    path('createbuilding/', views.add_building, name='createbuilding'),
    path('building/<int:building_id>', views.building_info, name='building_info'),
    path('request/<int:request_id>', views.request_info, name='request_info'),
    path('request/<int:request_id>/add_note', views.add_note, name='add_note'),
    path('request/edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('request/delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('request/<int:request_id>/edit_request', views.edit_request, name='edit_request'),
]