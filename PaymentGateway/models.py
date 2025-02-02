import uuid
from django.db import models
from enum import Enum


class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class PaymentGateway(models.Model):
    gateway_name = models.CharField(max_length=100, unique=True)  # نام درگاه پرداخت
    api_url = models.URLField()  # URL API برای ارتباط با درگاه
    merchant_id = models.CharField(max_length=50)  # شناسه مرچنت
    API_key = models.CharField(max_length=200)  # کلید محرمانه برای امنیت
    active = models.BooleanField(default=True)  # فعال بودن یا نبودن درگاه

    def __str__(self):
        return self.gateway_name


class PaymentTransaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # شناسه یونیک تراکنش
    national_code = models.CharField(max_length=10)  # کد ملی کاربر
    amount = models.BigIntegerField()  # مبلغ تراکنش (تومان)
    payment_method = models.ForeignKey(PaymentGateway, related_name='transactions', on_delete=models.CASCADE)  # درگاه پرداخت
    wallet_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # شناسه کیف پول از سیستم دیگر (UUID)
    status = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in PaymentStatus], default=PaymentStatus.PENDING.value)  # وضعیت تراکنش
    timestamp = models.DateTimeField(auto_now_add=True)  # زمان انجام تراکنش
    description = models.TextField(blank=True, null=True)  # توضیحات (اختیاری)

    def __str__(self):
        return f"PaymentTransaction {self.transaction_id} - {self.status} - {self.amount} for {self.national_code}"

