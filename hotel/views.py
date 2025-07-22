from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Room, Booking, Train, Holiday, Cab, Bus, Payment, Feedback, Offer, Wishlist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from flights.models import Flight, FlightBooking
from tourism.models import TourBooking, TourPackage
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from payment.models import Payment as GlobalPayment
from notifications.views import create_notification

def hotel_list(request):
    rooms = Room.objects.all()
    city = request.GET.get('city', '').strip()
    room_type = request.GET.get('room_type', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    status = request.GET.get('status', '').strip()

    if city:
        rooms = rooms.filter(city__icontains=city)
    if room_type:
        rooms = rooms.filter(room_type__icontains=room_type)
    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)
    if status:
        rooms = rooms.filter(status=status)

    return render(request, 'hotel/room_list.html', {
        'rooms': rooms,
        'search': {
            'city': city,
            'room_type': room_type,
            'min_price': min_price,
            'max_price': max_price,
            'status': status,
        }
    })

# View to show hotel details
@login_required
def hotel_detail(request, hotel_id):
    room = get_object_or_404(Room, pk=hotel_id)
    message = None
    feedback_message = None
    feedbacks = Feedback.objects.filter(room=room).order_by('-created_at')
    has_booked = Booking.objects.filter(user=request.user, room=room, is_cancelled=False).exists()
    has_left_feedback = Feedback.objects.filter(user=request.user, room=room).exists()
    if request.method == 'POST':
        # Feedback form submission
        if 'feedback_submit' in request.POST:
            if not has_booked:
                feedback_message = 'You must book this room before leaving feedback.'
            elif has_left_feedback:
                feedback_message = 'You have already left feedback for this room.'
            else:
                rating = int(request.POST.get('rating', 0))
                comment = request.POST.get('comment', '').strip()
                if rating < 1 or rating > 5:
                    feedback_message = 'Please select a valid rating.'
                else:
                    Feedback.objects.create(user=request.user, room=room, rating=rating, comment=comment)
                    feedback_message = 'Thank you for your feedback!'
                    has_left_feedback = True
                    # Refresh feedbacks
                    feedbacks = Feedback.objects.filter(room=room).order_by('-created_at')
        # Booking form submission
        else:
            if room.status != 'available':
                message = 'Sorry, this room is not available.'
            else:
                check_in = request.POST.get('check_in')
                check_out = request.POST.get('check_out')
                if check_in and check_out:
                    booking = Booking.objects.create(
                        user=request.user,
                        room=room,
                        check_in=check_in,
                        check_out=check_out,
                        is_cancelled=False
                    )
                    room.status = 'unavailable'
                    room.save()
                    create_notification(request.user, f'You have successfully booked Room {room.number}.')
                    
                    request.session['booking_id'] = booking.id
                    request.session['booking_type'] = 'hotel'

                    return redirect('payment_page')
                else:
                    message = 'Please provide check-in and check-out dates.'
    return render(request, 'hotel/room_detail.html', {
        'room': room,
        'message': message,
        'feedbacks': feedbacks,
        'has_booked': has_booked,
        'has_left_feedback': has_left_feedback,
        'feedback_message': feedback_message,
    })

# View to list rooms in a hotel
def room_list(request, hotel_id):
    return HttpResponse(f'Room list for hotel {hotel_id} (to be implemented)')

# View to list bookings for a hotel
def booking_list(request, hotel_id):
    return HttpResponse(f'Booking list for hotel {hotel_id} (to be implemented)')

@login_required
def my_bookings(request):
    if request.method == 'POST':
        cancel_id = request.GET.get('cancel')
        if cancel_id:
            booking = Booking.objects.filter(id=cancel_id, user=request.user, is_cancelled=False).first()
            if booking:
                booking.is_cancelled = True
                booking.save()
                booking.room.status = 'available'
                booking.room.save()
                create_notification(request.user, f'You have cancelled your booking for Room {booking.room.number} ({booking.room.room_type}).', notification_type='warning')
    # Fetch all types of bookings
    hotel_bookings = Booking.objects.filter(user=request.user, is_cancelled=False).order_by('-created_at')
    cab_bookings = CabBooking.objects.filter(user=request.user, is_cancelled=False).order_by('-created_at')
    holiday_bookings = TourBooking.objects.filter(user=request.user, is_cancelled=False).order_by('-tour_date')
    flight_bookings = FlightBooking.objects.filter(user=request.user).order_by('-travel_date')
    return render(request, 'hotel/my_bookings.html', {
        'hotel_bookings': hotel_bookings,
        'cab_bookings': cab_bookings,
        'holiday_bookings': holiday_bookings,
        'flight_bookings': flight_bookings,
    })

