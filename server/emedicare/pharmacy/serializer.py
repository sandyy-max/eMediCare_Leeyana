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
    prescription_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicineRequest
        fields = [
            'id', 'patient_name', 'contact_number', 'patient_age',
            'medicine_name', 'dosage', 'quantity', 'form_type',
            'urgency', 'doctor_name', 'medical_condition', 'allergies',
            'additional_notes', 'prescription_file', 'prescription_file_url',
            'status', 'requested_at', 'updated_at', 'admin_notes',
            'admin_comments', 'processed_by', 'processed_at'
        ]
        read_only_fields = ['patient', 'status', 'requested_at', 'updated_at', 'admin_notes', 'admin_comments', 'processed_by', 'processed_at']
    
    def get_prescription_file_url(self, obj):
        if obj.prescription_file:
            return self.context['request'].build_absolute_uri(obj.prescription_file.url)
        return None
    
    def create(self, validated_data):
        # Set the patient from the request user
        validated_data['patient'] = self.context['request'].user
        print(f"Creating medicine request with validated data: {validated_data}")
        try:
            result = super().create(validated_data)
            print(f"Medicine request created in serializer: {result}")
            return result
        except Exception as e:
            print(f"Error in serializer create method: {str(e)}")
            raise
    
    def validate_contact_number(self, value):
        # Basic phone number validation
        if not value or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid contact number")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    
    def validate_prescription_file(self, value):
        if value:
            # Check file size (5MB limit)
            if value.size > 5 * 1024 * 1024:  # 5MB
                raise serializers.ValidationError("File size must be less than 5MB")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only PNG and JPG files are allowed")
            
            # Check minimum size (10KB)
            if value.size < 10 * 1024:  # 10KB
                raise serializers.ValidationError("File size must be at least 10KB")
        
        return value


class MedicineRequestAdminSerializer(serializers.ModelSerializer):
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone_number', read_only=True)
    prescription_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicineRequest
        fields = [
            'id', 'patient_name', 'patient_email', 'patient_phone', 'contact_number', 'patient_age',
            'medicine_name', 'dosage', 'quantity', 'form_type', 'urgency', 'doctor_name', 
            'medical_condition', 'allergies', 'additional_notes', 'prescription_file', 'prescription_file_url',
            'status', 'requested_at', 'updated_at', 'admin_notes', 'admin_comments', 
            'processed_by', 'processed_at'
        ]
    
    def get_prescription_file_url(self, obj):
        if obj.prescription_file:
            return self.context['request'].build_absolute_uri(obj.prescription_file.url)
        return None
