from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from rooms.models import Room, GalleryImage


def home(request):
    featured_rooms = Room.objects.filter(available=True, featured=True)[:3]
    if featured_rooms.count() < 3:
        featured_rooms = Room.objects.filter(available=True)[:3]
    gallery_images = GalleryImage.objects.filter(featured=True)[:8]
    return render(request, 'website/home.html', {
        'featured_rooms': featured_rooms,
        'gallery_images': gallery_images,
    })


def about(request):
    return render(request, 'website/about.html')


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '')
        email   = request.POST.get('email', '')
        subject = request.POST.get('subject', 'Contact from F2 Hotel Website')
        message = request.POST.get('message', '')
        try:
            send_mail(
                f'F2 Hotel Contact: {subject}',
                f'From: {name} ({email})\n\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                ['info@f2hotel.com'],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(request, 'Thank you! Your message has been sent. We will get back to you shortly.')
    return render(request, 'website/contact.html')


def handler404(request, exception=None):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
