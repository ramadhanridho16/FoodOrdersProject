from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.categories),
    path('', views.index),
    path('async/<str:name>/', views.test_async),
    path('except/', views.test_exception),
    path('images/', views.image_test),
]
