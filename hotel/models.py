from django.db import models
from django.utils import timezone

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # Allow blank for optional phone
    address = models.TextField(blank=True, null=True)  # Allow blank for optional address
    date_of_birth = models.DateField(blank=True, null=True)  # Optional date of birth
    notes = models.TextField(blank=True, null=True)  # Optional notes about the guest

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )
    number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"

class Booking(models.Model):
    PAYMENT_STATUSES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Allow blank for auto-computation
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUSES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False)  # Added field for check-in status

    def __str__(self):
        return f"{self.guest.name} - Room {self.room.number}"

    def compute_total_price(self):
        """Calculate total price based on room rate and number of days."""
        num_days = (self.check_out - self.check_in).days
        return self.room.price * num_days

    def save(self, *args, **kwargs):
        """Override save method to compute total price before saving."""
        if not self.total_price:  # Compute only if total_price is not manually set
            self.total_price = self.compute_total_price()
        super().save(*args, **kwargs)

    def total_paid(self):
        """Calculate the total amount paid for this booking."""
        return sum(payment.amount for payment in self.payments.all())

    def is_fully_paid(self):
        """Check if the booking is fully paid."""
        return self.total_paid() >= self.total_price

    def update_payment_status(self, manual_override=False):
        """Update the payment status based on the total paid or allow manual override."""
        if manual_override:
            print(f"Manual Override: Payment Status set to {self.payment_status}")
        else:
            total_paid = self.total_paid()
            if total_paid >= self.total_price:
                self.payment_status = 'paid'
            elif total_paid > 0:
                self.payment_status = 'partial'
            else:
                self.payment_status = 'pending'
        self.save()

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount}"

    def save(self, *args, **kwargs):
        """Validate payment amount before saving."""
        if self.amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if self.booking.total_paid() + self.amount > self.booking.total_price:
            raise ValueError("Payment exceeds the total price for the booking.")
        super().save(*args, **kwargs)