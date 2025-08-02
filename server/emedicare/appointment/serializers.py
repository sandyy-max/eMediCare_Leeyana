from rest_framework import serializers
from .models import Appointment, Confirmation, Doctor
from datetime import timedelta


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'department', 'available_days', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'full_name', 'phone_number', 'email', 'department', 'dob', 'symptoms', 'created_at']
        read_only_fields = ['created_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['patient', 'is_confirmed', 'created_at']

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)


class ConfirmationSerializer(serializers.ModelSerializer):
    appointment_details = AppointmentSerializer(source='appointment', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = Confirmation
        fields = [
            'id', 'appointment', 'doctor', 'appointment_date', 'appointment_time',
            'appointment_details', 'doctor_name'
        ]

    def validate(self, data):
        doctor = data['doctor']
        date_ = data['appointment_date']
        time_ = data['appointment_time']

        # Doctor not available that weekday?
        weekday = date_.strftime('%A')
        if doctor.available_days and weekday not in doctor.available_days:
            raise serializers.ValidationError(f"Doctor is not available on {weekday}.")

        # Conflict check
        if Confirmation.objects.filter(
            doctor=doctor,
            appointment_date=date_,
            appointment_time=time_
        ).exists():
            raise serializers.ValidationError("This doctor already has an appointment at this date and time.")

        return data


class PatientAppointmentHistorySerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'department', 'created_at', 'is_confirmed', 'full_name', 'doctor']

    def get_doctor(self, obj):
        if hasattr(obj, 'confirmation'):
            return obj.confirmation.doctor.name
        return None
