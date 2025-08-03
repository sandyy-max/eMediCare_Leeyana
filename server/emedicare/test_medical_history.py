#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from clinical.models import Prescription
from appointment.models import Doctor, Appointment
from userauth.models import User
from notification.models import Notification

def test_medical_history():
    print("🏥 Testing Medical History Feature...")
    
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

        # Clear existing data for this patient
        Prescription.objects.filter(patient=patient).delete()
        Appointment.objects.filter(patient=patient).delete()
        print(f"🧹 Cleared existing medical data for {patient.full_name}")

        # Create sample prescriptions
        prescriptions = [
            {
                'patient': patient,
                'doctor': doctor,
                'diagnosis': 'Hypertension (High Blood Pressure)',
                'medicines': 'Amlodipine 5mg - 1 tablet daily in the morning\nLisinopril 10mg - 1 tablet daily in the morning',
                'prescribed_date': date.today() - timedelta(days=30),
                'reminder_time': '08:00:00',
                'reminder_start_date': date.today() - timedelta(days=30),
                'reminder_end_date': date.today() + timedelta(days=30)
            },
            {
                'patient': patient,
                'doctor': doctor,
                'diagnosis': 'Type 2 Diabetes',
                'medicines': 'Metformin 500mg - 1 tablet twice daily with meals\nGlimepiride 1mg - 1 tablet daily in the morning',
                'prescribed_date': date.today() - timedelta(days=15),
                'reminder_time': '08:00:00',
                'reminder_start_date': date.today() - timedelta(days=15),
                'reminder_end_date': date.today() + timedelta(days=45)
            },
            {
                'patient': patient,
                'doctor': doctor,
                'diagnosis': 'Seasonal Allergies',
                'medicines': 'Cetirizine 10mg - 1 tablet daily in the evening\nFluticasone nasal spray - 2 sprays in each nostril daily',
                'prescribed_date': date.today() - timedelta(days=7),
                'reminder_time': '20:00:00',
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

        # Create sample appointments
        appointments = [
            {
                'patient': patient,
                'full_name': patient.full_name,
                'phone_number': patient.phone_number,
                'email': patient.email or 'patient@example.com',
                'department': 'Cardiology',
                'dob': date.today() - timedelta(days=365*30),  # 30 years ago
                'symptoms': 'Chest pain and shortness of breath'
            },
            {
                'patient': patient,
                'full_name': patient.full_name,
                'phone_number': patient.phone_number,
                'email': patient.email or 'patient@example.com',
                'department': 'Endocrinology',
                'dob': date.today() - timedelta(days=365*30),
                'symptoms': 'Increased thirst and frequent urination'
            }
        ]

        created_appointments = []
        for appointment_data in appointments:
            try:
                appointment = Appointment.objects.create(**appointment_data)
                created_appointments.append(appointment)
                print(f"✅ Created appointment: {appointment.department}")
            except Exception as e:
                print(f"❌ Error creating appointment: {e}")

        print(f"\n🎉 Created {len(created_prescriptions)} prescriptions and {len(created_appointments)} appointments successfully!")
        
        # Check notifications
        notifications = Notification.objects.filter(patient=patient, notification_type='medicine')
        print(f"📧 Created {notifications.count()} medicine notifications")
        
        print(f"\n📋 Medical History Summary for {patient.full_name}:")
        print(f"- Prescriptions: {Prescription.objects.filter(patient=patient).count()}")
        print(f"- Appointments: {Appointment.objects.filter(patient=patient).count()}")
        print(f"- Notifications: {Notification.objects.filter(patient=patient).count()}")
        
        print("\n📋 Prescription Details:")
        for prescription in Prescription.objects.filter(patient=patient):
            print(f"- {prescription.diagnosis} (Prescribed: {prescription.prescribed_date})")
            print(f"  Doctor: {prescription.doctor.name}")
            print(f"  Medicines: {prescription.medicines[:50]}...")
            print()

        print("🔍 Testing API endpoints...")
        print("1. Start the server: python manage.py runserver")
        print("2. Login as patient")
        print("3. Go to Medical History page")
        print("4. Check Medications tab for prescriptions")
        print("5. Check Appointments tab for appointments")
        print("6. Verify that data is displayed correctly")

    except Exception as e:
        print(f"❌ Error in medical history test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_medical_history() 