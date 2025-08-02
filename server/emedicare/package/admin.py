# package/admin.py
from django.contrib import admin
from .models import HealthPackage, PackagePurchase

@admin.register(HealthPackage)
class HealthPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'created_at']
    list_filter = ['created_at', 'duration_days']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'description', 'price', 'duration_days')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

@admin.register(PackagePurchase)
class PackagePurchaseAdmin(admin.ModelAdmin):
    list_display = ['patient', 'package', 'selected_date', 'valid_until', 'payment_status']
    list_filter = ['payment_status', 'selected_date', 'purchased_at']
    search_fields = ['patient__full_name', 'package__name']
    readonly_fields = ['purchased_at', 'valid_until']
    
    fieldsets = (
        ('Purchase Information', {
            'fields': ('patient', 'package', 'selected_date', 'payment_status')
        }),
        ('Patient Details', {
            'fields': ('patient_details',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('purchased_at', 'valid_until'),
            'classes': ('collapse',)
        }),
    )
