from django.db import models
from django.contrib.auth.models import User
from hotel.models import Room
from tourism.models import TourPackage
from flights.models import Flight # Import the flight model

# Create your models here.

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user.username}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    # Add other item types as needed, e.g., tour_package, flight

    def __str__(self):
        if self.room:
            return f"Room {self.room.number} in {self.wishlist.user.username}'s wishlist"
        return f"WishlistItem {self.pk}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = getattr(self.user, 'username', None)
        return f"Cart for {username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.room:
            room_number = getattr(self.room, 'number', None)
            return f"Room {room_number} in cart"
        elif self.tour_package:
            tour_name = getattr(self.tour_package, 'name', None)
            return f"Tour {tour_name} in cart"
        elif self.flight:
            return f"Flight {self.flight.flight_number} in cart"
        else:
            return f"CartItem {self.pk}"
