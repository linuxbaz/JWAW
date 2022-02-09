from django.db import models
from django.urls import reverse
import os
#from .settings import BASE_DIR
from django.contrib.auth import get_user_model
User = get_user_model()

#Document_ROOT = os.path.join(BASE_DIR, 'media/document/')


absent_typy_choice = (('n', 'غیبت حضوری'), ('v', 'غیبت مجازی'), ('e', 'غیبت امتحان'), ('d', 'اخراج از کلاس'),
                      ('d', 'تاخیر در کلاس '), ('d', 'فرار از مدرسه'), ('d', 'بی انظباطی'))

level_choice = (('10', 'دهم'), ('11', 'یازدهم'), ('12', 'دوازدهم'))


class School(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    school_name = models.CharField(max_length=50)
    school_phone = models.CharField(max_length=30)
    school_address = models.CharField(max_length=100)
    studyfield_code_list = models.TextField(
        max_length=120, null=True, blank=True)
    studyfield_name_list = models.TextField(
        max_length=1024, null=True, blank=True)
    school_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    school_sms_api = models.CharField(max_length=120, null=True, blank=True)
    school_sms_username = models.CharField(
        max_length=30, null=True, blank=True)
    school_sms_password = models.CharField(
        max_length=30, null=True, blank=True)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('school_detail', args=[str(self.id)])


class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    school = school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    course_level = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.course_name

    def get_absolute_url(self):
        return reverse('school_detail', args=[str(self.id)])


class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True)
    studyfield_code = models.CharField(max_length=10, null=True, blank=True)
    studyfield_name = models.CharField(max_length=40, null=True, blank=True)
    input_date = models.DateField(null=True, blank=True)
    parent_mobile = models.CharField(max_length=11)
    student_level = models.CharField(
        max_length=2, choices=level_choice, blank=True, default='10')

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])


class Absent(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True)
    absent_date = models.DateField()
    sent = models.BooleanField(default=False)
    absent_type = models.CharField(
        max_length=1, choices=absent_typy_choice, blank=True, default='n')
    absent_detail = models.TextField(
        max_length=512, null=True, blank=True)

    def __str__(self):
        return str(self.absent_date)

    def get_absolute_url(self):
        return reverse('absent-detail', args=[str(self.absent_detail)])


class Like(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True)
    date_send = models.DateField(null=True, blank=True)


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
