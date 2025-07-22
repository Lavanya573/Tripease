"""
URL configuration for tripease_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home
from django.views.generic import TemplateView
from hotel import views as hotel_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('hotel/', include('hotel.urls')),
    path('tourism/', include('tourism.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('feedback/', include('feedback.urls')),
    path('notifications/', include('notifications.urls')),
    path('support/', include('support.urls')),
    path('authentication/', include('authentication.urls')),
    path('payment/', include('payment.urls')),
    path('flights/', include('flights.urls')),
    path('cabs/', hotel_views.cabs_page, name='cabs_page'),
    path('buses/', hotel_views.buses_page, name='buses_page'),
    path('trains/', hotel_views.trains_page, name='trains_page'),
    path('holidays/', hotel_views.holidays_page, name='holidays_page'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    # path('chat/', include('chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
