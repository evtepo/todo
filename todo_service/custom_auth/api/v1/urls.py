from django.urls import path

from custom_auth.api.v1 import views


urlpatterns = [
    path("check-user-task/", views.CheckUserTaskAPIView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
]