from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('submit/', views.submit_feedback, name='submit_feedback'),
] 