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
    path('student_10/', views.StudentListLevel_view,
         name='student_10'),
    path('regabsent/<student_id>',
         views.newAbsent.as_view(), name='regabsent'),
    path('students_list/', views.StudentListView.as_view(), name='StudentListView'),
    ]
