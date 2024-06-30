from django.db import models
import requests, json


class TelegramProfile(models.Model):
    ACCESS_LEVEL = (
        ("Allowed", "Allowed"),
        ('Unallowable', 'Unallowable'),
    )
    telegram_id = models.BigIntegerField()
    user_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    invitation_link = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(default=0)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL)

    def __str__(self) -> str:
        return f"{self.user_name}"
    
    class Meta:
        verbose_name = 'کابران'
        verbose_name_plural = 'کابران'

# Create your models here.

class TelegramTicket(models.Model):
    TELEGRAM_TICKET_STATUS = (
        ("Closed", "Closed"),
        ("Open", "Open"),
    )

    telegram_account = models.ForeignKey(TelegramProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=55, blank=True, null=True)
    text = models.CharField(max_length=1024)
    status = models.CharField(max_length=6, default="Open", choices=TELEGRAM_TICKET_STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت'


class TelegramTicketAnswer(models.Model):
    ticket = models.ForeignKey(TelegramTicket, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.ticket.title}"
    
    def save(self, *args, **kwargs) :
        url = f"https://api.telegram.org/bot7111711383:AAH5xL-FunByrIZvV_HyWr2y7d5e1UqKELo/sendMessage"

        headers = {
            "Content-Type" : "application/json"
        }

        text = f"پشتیبانی:\n\nتیکت شما:\n{self.ticket.text}\n\nپاسخ آن:\n{self.text}"
        data = {
            "chat_id" : self.ticket.telegram_account.telegram_id,
            "text" : text
        }

        data = json.dumps(data)
        result = requests.post(url=url, data=data, headers=headers)
        print(result)
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'پاسخ تیکت'
        verbose_name_plural = 'پاسخ تیکت'


class SupportAccount(models.Model):
    PLATFORM_CHOICES = (
        ('Telegram', 'تلگرام'),
        ('Gmail', 'ایمیل'),
        ('Phone', 'تلفن'),
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.platform}"

    class Meta:
        verbose_name = 'حساب های پشتیبانی'
        verbose_name_plural = 'حساب های پشتیبانی'


class TelegramChannels(models.Model):
    TITLE_CHOICES = (
        ('Forex', 'سیگنال فارکس'),
        ('Crypto', 'سیگنال کریپتو'),
        ('TraderBot', 'ربات های تریدر'),
        ('Broker', 'ثبت نام بروکر'),
        ('Bonus', 'بونوس'),
        ('PotentialCurrencies', 'ارزهای پر پتانسیل'),
        ("Airdrop", 'ایردراپ ها'),
        ("Eduction", 'آموزش')
    )

    title = models.CharField(max_length=25, choices=TITLE_CHOICES)
    link = models.CharField(max_length=555)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = 'لینک های ربات'
        verbose_name_plural = 'لینک های ربات'

class VipAccountAmount(models.Model):
    amount = models.FloatField()
    expired = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.amount}"
    
    def save(self, *args, **kwargs):
        instance = VipAccountAmount.objects.all().count()

        if instance >= 1:
            return

        super().save(*args, **kwargs)  

    class Meta:
        verbose_name = 'اشتراک ویژه'
        verbose_name_plural = 'اشتراک ویژه'




class BotConfig(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'تنظیمات بات'
        verbose_name_plural = 'تنظیمات بات'

    def save(self, *args, **kwargs):
        instance = BotConfig.objects.all().count()

        if instance >= 1:
            return

        super().save(*args, **kwargs)  


