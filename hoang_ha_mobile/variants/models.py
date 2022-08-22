from turtle import color
from xml.dom import pulldom
from django.db import models

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from products.models import Product

User = get_user_model()

# Create your models here.



class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variants")
    color = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    size = models.CharField(max_length=255, null=True, blank=True)
    strap = models.CharField(max_length=255, null=True, blank=True)
    general = models.CharField(max_length=255, null=True, blank=True)
    utilities = models.CharField(max_length=255, null=True, blank=True)
    network = models.CharField(max_length=255, null=True, blank=True)
    storage = models.CharField(max_length=255, null=True, blank=True)
    os_cpu = models.CharField(max_length=255, null=True, blank=True)
    front_cam = models.CharField(max_length=255, null=True, blank=True)
    camera = models.CharField(max_length=255, null=True, blank=True)
    pin = models.CharField(max_length=255, null=True, blank=True)
    screen = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(null=True, upload_to="images/")
    price = models.BigIntegerField(null=True)
    sale = models.BigIntegerField(null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,related_name="variant_created", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,related_name="variant_updated", null=True)
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, related_name="variant_deleted", null=True)

    

    class Meta:
        db_table ='variant'
        unique_together = ['product','color','version']

    def __str__(self) :
        return self.product.name + " + " + str(self.version) + " + " + str(self.color)

    # def validate_unique(self, *args, **kwargs):
    #     super().validate_unique(*args, **kwargs) # python3
    #     if self.__class__.objects.filter(product = self.product,color =self.color,version =self.version).exists():
    #         raise ValidationError(
    #             message='This variant already exists.',
    #         )