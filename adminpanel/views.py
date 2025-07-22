from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from authentication.models import UserProfile

# Admin dashboard
def dashboard(request):
    return HttpResponse('Admin dashboard (to be implemented)')

# List users
def user_list(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'adminpanel/user_list.html', {'users': users})

# List reports
def report_list(request):
    return HttpResponse('Report list (to be implemented)')
