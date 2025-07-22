from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment_page'),
    path('process/', views.process_payment, name='process_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('qr/', views.payment_page, name='payment_qr'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('success/', views.payment_success, name='payment_success'),
] 