from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    is_manager = models.BooleanField(
        _('manager status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_parent = models.BooleanField(
        _('parent status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
