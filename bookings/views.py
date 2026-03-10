from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        showtime = serializer.validated_data['showtime']
        num_tickets = serializer.validated_data['num_tickets']

        # Lock row to prevent overbooking
        showtime.__class__.objects.select_for_update().get(pk=showtime.pk)

        if showtime.available_seats < num_tickets:
            return Response(
                {'error': f'Only {showtime.available_seats} seats left.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        showtime.available_seats -= num_tickets
        showtime.save()

        booking = serializer.save(user=request.user)

        return Response({
            'booking_id': str(booking.id),
            'booking_ref': booking.booking_ref,
            'total_amount': float(booking.total_amount),
            'status': booking.status,
            'message': 'Booking created. Please complete payment.'
        }, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('showtime__film', 'showtime__venue')


class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            booking = Booking.objects.select_for_update().get(
                id=pk, user=request.user
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=404)

        if booking.status == 'cancelled':
            return Response({'error': 'Already cancelled.'}, status=400)

        if booking.status == 'confirmed':
            showtime = booking.showtime
            showtime.available_seats += booking.num_tickets
            showtime.save()

        booking.status = 'cancelled'
        booking.save()

        return Response({'message': 'Booking cancelled successfully.'})


class AdminBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Booking.objects.all().select_related(
            'user', 'showtime__film', 'showtime__venue'
        )
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset