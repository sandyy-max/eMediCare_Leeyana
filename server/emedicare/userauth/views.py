from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, PasswordChangeSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                phone_number=serializer.validated_data['phone_number'],
                password=serializer.validated_data['password']
            )
            if user:
                tokens = get_tokens(user)
                return Response({"message": "Login successful", "tokens": tokens})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        print(f"PUT request data: {request.data}")
        print(f"Content-Type: {request.content_type}")
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicalInfoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def get(self, request):
        """Get user's medical information"""
        user = request.user
        medical_info = {
            'blood_group': getattr(user, 'blood_group', ''),
            'allergies': getattr(user, 'allergies', ''),
            'chronic_conditions': getattr(user, 'chronic_conditions', ''),
            'current_medications': getattr(user, 'current_medications', ''),
            'emergency_contact': getattr(user, 'emergency_contact', ''),
            'emergency_phone': getattr(user, 'emergency_phone', ''),
            'height': getattr(user, 'height', ''),
            'weight': getattr(user, 'weight', ''),
            'blood_pressure': getattr(user, 'blood_pressure', ''),
            'diabetes_status': getattr(user, 'diabetes_status', ''),
            'smoking_status': getattr(user, 'smoking_status', ''),
            'alcohol_consumption': getattr(user, 'alcohol_consumption', ''),
            'family_history': getattr(user, 'family_history', ''),
            'lifestyle_info': getattr(user, 'lifestyle_info', ''),
            'surgeries': getattr(user, 'surgeries', ''),
        }
        return Response(medical_info, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user's medical information"""
        user = request.user
        data = request.data
        
        # Update medical fields
        medical_fields = [
            'blood_group', 'allergies', 'chronic_conditions', 'current_medications',
            'emergency_contact', 'emergency_phone', 'height', 'weight', 'blood_pressure',
            'diabetes_status', 'smoking_status', 'alcohol_consumption', 'family_history',
            'lifestyle_info', 'surgeries'
        ]
        
        updated_fields = []
        for field in medical_fields:
            if field in data:
                setattr(user, field, data[field])
                updated_fields.append(field)
        
        if updated_fields:
            user.save()
            return Response({
                "message": "Medical information updated successfully",
                "updated_fields": updated_fields
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "No medical information provided for update"
            }, status=status.HTTP_400_BAD_REQUEST)

