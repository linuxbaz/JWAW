from django.urls import path

from . import views
#all pattern
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    ]
