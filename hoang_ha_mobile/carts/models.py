from django.db import models

from django.contrib.auth import get_user_model
from variants.models import Variant

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="carts")
    quantity = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'carts'