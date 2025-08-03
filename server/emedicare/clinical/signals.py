from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Prescription
from notification.models import Notification
from datetime import timedelta, datetime

@receiver(post_save, sender=Prescription)
def create_medicine_reminders(sender, instance, created, **kwargs):
    if created:
        # Create notification for new prescription
        prescription_notification = Notification.objects.create(
            patient=instance.patient,
            title="New Prescription Added",
            message=f"Dr. {instance.doctor.name} has prescribed new medicines for {instance.diagnosis}. Check your medical history for details.",
            notification_type="medicine"
        )
        
        # Create medicine reminders
        start = instance.reminder_start_date
        end = instance.reminder_end_date
        
        # Handle reminder_time properly - it's a TimeField
        if hasattr(instance.reminder_time, 'strftime'):
            time_str = instance.reminder_time.strftime('%H:%M')
        else:
            # If it's a string, try to parse it
            time_str = str(instance.reminder_time)

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
