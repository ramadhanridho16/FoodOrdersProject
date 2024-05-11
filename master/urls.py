from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('async/<str:name>/', views.test_async),
    path('except/', views.test_exception),
]
