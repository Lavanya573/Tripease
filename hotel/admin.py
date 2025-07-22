from django.contrib import admin
from .models import Room, Booking, Order, Stock, Offer, Wishlist

# Register Train model if it exists
try:
    from .models import Train
    admin.site.register(Train)
except ImportError:
    pass

# Register Cabs, Buses, Holidays models if they exist
try:
    from .models import Cab
    admin.site.register(Cab)
except ImportError:
    pass
try:
    from .models import Bus
    admin.site.register(Bus)
except ImportError:
    pass
try:
    from .models import Holiday
    admin.site.register(Holiday)
except ImportError:
    pass

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(Stock)
admin.site.register(Offer)
admin.site.register(Wishlist)
