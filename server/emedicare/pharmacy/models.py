from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='prescriptions/')

    def __str__(self):
        return f"{self.patient.phone_number} - {self.uploaded_at}"

class MedicineRequest(models.Model):
    URGENCY_CHOICES = [
        ('routine', 'Routine (3-5 days)'),
        ('urgent', 'Urgent (1-2 days)'),
        ('emergency', 'Emergency (Same day)'),
    ]
    
    FORM_TYPE_CHOICES = [
        ('tablets', 'Tablets'),
        ('capsules', 'Capsules'),
        ('liquid', 'Liquid/Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream/Ointment'),
        ('drops', 'Drops'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('completed', 'Completed'),
    ]
    
    # Patient Information
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicine_requests')
    patient_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    
    # Medicine Information
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES, blank=True)
    
    # Request Details
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='routine')
    doctor_name = models.CharField(max_length=150, blank=True)
    medical_condition = models.TextField()
    allergies = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    
    # Prescription File
    prescription_file = models.FileField(
        upload_to='prescriptions/medicine_requests/',
        blank=True,
        null=True,
        help_text='Upload prescription image (PNG, JPG only, max 5MB)'
    )
    
    # System Fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)
    admin_comments = models.TextField(blank=True, help_text='Comments from admin for approval/rejection')
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_requests'
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.medicine_name} ({self.status})"
    
    class Meta:
        ordering = ['-requested_at']
