from django.urls import path
from . import views
from .views import offers_page, wishlist_page

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('<int:hotel_id>/bookings/', views.booking_list, name='booking_list'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('book-cab/<int:cab_id>/', views.book_cab, name='book_cab'),
    path('book-train/<int:train_id>/', views.book_train, name='book_train'),
    path('book-holiday/<int:holiday_id>/', views.book_holiday, name='book_holiday'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('book-bus/<int:bus_id>/', views.book_bus, name='book_bus'),
    path('review-booking/<str:booking_type>/<int:booking_id>/', views.review_booking, name='review_booking'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('features/', views.features_page, name='features'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
urlpatterns += [
    path('offers/', offers_page, name='offers_page'),
    path('wishlist/', wishlist_page, name='wishlist_page'),
] 