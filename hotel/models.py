from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    ROOM_STATUS = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    number = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100, default='')  # New field for city/location
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=12, choices=ROOM_STATUS, default='available')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/rooms/', blank=True, null=True)

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='hotel_bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField()

    def __str__(self):
        room_number = getattr(self.room, 'number', None)
        username = getattr(self.user, 'username', None)
        return f"Booking {self.pk} - Room {room_number} by {username}"

class Order(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='hotel_orders')
    item = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        booking_pk = getattr(self.booking, 'pk', None)
        return f"Order {self.pk} for Booking {booking_pk}"

class Stock(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    threshold = models.PositiveIntegerField()  # For low stock alert
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity <= self.threshold

    def __str__(self):
        return self.name

# Simple Train model for admin
class Train(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.number})"

# Simple Cab model for admin
class Cab(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.number})"

# Simple Bus model for admin
class Bus(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.number})"

# Simple Holiday model for admin
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='images/holidays/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

class Payment(models.Model):
    PAYMENT_MODES = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('cash', 'Cash'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    status = models.CharField(max_length=20, default='Success')
    details = models.TextField(blank=True)

    def __str__(self):
        return f"Payment {self.pk} by {self.user.username} - {self.amount} ({self.payment_mode})"

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_feedbacks')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='hotel_feedbacks')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for Room {self.room.number} ({self.rating} stars)"

class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/offers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist for {self.user.username} - Room {self.room}" if self.room else f"Wishlist for {self.user.username}";

class CabBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"CabBooking {self.pk} - {self.cab.name} by {self.user.username}"
