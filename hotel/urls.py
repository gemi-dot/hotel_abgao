from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),  # 👈 Add this
    path('bookings/<int:pk>/toggle-checkin/', views.toggle_checkin, name='toggle_checkin'),



]
