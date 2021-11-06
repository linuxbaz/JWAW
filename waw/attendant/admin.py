from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Student)
class StadentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_mobile', 'input_date')

    fieldsets = (
        (None, {
            'fields': ('parent_mobile', 'id', 'input_date')
        }),
    )


@admin.register(models.Absent)
class AbsentAdmin(admin.ModelAdmin):
    model = models.Absent
