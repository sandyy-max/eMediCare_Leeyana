from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Prescription
from notification.models import Notification
from datetime import timedelta, datetime

@receiver(post_save, sender=Prescription)
def create_medicine_reminders(sender, instance, created, **kwargs):
    if created:
        start = instance.reminder_start_date
        end = instance.reminder_end_date
        time_str = instance.reminder_time.strftime('%H:%M')

        # Loop through each date in reminder range
        current = start
        while current <= end:
            message = f"Reminder: Take your medicines as prescribed on {current.strftime('%Y-%m-%d')} at {time_str}."
            Notification.objects.create(
                patient=instance.patient,
                title="Medicine Reminder",
                message=message,
                notification_type="medicine"
            )
            current += timedelta(days=1)
