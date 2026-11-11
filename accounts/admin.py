from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser."""

    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_approved', 'date_joined']
    list_filter = ['role', 'is_approved', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Alumni Info', {
            'fields': ('role', 'is_approved', 'phone'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Alumni Info', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'is_approved', 'phone'),
        }),
    )

    actions = ['approve_selected_users']

    def approve_selected_users(self, request, queryset):
        updated = queryset.filter(role=CustomUser.Role.ALUMNI).update(is_approved=True)
        self.message_user(request, f'{updated} alumni account(s) approved.')
    approve_selected_users.short_description = 'Approve selected alumni accounts'
