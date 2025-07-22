from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Flight, FlightBooking
from django.utils import timezone
from notifications.views import create_notification

# Create your views here.

# Flight search and listing
def flight_list(request):
    flights = Flight.objects.all()
    from_city = request.GET.get('from_city', '').strip()
    to_city = request.GET.get('to_city', '').strip()
    date = request.GET.get('date', '').strip()
    passengers = request.GET.get('passengers', '').strip()

    if from_city:
        flights = flights.filter(from_city__icontains=from_city)
    if to_city:
        flights = flights.filter(to_city__icontains=to_city)
    if date:
        flights = flights.filter(departure__date=date)
    # Optionally filter by available seats
    if passengers:
        try:
            p = int(passengers)
            flights = flights.filter(seats_available__gte=p)
        except:
            pass

    return render(request, 'flights/flight_list.html', {
        'flights': flights,
        'search': {
            'from_city': from_city,
            'to_city': to_city,
            'date': date,
            'passengers': passengers,
        }
    })

# Flight detail and booking
@login_required
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        num_passengers = request.POST.get('num_passengers')
        try:
            num_passengers = int(num_passengers)
        except:
            num_passengers = 1
        if flight.seats_available < num_passengers:
            message = 'Not enough seats available.'
        else:
            booking = FlightBooking.objects.create(
                user=request.user,
                flight=flight,
                travel_date=travel_date,
                num_passengers=num_passengers
            )
            flight.seats_available -= num_passengers
            flight.save()
            create_notification(request.user, f'You have successfully booked a flight from {flight.from_city} to {flight.to_city}.')
            
            # Store booking info in session for payment
            request.session['booking_id'] = booking.id
            request.session['booking_type'] = 'flight'

            return redirect('payment_page')
    return render(request, 'flights/flight_detail.html', {'flight': flight})

# User's flight bookings
@login_required
def my_flight_bookings(request):
    bookings = FlightBooking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'flights/my_flight_bookings.html', {'bookings': bookings})
