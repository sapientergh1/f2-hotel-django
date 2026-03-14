from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests
import json
from bookings.models import Booking
from .models import Payment


@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    # Convert GHS to pesewas (Paystack uses smallest currency unit)
    amount_pesewas = int(booking.total_price * 100)

    context = {
        'booking': booking,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_pesewas': amount_pesewas,
        'amount_ghs': booking.total_price,
    }
    return render(request, 'payments/initiate.html', context)


@login_required
def verify_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    reference = request.GET.get('reference', '')

    if not reference:
        messages.error(request, 'Payment reference not found.')
        return redirect('payments:initiate', booking_id=booking_id)

    # Verify with Paystack API
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        if data['data']['status'] == 'success':
            # Update or create payment record
            payment, created = Payment.objects.get_or_create(
                booking=booking,
                defaults={
                    'amount': booking.total_price,
                    'payment_method': 'paystack',
                }
            )
            payment.transaction_id = data['data']['id']
            payment.paystack_reference = reference
            payment.status = 'success'
            payment.paid_at = timezone.now()
            payment.save()

            # Update booking status
            booking.status = 'confirmed'
            booking.save()

            messages.success(request, f'Payment successful! Your booking {booking.booking_reference} is confirmed.')
            return redirect('payments:success', booking_id=booking_id)
        else:
            messages.error(request, 'Payment verification failed. Please try again.')
    else:
        messages.error(request, 'Could not verify payment. Please contact support.')

    return redirect('payments:initiate', booking_id=booking_id)


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'payments/success.html', {'booking': booking})


@login_required
def payment_cancel(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'payments/cancel.html', {'booking': booking})


@csrf_exempt
def paystack_webhook(request):
    """Handle Paystack webhook notifications"""
    if request.method == 'POST':
        import hmac, hashlib
        paystack_signature = request.headers.get('x-paystack-signature', '')
        body = request.body

        # Verify signature
        computed = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
            body, hashlib.sha512
        ).hexdigest()

        if computed == paystack_signature:
            data = json.loads(body)
            if data.get('event') == 'charge.success':
                reference = data['data']['reference']
                try:
                    payment = Payment.objects.get(paystack_reference=reference)
                    payment.status = 'success'
                    payment.save()
                    payment.booking.status = 'confirmed'
                    payment.booking.save()
                except Payment.DoesNotExist:
                    pass

    return JsonResponse({'status': 'ok'})
