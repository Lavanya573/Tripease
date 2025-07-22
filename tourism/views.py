from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TourPackage, TourBooking
from django.utils import timezone
from django.urls import reverse
from notifications.views import create_notification

# Create your views here.

# List all tour packages
def package_list(request):
    packages = TourPackage.objects.filter(is_active=True)
    destination = request.GET.get('destination', '').strip()
    category = request.GET.get('category', '').strip()
    if destination:
        packages = packages.filter(destination__icontains=destination)
    if category:
        packages = packages.filter(category=category)
    return render(request, 'tourism/package_list.html', {'packages': packages})

# Show details for a specific tour package and handle booking
@login_required
def package_detail(request, package_id):
    package = get_object_or_404(TourPackage, pk=package_id)
    if request.method == 'POST':
        tour_date = request.POST.get('tour_date')
        num_people = request.POST.get('num_people')
        try:
            num_people = int(num_people)
        except:
            num_people = 1
        if tour_date and num_people > 0:
            booking = TourBooking.objects.create(
                user=request.user,
                tour_package=package,
                tour_date=tour_date,
                num_people=num_people,
                is_cancelled=False
            )
            create_notification(request.user, f'You have successfully booked the "{package.name}" tour package.')
            
            # Store booking info in session for payment
            request.session['booking_id'] = booking.id
            request.session['booking_type'] = 'tour'

            return redirect('payment_page')
    return render(request, 'tourism/package_detail.html', {'package': package})

# Book a specific tour package (not needed, handled in package_detail)
# def book_package(request, package_id):
#     return HttpResponse(f'Book tour package {package_id} (to be implemented)')

# List all bookings for the user
@login_required
def my_tour_bookings(request):
    bookings = TourBooking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tourism/my_tour_bookings.html', {'bookings': bookings})

@login_required
def review_tour_booking(request, booking_id):
    booking = get_object_or_404(TourBooking, pk=booking_id, user=request.user)
    return render(request, 'tourism/review_tour_booking.html', {'booking': booking})
