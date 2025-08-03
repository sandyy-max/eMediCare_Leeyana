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
from notification.models import Notification

def test_medical_flow():
    print("🏥 Testing Medical History Flow...")
    
    # Get the first patient and doctor
    try:
        patient = User.objects.filter(role='patient').first()
        doctor = Doctor.objects.first()

        if not patient:
            print("❌ No patient found. Please create a patient user first.")
            return

        if not doctor:
            print("❌ No doctor found. Please run add_doctors.py first.")
            return

        print(f"✅ Using patient: {patient.full_name}")
        print(f"✅ Using doctor: {doctor.name}")

        # Clear existing prescriptions for this patient
        Prescription.objects.filter(patient=patient).delete()
        print(f"🧹 Cleared existing prescriptions for {patient.full_name}")

        # Create sample prescriptions
        from datetime import time
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
            prescription = Prescription.objects.create(**prescription_data)
            created_prescriptions.append(prescription)
            print(f"✅ Created: {prescription.diagnosis}")

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

        print("🔍 Testing API endpoints...")
        print("1. Login as patient and go to medical history page")
        print("2. Check if prescriptions appear in Medications tab")
        print("3. Check notifications page for medicine reminders")
        print("4. Verify that admin can see prescriptions in admin panel")

    except Exception as e:
        print(f"❌ Error in medical flow test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_medical_flow() 