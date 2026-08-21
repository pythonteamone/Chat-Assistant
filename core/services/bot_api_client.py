import requests
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class TelegramAPIClient:
    @staticmethod
    def send_message(business_connection_id: str, text: str, chat_id: int = None):
        """
        ارسال پیام متنی از طریق بیزینس کانکشن
        مستندات: https://core.telegram.org/bots/api#sendmessage
        """
        url = f"{BASE_URL}/sendMessage"

        payload = {
            "business_connection_id": business_connection_id,
            "text": text,
            "parse_mode": "HTML",  # برای پشتیبانی از فرمت‌دهی متن
        }

        # اگر چت آیدی مشخص باشد، آن را اضافه می‌کنیم
        if chat_id:
            payload["chat_id"] = chat_id

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()  # بررسی خطاهای HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in Telegram API request: {e}")
            return None

    @staticmethod
    def get_me():
        """
        تست اتصال بات و دریافت اطلاعات پروفایل بات
        """
        url = f"{BASE_URL}/getMe"
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error getting bot info: {e}")
            return None