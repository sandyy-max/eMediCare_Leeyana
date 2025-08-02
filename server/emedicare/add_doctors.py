#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from appointment.models import Doctor

def create_doctors():
    # Clear existing doctors
    Doctor.objects.all().delete()
    print("Cleared existing doctors")

    # Create doctors with user's preferred names
    doctors = [
        {
            'name': 'Dr. Puspa',
            'department': 'Cardiology',
            'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'is_available': True
        },
        {
            'name': 'Dr. Darshan',
            'department': 'Cardiology',
            'available_days': ['Monday', 'Wednesday', 'Friday'],
            'is_available': True
        },
        {
            'name': 'Dr. Subham',
            'department': 'Pulmonology',
            'available_days': ['Tuesday', 'Thursday', 'Saturday'],
            'is_available': True
        },
        {
            'name': 'Dr. Sandhya',
            'department': 'Pulmonology',
            'available_days': ['Monday', 'Wednesday', 'Friday'],
            'is_available': True
        },
        {
            'name': 'Dr. Sabnam',
            'department': 'Dermatology',
            'available_days': ['Monday', 'Tuesday', 'Thursday', 'Friday'],
            'is_available': True
        },
        {
            'name': 'Dr. Sudan',
            'department': 'Pediatrics',
            'available_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'is_available': True
        },
        {
            'name': 'Dr. Anjali',
            'department': 'Gynecology',
            'available_days': ['Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'is_available': True
        }
    ]

    for doctor_data in doctors:
        doctor = Doctor.objects.create(**doctor_data)
        print(f"Created: {doctor}")

    print(f"\n✅ Created {len(doctors)} doctors successfully!")
    print("\nDoctor Details:")
    for doctor in Doctor.objects.all():
        print(f"- {doctor.name} ({doctor.department}) - Available: {', '.join(doctor.available_days)}")

if __name__ == "__main__":
    create_doctors() 
    