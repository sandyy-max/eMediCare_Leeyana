from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date

User = settings.AUTH_USER_MODEL

DEPARTMENT_CHOICES = [
    ('Cardiology', 'Cardiology'),
    ('Pulmonology', 'Pulmonology'),
    ('Dermatology', 'Dermatology'),
    ('Pediatrics', 'Pediatrics'),
    ('Gynecology', 'Gynecology'),
]


class Doctor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    available_days = models.JSONField(default=list, blank=True, null=True)  # e.g. ["Monday", "Tuesday"]
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.department}"


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    dob = models.DateField()
    symptoms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment({self.full_name} - {self.department} - {self.created_at.date()})"

    class Meta:
        ordering = ['-created_at']


class Confirmation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='confirmation')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    def __str__(self):
        return f"Confirmed: {self.appointment.full_name} with Dr. {self.doctor.name} on {self.appointment_date} at {self.appointment_time}"

    def clean(self):
        if self.appointment_date < date.today():
            raise ValidationError("Appointment date cannot be in the past.")

        # ✅ Check for doctor conflict (same date & time)
        conflict = Confirmation.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time
        ).exclude(pk=self.pk)

        if conflict.exists():
            raise ValidationError("This doctor already has an appointment at this date and time.")

        # ✅ Check if doctor is available that day (based on available_days)
        if self.doctor.available_days:
            weekday_name = self.appointment_date.strftime('%A')  # e.g., "Monday"
            if weekday_name not in self.doctor.available_days:
                raise ValidationError(f"Doctor is not available on {weekday_name}.")

    def save(self, *args, **kwargs):
        self.clean()  # validate before saving
        super().save(*args, **kwargs)

        # ✅ Mark appointment as confirmed if not already
        if not self.appointment.is_confirmed:
            self.appointment.is_confirmed = True
            self.appointment.save(update_fields=['is_confirmed'])
