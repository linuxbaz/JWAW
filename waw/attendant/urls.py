from django.urls import path

from . import views


#all pattern
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('students_list/', views.StudentListView.as_view(), name='StudentListView'),
    path('student/<pk>', views.StdDetail_view,
         name='student-detail'),
    ]