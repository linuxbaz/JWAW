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


@login_required()
def StdDetail_view(request, pk):
  #if student ID is fake handle it
    absent_date_list = []
    try:
        std = models.Student.objects.get(pk=pk)
        absent_list = list(models.Absent.objects.filter(
            student=pk).values_list('absent_type', 'absent_date'))
        dict = {'parent_mobile': std.parent_mobile,
                'absent_list': absent_list}
    except std.DoesNotExist:
        raise print("Student does not exist")
    return render(request, 'attendant/student_detail.html', dict)


class AbsenttListView(generic.DetailView):
    model = models.Absent
    template_name = "attendant/students_detail.html"


def StudentListLevel_view(request):
    list = models.Student.objects.filter(student_level=10)
    dict = {'student_list_level': list}
    return render(request, 'attendant/students_list_with_level.html', dict)


class AbsentCreate(generic.CreateView):
    model = models.Absent
    form_class = AbsentForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewAbsentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewAbsentForm()

    return render(request, 'ceate_absent.html', {'form': form})


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
        error = 'not login'
        return render(request, 'attendant/login_error.html', {'error': error})
