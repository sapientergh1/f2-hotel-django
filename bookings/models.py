from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room
from decimal import Decimal


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username} - {self.room.name}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random, string
            self.booking_reference = 'F2-' + ''.join(random.choices(string.digits, k=8))
        if not self.total_price:
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self):
        nights = (self.check_out - self.check_in).days
        return Decimal(str(nights)) * self.room.price_per_night

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    @property
    def can_cancel(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.status in ('pending', 'confirmed') and self.check_in > timezone.now().date() + timedelta(days=1)
