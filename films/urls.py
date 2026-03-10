from django.urls import path
from .views import FilmListView, FilmDetailView, ShowtimeListView, VenueListView

urlpatterns = [
    path('', FilmListView.as_view(), name='film-list'),
    path('<uuid:pk>/', FilmDetailView.as_view(), name='film-detail'),
    path('showtimes/', ShowtimeListView.as_view(), name='showtime-list'),
    path('venues/', VenueListView.as_view(), name='venue-list'),
]