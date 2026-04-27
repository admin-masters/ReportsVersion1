from django.core.management.base import BaseCommand

from etl.inclinic_pipeline import run_pipeline


class Command(BaseCommand):
    help = "Run RAW->BRONZE->SILVER->GOLD ETL pipeline"

    def add_arguments(self, parser):
        parser.add_argument("--run-id", default=None)

    def handle(self, *args, **options):
        result = run_pipeline(run_id=options["run_id"], trigger_type="manual")
        run_id = result["run_id"]
        status = result["status"]
        failed_tables = len(result.get("errors", {}))
        total_tables = result.get("summary", {}).get("total_tables", failed_tables)

        if status == "SUCCESS":
            self.stdout.write(self.style.SUCCESS(f"ETL completed for run_id={run_id}"))
        elif status == "PARTIAL_SUCCESS":
            self.stdout.write(
                self.style.WARNING(
                    f"ETL completed with partial source failures for run_id={run_id} "
                    f"({failed_tables}/{total_tables} source tables failed)"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"ETL completed with no successful source extractions for run_id={run_id}; "
                    f"all {total_tables} source tables failed"
                )
            )
