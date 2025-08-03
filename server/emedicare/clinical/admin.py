from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'diagnosis', 'prescribed_date', 'reminder_time']
    list_filter = ['prescribed_date', 'doctor__department', 'reminder_start_date']
    search_fields = ['patient__full_name', 'diagnosis', 'medicines']
    readonly_fields = ['prescribed_date']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'doctor')
        }),
        ('Medical Information', {
            'fields': ('diagnosis', 'medicines')
        }),
        ('Prescription Details', {
            'fields': ('prescribed_date', 'reminder_time', 'reminder_start_date', 'reminder_end_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new prescriptions
            # Ensure the prescription is properly linked
            obj.patient = obj.patient  # Ensure patient is set
            obj.doctor = obj.doctor    # Ensure doctor is set
        super().save_model(request, obj, form, change)
