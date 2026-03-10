import uuid
from django.db import models


class Film(models.Model):
    GENRE_CHOICES = [
        ('drama', 'Drama'),
        ('documentary', 'Documentary'),
        ('comedy', 'Comedy'),
        ('thriller', 'Thriller'),
        ('horror', 'Horror'),
        ('animation', 'Animation'),
        ('short', 'Short Film'),
        ('experimental', 'Experimental'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    director = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    language = models.CharField(max_length=100)
    duration_mins = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Showtime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='showtimes')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f'{self.film.title} — {self.start_time}'