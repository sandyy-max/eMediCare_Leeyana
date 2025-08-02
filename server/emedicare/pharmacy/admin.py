from django.contrib import admin
from .models import Medicine, Prescription, MedicineRequest

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock', 'price']
    search_fields = ['name']
    list_editable = ['stock', 'price']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'uploaded_at']
    search_fields = ['patient__phone_number']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']

@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'medicine_name', 'quantity', 'urgency', 'status', 'requested_at']
    list_filter = ['status', 'urgency', 'form_type']
    search_fields = ['patient_name', 'medicine_name', 'contact_number']
    readonly_fields = ['requested_at', 'updated_at']
    list_editable = ['status']
    actions = ['approve_requests', 'deny_requests', 'mark_completed']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'patient_name', 'contact_number', 'patient_age')
        }),
        ('Medicine Information', {
            'fields': ('medicine_name', 'dosage', 'quantity', 'form_type')
        }),
        ('Request Details', {
            'fields': ('urgency', 'doctor_name', 'medical_condition', 'allergies', 'additional_notes')
        }),
        ('Admin Management', {
            'fields': ('status', 'admin_notes', 'requested_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='Approve selected requests')
    def approve_requests(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Deny selected requests')
    def deny_requests(self, request, queryset):
        queryset.update(status='denied')
    
    @admin.action(description='Mark as completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
