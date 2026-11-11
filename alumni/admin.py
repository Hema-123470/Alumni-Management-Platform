from django.contrib import admin
from .models import AlumniProfile


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'batch_year', 'department', 'current_company', 'city', 'updated_at']
    list_filter   = ['batch_year', 'department', 'country']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'current_company', 'skills']
    ordering      = ['-updated_at']
