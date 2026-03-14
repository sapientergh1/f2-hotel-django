from django.shortcuts import render, get_object_or_404
from .models import Room, GalleryImage, RoomReview
from bookings.models import Booking
import datetime


def room_list(request):
    rooms = Room.objects.filter(available=True)
    room_type    = request.GET.get('type', '')
    check_in     = request.GET.get('check_in', '')
    check_out    = request.GET.get('check_out', '')
    guests       = request.GET.get('guests', '')

    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if guests:
        try:
            rooms = rooms.filter(capacity__gte=int(guests))
        except ValueError:
            pass

    if check_in and check_out:
        try:
            ci = datetime.datetime.strptime(check_in, '%Y-%m-%d').date()
            co = datetime.datetime.strptime(check_out, '%Y-%m-%d').date()
            booked_ids = Booking.objects.filter(
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in__lt=co,
                check_out__gt=ci,
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=booked_ids)
        except ValueError:
            pass

    context = {
        'rooms':         rooms,
        'room_types':    Room.ROOM_TYPES,
        'selected_type': room_type,
        'check_in':      check_in,
        'check_out':     check_out,
        'guests':        guests,
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail(request, pk):
    room         = get_object_or_404(Room, pk=pk, available=True)
    reviews      = room.reviews.all()[:5]
    similar_rooms = Room.objects.filter(room_type=room.room_type, available=True).exclude(pk=pk)[:3]
    check_in  = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    guests    = request.GET.get('guests', 1)
    context = {
        'room':          room,
        'reviews':       reviews,
        'similar_rooms': similar_rooms,
        'check_in':      check_in,
        'check_out':     check_out,
        'guests':        guests,
    }
    return render(request, 'rooms/room_detail.html', context)


def gallery(request):
    images   = GalleryImage.objects.all()
    category = request.GET.get('category', '')
    if category:
        images = images.filter(category=category)
    categories = GalleryImage._meta.get_field('category').choices

    # Placeholder images shown when DB has no gallery entries
    placeholder_images = [
        ('https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=700&q=80', 'Deluxe Room', 'rooms'),
        ('https://images.unsplash.com/photo-1590490360182-c33d57733427?w=700&q=80', 'Standard Room', 'rooms'),
        ('https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=700&q=80', 'Executive Room', 'rooms'),
        ('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=700&q=80', 'Swimming Pool', 'pool'),
        ('https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=700&q=80', 'Restaurant', 'restaurant'),
        ('https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=700&q=80', 'Hotel Lobby', 'lobby'),
        ('https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=700&q=80', 'Apartment Suite', 'rooms'),
        ('https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=700&q=80', 'Hotel Exterior', 'exterior'),
        ('https://images.unsplash.com/photo-1551218808-94e220e084d2?w=700&q=80', 'Hotel Bar', 'restaurant'),
    ]

    context = {
        'images':             images,
        'categories':         categories,
        'selected_category':  category,
        'placeholder_images': placeholder_images,
    }
    return render(request, 'rooms/gallery.html', context)
