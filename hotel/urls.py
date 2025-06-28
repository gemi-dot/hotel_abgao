from django.urls import path
from . import views

from .views import revenue_report

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('rooms/vacant/', views.vacant_rooms, name='vacant_rooms'),

    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/toggle-check-in/', views.toggle_check_in, name='toggle_check_in'),
    path('bookings/<int:booking_id>/pay/', views.mark_as_paid, name='mark_as_paid'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('bookings/history/', views.booking_history, name='booking_history'),
    path('bookings/<int:pk>/toggle-check-in/', views.toggle_check_in, name='toggle_check_in'),
    path('bookings/<int:booking_id>/mark-paid/', views.mark_as_paid, name='mark_as_paid'),

    path('bookings/<int:booking_id>/payment/', views.create_or_update_payment, name='create_payment'),

 
    path('available-rooms/', views.available_rooms, name='available_rooms'),
    path('reports/booking-summary/', views.booking_summary, name='booking_summary'),
    path('reports/occupancy/', views.occupancy_report, name='occupancy_report'),
    path('reports/revenue/', revenue_report, name='revenue_report'),
    #path('trial-expired/', views.trial_expired, name='trial_expired'),



]

