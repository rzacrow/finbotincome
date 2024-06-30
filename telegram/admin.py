from django.contrib import admin
from .models import TelegramChannels, TelegramTicket, TelegramTicketAnswer, TelegramProfile, VipAccountAmount, SupportAccount, BotConfig
from django.contrib import messages


@admin.register(TelegramProfile)
class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'full_name', 'access_level']


@admin.register(TelegramChannels)
class TelegramChannelsAdmin(admin.ModelAdmin):
    list_display = ['title', 'link']


@admin.register(SupportAccount)
class SupportAccountAdmin(admin.ModelAdmin):
    list_display = ['platform', 'value']


@admin.register(VipAccountAmount)
class VipAccountAmountAdmin(admin.ModelAdmin):
    list_display = ['amount', 'expired']

    def save_model(self, request, obj, form, change):
        instances = VipAccountAmount.objects.all().count()
        if instances >= 1:
            messages.add_message(request, messages.ERROR, "تنها مجاز به تعریف یک مقدار هستید. برای تغییر مقدار،فیلد موجود را حذف کنید.")
            return
        
        super().save_model(request, obj, form, change)

class TelegramTicketAnswerInline(admin.TabularInline):
    model = TelegramTicketAnswer
    extra = 1

@admin.register(TelegramTicket)
class TelegramTicketAdmin(admin.ModelAdmin):
    list_display = ['telegram_account', 'title', 'status']
    ordered = ['-created']
    fields = ['telegram_account', 'text', 'status']

    inlines = [
        TelegramTicketAnswerInline,
    ]

@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'username']
