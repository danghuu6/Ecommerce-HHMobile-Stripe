from django.db import models
from variants.models import Variant
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=18)
    content = models.TextField()
    rating = models.IntegerField(default = 0)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="comments", null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name ="comment_created" ,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="comment_updated", blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="comment_deleted", blank=True, null=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return str(self.name) + " + " + str(self.rating)
    
    