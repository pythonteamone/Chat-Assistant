from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from core.services.bot_api_client import TelegramAPIClient
from core.services.dispatcher import process_update
from django.utils import timezone
from datetime import timedelta
from core.models import BusinessAccount


@csrf_exempt
def webhook_endpoint(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body)
            print(update)
            process_update(update)

            return JsonResponse({"status": "ok"})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            print(f" Error: {e}")
            return JsonResponse({"status": "error"}, status=500)

        return JsonResponse({"status": "method not allowed"}, status=405)

def test_connection(request):
    bot_info = TelegramAPIClient.get_me()
    if bot_info and bot_info.get('ok'):
        return JsonResponse({
            "status": "success",
            "message": "Connection to Telegram API is successful!",
            "bot_name": bot_info['result']['first_name']
        })
    return JsonResponse({"status": "ok", "message": "Server is running!"})