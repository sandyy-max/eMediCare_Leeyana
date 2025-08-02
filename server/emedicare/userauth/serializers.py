from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'full_name', 'email', 'address', 'age', 'gender']
        extra_kwargs = {
            'email': {'required': False},
        }

    def validate(self, attrs):
        # Assume role='patient' for registration
        required_fields = ['full_name', 'address', 'age', 'gender']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: f"{field} is required for patients."})
        return attrs

    def create(self, validated_data):
        # Force role='patient' on creation
        validated_data['role'] = 'patient'
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'role', 'full_name', 'email', 'address', 'age', 'gender', 'blood_group', 'emergency_contact', 'department']
        read_only_fields = ['phone_number', 'role']  # These cannot be changed by users

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    
    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
