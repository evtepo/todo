INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",

    "tasks.apps.TasksConfig",
    "custom_auth.apps.AuthConfig",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    INSTALLED_APPS.append("debug_toolbar_force")
