from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    """
    Comprehensive notification model for all types of notifications
    including admin messages, system updates, appointment reminders, etc.
    """
    NOTIFICATION_TYPES = [
        ('appointment', 'Appointment'),
        ('medicine', 'Medicine'),
        ('package', 'Package'),
        ('admin', 'Admin'),
        ('system', 'System'),
    ]
    
    # Recipient information
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text="Targeted patient. Leave empty if sending to all."
    )
    
    # Notification content
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system'
    )
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=True)  # Default to True for immediate notifications
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Time when the notification should be triggered (for scheduled notifications)."
    )
    
    # Admin options
    send_to_all = models.BooleanField(
        default=False, 
        help_text="Check to send this message to all patients."
    )
    
    # Additional data (for complex notifications)
    related_id = models.IntegerField(
        null=True, 
        blank=True,
        help_text="ID of related object (appointment, medicine request, etc.)"
    )
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        recipient = "All Patients" if self.send_to_all else self.patient.full_name if self.patient else "Unassigned"
        return f"{self.notification_type.title()} notification for {recipient}: {self.title}"

    @classmethod
    def create_notification(cls, patient, title, message, notification_type='system', send_to_all=False, related_id=None):
        """
        Helper method to create notifications easily
        """
        if send_to_all:
            # Create notification for all patients
            patients = User.objects.filter(role='patient')
            notifications = []
            for patient_user in patients:
                notification = cls.objects.create(
                    patient=patient_user,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    related_id=related_id
                )
                notifications.append(notification)
            return notifications
        else:
            # Create notification for specific patient
            return cls.objects.create(
                patient=patient,
                title=title,
                message=message,
                notification_type=notification_type,
                related_id=related_id
            )

    @classmethod
    def create_appointment_notification(cls, patient, appointment):
        """
        Create appointment-related notification
        """
        title = f"Appointment {appointment.status.title()}"
        message = f"Your appointment scheduled for {appointment.appointment_date} has been {appointment.status}."
        return cls.create_notification(
            patient=patient,
            title=title,
            message=message,
            notification_type='appointment',
            related_id=appointment.id
        )

    @classmethod
    def create_medicine_notification(cls, patient, medicine_request):
        """
        Create medicine request notification
        """
        title = f"Medicine Request {medicine_request.status.title()}"
        message = f"Your medicine request for {medicine_request.medicine_name} has been {medicine_request.status}."
        return cls.create_notification(
            patient=patient,
            title=title,
            message=message,
            notification_type='medicine',
            related_id=medicine_request.id
        )

    @classmethod
    def create_package_notification(cls, patient, package_purchase):
        """
        Create package booking notification
        """
        title = f"Package Booking Confirmed"
        message = f"Your {package_purchase.package.name} package has been booked successfully for {package_purchase.selected_date}."
        return cls.create_notification(
            patient=patient,
            title=title,
            message=message,
            notification_type='package',
            related_id=package_purchase.id
        )
