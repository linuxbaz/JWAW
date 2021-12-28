from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
import requests
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import simplejson as json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from .forms import AbsentForm, DocumentForm, Sent_to_parent_Form
from . import date_conversion
from django.views import generic
from django.shortcuts import render, redirect
from django.template import RequestContext
from rest_framework import viewsets
from .serializers import StudentSerializer
from rest_framework import generics, permissions

# Create Restful View here.

# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from rest_framework import status
# from django.contrib import messages
#
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserSerializer
# from django.contrib.auth.models import User

#test


# class UserCreate(APIView):
#     """
#     Creates the user.
#     """
#
#     def post(self, request, format='json'):
#         return Response('hello')
#
#
# class UserCreate(APIView):
#     """
#     Creates the user.
#     """
#
#     def post(self, request, format='json'):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentView(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer


# Create your views here.
today = datetime.date.today()
absent_type_help_text = {
                            'n': 'غیبت حضوری',
                            'v': 'غیبت مجازی',
                            'e': 'غیبت امتحان',
                            'd': 'اخراج از کلاس',
                            'd': 'تاخیر در کلاس ',
                            'd': 'فرار از مدرسه',
                            'd': 'بی انظباطی',
                            }


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += str(ele)

    # return string
    return str1


def get_user_group(request):
    if request.user.groups.filter(name='managers').exists():
        group = 'managers'
    else:
        group = 'parents'
    return group

#Get name and school's student from user who logins


def get_info_of__school(request):
    id_list = []  # students whobelong to the specified school
    uid = request.user.id
    school_id = models.School.objects.filter(school_admin=uid)[0]
    school_name = models.School.objects.filter(
        id=school_id).values_list('school_name')[0]
    school_study_code_list = models.School.objects.filter(
        id=school_id).values_list('studyfield_code_list')[0]
    school_study_name_list = models.School.objects.filter(
        id=school_id).values_list('studyfield_name_list')[0]
    students_list = models.Student.objects.filter(school_id=school_id)
    for std in students_list:
        id_list.append(std.id)
    school_info = {'id_list': id_list, 'school_name': school_name,
                   'school_study_code_list': school_study_code_list,
                   'school_study_name_list': school_study_name_list,
                   }
    return school_info


@login_required
def Index(request):
    if (get_user_group(request) == 'managers'):
        context = {}
        school_info = get_info_of__school(request)
        n_absent = models.Absent.objects.all().filter(
            student__in=school_info['id_list']).count()
        n_student = models.Student.objects.all().filter(
            id__in=school_info['id_list']).count()
        percent_absent = int((n_absent / (n_student * 50))*100)
        context = {'number_student': n_student,
                   'percent_absent': percent_absent,
                   'school_name': school_info['school_name'][0]}
    else:
        context = {'error': 'لطفا با نام کاربری وارد شوید'}
    return render(request, 'attendant/index.html', context)


@ login_required()
def StudentListView(request, base=0):
    students_list = []
    if (get_user_group(request) == 'managers'):
        school_info = get_info_of__school(request)
    # Make List studyfields of School by converting string to list
        str_studycode_tuple = ''.join(
            school_info['school_study_code_list'][0])

        str = '['+str_studycode_tuple+']'
        jsonDec = json.decoder.JSONDecoder()
        StudyFieldCode_list = jsonDec.decode(str)
        StudyFieldName_list = (
            school_info['school_study_name_list'][0]).split(",")
        # Pair of code and name of field Convert to a dictionary.
        zip_iterator = zip(StudyFieldCode_list, StudyFieldName_list)
        dict_studyfields = dict(zip_iterator)
    # If the manager go to filters
        if request.method == 'POST':
            filter_field = (request.POST['filter_field'])
            filter_base = (request.POST['filter_base'])
            students_list = models.Student.objects.filter(
                id__in=school_info['id_list']).filter(
                    student_level=filter_base).filter(
                    studyfield_code=filter_field)

        else:  # all Student are listed for by base 0
            if base == '0':
                students_list = models.Student.objects.filter(
                    id__in=school_info['id_list'])
            else:  # If linke base in html page clicked
                students_list = models.Student.objects.filter(
                    id__in=school_info['id_list']).filter(student_level=base)
    else:
        #Parents username is p plus ID that p is deleted to set the ID
        uname = request.user.username[1:11]
        students_list = list(models.Student.objects.filter(id=uname))
    context = {'students_list': students_list,
               'fieldcode_list': dict_studyfields
               }
    return render(request, 'attendant/students_list.html', context)


