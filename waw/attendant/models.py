from django.db import models
import uuid  # Required for unique book instances
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Student(models.Model):
    """
    Model representing a student (but not a specific copy of a student).
    """
    id = models.CharField(primary_key=True, max_length=10)
    input_date = models.DateField(null=True, blank=True)
    parent_mobile = models.CharField(max_length=11)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('student-detail', args=[str(self.id)])


class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    absent_date = models.DateField()
    ABSENT_TYPE = (
                    ('n', 'Normal'),
                    ('v', 'Virtual'),
                    ('e', 'Exam')
                    )
    absent_type = models.CharField(
                                    max_length=1, choices=ABSENT_TYPE, blank=True, default='N')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return reverse('absent-detail', args=[str(self.absent_type)])
