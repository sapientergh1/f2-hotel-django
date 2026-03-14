from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'user', 'room', 'check_in', 'check_out', 'guests', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'check_in', 'room__room_type']
    list_editable = ['status']
    search_fields = ['booking_reference', 'user__username', 'room__name']
    readonly_fields = ['booking_reference', 'total_price', 'created_at']
    date_hierarchy = 'check_in'
