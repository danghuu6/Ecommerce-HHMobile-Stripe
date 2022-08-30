from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


STATUS_CHOICES = [
    ("incomplete", "incomplete"),
    ("charge", "charge"),
    ("refund", "refund"),
    ("failed", "failed"),
]


class Transaction(models.Model):
    time = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=255, choices=STATUS_CHOICES, default='incomplete')
    amount = models.CharField(max_length=255)
    fees = models.CharField(max_length=255)
    net = models.CharField(max_length=255)
    order = models.IntegerField()
    source = models.CharField(max_length=255)
    Customer = models.CharField(max_length=255)

    def __str__(self):
        return self.Customer +" "+self.type+" "+self.order