from django.utils import timezone
import datetime as dt
import requests
from datetime import timedelta

from core.services.bot_api_client import TelegramAPIClient , BASE_URL , BOT_TOKEN
from core.models import BusinessAccount


def process_update(update):
    """پردازش آپدیت‌های دریافتی از تلگرام"""
    if 'message' in update:
        print("massage")
        handle_message(update['message'])
    elif 'business_message' in update:
        print("business_message")
        handle_business_message(update['business_message'])
    elif 'business_connection' in update:
        print("business_connection")
        handle_business_connection(update['business_connection'])
    else:
        print(f"Unknown update type: {list(update.keys())}")


def handle_message(message_data):
    """پردازش پیام و ارسال پاسخ با کیبورد"""
    chat_id = message_data['chat']['id']
    text = message_data.get('text', '')
    print(f"💬 پیام دریافت شد | Chat ID: {chat_id} | Text: {text}")

    response_text, keyboard = generate_response(text)

    # ارسال مستقیم به تلگرام (بدون نیاز به bot_api_client)
    send_to_telegram(chat_id, response_text, keyboard)


def send_to_telegram(chat_id, text, keyboard=None):
    """ارسال مستقیم پیام به تلگرام"""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    # اگر کیبورد وجود داشت، اضافه کن
    if keyboard:
        payload["reply_markup"] = keyboard

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ پیام ارسال شد: {response.json().get('description', 'OK')}")
        return response.json()
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")
        return None


def generate_response(text):
    """منطق پاسخ‌دهی هوشمند با کیبورد متنی"""
    text_lower = text.lower().strip()

    # منوی اصلی (سلام یا /start)
    if text_lower == '/start':
        keyboard = {
            "keyboard": [
                [{"text": "🎁 پلن رایگان"}, {"text": "🛠️ پلن عادی"}],
                [{"text": " پلن پرو"}, {"text": " راهنما"}],
                [{"text": "👤 حساب کاربری"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
        return "سلام! 👋\nبه ربات منیجر چت ها خوش آمدی.\n\nلطفاً یکی از پلن‌ها را از منوی پایین انتخاب کن: 👇", keyboard

    # پاسخ به دکمه‌ها
    elif text_lower in ['🎁 پلن رایگان', 'پلن رایگان']:
        return "🎁 پلن رایگان:\n- دسترسی پایه\n- محدودیت استفاده\n\nبرای ارتقا به پلن‌های بالاتر با پشتیبانی تماس بگیرید.", {"inline_keyboard" : [[{"text": "فعال سازی پلن رایگان"}],[{"text" : "باز گشت به منو"}]]}

    elif text_lower in ['🛠️ پلن عادی', 'پلن عادی']:
        return "🛠️ پلن عادی:\n- دسترسی کامل به امکانات پایه\n- پشتیبانی استاندارد\n\nقیمت: ۱۰ هزار تومان در ماه", None

    elif text_lower in ['🚀 پلن پرو', 'پلن پرو']:
        return "🚀 پلن پرو:\n- تمام امکانات\n- پشتیبانی ویژه\n- بدون محدودیت\n\nقیمت: ۳۰۰ هزار تومان در ماه", None

    elif text_lower in ['📚 راهنما', 'راهنما']:
        return " راهنما:\n\n1️⃣ برای شروع، یکی از پلن‌ها را انتخاب کنید.\n2️⃣ پس از انتخاب، اطلاعات حساب شما ثبت می‌شود.\n3️⃣ در صورت نیاز به کمک، با پشتیبانی تماس بگیرید.", None

    elif text_lower in [' حساب کاربری', 'حساب کاربری']:
        return "👤 حساب کاربری:\n\nبرای مشاهده اطلاعات حساب خود، لطفاً با پشتیبانی تماس بگیرید.", None

    elif "فعال سازی پلن رایگان" in text_lower :
        return "فعال شد 🎉✨"

    else:
        return "یکی از گزینه ها را انتخاب کنید یا روی : \n  /start \n بزنید ", None


def handle_business_message(message_data):
    """پردازش پیام‌های بیزنس"""
    chat_id = message_data.get('chat', {}).get('id')
    a = message_data
    if BusinessAccount.objects.get(business_connection_id=message_data.get('business_connection_id')) :
        v = BusinessAccount.objects.get(business_connection_id=message_data.get('business_connection_id'))
        if v.user_id == message_data.get('from','').get('id','') :
            d = dt.datetime.now()
            v.updated_at = d
            v.save()
        else:
            time_diff = timezone.now() - v.updated_at
            print(v.updated_at, "updated_at")
            print('time_diff', time_diff)

            if time_diff < timedelta(minutes=5):
                print(f"User {v.user_id} is recently active ({time_diff.seconds}s ago). Bot skipping...")
            else:
                print(f"User {v.user_id} seems offline/inactive. Bot taking over.")
                business_connection_id = message_data.get('business_connection_id', '')
                text = message_data.get('text', '')
                print(f" پیام بیزنس دریافت شد | Chat ID: {chat_id} | Text: {text}")
                response_text = respons_business_message(text)
                client = TelegramAPIClient()
                client.send_message(business_connection_id=business_connection_id, text=response_text, chat_id=chat_id)
                print(f"پاسخ کاربر {chat_id} داده شد .")

def respons_business_message(message_data):
    text_lower = message_data.lower()
    if 'سلام' in text_lower or 'درود' in text_lower:
        return "سلام!  من ربات دستیار هوشمند هستم. چطور می‌توانم کمکتان کنم؟"
    elif 'قیمت' in text_lower or 'هزینه' in text_lower:
        return "برای اطلاع از قیمت‌ها، لطفاً با پشتیبانی تماس بگیرید."
    else:
        return "پیام شما دریافت شد. به زودی پاسخ می‌دهیم."

def handle_business_connection(connection_data):
    """ثبت اتصال بیزنس جدید"""
    business_connection_id = connection_data.get('id','')
    user_id = connection_data.get('user','').get('id')
    first_name = connection_data.get('user','').get('first_name','')
    username = connection_data.get('user','').get('username','')
    is_enabled = connection_data.get('is_enabled','')
    if is_enabled:
        if BusinessAccount.objects.filter(user_id=user_id):
            v = BusinessAccount.objects.get(user_id=user_id)
            if v.business_connection_id == business_connection_id:
                return
            else:
                v.business_connection_id = business_connection_id
                v.username = username
                v.first_name = first_name
                v.is_active = True
                v.save()
                print(f"updated business connection for userid: {v.user_id}")

        else:
            BusinessAccount.objects.create(user_id=user_id,
                                           business_connection_id=business_connection_id,
                                           first_name=first_name,
                                           username=username)
        print(" New business connection established!")
        print(f"Connection ID: {connection_data.get('id')}")
    else:
        if BusinessAccount.objects.filter(user_id=user_id):
            v = BusinessAccount.objects.get(user_id=user_id)
            print(v.is_active)
            v.is_active = False
            v.save()
            print(is_enabled, "is active" , v.is_active)
        else:
            print("not fonde")