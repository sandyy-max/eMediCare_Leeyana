# package/models.py
from django.db import models
from django.conf import settings
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class HealthPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.IntegerField(default=3)  # Package valid for X days after purchase
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PackagePurchase(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(HealthPackage, on_delete=models.CASCADE)
    selected_date = models.DateField(default='2024-01-01')  # Date patient chooses
    purchased_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Success')  # Simplified
    valid_until = models.DateField(blank=True, null=True)
    patient_details = models.JSONField(default=dict, blank=True)  # Store patient details

    def save(self, *args, **kwargs):
        if not self.valid_until:
            self.valid_until = self.selected_date + timedelta(days=self.package.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} - {self.package.name}"
