from django.urls import path
from .views import (
    BookingCreateView, BookingDetailView,
    MyBookingsView, BookingCancelView, AdminBookingsView
)

urlpatterns = [
    path('', BookingCreateView.as_view(), name='booking-create'),
    path('my/', MyBookingsView.as_view(), name='my-bookings'),
    path('admin/', AdminBookingsView.as_view(), name='admin-bookings'),
    path('<uuid:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<uuid:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]