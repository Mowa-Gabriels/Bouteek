from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from store.models import *
from .paystack import PayStack

# Create your models here.

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_verified = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    ref = models.CharField(max_length=100, null=True)
    amount = models.FloatField(max_length=100, null=True)

    def _str_(self):
        return self.id  

    def verify_payment(self):
        paystack = PayStack()
        status,result = paystack.verify_paystack(self.id)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
