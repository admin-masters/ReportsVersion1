from __future__ import annotations

import logging
from typing import Callable

from django.db import DatabaseError
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from reporting.api_services import build_in_clinic_rows, build_patient_education_rows, build_red_flag_alert_rows


logger = logging.getLogger(__name__)


def _payload_response(subsystem: str, rows: list[dict[str, object]], *, status: int = 200, detail: str | None = None) -> JsonResponse:
    results = []
    for index, row in enumerate(rows, start=1):
        item = {"id": index}
        item.update(row)
        results.append(item)
    payload: dict[str, object] = {
        "subsystem": subsystem,
        "count": len(results),
        "results": results,
    }
    if detail:
        payload["detail"] = detail
    return JsonResponse(payload, status=status)


def _render_api(subsystem: str, builder: Callable[[], list[dict[str, object]]]) -> JsonResponse:
    try:
        return _payload_response(subsystem, builder())
    except DatabaseError:
        logger.exception("Unified reporting API database failure for %s", subsystem)
        return _payload_response(subsystem, [], status=503, detail="Reporting data is currently unavailable.")
    except Exception:
        logger.exception("Unified reporting API failed for %s", subsystem)
        return _payload_response(subsystem, [], status=500, detail="Unexpected reporting API error.")


@require_GET
def red_flag_alert_api(_request: HttpRequest) -> JsonResponse:
    return _render_api("red_flag_alert", build_red_flag_alert_rows)


@require_GET
def in_clinic_api(_request: HttpRequest) -> JsonResponse:
    return _render_api("in_clinic", build_in_clinic_rows)


@require_GET
def patient_education_api(_request: HttpRequest) -> JsonResponse:
    return _render_api("patient_education", build_patient_education_rows)
