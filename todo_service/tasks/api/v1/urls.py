from django.urls import path

from tasks.api.v1 import views


urlpatterns = [
    path("tag/", views.TagListAPIView.as_view()),
    path("tag/<str:tag_id>", views.TagDetailAPIView.as_view()),
    path("task/", views.TaskListAPIView.as_view()),
    path("task/<str:task_id>", views.TaskDetailAPIView.as_view()),
]
