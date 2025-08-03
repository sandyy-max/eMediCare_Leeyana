#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from userauth.models import User

def test_medical_info():
    print("🏥 Testing Medical Info Endpoint...")
    
    # Get the first patient
    patient = User.objects.filter(role='patient').first()
    if not patient:
        print("❌ No patient found. Please create a patient user first.")
        return
    
    print(f"✅ Using patient: {patient.full_name}")
    
    # Test updating medical info
    print("\n📝 Testing medical info update...")
    
    # Update some medical fields
    patient.allergies = "Penicillin, Peanuts"
    patient.chronic_conditions = "Hypertension, Type 2 Diabetes"
    patient.current_medications = "Metformin 500mg daily, Lisinopril 10mg daily"
    patient.surgeries = "Appendectomy (2015), Knee surgery (2018)"
    patient.blood_group = "A+"
    patient.emergency_contact = "John Doe"
    patient.emergency_phone = "9876543210"
    patient.height = "170"
    patient.weight = "75"
    patient.blood_pressure = "120/80"
    patient.diabetes_status = "Controlled"
    patient.smoking_status = "Non-smoker"
    patient.alcohol_consumption = "Occasional"
    patient.family_history = "Father: Heart disease, Mother: Diabetes"
    patient.lifestyle_info = "Regular exercise, balanced diet"
    
    patient.save()
    
    print("✅ Medical info updated successfully!")
    
    # Display the updated info
    print(f"\n📋 Medical Info for {patient.full_name}:")
    print(f"- Blood Group: {patient.blood_group}")
    print(f"- Allergies: {patient.allergies}")
    print(f"- Chronic Conditions: {patient.chronic_conditions}")
    print(f"- Current Medications: {patient.current_medications}")
    print(f"- Surgeries: {patient.surgeries}")
    print(f"- Emergency Contact: {patient.emergency_contact}")
    print(f"- Emergency Phone: {patient.emergency_phone}")
    print(f"- Height: {patient.height} cm")
    print(f"- Weight: {patient.weight} kg")
    print(f"- Blood Pressure: {patient.blood_pressure}")
    print(f"- Diabetes Status: {patient.diabetes_status}")
    print(f"- Smoking Status: {patient.smoking_status}")
    print(f"- Alcohol Consumption: {patient.alcohol_consumption}")
    print(f"- Family History: {patient.family_history}")
    print(f"- Lifestyle Info: {patient.lifestyle_info}")
    
    print("\n🔍 Testing API endpoints...")
    print("1. Start the server: python manage.py runserver")
    print("2. Login as patient")
    print("3. Go to Profile page")
    print("4. Click on Medical Info tab")
    print("5. Verify all fields are populated")
    print("6. Try updating the medical information")
    print("7. Check that changes are saved")

if __name__ == "__main__":
    test_medical_info() 