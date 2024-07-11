from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.registration),
    path("resend-verify/", views.resend_verification),
    path("login/", views.login),
    path("verify/", views.verify),
    path("check/", views.check),
]
