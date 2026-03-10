from django.contrib import admin
from .models import Film, Venue, Showtime


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'genre', 'language', 'duration_mins', 'is_featured']
    list_filter = ['genre', 'language', 'is_featured']
    search_fields = ['title', 'director']
    list_editable = ['is_featured']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['film', 'venue', 'start_time', 'price', 'available_seats', 'is_active']
    list_filter = ['is_active', 'venue']
    list_editable = ['is_active']