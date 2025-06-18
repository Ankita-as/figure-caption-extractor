# Figure Caption Extraction System

## Overview
This Python-based project extracts **figure captions** and associated metadata from biomedical research articles available on **PubMed Central (PMC)**. It leverages the **Open Access JSON format** to fetch and parse article content, enriches captions with biomedical entities, stores the data in a **DuckDB** database, and exposes it via a secured REST API.

---

## Components

1. **Ingestion Pipeline**  
   Accepts paper IDs, fetches article metadata and captions, and extracts biomedical entities from captions.

2. **Storage**  
   Uses **DuckDB**, an embedded analytical database, for efficient querying and persistence of extracted data.

3. **API Server**  
   Provides REST endpoints to upload paper ID lists, query stored figure captions and metadata, protected by API keys.

4. **Configuration Manager**  
   Centralizes configuration for storage backend, API keys, and logging.

5. **Command-Line Interface (CLI)**  
   Command-line tools to run ingestion jobs and query data conveniently.

6. **Docker**  
   Containerized deployment for easy setup and scaling.

---

## Features

- 🔍 Input PMC IDs to retrieve data.  
- 🌐 Downloads article data from NCBI’s Open Access subset.  
- 🧾 Parses and extracts **figure captions** from research articles.  
- 🧬 Enriches captions with biomedical entity recognition.  
- ⚠️ Robust error handling for missing captions or invalid IDs.  
- 🔐 REST API secured with API keys for controlled access.

---

## How It Works

1. The system constructs a download URL using the provided PMC ID.  
2. It fetches the article archive (`.tar.gz`) from the NCBI FTP server.  
3. Extracts the relevant JSON (`*.xml.json`) containing article content.  
4. Parses JSON to identify sections labeled `"fig"` or `"figure"`.  
5. Extracts and enriches figure captions, then stores them in DuckDB.

---

## Requirements

- Python 3.7 or higher

### Install dependencies

```bash
pip install -r requirements.txt

Key dependencies include:

requests — for HTTP requests

fastapi & uvicorn — for the REST API server

duckdb — for embedded database storage

pydantic — data validation

typer — CLI tooling

python-dotenv — configuration management via environment variables

##Usage
Extract figure captions for a specific PMC ID
##Set the PMC ID in main.py (or your script entrypoint):

pmc_id = "PMC7766027"
##Run the script:

python main.py
##Sample output for PMC7766027

Extracted Figure Captions:

1. Tempering SEM microstructure of the experiment material: (a) novel steel and (b) 3051Mn2MoV.

2. High temperature tensile sample.

3. Low cycle fatigue (LCF) test sample.

4. Monotonic tensile stress-strain curves of the novel steel and 30SiMn2MoV steel at 700 °C.

... (additional captions)
##Batch ingestion
To ingest multiple papers via a text file (paper_ids.txt), run:

python batch_ingest.py paper_ids.txt
Deployment
The system can be containerized using Docker for simplified deployment.

Configure via environment variables or .env files for API keys, database path, logging, etc.

Logs can be directed to stdout or log files as configured.

License
This project is open-source and free to use for educational or research purposes.

Author
Ankita Sinha
B.Tech Computer Science & Engineering @ VIT Bhopal
GitHub: https://github.com/Ankita-as/Bootcamp

API
Default running at: http://127.0.0.1:8000/
                     
http://localhost:8000/docs
                     
http://localhost:8000/redoc
                    