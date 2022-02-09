from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('student/<pk>', views.StdDetail_view, name='student-detail'),
    path('todayAbsent', views.Absent_today_View, name='todayAbsent'),
    path('reg_today_absent/<student_id>',
         views.RegNewAbsent_view, name='reg_today_absent'),
    path('upfile/', views.upfile_view, name='upfile'),
    path('students_list/<base>', views.StudentListView, name='StudentListView'),
    path('profile/', views.userprofile_view, name='userprofile'),
    path('likestudent/', views.likeStudent, name='likestudent'),
    path('userdata/', views.userdata, name='userdata')
    # Restful API


]
