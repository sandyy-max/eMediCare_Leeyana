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
    search_fields = ['patient__phone']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']

@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['patient', 'medicine', 'quantity', 'requested_at', 'status']
    list_filter = ['status']
    search_fields = ['patient__phone', 'medicine__name']
    actions = ['approve_requests', 'deny_requests']

    @admin.action(description='Approve selected requests')
    def approve_requests(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description='Deny selected requests')
    def deny_requests(self, request, queryset):
        queryset.update(status='denied')
