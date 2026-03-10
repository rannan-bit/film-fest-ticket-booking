import uuid
from django.db import models
from django.conf import settings


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    showtime = models.ForeignKey(
        'films.Showtime',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    num_tickets = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_ref = models.CharField(max_length=255, blank=True)
    booking_ref = models.CharField(max_length=10, unique=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f'Booking {self.booking_ref} — {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = str(self.id)[:8].upper()
        super().save(*args, **kwargs)