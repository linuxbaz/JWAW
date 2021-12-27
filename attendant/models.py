from django.db import models
import uuid  # Required for unique book instances
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    absent_date = models.DateField()
    sent = models.BooleanField(default=False)
    ABSENT_TYPE = (
                    ('n', 'حضوری'),
                    ('v', 'مجازی'),
                    ('e', 'امتحان'),
                    ('d', 'اخراج از کلاس')
                    )
    absent_type = models.CharField(
                                    max_length=1, choices=ABSENT_TYPE, blank=True, default='n')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.absent_date)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('absent-detail', args=[str(self.absent_type)])


class test(models.Model):
    pass


class School(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    school_name = models.CharField(max_length=50)
    school_phone = models.CharField(max_length=30)
    school_address = models.CharField(max_length=100)
    # JSON-serialized (text) version of your list
    studyfield_code_list = models.TextField(
        max_length=120, null=True, blank=True)
    studyfield_name_list = models.TextField(
        max_length=1024, null=True, blank=True)
    school_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('school_detail', args=[str(self.id)])


class Student(models.Model):
    """
    Model representing a student (but not a specific copy of a student).
    """
    id = models.CharField(primary_key=True, max_length=10)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True)
    studyfield_code = models.CharField(max_length=10, null=True, blank=True)
    studyfield_name = models.CharField(max_length=40, null=True, blank=True)
    input_date = models.DateField(null=True, blank=True)
    parent_mobile = models.CharField(max_length=11)
    LEVEL = (
                    ('10', 'دهم'),
                    ('11', 'یازدهم'),
                    ('12', 'دوازدهم')
                    )
    student_level = models.CharField(
        max_length=2, choices=LEVEL, blank=True, default='10')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a particular student instance.
        """
        return reverse('student-detail', args=[str(self.id)])


class Like(models.Model):
    student = models.ForeignKey(
        'Student', on_delete=models.SET_NULL, null=True, blank=True)
    date_send = models.DateField(null=True, blank=True)


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
