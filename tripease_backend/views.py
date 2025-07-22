from django.shortcuts import render
from tourism.models import TourPackage
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    featured_packages = TourPackage.objects.filter(is_active=True)[:3]
    return render(request, 'home.html', {'featured_packages': featured_packages}) 