from django.contrib import admin
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('patient_display', 'title', 'notification_type', 'is_read', 'is_sent', 'send_to_all', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_sent', 'send_to_all', 'created_at')
    search_fields = ('patient__full_name', 'title', 'message')

    def save_model(self, request, obj, form, change):
        if obj.send_to_all:
            # Send to all patients
            patients = User.objects.filter(role='patient')  # Fixed role field
            for patient in patients:
                Notification.objects.create(
                    patient=patient,
                    title=obj.title,
                    message=obj.message,
                    notification_type=obj.notification_type,
                    scheduled_time=obj.scheduled_time,
                    is_sent=False
                )
        else:
            super().save_model(request, obj, form, change)

    def patient_display(self, obj):
        return "All Patients" if obj.send_to_all else obj.patient.full_name
    patient_display.short_description = "Recipient"
