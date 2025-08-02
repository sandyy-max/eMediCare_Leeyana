from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 
            'is_read', 'created_at', 'related_id'
        ]
        read_only_fields = ['id', 'created_at', 'related_id']

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'patient', 'title', 'message', 'notification_type',
            'send_to_all', 'related_id', 'admin_notes'
        ]

    def create(self, validated_data):
        # If send_to_all is True, create notifications for all patients
        if validated_data.get('send_to_all'):
            patients = self.context['request'].user.objects.filter(role='patient')
            notifications = []
            for patient in patients:
                notification_data = validated_data.copy()
                notification_data['patient'] = patient
                notification = Notification.objects.create(**notification_data)
                notifications.append(notification)
            return notifications[0] if notifications else None
        else:
            return super().create(validated_data)
