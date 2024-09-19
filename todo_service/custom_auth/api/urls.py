from django.urls import include, path


urlpatterns = [
    path("v1/auth/", include("custom_auth.api.v1.urls")),
]
