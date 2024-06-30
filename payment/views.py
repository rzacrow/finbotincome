from django.shortcuts import render, HttpResponse
from django.views.generic import View
from telegram.models import TelegramProfile, VipAccountAmount, BotConfig
from .models import Invoice
import requests, json
import datetime
from datetime import timedelta

# Create your views here.
class BotVerifyPayment(View):
    def get(self, request):
        try:
            status = request.GET.get('Status')

            authority = request.GET.get('Authority')
            bc = BotConfig.objects.last()

            try:
                bot_username = bc.username
                bot_token = bc.token
            except:
                bot_username, bot_token = ""

            bot_url = f"https://t.me/{bot_username}"

            if status == "OK":
                try:
                    invoice = Invoice.objects.get(authority=authority)
                except:
                    return HttpResponse(content="سفارشی با این کد رهگیری پیدا نشد! در صورت پرداخت از طریق ربات، این موضوع را با پشتیبانی در میان بگذارید")


                if invoice.status != "Active":
                    return HttpResponse(content="کد نامعتبر")


                invoice.status = "Paid"
                telegram_id = invoice.telegram_profile.telegram_id
                
                try:
                    account_detail = VipAccountAmount.objects.last()
                    if account_detail.expired:
                        expired = invoice.created_at + timedelta(int(account_detail.expired))
                        invoice.expired_at = expired
                except:
                    pass

                invoice.save()
                msg_id = invoice.msg_id

                tele_account = TelegramProfile.objects.get(telegram_id=telegram_id)
                tele_account.access_level = "Allowed"
                tele_account.save()
                success_message = "پرداخت شما موفقیت آمیز بود، برای شروع استفاده از سرویس ها از گزینه های زیر دستور منو را انتخاب کنید"

                data = {
                    "chat_id" : telegram_id,
                    "text" : success_message
                }

                delete_data = {
                    "chat_id" : telegram_id,
                    "message_id" : msg_id,
                }

                data = json.dumps(data)
                delete_data = json.dumps(delete_data)

                headers = {
                    "Content-Type": "application/json"
                }

                update_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                delete_url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"


                requests.post(url=url, data=data, headers=headers)
                requests.post(url=update_url)
                requests.post(url=delete_url, data=delete_data, headers=headers)
            
            context = {
                'status' : status,
                'url' : bot_url
            }

            return render(request, "payment/verify.html", context=context)
        except:
            return HttpResponse(content="خطایی رخ داد!")
