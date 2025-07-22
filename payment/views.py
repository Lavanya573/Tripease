from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Payment
from django.contrib.auth.decorators import login_required
from flights.models import FlightBooking
from tourism.models import TourBooking
from hotel.models import Booking, Cab

# Payment page
@login_required
def payment_page(request):
    booking_id = request.session.get('booking_id')
    booking_type = request.session.get('booking_type')

    amount = 0
    if booking_type == 'cab':
        cab = get_object_or_404(Cab, id=booking_id)
        amount = 1000  # Example fixed price for cab booking
    context = {
        'booking_id': booking_id,
        'booking_type': booking_type,
        'amount': amount,
    }
    return render(request, 'payment/payment_methods.html', context)

# Process payment
@login_required
def process_payment(request):
    if request.method == 'POST':
        booking_id = request.session.get('booking_id')
        booking_type = request.session.get('booking_type')
        payment_method = request.POST.get('payment_method')

        amount = 0
        if booking_type == 'flight':
            booking = get_object_or_404(FlightBooking, id=booking_id)
            amount = booking.flight.price
        elif booking_type == 'tour':
            booking = get_object_or_404(TourBooking, id=booking_id)
            amount = booking.tour_package.price
        elif booking_type == 'hotel':
            booking = get_object_or_404(Booking, id=booking_id)
            amount = booking.room.price_per_night
        elif booking_type == 'cab':
            cab = get_object_or_404(Cab, id=booking_id)
            amount = 1000  # Example fixed price for cab booking

        Payment.objects.create(
            user=request.user,
            amount=amount,
            mode=payment_method,
            status='Success'
        )

        # Clear booking info from session
        if 'booking_id' in request.session:
            del request.session['booking_id']
        if 'booking_type' in request.session:
            del request.session['booking_type']

        return redirect('payment_success')
    
    return redirect('payment_page')

# Payment Success page
@login_required
def payment_success(request):
    return render(request, 'payment/payment_success.html')

# Payment history
@login_required
def my_payments(request):
    payments = Payment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'payment/payment_history.html', {'payments': payments})

def payment_history(request):
    return my_payments(request)
