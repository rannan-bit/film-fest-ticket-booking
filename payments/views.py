import razorpay
import hmac
import hashlib
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from bookings.models import Booking

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')

        try:
            booking = Booking.objects.get(
                id=booking_id,
                user=request.user,
                status='pending'
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or already paid.'}, status=404)

        amount_paise = int(booking.total_amount * 100)

        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': booking.booking_ref,
            'notes': {
                'booking_id': str(booking.id),
                'film': booking.showtime.film.title,
            }
        })

        return Response({
            'order_id': order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'booking_ref': booking.booking_ref,
            'attendee_name': request.user.get_full_name(),
            'email': request.user.email,
        })


class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        booking_id = request.data.get('booking_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        if not all([booking_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response({'error': 'Missing payment fields.'}, status=400)

        msg = f'{razorpay_order_id}|{razorpay_payment_id}'
        expected_sig = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            msg.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, razorpay_signature):
            return Response({'error': 'Payment verification failed.'}, status=400)

        try:
            booking = Booking.objects.select_for_update().get(
                id=booking_id, user=request.user
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=404)

        booking.status = 'confirmed'
        booking.payment_ref = razorpay_payment_id
        booking.save()

        return Response({
            'message': 'Payment confirmed!',
            'booking_ref': booking.booking_ref,
            'status': 'confirmed'
        })


class PaymentFailedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        booking_id = request.data.get('booking_id')

        try:
            booking = Booking.objects.select_for_update().get(
                id=booking_id, user=request.user, status='pending'
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=404)

        showtime = booking.showtime
        showtime.available_seats += booking.num_tickets
        showtime.save()

        booking.status = 'failed'
        booking.save()

        return Response({'message': 'Payment failed. Seats released.'})