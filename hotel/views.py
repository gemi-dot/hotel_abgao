from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import RoomForm, BookingForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db.models import Q

from datetime import datetime


from django.contrib.auth.decorators import login_required


# DASHBOARD
@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    checked_in = Booking.objects.filter(is_checked_in=True).count()  # Correct field name

     # Add this 👇
    recent_bookings = Booking.objects.select_related('room').order_by('-check_in')[:5]


    return render(request, 'hotel/dashboard.html', {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'checked_in': checked_in,
        'recent_bookings': recent_bookings,  # 👈 YOU FORGOT THIS
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


#
def available_rooms(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'hotel/available_rooms.html', {'rooms': rooms})
#


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


####
@login_required

def booking_create(request):
    room_id = request.GET.get('room_id')
    form = BookingForm(request.POST or None, initial={'room': room_id})

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        if not booking.room.is_available:
            messages.error(request, 'This room is not available.')
        else:
            booking.save()
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


def booking_history(request):
    name = request.GET.get('name')
    bookings = Booking.objects.filter(customer_name__icontains=name) if name else []
    return render(request, 'hotel/booking_history.html', {'bookings': bookings, 'name': name})



@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'hotel/booking_form.html', {'form': form})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'hotel/booking_detail.html', {'booking': booking})


@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'hotel/booking_form.html', {'form': form})
