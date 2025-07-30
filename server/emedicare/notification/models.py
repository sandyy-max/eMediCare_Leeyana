from django.db import models
from django.conf import settings
from clinical.models import Prescription

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Notification model for sending both automatic medicine reminders
    and custom messages to patients (individually or in bulk).
    """
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text="Targeted patient. Leave empty if sending to all."
    )
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='notifications',
        blank=True,
        null=True,
        help_text="Optional. Linked prescription for auto-reminders."
    )
    message = models.TextField()
    scheduled_time = models.DateTimeField(
        help_text="Time when the notification should be triggered."
    )
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW FIELD: Admin option to send to all patients
    send_to_all = models.BooleanField(default=False, help_text="Check to send this message to all patients.")

    def __str__(self):
        recipient = "All Patients" if self.send_to_all else self.patient.full_name if self.patient else "Unassigned"
        return f"Notification for {recipient} on {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
