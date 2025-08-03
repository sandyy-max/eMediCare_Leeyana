#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from clinical.models import Prescription
from appointment.models import Doctor
from userauth.models import User

def create_test_data():
    print("🏥 Creating test medical history data...")
    
    # Get or create a patient
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
    
    # Get or create a doctor
    doctor = Doctor.objects.first()
    if not doctor:
        print("Creating test doctor...")
        doctor = Doctor.objects.create(
            name='Dr. Test Doctor',
            department='Cardiology',
            available_days=['Monday', 'Tuesday', 'Wednesday'],
            is_available=True
        )
    
    # Clear existing prescriptions for this patient
    Prescription.objects.filter(patient=patient).delete()
    
    # Create test prescriptions
    prescriptions = [
        {
            'diagnosis': 'Hypertension',
            'medicines': 'Amlodipine 5mg daily\nLisinopril 10mg daily',
            'prescribed_date': date.today() - timedelta(days=7),
            'reminder_time': '08:00:00',
            'reminder_start_date': date.today() - timedelta(days=7),
            'reminder_end_date': date.today() + timedelta(days=30)
        },
        {
            'diagnosis': 'Type 2 Diabetes',
            'medicines': 'Metformin 500mg twice daily\nGlimepiride 1mg daily',
            'prescribed_date': date.today() - timedelta(days=14),
            'reminder_time': '08:00:00',
            'reminder_start_date': date.today() - timedelta(days=14),
            'reminder_end_date': date.today() + timedelta(days=45)
        },
        {
            'diagnosis': 'Asthma',
            'medicines': 'Salbutamol inhaler as needed\nBudesonide inhaler daily',
            'prescribed_date': date.today() - timedelta(days=21),
            'reminder_time': '08:00:00',
            'reminder_start_date': date.today() - timedelta(days=21),
            'reminder_end_date': date.today() + timedelta(days=60)
        }
    ]
    
    created_prescriptions = []
    for prescription_data in prescriptions:
        prescription = Prescription.objects.create(
            patient=patient,
            doctor=doctor,
            **prescription_data
        )
        created_prescriptions.append(prescription)
        print(f"✅ Created prescription: {prescription.diagnosis}")
    
    print(f"\n🎉 Successfully created {len(created_prescriptions)} prescriptions!")
    print(f"Patient: {patient.full_name}")
    print(f"Doctor: {doctor.name}")
    print(f"Total prescriptions in database: {Prescription.objects.count()}")

if __name__ == "__main__":
    create_test_data() 