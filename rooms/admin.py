from django.contrib import admin
from .models import Room, RoomReview, GalleryImage


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'price_per_night', 'capacity', 'available', 'featured']
    list_filter = ['room_type', 'available', 'featured']
    list_editable = ['available', 'featured', 'price_per_night']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'room_type', 'description', 'price_per_night', 'capacity', 'size_sqm', 'floor', 'bed_type')}),
        ('Images', {'fields': ('image', 'image2', 'image3')}),
        ('Status', {'fields': ('available', 'featured')}),
        ('Amenities', {'fields': ('has_ac', 'has_wifi', 'has_tv', 'has_fridge', 'has_desk', 'has_private_bathroom', 'has_room_service', 'has_balcony', 'has_kitchenette', 'has_living_room')}),
    )


@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['room__name', 'user__username']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'order']
    list_filter = ['category', 'featured']
    list_editable = ['featured', 'order']
