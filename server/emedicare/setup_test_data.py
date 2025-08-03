#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta, time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from clinical.models import Prescription
from appointment.models import Doctor
from userauth.models import User
from notification.models import Notification

def setup_test_data():
    print("🏥 Setting up test data...")
    
    # Create a test patient if none exists
    patient = User.objects.filter(role='patient').first()
    if not patient:
        print("Creating test patient...")
        patient = User.objects.create(
            phone_number='1234567890',
            full_name='Test Patient',
            email='patient@test.com',
            role='patient',
            password='testpass123'
        )
        print(f"✅ Created patient: {patient.full_name}")
    else:
        print(f"✅ Using existing patient: {patient.full_name}")

    # Create doctors if none exist
    if Doctor.objects.count() == 0:
        print("Creating test doctors...")
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
            }
        ]
        
        for doctor_data in doctors:
            doctor = Doctor.objects.create(**doctor_data)
            print(f"✅ Created doctor: {doctor.name}")
    else:
        print(f"✅ Found {Doctor.objects.count()} existing doctors")

    # Get the first doctor
    doctor = Doctor.objects.first()
    if not doctor:
        print("❌ No doctors found!")
        return

    # Clear existing prescriptions for this patient
    Prescription.objects.filter(patient=patient).delete()
    print(f"🧹 Cleared existing prescriptions for {patient.full_name}")

    # Create sample prescriptions
    prescriptions = [
        {
            'patient': patient,
            'doctor': doctor,
            'diagnosis': 'Hypertension (High Blood Pressure)',
            'medicines': 'Amlodipine 5mg - 1 tablet daily in the morning\nLisinopril 10mg - 1 tablet daily in the morning',
            'prescribed_date': date.today() - timedelta(days=30),
            'reminder_time': time(8, 0),  # 08:00:00
            'reminder_start_date': date.today() - timedelta(days=30),
            'reminder_end_date': date.today() + timedelta(days=30)
        },
        {
            'patient': patient,
            'doctor': doctor,
            'diagnosis': 'Type 2 Diabetes',
            'medicines': 'Metformin 500mg - 1 tablet twice daily with meals\nGlimepiride 1mg - 1 tablet daily in the morning',
            'prescribed_date': date.today() - timedelta(days=15),
            'reminder_time': time(8, 0),  # 08:00:00
            'reminder_start_date': date.today() - timedelta(days=15),
            'reminder_end_date': date.today() + timedelta(days=45)
        },
        {
            'patient': patient,
            'doctor': doctor,
            'diagnosis': 'Seasonal Allergies',
            'medicines': 'Cetirizine 10mg - 1 tablet daily in the evening\nFluticasone nasal spray - 2 sprays in each nostril daily',
            'prescribed_date': date.today() - timedelta(days=7),
            'reminder_time': time(20, 0),  # 20:00:00
            'reminder_start_date': date.today() - timedelta(days=7),
            'reminder_end_date': date.today() + timedelta(days=23)
        }
    ]

    created_prescriptions = []
    for prescription_data in prescriptions:
        try:
            prescription = Prescription.objects.create(**prescription_data)
            created_prescriptions.append(prescription)
            print(f"✅ Created prescription: {prescription.diagnosis}")
        except Exception as e:
            print(f"❌ Error creating prescription: {e}")

    print(f"\n🎉 Created {len(created_prescriptions)} prescriptions successfully!")
    
    # Check notifications
    notifications = Notification.objects.filter(patient=patient, notification_type='medicine')
    print(f"📧 Created {notifications.count()} medicine notifications")
    
    print(f"\n📋 Medical History Summary for {patient.full_name}:")
    for prescription in Prescription.objects.filter(patient=patient):
        print(f"- {prescription.diagnosis} (Prescribed: {prescription.prescribed_date})")
        print(f"  Doctor: {prescription.doctor.name}")
        print(f"  Medicines: {prescription.medicines[:50]}...")
        print()

    print("🔍 Test Data Setup Complete!")
    print("1. Login as patient with phone: 1234567890, password: testpass123")
    print("2. Go to Medical History page")
    print("3. Check Medications tab for prescriptions")
    print("4. Check notifications page for medicine reminders")

if __name__ == "__main__":
    setup_test_data() 