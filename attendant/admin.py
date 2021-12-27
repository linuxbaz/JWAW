from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.


admin.site.register(models.Like)


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id',  'studyfield_code', 'studyfield_name', 'parent_mobile', 'input_date',
                    'student_level', 'student_name', 'school')

    fieldsets = (
        (None, {
            'fields': ('id', 'studyfield_code', 'studyfield_name', 'parent_mobile', 'input_date',
                       'student_level', 'student_name', 'school')
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
class SchoolAdmin(admin.ModelAdmin):
    model = models.School
