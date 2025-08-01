#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emedicare.settings')
django.setup()

from pharmacy.models import Medicine

# Sample medicines data
medicines_data = [
    {
        'name': 'Paracetamol 500mg',
        'description': 'Pain relief and fever reducer. Safe for adults and children over 6 years.',
        'stock': 50,
        'price': 5.99
    },
    {
        'name': 'Amoxicillin 250mg',
        'description': 'Broad-spectrum antibiotic for bacterial infections',
        'stock': 30,
        'price': 12.50
    },
    {
        'name': 'Vitamin D3 1000IU',
        'description': 'Essential vitamin D supplement for bone health',
        'stock': 8,
        'price': 8.75
    },
    {
        'name': 'Metformin 500mg',
        'description': 'First-line treatment for type 2 diabetes',
        'stock': 25,
        'price': 15.20
    },
    {
        'name': 'Lisinopril 10mg',
        'description': 'ACE inhibitor for high blood pressure and heart failure',
        'stock': 40,
        'price': 18.99
    },
    {
        'name': 'Hydrocortisone Cream 1%',
        'description': 'Topical corticosteroid for skin inflammation and itching',
        'stock': 15,
        'price': 6.45
    }
]

def add_medicines():
    print("Adding sample medicines to database...")
    
    for medicine_data in medicines_data:
        medicine, created = Medicine.objects.get_or_create(
            name=medicine_data['name'],
            defaults=medicine_data
        )
        if created:
            print(f"Added: {medicine.name}")
        else:
            print(f"Already exists: {medicine.name}")
    
    print("Sample medicines added successfully!")

if __name__ == '__main__':
    add_medicines() 