from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
import requests
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .forms import AbsentForm, DocumentForm, Sent_to_parent_Form
from . import date_conversion
from django.views import generic
from django.shortcuts import render, redirect
from django.template import RequestContext

# Create your views here.


# Create your views here.


class Index(TemplateView):

    template_name = "attendant/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_student'] = models.Student.objects.all().count()
        return context


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = models.Student
    template_name = "attendant/students_list.html"
    paginate_by = 10


@login_required()
def StdDetail_view(request, pk):
  #if student ID is fake handle it
    absent_tuple_info = ((),)
    counter = 0
    try:
        std = models.Student.objects.get(pk=pk)
        absents = list(models.Absent.objects.filter(
            student=pk).values_list('absent_type', 'absent_date'))

        for absent_object in absents:
            counter += 1
            year = absent_object[1].strftime('%Y')
            month = absent_object[1].strftime('%m')
            day = absent_object[1].strftime('%d')
            #[dd,mm,dd]
            l = date_conversion.gregorian_to_jalali(
                int(year), int(month), int(day))
            A = [str(x) for x in l]
            str_date = " "
            str_date = str_date.join(A)
            #Save from the first of tuple instead of second place
            if counter == 1:
                absent_tuple_info = ((str_date, absent_object[0]),)
            else:
                absent_tuple_info += ((str_date, absent_object[0]),)

        dict = {'parent_mobile': std.parent_mobile,
                'absent_tuple_info': absent_tuple_info,
                'len': len(absent_tuple_info),
                'student_id': pk}
    except std.DoesNotExist:
        raise print("Student does not exist")
    return render(request, 'attendant/student_detail.html', dict)


@login_required()
def RegTodayAbsent_view(request, student_id):
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


class AbsentListlView(generic.ListView):

    model = models.Absent
    template_name = 'attendant/absent_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['absent_today_list'] = models.Absent.objects.all()
        #filter(absent_date=datetime.date.today())
        return context


@login_required()
def Absent_today_View(request, today=datetime.date.today()):
    today_list = models.Absent.objects.filter(absent_date=today)
    yesterday_list = models.Absent.objects.filter(
        absent_date=today - datetime.timedelta(days=1))
    #Save parent_phone to a list for sending SMS
    phones = []
    if today_list:
        for p in today_list:
            phones.append(p.student.parent_mobile)
    if request.method == 'POST':
        form = AbsentForm(request.POST)
        for number in phones:
            payload = {'Username': 'jaberedu', 'Password': '65361000',
                       'From': '-1', 'To':  number, 'Text': 'test message'}
            r = requests.post(
                'https://www.payam-resan.com/APISend.aspx', params=payload)
            return render(request, 'attendant/test.html', {'phone': phones,'result': r})
    else:
        dict = {'absent_today_list': today_list,
                'absent_yesterday_list': yesterday_list}
        return render(request, 'attendant/absent_detail.html', dict)


class AbsentCreatView(generic.CreateView):
    model = models.Absent
    fields = ['student', 'absent_type', 'absent_date']
    template_name = 'attendant/absent_form.html'
    success_url = reverse_lazy('attendant/index')


@login_required()
def RegNewAbsent_view(request, student_id):
    #Register New Absent Date for the Student
    std = models.Student.objects.get(pk=student_id)
    if request.method == 'POST':
        form = AbsentForm(request.POST)

        new_absent = form.save(commit=False)
        new_absent.student = std
        new_absent.save()
        form.save()

        return HttpResponseRedirect(reverse('student-detail', args=[str(student_id)]))
    else:
        form = AbsentForm()
    return render(request, 'attendant/absent_form.html', {'form': form, 'id': student_id})


def upfile_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = models.Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myapp.views.upfile'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = models.Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'attendant/upfile.html', {'documents': documents, 'form': form})
