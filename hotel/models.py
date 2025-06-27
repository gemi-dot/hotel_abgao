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


class Booking(models.Model):
    customer_name = models.CharField(max_length=100)

    #contact = models.CharField(max_length=50)  # Add this if not present
    contact = models.CharField(max_length=100, default='N/A', blank=True)



    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    is_checked_in = models.BooleanField(default=False)

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
