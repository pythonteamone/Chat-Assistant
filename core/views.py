from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from core.services.bot_api_client import TelegramAPIClient
from core.services.dispatcher import process_update  # <--- این خط باید فعال باشد

@csrf_exempt
def webhook_endpoint(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body)
            print(" New Update Received:")
            
            process_update(update)  # <--- این خط باید فعال باشد
            
            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            print(f" Error: {e}")
            return JsonResponse({"status": "error"}, status=500)
    return JsonResponse({"status": "method not allowed"}, status=405)

def test_connection(request):
    return JsonResponse({"status": "ok", "message": "Server is running!"})