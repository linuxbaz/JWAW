from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import ModelForm
from .models import *


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class Sent_to_parent_Form(forms.Form):
    btn = forms.CharField()


class AbsentForm(ModelForm):
    student = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(AbsentForm, self).__init__(*args, **kwargs)

        self.fields['absent_type'].required = True
        self.fields['absent_date'].required = True


    class Meta:
        model = Absent
        fields = ['absent_type', 'absent_date']
        widgets = {
            'absent_date': DateInput(),
        }
