from django.urls import path
from .views import BotVerifyPayment
urlpatterns = [
    path('telegram/verify/', BotVerifyPayment.as_view(), name="bot_verify_payment")
]
