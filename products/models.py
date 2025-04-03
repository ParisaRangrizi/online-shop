from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="دسته والد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="اسلاگ دسته‌بندی", default='')  # اسلاگ برای URL دسته‌بندی

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    brand = models.CharField(max_length=100, verbose_name="برند")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name="تصویر محصول")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ محصول",  default='')  # اسلاگ برای URL محصول

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

class Discount(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'درصدی'),
        ('fixed', 'نقدی'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts', verbose_name="محصول")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, verbose_name="نوع تخفیف")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار تخفیف")
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="حداکثر مقدار (برای درصدی)")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف‌ها"

    def __str__(self):
        return f"{self.get_discount_type_display()} تخفیف برای {self.product.name}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="کد تخفیف")
    discount_type = models.CharField(max_length=10, choices=Discount.DISCOUNT_TYPES, verbose_name="نوع تخفیف")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مقدار تخفیف")
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="حداکثر مقدار (برای درصدی)")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"

    def __str__(self):
        return self.code