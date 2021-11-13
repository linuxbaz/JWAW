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
def AbsentDetail_view(request, pk):
    absent = models.Absent.objects.get(pk=pk)
    return render(request, 'attendant/absent_detail.html', absent)


class AbsenttListView(generic.DetailView):
    model = models.Absent
    template_name = "attendant/students_detail.html"


def StudentListLevel_view(request):
    list = models.Student.objects.filter(student_level=10)
    dict = {'student_list_level': list}
    return render(request, 'attendant/students_list_with_level.html', dict)


def RegNewAbsent_view(request, student_id):
    #Register New Absent Date for the Student
    std = models.Student.objects.get(pk=student_id)
    if request.method == 'POST':
        form = AbsentForm(request.POST)

        absent_object = models.Absent()
        absent_object.absent_date = form.absent_date
        absent_object.absent_type = form.absent_type
        absent_object.save()
        return HttpResponseRedirect(reverse('rstudent_10'))
    else:
        form = AbsentForm()
    return render(request, 'attendant/absent_form.html', {'form': form, 'id': student_id})


def NewAbsent_view(request, pk):

    std = models.Student.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AbsentForm(request.POST)
        # check whether it's valid:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AbsentForm()

    return render(request, 'ceate_absent.html', {'form': form})


class newAbsent(FormView):
    form_class = AbsentForm
    success_url = "/"
    template_name = "attendant/absent_form.html"

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
