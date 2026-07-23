# Sprint 1 Retrospective

## Sprint Goal

Build a complete ETL pipeline to ingest Nifty100 datasets into SQLite with data quality validation.

---

## What Went Well

- Successfully built an ETL pipeline for 12 datasets.
- Implemented data normalization.
- Loaded all datasets into SQLite.
- Added 16 Data Quality validation rules.
- Created automated loading and audit logging.
- Completed manual data quality review.
- All unit tests passed successfully.

---

## Challenges Faced

- SQLite schema mismatches.
- TEXT vs INTEGER primary key issues.
- Foreign key constraint failures.
- Financial ratios schema mismatch.
- Duplicate loading issues.
- Python package import issues while running pytest.

---

## Solutions Implemented

- Updated database schema.
- Corrected primary and foreign key data types.
- Filtered invalid foreign key records.
- Fixed loader bugs.
- Added load audit.
- Configured pytest correctly.

---

## Key Learnings

- SQLite database design
- ETL architecture
- Data normalization
- Data quality validation
- Foreign key handling
- SQL querying
- Unit testing with pytest
- ETL debugging

---

## Sprint Outcome

Sprint 1 completed successfully.

All planned tasks from Day 1 to Day 7 were completed and the ETL pipeline is fully functional.