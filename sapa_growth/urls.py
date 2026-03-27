from django.urls import path

from sapa_growth import views


app_name = "sapa_growth"

urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("login/", views.login, name="login"),
    path("access/", views.access_page, name="access"),
    path("send-access-email/", views.send_access_email_view, name="send-access-email"),
    path("", views.dashboard, name="dashboard"),
    path("certified-clinics/", views.certified_clinics_partial, name="certified-clinics"),
    path("certified-clinics/export/", views.certified_export, name="certified-export"),
    path("details/<str:metric>/", views.detail_view, name="detail"),
    path("details/<str:metric>/export/", views.detail_export, name="detail-export"),
    path("export/dashboard.pdf", views.dashboard_export, name="dashboard-export"),
]
