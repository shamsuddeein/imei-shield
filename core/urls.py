from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("about/", views.about, name="about"),  # About page
    path("report/", views.report_create, name="report"),  # Report stolen phone
    path("check/", views.check_imei, name="check"),  # Check IMEI
    path("admin-dashboard/", views.admin_dashboard, name="dashboard"),  # Admin dashboard
    path("login/", views.admin_login, name="login"),
    # ...
    path("logout/", views.custom_logout, name="logout"),
]

