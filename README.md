# sports-analytics-platform
Production-grade sports analytics data platform — AWS, Kafka, Snowflake, dbt, Airflow, LLM

## Architecture
Diagram coming soon]

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Ingestion | Sportradar API / Kaggle datasets |
| Streaming | Apache Kafka (AWS MSK) — Snappy compression |
| Storage | AWS S3 (Parquet + Snappy) + Glue Data Catalog |
| Warehouse | Snowflake (raw → staging → mart) |
| Transform | AWS Glue ETL + dbt Core |
| Orchestration | Apache Airflow (AWS MWAA) |
| AI Layer | LLM + MCP server (natural language → SQL) |
| Observability | CloudWatch, Great Expectations, dbt tests |

## Project Status
In Progress — Started May 2026

## Phases
| Phase | Focus | Status |
|-------|-------|--------|
| 1 | AWS Setup + Data Ingestion | In Progress |
| 2 | Snowflake + dbt | Upcoming |
| 3 | Kafka Streaming + Airflow | Upcoming |
| 4 | AI Layer + Polish | Upcoming |
