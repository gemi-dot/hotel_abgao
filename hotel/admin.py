
# Register your models here.
from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'price', 'is_available')
    list_editable = ('is_available',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'room', 'check_in', 'check_out', 'is_checked_in')
    list_filter = ('is_checked_in',)