@ login_required()
def StdDetail_view(request, pk):
  #if student ID is fake handle it
    absent_tuple_info = ()
    dict = {}
    counter = 0

    std = models.Student.objects.get(pk=pk)

    absents = list(models.Absent.objects.filter(student=pk))
    if absents:
        absent_tuple_info = date_conversion.to_persion_date(absents)
    dict = {'parent_mobile': std.parent_mobile,
            'absent_tuple_info': absent_tuple_info,
            'len': len(absent_tuple_info),
            'student_id': pk,
            'absent_type_help_text': absent_type_help_text}
    return render(request, 'attendant/student_detail.html', dict)


"""
    Report for absent
"""


@login_required()
def Absent_today_View(request):
    yesterday = today - datetime.timedelta(days=1)
    absent_tuple_info = ()

    #Go to specific school with find school_id value
    if (get_user_group(request) == 'managers'):
        school_info = get_info_of__school(request)

    today_list = models.Absent.objects.filter(
        absent_date=today).filter(student__in=school_info['id_list']).filter(sent=False)

    yesterday_list = models.Absent.objects.filter(
        absent_date=yesterday).filter(student__in=school_info['id_list'])

    all_days = models.Absent.objects.all().filter(
        student__in=school_info['id_list'])
    absent_tuple_info = date_conversion.to_persion_date(all_days)

    x = datetime.datetime.now()
    present = date_conversion.gregorian_to_jalali(x.year, x.month, x.day)

    test_button_name = 'No'
    #Save parent_phone to a list for sending SMS
    dict = {'absent_today_list': today_list,
            'absent_yesterday_list': yesterday_list,
            'absent_type_help_text': absent_type_help_text,
            'absent_tuple_info': absent_tuple_info,
            'len': len(absent_tuple_info),
            'today_is': present}
    return render(request, 'attendant/absent_detail.html', dict)


"""
    Send SMS to parent
"""


def likeStudent(request):
    if request.method == 'GET':
        data_text = request.GET['data_text']
        #convert to list that [0] is student_id and [1] is absent_id
        data_list = data_text.split(",")
        #Make prameters for SMS
        student_id = data_list[0]
        absent_id = data_list[1]
        x = datetime.datetime.now()
        perion_date = date_conversion.gregorian_to_jalali(
            x.year, x.month, x.day)

        absent_type = models.Absent.objects.filter(
            id=absent_id).values_list("absent_type")[0]
        #get absent_type for making SMS
        sms = "هنرستان جابر این حیان:سلام والدین گرامی "+"فرزند شما در تاریخ " + \
            listToString(perion_date)+" "+" " + \
            absent_type_help_text[absent_type[0]]+" "+" داشته است"

        likedstudent = models.Student.objects.get(
            pk=student_id)  # getting the liked student
        payload = {'Username': 'jaberedu', 'Password': '36318513',
                   'From': '-1', 'To':  likedstudent.parent_mobile, 'Text': sms}
        r = requests.post(
            'https://www.payam-resan.com/APISend.aspx', params=payload)
        # Creating Like Object
        m = models.Like(student=likedstudent, date_send=today)
        m.save()  # saving it to store in database

        #Flag sent of Absent object True
        m = models.Absent.objects.get(id=absent_id)
        m.sent = True
        m.save()
        # Sending an success response
        return HttpResponse(r)
    else:
        return HttpResponse("Request method is not a GET")

#list Student using Ajax in template


def LoadStudentFromBase(request):
    pass


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
