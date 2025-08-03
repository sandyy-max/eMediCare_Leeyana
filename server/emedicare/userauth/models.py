from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, role='patient', **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(phone_number, password, role='admin', **extra_fields)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True, default='patient')

    # Common fields
    full_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Patient-specific
    address = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    
    # Medical Information
    allergies = models.TextField(blank=True, null=True, help_text="List of allergies")
    chronic_conditions = models.TextField(blank=True, null=True, help_text="Current medical conditions")
    current_medications = models.TextField(blank=True, null=True, help_text="Current medications being taken")
    surgeries = models.TextField(blank=True, null=True, help_text="Previous surgeries")
    emergency_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Emergency contact phone number")
    height = models.CharField(max_length=10, blank=True, null=True, help_text="Height in cm")
    weight = models.CharField(max_length=10, blank=True, null=True, help_text="Weight in kg")
    blood_pressure = models.CharField(max_length=20, blank=True, null=True, help_text="Blood pressure reading")
    diabetes_status = models.CharField(max_length=20, blank=True, null=True, help_text="Diabetes status")
    smoking_status = models.CharField(max_length=20, blank=True, null=True, help_text="Smoking status")
    alcohol_consumption = models.CharField(max_length=20, blank=True, null=True, help_text="Alcohol consumption status")
    family_history = models.TextField(blank=True, null=True, help_text="Family medical history")
    lifestyle_info = models.TextField(blank=True, null=True, help_text="Lifestyle information")

    # Doctor-specific
    department = models.CharField(max_length=100, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name if self.full_name else self.phone_number
