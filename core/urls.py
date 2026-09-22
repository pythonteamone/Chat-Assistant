from django.urls import path
from core import views

urlpatterns = [
    path('webhook/', views.webhook_endpoint, name='webhook'),
    path('test/', views.test_connection, name='test'),
]