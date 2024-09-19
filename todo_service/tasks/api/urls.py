from django.urls import include, path


urlpatterns = [
    path("v1/", include("tasks.api.v1.urls")),
]
