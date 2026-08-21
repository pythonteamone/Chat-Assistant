
from django.db import models

class BusinessAccount(models.Model):
    """
    مدلی برای ذخیره اطلاعات اکانت‌های بیزینس متصل شده به بات
    """
    user_id = models.BigIntegerField(
        unique=True, 
        help_text="آیدی عددی منحصر به فرد کاربر در تلگرام"
    )
    business_connection_id = models.CharField(
        max_length=255, 
        unique=True, 
        help_text="شناسه اتصال بیزینس دریافتی از تلگرام"
    )
    first_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="نام اول کاربر"
    )
    username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="نام کاربری تلگرام"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="وضعیت فعال بودن اتصال"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="تاریخ ایجاد رکورد"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="تاریخ آخرین بروزرسانی"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "اکانت بیزینس"
        verbose_name_plural = "اکانت‌های بیزینس"

    def __str__(self):
        return f"Business Account: {self.username or self.user_id}"