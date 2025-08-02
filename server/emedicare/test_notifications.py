#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from notification.models import Notification
from userauth.models import User

def create_test_notifications():
    # Get the first patient user
    try:
        patient = User.objects.filter(role='patient').first()
        if not patient:
            print("No patient users found. Please create a patient user first.")
            return
        
        print(f"Creating test notifications for patient: {patient.full_name}")
        
        # Clear existing test notifications
        Notification.objects.filter(patient=patient).delete()
        
        # Create test notifications
        notifications = [
            {
                'title': 'Welcome to eMediCare!',
                'message': 'Thank you for joining our healthcare platform. We\'re here to provide you with the best medical care.',
                'notification_type': 'system',
                'is_read': False
            },
            {
                'title': 'Appointment Reminder',
                'message': 'You have an upcoming appointment tomorrow at 10:00 AM. Please arrive 15 minutes early.',
                'notification_type': 'appointment',
                'is_read': False
            },
            {
                'title': 'Medicine Request Approved',
                'message': 'Your medicine request for Paracetamol has been approved and is ready for pickup.',
                'notification_type': 'medicine',
                'is_read': True
            },
            {
                'title': 'Package Booking Confirmed',
                'message': 'Your Cardiology Package has been booked successfully for next week.',
                'notification_type': 'package',
                'is_read': False
            },
            {
                'title': 'System Maintenance Notice',
                'message': 'Our system will be under maintenance tonight from 2:00 AM to 4:00 AM. Some services may be temporarily unavailable.',
                'notification_type': 'admin',
                'is_read': False
            }
        ]
        
        for i, notif_data in enumerate(notifications):
            # Create notifications with different timestamps
            created_at = datetime.now() - timedelta(hours=i*2)
            notification = Notification.objects.create(
                patient=patient,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['notification_type'],
                is_read=notif_data['is_read'],
                created_at=created_at
            )
            print(f"Created notification: {notification.title}")
        
        # Get notification count
        total_notifications = Notification.objects.filter(patient=patient).count()
        unread_notifications = Notification.objects.filter(patient=patient, is_read=False).count()
        
        print(f"\n✅ Test notifications created successfully!")
        print(f"Total notifications: {total_notifications}")
        print(f"Unread notifications: {unread_notifications}")
        
    except Exception as e:
        print(f"Error creating test notifications: {e}")

if __name__ == "__main__":
    create_test_notifications() 