def cabs_page(request):
    cabs = Cab.objects.all()
    from_city = request.GET.get('from_city', '').strip()
    to_city = request.GET.get('to_city', '').strip()
    date = request.GET.get('date', '').strip()
    if from_city:
        cabs = cabs.filter(from_city__icontains=from_city)
    if to_city:
        cabs = cabs.filter(to_city__icontains=to_city)
    if date:
        cabs = cabs.filter(departure__date=date)
    return render(request, 'hotel/cabs_page.html', {'cabs': cabs})

def buses_page(request):
    buses = Bus.objects.all()
    from_city = request.GET.get('from_city', '').strip()
    to_city = request.GET.get('to_city', '').strip()
    date = request.GET.get('date', '').strip()
    if from_city:
        buses = buses.filter(from_city__icontains=from_city)
    if to_city:
        buses = buses.filter(to_city__icontains=to_city)
    if date:
        buses = buses.filter(departure__date=date)
    return render(request, 'hotel/buses_page.html', {'buses': buses})

def trains_page(request):
    trains = Train.objects.all()
    from_city = request.GET.get('from_city', '').strip()
    to_city = request.GET.get('to_city', '').strip()
    date = request.GET.get('date', '').strip()
    if from_city:
        trains = trains.filter(from_city__icontains=from_city)
    if to_city:
        trains = trains.filter(to_city__icontains=to_city)
    if date:
        trains = trains.filter(departure__date=date)
    return render(request, 'hotel/trains_page.html', {'trains': trains})

def holidays_page(request):
    holidays = Holiday.objects.all()
    return render(request, 'hotel/holidays_page.html', {'holidays': holidays})
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payments/payment_list.html', {'payments': payments})

def features_page(request):
    return render(request, 'hotel/features.html')

@login_required
def book_cab(request, cab_id):
    cab = get_object_or_404(Cab, pk=cab_id)
    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        # Create a CabBooking record
        cab_booking = CabBooking.objects.create(
            user=request.user,
            cab=cab,
            travel_date=travel_date,
            is_cancelled=False
        )
        # Store cab booking info in session for payment
        request.session['booking_id'] = cab_booking.id
        request.session['booking_type'] = 'cab'
        return redirect('payment_page')
    return render(request, 'hotel/cab_booking.html', {'cab': cab})

@login_required
def book_train(request, train_id):
    train = get_object_or_404(Train, pk=train_id)
    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        # booking = TrainBooking.objects.create(
        #     user=request.user,
        #     train=train,
        #     travel_date=travel_date,
        #     is_cancelled=False
        # )
        return redirect('my_bookings')
    return render(request, 'hotel/train_booking.html', {'train': train})

@login_required
def book_holiday(request, holiday_id):
    package = get_object_or_404(TourPackage, pk=holiday_id)
    if request.method == 'POST':
        tour_date = request.POST.get('tour_date')
        num_people = request.POST.get('num_people')
        # Create the booking record
        TourBooking.objects.create(
            user=request.user,
            tour_package=package,
            tour_date=tour_date,
            num_people=num_people,
            is_cancelled=False
        )
        # Create a notification
        create_notification(request.user, f'You have successfully booked the "{package.name}" holiday.')
        # Redirect to payment
        return redirect('payment_page')
    return render(request, 'hotel/holiday_booking.html', {'package': package})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        travel_date = request.POST.get('travel_date')
        num_passengers = request.POST.get('num_passengers')
        booking = FlightBooking.objects.create(
            user=request.user,
            flight=flight,
            travel_date=travel_date,
            num_passengers=num_passengers
        )
        return redirect(f'/hotel/review-booking/flight/{booking.id}/')
    return render(request, 'hotel/flight_booking.html', {'flight': flight})

