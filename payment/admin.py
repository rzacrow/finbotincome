from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['telegram_profile','amount', 'status']
    exclude = ['user', 'msg_id']
    readonly_fields = ['created_at']
# Register your models here.
