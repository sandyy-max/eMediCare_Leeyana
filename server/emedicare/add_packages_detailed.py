#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from package.models import HealthPackage

def create_packages():
    # Clear existing packages
    HealthPackage.objects.all().delete()
    print("Cleared existing packages")
    
    # Create Cardiology Package
    cardiology_package = HealthPackage.objects.create(
        name="Cardiology Package",
        description="Comprehensive cardiac health screening with advanced diagnostics and expert cardiologist consultation. Includes ECG, echocardiogram, stress test, and detailed cardiac markers analysis.",
        price=28000.00,
        duration_days=3
    )
    print(f"Created: {cardiology_package.name} - NPR {cardiology_package.price}")
    
    # Create Pulmonology Package
    pulmonology_package = HealthPackage.objects.create(
        name="Pulmonology Package",
        description="Complete respiratory health assessment with lung function tests and pulmonologist evaluation. Includes spirometry, chest X-ray, arterial blood gas analysis, and allergy testing.",
        price=25200.00,
        duration_days=3
    )
    print(f"Created: {pulmonology_package.name} - NPR {pulmonology_package.price}")
    
    # Create Premium Wellness Package
    premium_package = HealthPackage.objects.create(
        name="Premium Wellness Package",
        description="Ultimate health assessment with comprehensive diagnostics, cancer screening, and personalized wellness plan. Includes all basic tests plus advanced screening, specialist consultations, and nutritionist session.",
        price=49000.00,
        duration_days=5
    )
    print(f"Created: {premium_package.name} - NPR {premium_package.price}")
    
    print("\n✅ All packages created successfully!")
    print("\nPackage Details:")
    print("1. Cardiology Package: NPR 28,000 (30% off from NPR 40,000)")
    print("2. Pulmonology Package: NPR 25,200 (30% off from NPR 36,000)")
    print("3. Premium Wellness Package: NPR 49,000 (30% off from NPR 70,000)")
    
    # Verify packages in database
    all_packages = HealthPackage.objects.all()
    print(f"\nTotal packages in database: {all_packages.count()}")
    for package in all_packages:
        print(f"- {package.name}: NPR {package.price}")

if __name__ == "__main__":
    create_packages() 