from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('room_type', models.CharField(
                    choices=[('standard','Standard Room'),('deluxe','Deluxe Room'),('executive','Executive Room'),('family','Family Room'),('apartment','Apartment')],
                    default='standard', max_length=20)),
                ('description', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capacity', models.PositiveIntegerField(default=2)),
                ('size_sqm', models.PositiveIntegerField(default=25, help_text='Room size in square meters')),
                ('image', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('available', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('floor', models.PositiveIntegerField(default=1)),
                ('bed_type', models.CharField(default='Queen Bed', max_length=100)),
                ('has_ac', models.BooleanField(default=True, verbose_name='Air Conditioning')),
                ('has_wifi', models.BooleanField(default=True, verbose_name='Free WiFi')),
                ('has_tv', models.BooleanField(default=True, verbose_name='Flat Screen TV')),
                ('has_fridge', models.BooleanField(default=True, verbose_name='Refrigerator')),
                ('has_desk', models.BooleanField(default=True, verbose_name='Work Desk')),
                ('has_private_bathroom', models.BooleanField(default=True, verbose_name='Private Bathroom')),
                ('has_room_service', models.BooleanField(default=True, verbose_name='Room Service')),
                ('has_balcony', models.BooleanField(default=False, verbose_name='Balcony')),
                ('has_kitchenette', models.BooleanField(default=False, verbose_name='Kitchenette')),
                ('has_living_room', models.BooleanField(default=False, verbose_name='Living Room')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['room_type', 'price_per_night']},
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='gallery/')),
                ('category', models.CharField(
                    choices=[('rooms','Rooms'),('restaurant','Restaurant'),('pool','Swimming Pool'),('lobby','Lobby'),('exterior','Exterior')],
                    default='rooms', max_length=50)),
                ('featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['order', '-created_at']},
        ),
        migrations.CreateModel(
            name='RoomReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
