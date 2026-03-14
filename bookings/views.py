from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from rooms.models import Room
from .forms import BookingForm
import datetime


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id, available=True)
    check_in = request.GET.get('check_in', '')
    check_out = request.GET.get('check_out', '')
    guests = request.GET.get('guests', 1)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_price = booking.calculate_total()

            # Check availability
            conflicting = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            )
            if conflicting.exists():
                messages.error(request, 'Sorry, this room is not available for the selected dates.')
            elif booking.check_in >= booking.check_out:
                messages.error(request, 'Check-out date must be after check-in date.')
            elif booking.check_in < timezone.now().date():
                messages.error(request, 'Check-in date cannot be in the past.')
            elif booking.guests > room.capacity:
                messages.error(request, f'This room can accommodate maximum {room.capacity} guests.')
            else:
                booking.save()
                messages.success(request, f'Booking created! Reference: {booking.booking_reference}')
                return redirect('payments:initiate', booking_id=booking.id)
    else:
        initial = {}
        if check_in:
            initial['check_in'] = check_in
        if check_out:
            initial['check_out'] = check_out
        if guests:
            initial['guests'] = guests
        form = BookingForm(initial=initial)

    # Calculate price preview
    total_preview = None
    if check_in and check_out:
        try:
            ci = datetime.datetime.strptime(check_in, '%Y-%m-%d').date()
            co = datetime.datetime.strptime(check_out, '%Y-%m-%d').date()
            nights = (co - ci).days
            if nights > 0:
                total_preview = nights * room.price_per_night
        except:
            pass

    context = {
        'form': form,
        'room': room,
        'total_preview': total_preview,
    }
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        if booking.can_cancel:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, f'Booking {booking.booking_reference} has been cancelled.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
    return redirect('accounts:dashboard')
