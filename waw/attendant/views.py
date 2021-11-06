from django.shortcuts import render
from . import models

# Create your views here.
from django.views.generic.base import TemplateView


from django.http import HttpResponse


class Index(TemplateView):

    template_name = "attendant/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_student'] = models.Absent.objects.all().count()
        return context
