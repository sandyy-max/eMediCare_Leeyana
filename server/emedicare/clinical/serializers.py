from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'medicines', 'prescribed_date', 'reminder_time', 'reminder_start_date', 'reminder_end_date']
        read_only_fields = ['prescribed_date']
