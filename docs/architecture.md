# System Architecture

## Overview
The platform ingests documents through the **upload** API, orchestrates OCR and entity extraction workers, and indexes structured data for search. Each service communicates asynchronously through a message bus to keep the pipeline resilient and horizontally scalable.

## Pipeline Flow
1. **Upload service** receives document metadata and stores raw objects in MinIO. It publishes an `upload.received` message with locations and MIME details.
2. **OCR worker** consumes `upload.received`, runs OCR against the stored object, and emits `ocr.completed` with text storage references. Failures may emit `ocr.failed` for dead-letter handling.
3. **Extraction worker** consumes `ocr.completed`, extracts entities and summaries, then publishes `extract.completed`. Any recoverable issues emit `extract.failed`.
4. **Search service** subscribes to `extract.completed`, indexes the extracted content, and confirms via `search.indexed` once persisted.
5. Health checks and idempotency middleware ensure each stage can restart safely without duplicating work.

## Message Topics
- `upload.received` – new document received and persisted.
- `ocr.completed` / `ocr.failed` – OCR finished with text locations or failure details.
- `extract.completed` / `extract.failed` – extraction finished with entity payloads or failure context.
- `search.indexed` – document indexed and queryable.

## Storage Layout
- **MinIO buckets**
  - `uploads/` – raw user uploads partitioned by account and date (e.g., `uploads/{account_id}/{yyyy}/{mm}/{dd}/{upload_id}`).
  - `ocr/` – OCR text artifacts keyed by upload id (e.g., `ocr/{upload_id}.json`).
  - `extractions/` – structured extraction outputs (entities, summaries) keyed by upload id.
- **Postgres**
  - `uploads` table holds upload metadata, content type, and MinIO path.
  - `extractions` table tracks extracted entities, status, and indexing status.
  - `search_index` (logical) or external search backend references extracted content IDs.

## Data Models
- **UploadRecord**: `{upload_id, filename, content_type, account_id, object_path, received_at}`
- **OcrResult**: `{upload_id, text_path, engine, language, completed_at}`
- **ExtractionResult**: `{upload_id, entities, summary, confidence, completed_at}`
- **SearchIndexRecord**: `{upload_id, terms, indexed_at, version}`

## Operational Notes
- All message payloads conform to JSON Schemas in `contracts/` and are validated before processing.
- Workers wrap handlers with logging and idempotency middleware to prevent duplicate work on retries.
- Docker Compose provisions Postgres, MinIO, RabbitMQ, and all services for local development; `make seed` initializes buckets and runs placeholder migrations.
