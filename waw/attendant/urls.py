from django.urls import path

from . import views


#all pattern
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('student/<pk>', views.StdDetail_view,
         name='student-detail'),
    #path('student_10/<id>', views.StudentListLevel_view),
    path('todayAbsent', views.Absent_today_View, name='todayAbsent'),

    path('reg_today_absent/<student_id>',
         views.RegNewAbsent_view, name='reg_today_absent'),
    path('upfile/', views.upfile_view, name='upfile'),
    path('students_list/', views.StudentListView, name='StudentListView'),
    path('regtodayabsent/', views.AbsentCreatView.as_view(), name='AbsentCreatView'),
    path('profile/', views.userprofile_view, name='userprofile'),
    ]
