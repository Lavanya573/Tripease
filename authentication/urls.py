from django.urls import path
from . import views
from hotel.views import edit_profile

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
] 