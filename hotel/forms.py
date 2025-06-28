from django import forms
from .models import Room, Booking

from .models import Payment

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'price', 'is_available']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['contact', 'customer_name', 'room', 'check_in', 'check_out', 'is_checked_in']




       
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'is_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # All fields optional for now

