
from email.mime import image
from django.db import models
from django.contrib.auth import get_user_model
from tags.models import Tag
User = get_user_model()
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(default="", null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", null=True)
    viewers = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="articles")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name ="article_created" ,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="article_updated", blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name ="article_deleted", blank=True, null=True)
    image = models.ImageField(null=True, upload_to = "images/")
    
    class Meta: 
        db_table = 'articles'
    def __str__(self):
        return self.title