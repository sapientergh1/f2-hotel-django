"""
Management command to populate F2 Hotel with sample room data.
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from rooms.models import Room


class Command(BaseCommand):
    help = 'Seed the database with sample F2 Hotel rooms'

    def handle(self, *args, **kwargs):
        rooms_data = [
            {
                'name': 'Classic Standard Room',
                'room_type': 'standard',
                'description': 'A comfortable and well-appointed room ideal for solo travellers and couples. Features a cosy queen-size bed, modern furnishings, and all essential amenities to ensure a pleasant stay. Enjoy the convenience of in-room air conditioning, a flat-screen TV, and complimentary WiFi throughout your visit.',
                'price_per_night': 250.00,
                'capacity': 2,
                'size_sqm': 22,
                'floor': 1,
                'bed_type': 'Queen Bed',
                'featured': True,
                'has_balcony': False,
                'has_kitchenette': False,
            },
            {
                'name': 'Superior Standard Room',
                'room_type': 'standard',
                'description': 'An upgraded standard room with extra space and garden views. Features a larger workspace and enhanced bathroom amenities, making it great for short business trips or a comfortable couple\'s getaway.',
                'price_per_night': 300.00,
                'capacity': 2,
                'size_sqm': 26,
                'floor': 2,
                'bed_type': 'King Bed',
                'featured': False,
            },
            {
                'name': 'Deluxe Double Room',
                'room_type': 'deluxe',
                'description': 'Experience elevated comfort in our Deluxe Double Room. Designed with a refined aesthetic, this spacious room features premium bedding, a well-lit work desk, and an upgraded private bathroom. Ideal for guests seeking a step above standard accommodation without compromising on value.',
                'price_per_night': 380.00,
                'capacity': 2,
                'size_sqm': 30,
                'floor': 2,
                'bed_type': 'King Bed',
                'featured': True,
                'has_balcony': True,
            },
            {
                'name': 'Deluxe Twin Room',
                'room_type': 'deluxe',
                'description': 'Our Deluxe Twin Room is the perfect choice for two friends or colleagues travelling together. Featuring two comfortable single beds, modern décor, and all premium amenities. Enjoy the balcony with a relaxing view of the surroundings.',
                'price_per_night': 380.00,
                'capacity': 2,
                'size_sqm': 30,
                'floor': 3,
                'bed_type': '2 × Single Beds',
                'has_balcony': True,
            },
            {
                'name': 'Executive Business Room',
                'room_type': 'executive',
                'description': 'Tailored for the discerning business traveller, the Executive Business Room features a spacious ergonomic workspace, high-speed WiFi, premium furnishings, and a luxuriously appointed bathroom. Enjoy a comfortable chair, reading lamp, and a dedicated work area to stay productive in style.',
                'price_per_night': 500.00,
                'capacity': 2,
                'size_sqm': 38,
                'floor': 3,
                'bed_type': 'King Bed',
                'featured': True,
                'has_balcony': True,
            },
            {
                'name': 'Executive Premium Suite',
                'room_type': 'executive',
                'description': 'The pinnacle of our room offerings for solo and couple travellers. This premium suite features a separate lounge area, walk-in wardrobe, spa-quality bathroom with rain shower, and panoramic views. The perfect blend of luxury and functionality.',
                'price_per_night': 650.00,
                'capacity': 2,
                'size_sqm': 50,
                'floor': 4,
                'bed_type': 'Super King Bed',
                'has_balcony': True,
                'has_living_room': True,
            },
            {
                'name': 'Family Comfort Room',
                'room_type': 'family',
                'description': 'Designed with families in mind, the Family Comfort Room provides generous space and multiple sleeping arrangements. Features one king bed and two single beds, a large bathroom, and plenty of storage space. Children under 12 stay free — ask at reception for details.',
                'price_per_night': 550.00,
                'capacity': 5,
                'size_sqm': 45,
                'floor': 2,
                'bed_type': '1 King + 2 Singles',
                'featured': True,
            },
            {
                'name': 'Family Suite',
                'room_type': 'family',
                'description': 'Our spacious Family Suite offers the ultimate comfort for larger families. With a separate sleeping area for parents, bunk beds for children, a lounge, and a kitchenette for simple meal preparation. The ideal choice for an extended family retreat in Kumasi.',
                'price_per_night': 700.00,
                'capacity': 6,
                'size_sqm': 60,
                'floor': 3,
                'bed_type': 'Mixed',
                'has_kitchenette': True,
                'has_living_room': True,
            },
            {
                'name': 'Studio Apartment',
                'room_type': 'apartment',
                'description': 'Our self-contained Studio Apartment is ideal for guests planning an extended stay. Features an open-plan living and sleeping area, a well-equipped kitchenette with microwave and refrigerator, a dining space for two, and a modern bathroom. Enjoy the independence of apartment living with all hotel services on call.',
                'price_per_night': 600.00,
                'capacity': 2,
                'size_sqm': 45,
                'floor': 1,
                'bed_type': 'Queen Bed',
                'featured': True,
                'has_kitchenette': True,
                'has_living_room': True,
            },
            {
                'name': 'One-Bedroom Apartment',
                'room_type': 'apartment',
                'description': 'A fully self-contained one-bedroom apartment offering the best of both worlds — the privacy of a home with all the luxuries of a hotel. Features a separate bedroom, full living room, modern kitchen, and a spacious bathroom. Perfect for long-stay guests and corporate travellers.',
                'price_per_night': 800.00,
                'capacity': 3,
                'size_sqm': 70,
                'floor': 4,
                'bed_type': 'King Bed',
                'featured': False,
                'has_kitchenette': True,
                'has_living_room': True,
                'has_balcony': True,
            },
        ]

        created = 0
        for data in rooms_data:
            room, was_created = Room.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {room.name}'))
            else:
                self.stdout.write(f'  – Already exists: {room.name}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! {created} new rooms created.'))
