from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import UserProfile

# User login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = AuthenticationForm(request, data=request.POST or None)
    reg_form = UserCreationForm(request.POST or None)
    reg_success = False
    if request.method == 'POST':
        if 'login' in request.POST:
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                next_url = request.GET.get('next') or '/authentication/profile/'
                return redirect(next_url)
        elif 'signup' in request.POST:
            if reg_form.is_valid():
                reg_form.save()
                reg_success = True
    return render(request, 'authentication/login.html', {'form': form, 'reg_form': reg_form, 'reg_success': reg_success})

# User logout
def logout_view(request):
    logout(request)
    return render(request, 'authentication/logged_out.html')

# User registration
def register_view(request):
    return HttpResponse('Register page (to be implemented)')

# User profile
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'authentication/profile.html', {'profile': profile})
