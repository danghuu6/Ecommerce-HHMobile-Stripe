
from tkinter import CASCADE
from django.db import models
from django.apps import apps
from django.contrib.auth.models import  AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.
#custom user model

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(blank=True,null=True)
    sex = models.CharField(max_length=4)
    updated_at = models.DateTimeField(auto_now=True)
    block_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True)
    block_by = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, upload_to = "images/profile/")
    username = None

    objects = UserManager()
    REQUIRED_FIELDS = ["phone"]
    USERNAME_FIELD = "email"

    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.email

class Address(models.Model): #/api address google address autocomplete
    address = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
   
    class Meta:
        db_table = 'address'
    def __str__(self):
        return self.street

class Pin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    pin = models.IntegerField()