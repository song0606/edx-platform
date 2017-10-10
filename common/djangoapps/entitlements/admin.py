from django.contrib import admin
from .models import CourseEntitlement


@admin.register(CourseEntitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ('user', 'root_course', 'enroll_end_date',
                    'mode', 'enrollment_course', 'is_active')
