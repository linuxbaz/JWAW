from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.views import generic
from django.shortcuts import render
# Create your views here.


# Create your views here.


class Index(TemplateView):

    template_name = "attendant/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_student'] = models.Absent.objects.all().count()
        return context


class StudentListView(generic.ListView):
    model = models.Student
    template_name = "attendant/students_list.html"


def StdDetail_view(request, pk):
    try:
        std = models.Student.objects.get(pk=pk)
    except models.Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'attendant/student_detail.html', {'std': std})


class AbsenttListView(generic.DetailView):
    model = models.Absent
    template_name = "attendant/students_detail.html"
