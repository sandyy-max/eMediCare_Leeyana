from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='prescriptions/')

    def __str__(self):
        return f"{self.patient.phone} - {self.uploaded_at}"

class MedicineRequest(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')

    def __str__(self):
        return f"{self.patient.phone} requested {self.medicine.name}"
