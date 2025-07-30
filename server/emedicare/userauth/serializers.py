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
        fields = ['phone_number', 'role', 'full_name', 'email', 'address', 'age', 'gender', 'department']
