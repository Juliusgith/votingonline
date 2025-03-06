# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VerificationCode

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'registration_number', 'faculty', 'is_verified', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'registration_number')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Voting info', {'fields': ('registration_number', 'faculty', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'registration_number', 'faculty', 'password1', 'password2'),
        }),
    )

class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')
    search_fields = ('user__username', 'user__email', 'code')
    list_filter = ('is_used', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)