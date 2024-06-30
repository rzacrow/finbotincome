from django.db import models
from telegram.models import TelegramProfile
from accounts.models import User
# Create your models here.

class Invoice(models.Model):
    INVOICE_STATUS = (
        ('Active', 'فعال'),
        ('Paid', 'پرداخت شده'),
        ('Expired', 'منقضی شده'),
        ('Failed', 'پرداخت ناموفق'),
    )

    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    authority = models.CharField(max_length=36, blank=True)
    msg_id = models.CharField(max_length=25, blank=True, null=True)
    telegram_profile = models.ForeignKey(TelegramProfile, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Telegram Account")

    def __str__(self) -> str:
        return f"{self.telegram_profile} - {self.amount}"
    
    class Meta:
        verbose_name = 'فاکتور های فروش'
        verbose_name_plural = 'فاکتور های فروش'
