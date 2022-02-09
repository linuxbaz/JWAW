from django.contrib import admin
from attendant import models

admin.site.register(models.Like)


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id',  'studyfield_code', 'studyfield_name', 'parent_mobile',
                    'student_level', 'student_name', 'school')

    fieldsets = (
        (None, {
            'fields': ('id', 'studyfield_code', 'studyfield_name', 'parent_mobile',
                       'student_level', 'student_name', 'school')
        }),
    )


@admin.register(models.Absent)
class AbsentAdmin(admin.ModelAdmin):
    model = models.Absent
    list_display = ('student', 'absent_type',
                    'absent_date', 'sent', 'course')

    fieldsets = (
        (None, {
            'fields': ('student', 'absent_type', 'absent_date', 'sent', 'course')
        }),
    )


@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    model = models.School


@admin.register(models.Course)
class SchoolAdmin(admin.ModelAdmin):
    model = models.Course
