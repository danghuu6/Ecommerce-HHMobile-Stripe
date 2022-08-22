from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from variants.models import Variant

User = get_user_model()

STATUS_CHOICES = [
    ("processing", "processing"),
    ("confirmed", "confirmed"),
    ("delivering", "delivering"),
    ("delivered", "delivered"),
    ("canceled", "canceled"),
]
class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField(_('email address'))
    shipping = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    note = models.TextField()
    status = models.CharField(default="processing",choices= STATUS_CHOICES,max_length=255)
    total = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name ="order_created" ,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="order_updated", blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="order_deleted", blank=True, null=True)

    class Meta:
        db_table = 'orders' 
    
    def __str__(self):
        return self.email

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_details")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,related_name="order_variant_details")
    price = models.BigIntegerField()
    quantity = models.IntegerField()
    

    class Meta:
        db_table = 'orders_detail'

    def __str__(self):
        return str(self.variant)