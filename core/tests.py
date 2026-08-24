from django.test import TestCase
from core.services.dispatcher import process_update

class DispatcherTest(TestCase):
    def test_normal_message(self):
        update = {'message': {'chat': {'id': 123}, 'text': 'سلام'}}
        process_update(update) # اگر خطا ندهد، تست پاس است

    def test_business_message(self):
        update = {'business_message': {'chat': {'id': 456}, 'business_connection_id': 'abc', 'text': 'قیمت'}}
        process_update(update)