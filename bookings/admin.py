from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_ref', 'user', 'film_title', 'num_tickets', 'total_amount', 'status', 'booked_at']
    list_filter = ['status']
    search_fields = ['booking_ref', 'user__email', 'showtime__film__title']
    readonly_fields = ['booking_ref', 'booked_at', 'updated_at']

    def film_title(self, obj):
        return obj.showtime.film.title
    film_title.short_description = 'Film'