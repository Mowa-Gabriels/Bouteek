from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Payment(models.Model):
    paystack_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount   = models.DecimalField(default=0.00, decimal_places=2, max_digits=100, validators=[MinValueValidator(0), MaxValueValidator(100000000000)], null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user.email