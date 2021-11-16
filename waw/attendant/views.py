from django.views.generic.edit import FormView
from .forms import NewAbsentForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .forms import AbsentForm
from . import date_conversion
from django.views import generic
from django.shortcuts import render, redirect

# Create your views here.


# Create your views here.


class Index(TemplateView):

    template_name = "attendant/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_student'] = models.Absent.objects.all().count()
        return context


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = models.Student
    template_name = "attendant/students_list.html"
    paginate_by = 10


@login_required()
def StdDetail_view(request, pk):
  #if student ID is fake handle it
    absent_date_list = []
    try:
        std = models.Student.objects.get(pk=pk)
        absent_list = list(models.Absent.objects.filter(
            student=pk).values_list('absent_type', 'absent_date'))
        dict = {'parent_mobile': std.parent_mobile,
                'absent_list': absent_list,
                'student_id': pk}
    except std.DoesNotExist:
        raise print("Student does not exist")
    return render(request, 'attendant/student_detail.html', dict)


@login_required()
def RegTodayAbsent_view (request, student_id):
  #if student ID is fake handle it
    absent_date_list = []
    try:
        std = models.Student.objects.get(pk=student_id)
        absent_list = list(models.Absent.objects.filter(
            student=student_id).values_list('absent_type', 'absent_date'))
        dict = {'parent_mobile': std.parent_mobile,
                'absent_list': absent_list,
                'student_id': student_id}
    except std.DoesNotExist:
        raise print("Student does not exist")
    return render(request, 'attendant/student_detail.html', dict)


@login_required()
def AbsentDetail_view(request, pk):
    absent = models.Absent.objects.get(pk=pk)
    return render(request, 'attendant/absent_detail.html', absent)


class AbsenttListView(generic.DetailView):
    model = models.Absent
    template_name = "attendant/students_detail.html"


def StudentListLevel_view(request, id=10):
    list = models.Student.objects.filter(student_level=id)
    dict = {'student_list_level': list}
    return render(request, 'attendant/students_list_with_level.html', dict)

class AbsentCreatView(generic.CreateView):
    model = models.Absent
    fields = ['student','absent_type','absent_date']
    template_name ='attendant/absent_form.html'
    success_url	= reverse_lazy('attendant/index')

def RegNewAbsent_view(request, student_id):
    #Register New Absent Date for the Student
    std = models.Student.objects.get(pk=student_id)
    if request.method == 'POST':
        form = AbsentForm(request.POST)

        new_absent = form.save(commit=False)
        new_absent.student = std
        new_absent.save()
        form.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        form = AbsentForm()
    return render(request, 'attendant/absent_form.html', {'form': form, 'id': id})
