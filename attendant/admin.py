from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register(models.Like)


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_mobile', 'input_date',
                    'student_level', 'student_name', 'school')

    fieldsets = (
        (None, {
            'fields': ('parent_mobile', 'id', 'input_date', 'student_level',
                       'student_name', 'school')
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


@admin.register(models.School)
class AbsentAdmin(admin.ModelAdmin):
    model = models.Absent
    list_display = ('id', 'school_admin', 'school_name', 'school_address')

    fieldsets = (
        (None, {
            'fields': ('id', 'school_admin', 'school_name', 'school_address')
        }),
    )


@admin.register(models.Classroom)
class AbsentAdmin(admin.ModelAdmin):
    model = models.Absent
    list_display = ('school', 'id', 'classroom_name',
                    'classroom_field', 'classroom_level')

    fieldsets = (
        (None, {
            'fields': ('school', 'id', 'classroom_name', 'classroom_field', 'classroom_level')
        }),
    )
