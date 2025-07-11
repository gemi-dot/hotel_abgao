
from django.urls import path
from . import views
from .views import create_booking, booking_history, revenue_report

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('rooms/vacant/', views.vacant_rooms, name='vacant_rooms'),

    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    
    path('booking/create/', create_booking, name='create_booking'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('bookings/history/', views.booking_history, name='booking_history'),
    path('bookings/<int:pk>/toggle-check-in/', views.toggle_check_in, name='toggle_check_in'),
    path('bookings/<int:booking_id>/mark-paid/', views.mark_as_paid, name='mark_as_paid'),

    # filepath: /Users/macbookpro/hotel_abgao/hotel/urls.py
   
    path('bookings/<int:booking_id>/payment/', views.create_payment, name='create_payment'),

    path('guests/create/', views.guest_create, name='guest_create'),

    
    path('guests/', views.guest_list, name='guest_list'),

    path('guests/<int:pk>/edit/', views.guest_edit, name='guest_edit'),
    path('guests/<int:pk>/delete/', views.guest_delete, name='guest_delete'),



    # Reports
    path('booking/history/', booking_history, name='booking_history'),
    path('reports/booking-summary/', views.booking_summary, name='booking_summary'),
    path('reports/occupancy/', views.occupancy_report, name='occupancy_report'),
    path('reports/revenue/', revenue_report, name='revenue_report'),
]