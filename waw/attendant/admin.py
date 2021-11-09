from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_mobile', 'input_date', 'student_level')

    fieldsets = (
        (None, {
            'fields': ('parent_mobile', 'id', 'input_date', 'student_level')
        }),
    )


@admin.register(models.Absent)
class AbsentAdmin(admin.ModelAdmin):
    model = models.Absent
    list_display = ('student', 'absent_type', 'absent_date')

    fieldsets = (
        (None, {
            'fields': ('student', 'absent_type', 'absent_date')
        }),
    )
