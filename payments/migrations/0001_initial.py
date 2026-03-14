from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(
                    choices=[('paystack','Paystack'),('stripe','Stripe'),('cash','Cash'),('bank_transfer','Bank Transfer')],
                    default='paystack', max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=200)),
                ('paystack_reference', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(
                    choices=[('pending','Pending'),('success','Success'),('failed','Failed'),('refunded','Refunded')],
                    default='pending', max_length=20)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='bookings.booking')),
            ],
        ),
    ]
