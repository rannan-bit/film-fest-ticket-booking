from django.urls import path
from .views import InitiatePaymentView, VerifyPaymentView, PaymentFailedView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='payment-initiate'),
    path('verify/', VerifyPaymentView.as_view(), name='payment-verify'),
    path('failed/', PaymentFailedView.as_view(), name='payment-failed'),
]