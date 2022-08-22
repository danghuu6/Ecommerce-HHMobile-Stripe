from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name ="category_created" ,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="category_updated", blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="category_deleted", blank=True, null=True)

    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.name