from rest_framework import serializers
from .models import Booking
from films.serializers import ShowtimeSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    showtime_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Booking
        fields = ['showtime_id', 'num_tickets']

    def validate(self, data):
        from films.models import Showtime
        try:
            showtime = Showtime.objects.get(id=data['showtime_id'], is_active=True)
        except Showtime.DoesNotExist:
            raise serializers.ValidationError('Showtime not found or inactive.')

        if data['num_tickets'] < 1:
            raise serializers.ValidationError('At least 1 ticket is required.')
        if data['num_tickets'] > 10:
            raise serializers.ValidationError('Maximum 10 tickets per booking.')
        if showtime.available_seats < data['num_tickets']:
            raise serializers.ValidationError(
                f'Only {showtime.available_seats} seats available.'
            )

        data['showtime'] = showtime
        data['total_amount'] = showtime.price * data['num_tickets']
        return data

    def create(self, validated_data):
        validated_data.pop('showtime_id', None)
        return Booking.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer(read_only=True)
    attendee_name = serializers.SerializerMethodField()
    film_title = serializers.CharField(source='showtime.film.title', read_only=True)
    poster_url = serializers.SerializerMethodField()
    venue_name = serializers.CharField(source='showtime.venue.name', read_only=True)
    show_date = serializers.DateTimeField(source='showtime.start_time', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_ref', 'attendee_name', 'film_title',
            'poster_url', 'venue_name', 'show_date', 'showtime',
            'num_tickets', 'total_amount', 'status',
            'payment_ref', 'booked_at'
        ]

    def get_attendee_name(self, obj):
        return obj.user.get_full_name()

    def get_poster_url(self, obj):
        request = self.context.get('request')
        if obj.showtime.film.poster and request:
            return request.build_absolute_uri(obj.showtime.film.poster.url)
        return None