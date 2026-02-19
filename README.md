# ReportsVersion1 — Reporting v2.1 Implementation

This repository now contains a full Django + PostgreSQL medallion implementation for the In-Clinic Sharing System reporting pipeline.

## Implemented architecture

- **RAW**: exact source replication in `raw_server1`/`raw_server2` with all source columns as text + ingestion metadata.
- **BRONZE**: deduplicated and exclusion-filtered tables in `bronze`.
- **SILVER**: conformed dimensions/facts, parsing and identity logic in `silver`.
- **GOLD**: campaign-scoped schemas `gold_campaign_*` with KPI wide tables and global benchmark tables in `gold_global`.
- **CONTROL**: ETL run/watermark/DQ log tables in `control`.
- **OPS**: exclusion rules + thresholds in `ops`.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py run_etl
python manage.py runserver
```

## Main entry points

- ETL command: `etl.management.commands.run_etl`
- Dashboard page: `/` or `/campaign/<brand_campaign_id>/`
