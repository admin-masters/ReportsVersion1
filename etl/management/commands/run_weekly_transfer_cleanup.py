from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from etl.weekly_transfer_cleanup import run_weekly_transfer_cleanup


class Command(BaseCommand):
    help = "Run weekly transfer pipelines and delete approved source transaction data after successful reporting ingestion"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domains",
            default="inclinic,rfa",
            help="Comma-separated cleanup domains to run. Supported values: inclinic, rfa.",
        )

    def handle(self, *args, **options):
        raw_domains = [item.strip() for item in str(options["domains"]).split(",") if item.strip()]
        if not raw_domains:
            raise CommandError("At least one cleanup domain must be provided.")

        result = run_weekly_transfer_cleanup(raw_domains)
        cleanup_run_id = result["cleanup_run_id"]
        status = result["status"]

        if status == "SUCCESS":
            self.stdout.write(self.style.SUCCESS(f"Weekly transfer cleanup completed for cleanup_run_id={cleanup_run_id}"))
            return

        if status == "PARTIAL_SUCCESS":
            self.stdout.write(
                self.style.WARNING(
                    f"Weekly transfer cleanup completed with partial success for cleanup_run_id={cleanup_run_id}"
                )
            )
            return

        raise CommandError(f"Weekly transfer cleanup failed for cleanup_run_id={cleanup_run_id}")
