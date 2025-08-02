#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from package.models import HealthPackage

# Add the missing packages
packages_data = [
    {
        'name': 'Basic Health Check',
        'description': 'Essential health screening for adults',
        'price': 99.00,
        'duration_days': 3
    },
    {
        'name': 'Comprehensive Health Package',
        'description': 'Complete health assessment with detailed reports',
        'price': 199.00,
        'duration_days': 7
    },
    {
        'name': 'Premium Wellness Package',
        'description': 'Advanced screening with specialist consultation',
        'price': 299.00,
        'duration_days': 10
    }
]

for package_data in packages_data:
    package, created = HealthPackage.objects.get_or_create(
        name=package_data['name'],
        defaults=package_data
    )
    if created:
        print(f"Created package: {package.name}")
    else:
        print(f"Package already exists: {package.name}")

print("All packages added successfully!") 