from django.db import models
######
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
######



# Create your models here.
class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.number} - {self.type}'
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.room.is_available = not self.is_checked_in
        self.room.save()




class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, default='N/A', blank=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)  # Ensure Room model exists
    check_in = models.DateField()
    check_out = models.DateField()
    is_checked_in = models.BooleanField(default=False)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.room} ({self.payment_status})"
    

    def save(self, *args, **kwargs):
        if self.room and self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            if nights < 1:
                nights = 1
            self.amount = self.room.price * nights
        super().save(*args, **kwargs)


    @property
    def total_price(self):
        duration = (self.check_out - self.check_in).days
        return self.room.price * max(duration, 1)  # Avoid zero-day stays



    def __str__(self):
        return f'{self.customer_name} - Room {self.room.number}'


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.is_checked_in:
        self.room.is_available = False
    else:
        self.room.is_available = True
    self.room.save()



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=64, unique=True)
    trial_start = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def trial_expired(self):
        return timezone.now() > self.trial_start + timedelta(days=7)


#################
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id} - {'Paid' if self.is_paid else 'Pending'}"
