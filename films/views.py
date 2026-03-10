from rest_framework import generics, permissions, filters
from .models import Film, Venue, Showtime
from .serializers import FilmSerializer, VenueSerializer, ShowtimeSerializer


class FilmListView(generics.ListAPIView):
    serializer_class = FilmSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'director', 'genre', 'language']

    def get_queryset(self):
        queryset = Film.objects.all()
        genre = self.request.query_params.get('genre')
        language = self.request.query_params.get('language')
        featured = self.request.query_params.get('featured')
        if genre:
            queryset = queryset.filter(genre=genre)
        if language:
            queryset = queryset.filter(language__icontains=language)
        if featured:
            queryset = queryset.filter(is_featured=True)
        return queryset


class FilmDetailView(generics.RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.AllowAny]


class ShowtimeListView(generics.ListAPIView):
    serializer_class = ShowtimeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Showtime.objects.filter(is_active=True)
        film_id = self.request.query_params.get('film_id')
        if film_id:
            queryset = queryset.filter(film_id=film_id)
        return queryset


class VenueListView(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]