from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import RoomForm, BookingForm


from django.db.models import Q

from datetime import datetime



# DASHBOARD
@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    checked_in = Booking.objects.filter(is_checked_in=True).count()  # Correct field name

    return render(request, 'hotel/dashboard.html', {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'checked_in': checked_in,
    })


# ROOM VIEWS
@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms})

@login_required
def room_create(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'hotel/room_form.html', {'form': form})

@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'hotel/room_form.html', {'form': form})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('room_list')


# BOOKING VIEWS
@login_required

def booking_list(request):
    bookings = Booking.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    if start_date:
        bookings = bookings.filter(check_in__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out__lte=end_date)
    if status == 'checked_in':
        bookings = bookings.filter(is_checked_in=True)
    elif status == 'not_checked_in':
        bookings = bookings.filter(is_checked_in=False)

    return render(request, 'hotel/booking_list.html', {'bookings': bookings})



@login_required
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'hotel/booking_form.html', {'form': form})

@login_required
def toggle_checkin(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_checked_in = not booking.is_checked_in  # Toggling the correct field
    booking.save()
    return redirect('booking_list')


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return redirect('booking_list')


