from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.
from django.forms import ModelForm
from .models import *

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    
class DateInput(forms.DateInput):
    input_type = 'date'


class AbsentForm(ModelForm):
    student = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Absent
        fields = ['absent_type', 'absent_date']
        widgets = {
            'absent_date': DateInput(),
        }


class NewAbsentForm(forms.Form):
    absent_type = forms.CharField(help_text="نوع کلاس :")
    absent_date = forms.DateField(help_text="تاریخ غیبت :")
