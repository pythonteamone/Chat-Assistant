from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def webhook_endpoint(request):
    if request.method == "POST":
        update = json.loads(request.body)
        print("Update received from Telegram:", update)
        
        # در مرحله بعد dispatcher را اینجا صدا می‌زنیم
        
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "failed"}, status=400)