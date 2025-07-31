from rest_framework import serializers
from .models import Medicine, Prescription, MedicineRequest

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'file', 'uploaded_at']

class MedicineRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineRequest
        fields = '__all__'
        read_only_fields = ['patient', 'status', 'requested_at']
