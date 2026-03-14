from django.db import models


class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('executive', 'Executive Room'),
        ('family', 'Family Room'),
        ('apartment', 'Apartment'),
    ]

    name = models.CharField(max_length=200)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='standard')
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    size_sqm = models.PositiveIntegerField(default=25, help_text="Room size in square meters")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image2 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image3 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    floor = models.PositiveIntegerField(default=1)
    bed_type = models.CharField(max_length=100, default='Queen Bed')
    # Amenities
    has_ac = models.BooleanField(default=True, verbose_name="Air Conditioning")
    has_wifi = models.BooleanField(default=True, verbose_name="Free WiFi")
    has_tv = models.BooleanField(default=True, verbose_name="Flat Screen TV")
    has_fridge = models.BooleanField(default=True, verbose_name="Refrigerator")
    has_desk = models.BooleanField(default=True, verbose_name="Work Desk")
    has_private_bathroom = models.BooleanField(default=True, verbose_name="Private Bathroom")
    has_room_service = models.BooleanField(default=True, verbose_name="Room Service")
    has_balcony = models.BooleanField(default=False, verbose_name="Balcony")
    has_kitchenette = models.BooleanField(default=False, verbose_name="Kitchenette")
    has_living_room = models.BooleanField(default=False, verbose_name="Living Room")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_type', 'price_per_night']

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"

    def get_amenities(self):
        amenities = []
        if self.has_ac: amenities.append(('fa-wind', 'Air Conditioning'))
        if self.has_wifi: amenities.append(('fa-wifi', 'Free WiFi'))
        if self.has_tv: amenities.append(('fa-tv', 'Flat Screen TV'))
        if self.has_fridge: amenities.append(('fa-snowflake', 'Refrigerator'))
        if self.has_desk: amenities.append(('fa-desktop', 'Work Desk'))
        if self.has_private_bathroom: amenities.append(('fa-bath', 'Private Bathroom'))
        if self.has_room_service: amenities.append(('fa-concierge-bell', 'Room Service'))
        if self.has_balcony: amenities.append(('fa-door-open', 'Balcony'))
        if self.has_kitchenette: amenities.append(('fa-utensils', 'Kitchenette'))
        if self.has_living_room: amenities.append(('fa-couch', 'Living Room'))
        return amenities


class RoomReview(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.room.name}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=[
        ('rooms', 'Rooms'), ('restaurant', 'Restaurant'),
        ('pool', 'Swimming Pool'), ('lobby', 'Lobby'), ('exterior', 'Exterior'),
    ], default='rooms')
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
