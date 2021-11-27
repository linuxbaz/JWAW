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


absent_type_help_text = {'n': 'حضوری',
                         'v': 'مجازی', 'e': 'امتحان', 'd': 'اخراج از کلاس'}


class Index(TemplateView):

    template_name = "attendant/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        n_absent = models.Absent.objects.all().count()
        n_student = models.Student.objects.all().count()
        percent_absent = int((n_absent / (n_student * 50))*100)
        context = {'number_student': n_student,
                   'percent_absent': percent_absent}
        return context


@ login_required()
def StudentListView(request):
    students_list = []
    if request.user.groups.filter(name='admins').exists():
        students_list = list(models.Student.objects.all())
    else:
        txt = str(request.user.get_username)
        uname = txt[61:71]
        students_list = list(models.Student.objects.filter(id=uname))
    dict = {'students_list': students_list}
    return render(request, 'attendant/students_list.html', dict)


@ login_required()
def StdDetail_view(request, pk):
  #if student ID is fake handle it
    absent_tuple_info = ()
    counter = 0

    try:
        std = models.Student.objects.get(pk=pk)
        absents = list(models.Absent.objects.filter(student=pk))

        absent_tuple_info = date_conversion.to_persion_date(absents)

        dict = {'parent_mobile': std.parent_mobile,
                'absent_tuple_info': absent_tuple_info,
                'len': len(absent_tuple_info),
                'student_id': pk,
                'absent_type_help_text': absent_type_help_text}
    except std.DoesNotExist:
        raise print("Student does not exist")
    return render(request, 'attendant/student_detail.html', dict)


@login_required()
@permission_required('attendant.can_add_absent', raise_exception=True)
def Absent_today_View(request, today=datetime.date.today()):

    today_list = models.Absent.objects.filter(
        absent_date=today)
    yesterday_list = models.Absent.objects.filter(
        absent_date=today - datetime.timedelta(days=1))
    absents = models.Absent.objects.all()
    absent_tuple_info = date_conversion.to_persion_date(absents)

    x = datetime.datetime.now()
    present = date_conversion.gregorian_to_jalali(x.year, x.month, x.day)

    test_button_name = 'No'
    #Save parent_phone to a list for sending SMS
    phones = []
    if today_list:
        for p in today_list:
            phones.append(p.student.parent_mobile)
    if request.method == 'POST':
        form = AbsentForm(request.POST)
        test_button_name = str((request.POST).keys())[35]
        index = int(test_button_name)
        number = phones[index-1]

        payload = {'Username': 'jaberedu', 'Password': '65361000',
                   'From': '-1', 'To':  number, 'Text': 'test message'}
        r = requests.post(
            'https://www.payam-resan.com/APISend.aspx', params=payload)
        return render(request, 'attendant/sms_result.html', {'phone': phones, 'result': r, 'test': test_button_name})
    else:
        dict = {'absent_today_list': today_list,
                'absent_yesterday_list': yesterday_list,
                'absent_type_help_text': absent_type_help_text,
                'absent_tuple_info': absent_tuple_info,
                'len': len(absent_tuple_info),
                'today_is': present}
        return render(request, 'attendant/absent_detail.html', dict)


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


@login_required()
def userprofile_view(request):
    return render(request, 'attendant/test.html', {'parents': 'parents'})
