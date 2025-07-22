from django.contrib import admin
from .models import TourPackage, TourBooking

class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'category', 'price', 'duration_days', 'is_active', 'image_preview')
    search_fields = ('name', 'destination', 'category')
    list_filter = ('category', 'is_active')
    fields = ('name', 'description', 'destination', 'category', 'price', 'duration_days', 'is_active', 'image')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image}" style="height:60px;max-width:120px;object-fit:cover;" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

admin.site.register(TourPackage, TourPackageAdmin)
admin.site.register(TourBooking)
