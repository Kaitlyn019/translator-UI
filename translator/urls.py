from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client/', views.room, name='client'),
    path('server/', views.room, name='server'),
]