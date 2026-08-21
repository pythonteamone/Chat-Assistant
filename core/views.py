from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from core.services.bot_api_client import TelegramAPIClient
# from core.services.dispatcher import process_update



@csrf_exempt  # چون تلگرام نمی‌تواند CSRF Token بفرستد
def webhook_endpoint(request):
    if request.method == 'POST':
        try:
            # تبدیل بادی درخواست به فرمت JSON
            update = json.loads(request.body)

            # لاگ گرفتن برای دیباگ (می‌توانی در ترمینال ببینی چه چیزی می‌آید)
            print("📩 New Update Received:")
            print(json.dumps(update, indent=2))

            # --- نقطه اتصال به کدهای ایدا ---
            # اگر ایدا فایل dispatcher.py را ساخته باشد، اینجا صدا زده می‌شود:
            # process_update(update)

            return JsonResponse({"status": "ok"})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            print(f"❌ Error processing update: {e}")
            return HttpResponseBadRequest(f"Error: {e}")
    else:
        return HttpResponseBadRequest("Only POST method is allowed")


def test_connection(request):
    """
    تست ساده برای اطمینان از صحت اجرای پروژه
    """
    bot_info = TelegramAPIClient.get_me()
    if bot_info and bot_info.get('ok'):
        return JsonResponse({
            "status": "success",
            "message": "Connection to Telegram API is successful!",
            "bot_name": bot_info['result']['first_name']
        })
    else:
        return JsonResponse({"status": "error", "message": "Failed to connect to Telegram"}, status=500)
