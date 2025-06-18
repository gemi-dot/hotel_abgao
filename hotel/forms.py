from django import forms
from .models import Room, Booking

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'price', 'is_available']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['contact', 'customer_name', 'room', 'check_in', 'check_out', 'is_checked_in']
