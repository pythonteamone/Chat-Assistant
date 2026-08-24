from core.services.bot_api_client import TelegramAPIClient

def process_update(update):
    """پردازش آپدیت‌های دریافتی از تلگرام"""
    if 'message' in update:
        handle_message(update['message'])
    elif 'business_message' in update:
        handle_business_message(update['business_message'])
    elif 'business_connection' in update:
        handle_business_connection(update['business_connection'])
    else:
        print(f"Unknown update type: {list(update.keys())}")

def handle_message(message_data):
    """پردازش پیام‌های عادی"""
    chat_id = message_data['chat']['id']
    text = message_data.get('text', '')
    print(f"💬 پیام عادی دریافت شد | Chat ID: {chat_id} | Text: {text}")
    
    response_text = generate_response(text)
    client = TelegramAPIClient()
    client.send_message(business_connection_id="", text=response_text, chat_id=chat_id)

def handle_business_message(message_data):
    """پردازش پیام‌های بیزنس"""
    chat_id = message_data.get('chat', {}).get('id')
    business_connection_id = message_data.get('business_connection_id', '')
    text = message_data.get('text', '')
    print(f" پیام بیزنس دریافت شد | Chat ID: {chat_id} | Text: {text}")
    
    response_text = generate_response(text)
    client = TelegramAPIClient()
    client.send_message(business_connection_id=business_connection_id, text=response_text, chat_id=chat_id)

def handle_business_connection(connection_data):
    """ثبت اتصال بیزنس جدید"""
    print(" New business connection established!")
    print(f"Connection ID: {connection_data.get('id')}")

def generate_response(text):
    """منطق پاسخ‌دهی هوشمند"""
    text_lower = text.lower()
    if 'سلام' in text_lower or 'درود' in text_lower:
        return "سلام!  من ربات دستیار هوشمند هستم. چطور می‌توانم کمکتان کنم؟"
    elif 'قیمت' in text_lower or 'هزینه' in text_lower:
        return "برای اطلاع از قیمت‌ها، لطفاً با پشتیبانی تماس بگیرید."
    else:
        return "پیام شما دریافت شد. به زودی پاسخ می‌دهیم."