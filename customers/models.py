from django.db import models
from core.models import CustomUser

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    city = models.CharField(max_length=100, verbose_name="شهر")
    province = models.CharField(max_length=100, verbose_name="استان")
    details = models.TextField(verbose_name="جزئیات آدرس")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="کد پستی")
    is_default = models.BooleanField(default=False, verbose_name="پیش‌فرض")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"

    def __str__(self):
        return f"{self.province}، {self.city} - {self.details}"