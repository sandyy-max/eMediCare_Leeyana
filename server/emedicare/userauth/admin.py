from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

# Custom UserCreationForm for the admin add user page
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'full_name', 'email', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Custom UserChangeForm for editing users in admin
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'full_name', 'email', 'role', 'address', 'age', 'gender', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ['phone_number']
    list_display = ['phone_number', 'full_name', 'email', 'role', 'blood_group', 'is_staff']
    search_fields = ['phone_number', 'full_name', 'email']
    list_filter = ['is_staff', 'role']

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'address', 'age', 'gender', 'role')}),
        ('Medical Information', {'fields': ('blood_group', 'allergies', 'chronic_conditions', 'current_medications', 'surgeries', 'emergency_contact', 'emergency_phone', 'height', 'weight', 'blood_pressure', 'diabetes_status', 'smoking_status', 'alcohol_consumption', 'family_history', 'lifestyle_info')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'email', 'role', 'password1', 'password2', 'is_staff'),
        }),
    )

admin.site.register(User, UserAdmin)
