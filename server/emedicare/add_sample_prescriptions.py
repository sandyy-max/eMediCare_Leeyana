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

def create_sample_prescriptions():
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
        
        # Clear existing prescriptions for this patient
        Prescription.objects.filter(patient=patient).delete()
        print(f"Cleared existing prescriptions for {patient.full_name}")
        
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
        
        for prescription_data in prescriptions:
            prescription = Prescription.objects.create(**prescription_data)
            print(f"Created: {prescription}")
        
        print(f"\n✅ Created {len(prescriptions)} prescriptions successfully!")
        print(f"\nPrescription Details for {patient.full_name}:")
        for prescription in Prescription.objects.filter(patient=patient):
            print(f"- {prescription.diagnosis} (Prescribed: {prescription.prescribed_date})")
            print(f"  Doctor: {prescription.doctor.name}")
            print(f"  Medicines: {prescription.medicines[:50]}...")
            print()
            
    except Exception as e:
        print(f"❌ Error creating prescriptions: {e}")

if __name__ == "__main__":
    create_sample_prescriptions() 