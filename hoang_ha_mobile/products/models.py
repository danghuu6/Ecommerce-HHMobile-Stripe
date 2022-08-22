from email.policy import default
from django.db import models
from categories.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, unique= True)
    description = models.TextField(null=True)
    insurance = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    status = models.BooleanField(default=False)
    favorite = models.ManyToManyField(User,blank=True, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,related_name="product_created", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,related_name="product_updated", null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, related_name="product_deleted", null=True)

    class Meta:
        db_table = 'products' 

    def __str__(self):
        return self.name