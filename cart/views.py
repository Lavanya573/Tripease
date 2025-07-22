from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Wishlist, WishlistItem
from django.contrib.auth.decorators import login_required
from tourism.models import TourPackage
from flights.models import Flight  # Import the Flight model
from hotel.models import Room
from django.views.decorators.http import require_POST
from django.contrib import messages
from notifications.views import create_notification

@login_required
def view_wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('room').all()
    return render(request, 'cart/wishlist.html', {'wishlist_items': items})

@login_required
def add_to_wishlist(request, room_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    room = get_object_or_404(Room, pk=room_id)
    WishlistItem.objects.get_or_create(wishlist=wishlist, room=room)
    messages.success(request, f'"{room.room_type}" has been added to your wishlist.')
    return redirect('view_wishlist')

@require_POST
@login_required
def remove_from_wishlist(request, item_id):
    try:
        wishlist_item = get_object_or_404(WishlistItem, pk=item_id, wishlist__user=request.user)
        item_name = f"Room {wishlist_item.room.number} ({wishlist_item.room.room_type})" if wishlist_item.room else "Item"
        wishlist_item.delete()
        messages.success(request, f'{item_name} has been removed from your wishlist.')
    except Exception as e:
        messages.error(request, f'Error removing item from wishlist: {str(e)}')
    return redirect('view_wishlist')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('room', 'tour_package', 'flight').all()
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'items': items})

# View to add an item to the cart
@require_POST
@login_required
def add_to_cart(request, item_type, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if item_type == 'tour':
        try:
            package = TourPackage.objects.get(pk=item_id)
            CartItem.objects.create(cart=cart, tour_package=package, quantity=1)
            messages.success(request, f'"{package.name}" has been added to your cart.')
            create_notification(request.user, f'"{package.name}" was added to your cart.')
        except TourPackage.DoesNotExist:
            messages.error(request, 'Tour package not found.')
            pass  # Optionally handle other item types
    elif item_type == 'flight':
        try:
            flight = Flight.objects.get(pk=item_id)
            CartItem.objects.create(cart=cart, flight=flight, quantity=1)
            messages.success(request, f'Flight from {flight.from_city} to {flight.to_city} has been added to your cart.')
            create_notification(request.user, f'Flight from {flight.from_city} to {flight.to_city} was added to your cart.')
        except Flight.DoesNotExist:
            messages.error(request, 'Flight not found.')

    return redirect('view_cart')

# View to remove an item from the cart
@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        item = cart.items.get(pk=item_id)
        item_desc = None
        if item.room:
            item_desc = f"Room {item.room.number} ({item.room.room_type})"
        elif item.tour_package:
            item_desc = f"Tour Package: {item.tour_package.name}"
        elif item.flight:
            item_desc = f"Flight: {item.flight.airline} {item.flight.flight_number}"
        else:
            item_desc = "Item"
        item.delete()
        messages.success(request, f'{item_desc} has been removed from your cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in your cart.')
    return redirect('view_cart')

# View to clear the cart
def clear_cart(request):
    return HttpResponse('Clear cart (to be implemented)')
