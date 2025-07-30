from django.db import models
from django.conf import settings
from appointment.models import Doctor  # Reuse existing Doctor model

User = settings.AUTH_USER_MODEL

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medicines = models.TextField(help_text="Medicine names with dosage and timing instructions.")
    prescribed_date = models.DateField(auto_now_add=True)
    reminder_time = models.TimeField(help_text="Time of day patient should take the medicine.")
    reminder_start_date = models.DateField(help_text="When should reminders start?")
    reminder_end_date = models.DateField(help_text="When should reminders stop?")

    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor.name} on {self.prescribed_date}"
