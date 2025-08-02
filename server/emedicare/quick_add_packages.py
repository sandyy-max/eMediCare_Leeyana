import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from package.models import HealthPackage

# Add packages
packages = [
    {'name': 'Basic Health Check', 'description': 'Essential health screening for adults', 'price': 99.00, 'duration_days': 3},
    {'name': 'Comprehensive Health Package', 'description': 'Complete health assessment with detailed reports', 'price': 199.00, 'duration_days': 7},
    {'name': 'Premium Wellness Package', 'description': 'Advanced screening with specialist consultation', 'price': 299.00, 'duration_days': 10}
]

for p in packages:
    HealthPackage.objects.get_or_create(name=p['name'], defaults=p)
    print(f"Added: {p['name']}")

print("All packages added!") 