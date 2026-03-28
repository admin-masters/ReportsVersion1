from django.contrib import admin
from django.urls import include, path
from dashboard.views import campaign_overview, menu_page, campaign_login, export_report, etl_debug_page, send_access_email_view, campaign_access_page, reports_home
from reporting.api_views import in_clinic_api, patient_education_api, red_flag_alert_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", reports_home, name="reports-home"),
    path("inclinic/", menu_page, name="menu"),
    path("reporting/api/red_flag_alert/", red_flag_alert_api, name="reporting-api-red-flag-alert"),
    path("reporting/api/in_clinic/", in_clinic_api, name="reporting-api-in-clinic"),
    path("reporting/api/patient_education/", patient_education_api, name="reporting-api-patient-education"),
    path("sapa-growth/", include("sapa_growth.urls")),
    path("pe-reports/", include("pe_reports.urls")),
    path("debug/etl/", etl_debug_page, name="etl-debug"),
    path("campaign/<str:brand_campaign_id>/login/", campaign_login, name="campaign-login"),
    path("campaign/<str:brand_campaign_id>/access/", campaign_access_page, name="campaign-access"),
    path("campaign/<str:brand_campaign_id>/send-access-email/", send_access_email_view, name="campaign-send-access-email"),
    path("campaign/<str:brand_campaign_id>/", campaign_overview, name="campaign-overview-specific"),
    path("campaign/<str:brand_campaign_id>/export/", export_report, name="campaign-export"),
]