@login_required
def book_bus(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    # Here you would create a booking record for the user and the bus
    # For now, just show a confirmation page
    return render(request, 'hotel/book_bus_confirmation.html', {'bus': bus})

# Add review_booking view
@login_required
def review_booking(request, booking_type, booking_id):
    # booking_type: 'room', 'cab', 'train', 'holiday', 'flight'
    context = {}
    if booking_type == 'room':
        booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
        if request.method == 'POST':
            # If you have a 'confirmed' or 'is_finalized' field, set it here. Otherwise, just redirect.
            # booking.confirmed = True
            # booking.save()
            return redirect('/hotel/my-bookings/')
        context['booking'] = booking
        context['type'] = 'Room'
    elif booking_type == 'cab':
        # booking = get_object_or_404(CabBooking, pk=booking_id, user=request.user)
        # if request.method == 'POST':
        return redirect('my_bookings')
        # context['booking'] = booking
        # context['type'] = 'Cab'
    elif booking_type == 'train':
        # booking = get_object_or_404(TrainBooking, pk=booking_id, user=request.user)
        # if request.method == 'POST':
        return redirect('my_bookings')
        # context['booking'] = booking
        # context['type'] = 'Train'
    elif booking_type == 'holiday':
        booking = get_object_or_404(TourBooking, pk=booking_id, user=request.user)
        if request.method == 'POST':
            return redirect('my_bookings')
        context['booking'] = booking
        context['type'] = 'Holiday'
    elif booking_type == 'flight':
        booking = get_object_or_404(FlightBooking, pk=booking_id, user=request.user)
        if request.method == 'POST':
            return redirect('/hotel/my-bookings/')
        context['booking'] = booking
        context['type'] = 'Flight'
    else:
        return redirect('/')
    return render(request, 'hotel/review_booking.html', context)

@login_required
def payment_view(request):
    if request.method == 'POST':
        # Calculate total amount
        cart = request.session.get('cart', [])
        cab_ids = [int(item['id']) for item in cart if item['type'] == 'cab']
        train_ids = [int(item['id']) for item in cart if item['type'] == 'train']
        holiday_ids = [int(item['id']) for item in cart if item['type'] == 'holiday']
        room_ids = [int(item['id']) for item in cart if item['type'] == 'room']
        flight_ids = [int(item['id']) for item in cart if item['type'] == 'flight']
        cabs = Cab.objects.filter(id__in=cab_ids) if cab_ids else []
        trains = Train.objects.filter(id__in=train_ids) if train_ids else []
        holidays = Holiday.objects.filter(id__in=holiday_ids) if holiday_ids else []
        rooms = Room.objects.filter(id__in=room_ids) if room_ids else []
        flights = Flight.objects.filter(id__in=flight_ids) if flight_ids else []
        # Sum up prices
        total = 0
        for cab in cabs:
            total += float(getattr(cab, 'price', 0))
        for train in trains:
            total += float(getattr(train, 'price', 0)) if hasattr(train, 'price') else 0
        for holiday in holidays:
            total += float(getattr(holiday, 'price', 0)) if hasattr(holiday, 'price') else 0
        for room in rooms:
            total += float(getattr(room, 'price_per_night', 0))
        for flight in flights:
            total += float(getattr(flight, 'price', 0))
        payment_mode = request.POST.get('payment_method', 'card')
        Payment.objects.create(
            user=request.user,
            amount=total,
            payment_mode=payment_mode,
            status='Success',
            details=f"Cabs: {cab_ids}, Trains: {train_ids}, Holidays: {holiday_ids}, Rooms: {room_ids}, Flights: {flight_ids}"
        )
        request.session['cart'] = []
        request.session.modified = True
        return redirect('/hotel/cart/')
    cart = request.session.get('cart', [])
    cab_ids = [int(item['id']) for item in cart if item['type'] == 'cab']
    train_ids = [int(item['id']) for item in cart if item['type'] == 'train']
    holiday_ids = [int(item['id']) for item in cart if item['type'] == 'holiday']
    room_ids = [int(item['id']) for item in cart if item['type'] == 'room']
    flight_ids = [int(item['id']) for item in cart if item['type'] == 'flight']
    cabs = Cab.objects.filter(id__in=cab_ids) if cab_ids else []
    trains = Train.objects.filter(id__in=train_ids) if train_ids else []
    holidays = Holiday.objects.filter(id__in=holiday_ids) if holiday_ids else []
    rooms = Room.objects.filter(id__in=room_ids) if room_ids else []
    flights = Flight.objects.filter(id__in=flight_ids) if flight_ids else []
    user = request.user
    return render(request, 'hotel/payment.html', {
        'cabs': cabs,
        'trains': trains,
        'holidays': holidays,
        'rooms': rooms,
        'flights': flights,
        'user': user,
    })

@login_required
def my_payments(request):
    # Mark all payments as viewed
    GlobalPayment.objects.filter(user=request.user, is_viewed=False).update(is_viewed=True)
    payments = GlobalPayment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'payment/payment_history.html', {'payments': payments})

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'hotel/edit_profile.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    from .models import Room, Booking, Payment, Feedback
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    total_income = Payment.objects.aggregate(total=models.Sum('amount'))['total'] or 0
    feedback_count = Feedback.objects.count()
    return render(request, 'hotel/admin_dashboard.html', {
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'total_income': total_income,
        'feedback_count': feedback_count,
    })

def offers_page(request):
    offers = Offer.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'offers.html', {'offers': offers})

@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('room')
    return render(request, 'cart/wishlist.html', {'wishlist_items': wishlist_items})
