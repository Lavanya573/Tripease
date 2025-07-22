from django.urls import path
from . import views

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('<int:package_id>/', views.package_detail, name='package_detail'),
    path('bookings/', views.my_tour_bookings, name='my_tour_bookings'),
    path('review-booking/<int:booking_id>/', views.review_tour_booking, name='review_tour_booking'),
] 