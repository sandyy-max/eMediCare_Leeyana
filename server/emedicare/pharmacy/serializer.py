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
        fields = [
            'id', 'patient_name', 'contact_number', 'patient_age',
            'medicine_name', 'dosage', 'quantity', 'form_type',
            'urgency', 'doctor_name', 'medical_condition', 'allergies',
            'additional_notes', 'status', 'requested_at', 'updated_at',
            'admin_notes'
        ]
        read_only_fields = ['patient', 'status', 'requested_at', 'updated_at', 'admin_notes']
    
    def create(self, validated_data):
        # Set the patient from the request user
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_contact_number(self, value):
        # Basic phone number validation
        if not value or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid contact number")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
