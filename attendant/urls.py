from django.urls import path, include
from rest_framework import routers
from . import views
from .views import StudentView
from knox import views as knox_views


"""router = routers.DefaultRouter()
router.register('students', views.StudentView)"""

#all pattern
urlpatterns = [
    path('', views.Index, name='index'),
    path('student/<pk>', views.StdDetail_view,
         name='student-detail'),
    #path('student_10/<id>', views.StudentListLevel_view),
    path('todayAbsent', views.Absent_today_View, name='todayAbsent'),

    path('reg_today_absent/<student_id>',
         views.RegNewAbsent_view, name='reg_today_absent'),
    path('upfile/', views.upfile_view, name='upfile'),
    path('students_list/', views.StudentListView, name='StudentListView'),
    path('profile/', views.userprofile_view, name='userprofile'),
    #path('', include(router.urls)),
    path('api/users/', views.UserCreate.as_view(), name='account-create'),
    path('likestudent/', views.likeStudent, name='likestudent'),
    ]
