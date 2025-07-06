from django import forms
from .models import Room, Booking

from .models import Payment

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        
        fields = ['number', 'room_type', 'capacity', 'price', 'is_available']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest', 'room', 'check_in', 'check_out', 'total_price', 'payment_status']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

               
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment method'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter transaction ID'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest', 'room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Validate check-in and check-out dates."""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned_data