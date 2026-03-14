from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('booking/<int:booking_id>/pay/', views.initiate_payment, name='initiate'),
    path('booking/<int:booking_id>/verify/', views.verify_payment, name='verify'),
    path('booking/<int:booking_id>/success/', views.payment_success, name='success'),
    path('booking/<int:booking_id>/cancel/', views.payment_cancel, name='cancel'),
    path('webhook/', views.paystack_webhook, name='webhook'),
]
