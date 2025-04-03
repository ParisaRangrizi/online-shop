from django.db import models
from core.models import CustomUser
from products.models import Product, DiscountCode

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('confirmed', 'تأیید شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کد تخفیف")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    address = models.ForeignKey('customers.Address', on_delete=models.SET_NULL, null=True, verbose_name="آدرس")
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f"سفارش {self.id} - {self.user.email}"

    def total_price(self):
        total = sum(item.subtotal() for item in self.order_items.all())
        if self.discount_code:
            if self.discount_code.discount_type == 'percentage':
                discount = total * (self.discount_code.value / 100)
                if self.discount_code.max_amount:
                    discount = min(discount, self.discount_code.max_amount)
                total -= discount
            else:  # fixed
                total -= self.discount_code.value
        return max(total, 0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity