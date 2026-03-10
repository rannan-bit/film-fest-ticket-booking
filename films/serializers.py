from rest_framework import serializers
from .models import Film, Venue, Showtime


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'capacity', 'description']


class ShowtimeSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    is_sold_out = serializers.SerializerMethodField()

    class Meta:
        model = Showtime
        fields = ['id', 'venue', 'start_time', 'price',
                  'total_seats', 'available_seats', 'is_sold_out', 'is_active']

    def get_is_sold_out(self, obj):
        return obj.available_seats == 0


class FilmSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    showtimes = ShowtimeSerializer(many=True, read_only=True)
    showtimes_count = serializers.IntegerField(source='showtimes.count', read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'genre',
                  'language', 'duration_mins', 'poster_url', 'trailer_url',
                  'is_featured', 'showtimes', 'showtimes_count', 'created_at']

    def get_poster_url(self, obj):
        request = self.context.get('request')
        if obj.poster and request:
            return request.build_absolute_uri(obj.poster.url)
        return None