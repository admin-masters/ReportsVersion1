from __future__ import annotations

import json
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import resolve


class UnifiedReportingApiRoutingTests(SimpleTestCase):
    def test_routes_registered(self):
        self.assertEqual(resolve("/reporting/api/red_flag_alert/").view_name, "reporting-api-red-flag-alert")
        self.assertEqual(resolve("/reporting/api/in_clinic/").view_name, "reporting-api-in-clinic")
        self.assertEqual(resolve("/reporting/api/patient_education/").view_name, "reporting-api-patient-education")


class UnifiedReportingApiViewTests(SimpleTestCase):
    @patch(
        "reporting.api_views.build_red_flag_alert_rows",
        return_value=[
            {
                "campaign": "growth-clinic",
                "clinic_group": "Pune",
                "clinic": "Sunrise Clinic",
                "period_start": "2026-03-21",
                "period_end": "2026-03-25",
                "form_fills": 4,
                "red_flags_total": 3,
                "patient_video_views": 2,
                "reports_emailed_to_doctors": 4,
                "form_shares": 2,
                "patient_scans": 2,
                "follow_ups_scheduled": 1,
                "reminders_sent": 1,
            }
        ],
    )
    def test_red_flag_alert_returns_json_envelope(self, _mock_builder):
        response = self.client.get("/reporting/api/red_flag_alert/")
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["subsystem"], "red_flag_alert")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["id"], 1)
        self.assertEqual(payload["results"][0]["clinic"], "Sunrise Clinic")

    @patch(
        "reporting.api_views.build_patient_education_rows",
        return_value=[
            {
                "campaign": "pe-alpha-2026",
                "clinic_group": "Pune",
                "clinic": "Sunrise Clinic",
                "period_start": "2026-03-02",
                "period_end": "2026-03-24",
                "video_views": 3,
                "video_completions": 1,
                "cluster_shares": 3,
                "patient_scans": 3,
                "banner_clicks": 2,
            }
        ],
    )
    def test_patient_education_returns_contract_shape(self, _mock_builder):
        response = self.client.get("/reporting/api/patient_education/")
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["subsystem"], "patient_education")
        self.assertEqual(payload["results"][0]["video_views"], 3)
        self.assertEqual(payload["results"][0]["banner_clicks"], 2)

    @patch("reporting.api_views.build_in_clinic_rows", side_effect=RuntimeError("boom"))
    def test_in_clinic_returns_safe_error_envelope(self, _mock_builder):
        response = self.client.get("/reporting/api/in_clinic/")
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(payload["subsystem"], "in_clinic")
        self.assertEqual(payload["count"], 0)
        self.assertEqual(payload["results"], [])
        self.assertIn("detail", payload)
