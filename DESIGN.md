# DESIGN DOCUMENT: Figure Caption Extraction System

## 1. Overview

This system extracts figure captions and associated metadata from scientific articles in PubMed Central (PMC). It supports ingestion via CLI, file uploads, or a watched folder and exposes the data through a REST API.

---

## 2. Architecture

### Components:
- **Ingestor**: Fetches metadata using the BioC-PMC API and PubTator for entity extraction.
- **Parser**: Extracts title, abstract, captions, and figure URLs.
- **Database**: DuckDB (lightweight, embedded).
- **REST API**: FastAPI exposing endpoints to query data.
- **CLI**: Allows ingestion via command-line or batch files.
- **Watched Folder Handler**: Monitors folder and ingests new ID files.

---

## 3. Data Flow

```mermaid
graph TD
    A[User] --> B[CLI/API/Watched Folder]
    B --> C[Ingestor]
    C --> D[PubMed + PubTator APIs]
    D --> E[Parser]
    E --> F[DuckDB]
    F --> G[REST API (JSON/CSV)]
