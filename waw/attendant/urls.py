from django.urls import path

from . import views


#all pattern
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('students_list/', views.StudentListView.as_view(), name='StudentListView'),
    path('student/<pk>', views.StdDetail_view,
         name='student-detail'),
    path('Absent/<pk>', views.AbsentDetail_view,
         name='absent-detail'),
    #path('student_10/<id>', views.StudentListLevel_view),
    path('regabsent/<student_id>',
         views.newAbsent.as_view(), name='regabsent'),
    path('reg_today_absent/<student_id>', views.RegNewAbsent_view, name = 'reg_today_absent'),
    path('students_list/', views.StudentListView.as_view(), name='StudentListView'),
    path('regtodayabsent/', views.AbsentCreatView.as_view(), name='AbsentCreatView'),
    ]
