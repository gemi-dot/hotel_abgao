from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import RoomForm, BookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from datetime import datetime, timedelta
from django.utils import timezone

from django.core.paginator import Paginator


from django.db.models import F


from django.db.models import Sum, Avg
from datetime import datetime





# DASHBOARD
from django.shortcuts import render
from .models import Room, Booking

@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    checked_in = Booking.objects.filter(is_checked_in=True).count()

    # 👇 Refactored stats data
    stats = [
        {"title": "Total Rooms", "count": total_rooms, "bg": "primary"},
        {"title": "Available Rooms", "count": available_rooms, "bg": "success"},
        {"title": "Total Bookings", "count": total_bookings, "bg": "warning"},
        {"title": "Checked In", "count": checked_in, "bg": "info"},
    ]

    # Other logic...
    rooms = Room.objects.all()
    recent_bookings = Booking.objects.select_related("room").order_by("-check_in")[:10]

    return render(request, 'hotel/dashboard.html', {
        "stats": stats,
        "rooms": rooms,
        "recent_bookings": recent_bookings,
        # Include for backward compatibility (optional)
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "total_bookings": total_bookings,
        "checked_in": checked_in,
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

    return render(request, 'hotel/booking_list.html', {
        'bookings': bookings,
########        
        'start_date': start_date,
        'end_date': end_date,
        'status': status,        
        
        })

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



def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return redirect('dashboard')

######
@login_required
def booking_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    room_id = request.GET.get('room')

    bookings = Booking.objects.select_related('room').all()

    #if start_date:
    #    bookings = bookings.filter(check_in__date__gte=start_date)
    #if end_date:
    #    bookings = bookings.filter(check_out__date__lte=end_date)


    if start_date:
        bookings = bookings.filter(check_in__gte=start_date)
    if end_date:
        bookings = bookings.filter(check_out__lte=end_date)   



    if status == 'checked_in':
        bookings = bookings.filter(is_checked_in=True)
    elif status == 'not_checked_in':
        bookings = bookings.filter(is_checked_in=False)
    if room_id:
        bookings = bookings.filter(room__id=room_id)

    rooms = Room.objects.all()

    return render(request, 'hotel/booking_summary.html', {
        'bookings': bookings,
        'rooms': rooms,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'room_id': room_id,
    })

#####



@login_required
def occupancy_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        today = datetime.today().date()
        start_date = today.replace(day=1)
        end_date = today
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    total_days = (end_date - start_date).days + 1
    total_rooms = Room.objects.count()
    available_room_nights = total_rooms * total_days

    # Bookings that intersect the date range
    bookings = Booking.objects.filter(
        check_in__lte=end_date,
        check_out__gte=start_date
    )

    # Calculate occupied nights per booking
    occupied_nights = 0
    for booking in bookings:
        overlap_start = max(booking.check_in, start_date)
        overlap_end = min(booking.check_out, end_date)
        nights = (overlap_end - overlap_start).days
        occupied_nights += max(nights, 0)

    occupancy_rate = (occupied_nights / available_room_nights) * 100 if available_room_nights > 0 else 0

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_rooms': total_rooms,
        'available_nights': available_room_nights,
        'occupied_nights': occupied_nights,
        'occupancy_rate': round(occupancy_rate, 2),
    }

    
    return render(request, 'hotel/occupancy_report.html', context)




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking
from datetime import datetime

@login_required
def revenue_report(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    bookings = Booking.objects.select_related('room').all()

    # Parse input dates only if provided
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            bookings = bookings.filter(check_in__gte=start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            bookings = bookings.filter(check_out__lte=end_date)
    except ValueError:
        # Handle invalid date format gracefully
        start_date = end_date = None

    total_bookings = bookings.count()
    total_revenue = sum(b.total_price for b in bookings)
    avg_revenue = total_revenue / total_bookings if total_bookings > 0 else 0

    context = {
        'start_date': start_date_str,
        'end_date': end_date_str,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'avg_revenue': avg_revenue,
    }

    return render(request, 'hotel/revenue_report.html', context)
