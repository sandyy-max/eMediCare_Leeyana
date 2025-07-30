from django import forms
from django.contrib import admin
from .models import Appointment, Confirmation, Doctor

class ConfirmationAdminForm(forms.ModelForm):
    class Meta:
        model = Confirmation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter Appointment dropdown to only unconfirmed ones
        self.fields['appointment'].queryset = Appointment.objects.filter(is_confirmed=False)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'created_at', 'is_confirmed']
    list_filter = ['is_confirmed', 'department']
    search_fields = ['full_name', 'phone_number', 'email']

@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    form = ConfirmationAdminForm  # Use the custom form here

    list_display = ['appointment', 'doctor', 'appointment_date', 'appointment_time']
    list_filter = ['appointment_date', 'doctor__department']
    search_fields = ['appointment__full_name', 'doctor__name']
