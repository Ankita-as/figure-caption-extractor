from requests.adapters import HTTPAdapter, Retry
import requests
import duckdb
import os
import json
from src.logger import logger

# Setup requests session with retry logic
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

def fetch_paper_json(pmc_id):
    url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/bioc_json/{pmc_id}/unicode"
    logger.info(f"Requesting URL: {url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error fetching {pmc_id}: {e}")
        return None

    if "No result can be found" in response.text:
        logger.warning(f"No data found for PMC ID: {pmc_id}")
        return None

    try:
        paper_json = response.json()
    except ValueError as e:
        logger.error(f"JSON decode error for {pmc_id}: {e}")
        return None

    # Debug: log part of JSON to verify structure
    if isinstance(paper_json, dict):
        logger.debug(f"Fetched JSON keys for {pmc_id}: {list(paper_json.keys())}")
    elif isinstance(paper_json, list):
        logger.debug(f"Fetched JSON is a list with length {len(paper_json)} for {pmc_id}")
    else:
        logger.debug(f"Fetched JSON type {type(paper_json)} for {pmc_id}")

    return paper_json


def extract_figure_captions(paper_json):
    captions = []

    if not paper_json:
        logger.warning("No JSON data to process")
        return captions

    if isinstance(paper_json, list):
        logger.warning("Received JSON as a list, processing first element")
        paper_json = paper_json[0] if paper_json else {}

    if not isinstance(paper_json, dict):
        logger.error("Unexpected JSON format after handling list")
        return captions

    documents = paper_json.get("documents", [])
    if not documents:
        logger.warning("No documents found in paper_json")
        return captions

    section_types_found = set()
    for document in documents:
        passages = document.get("passages", [])
        for passage in passages:
            section_type = passage.get("infons", {}).get("section_type", "").lower()
            if section_type:
                section_types_found.add(section_type)

    logger.info(f"Section types found: {section_types_found}")

    for document in documents:
        passages = document.get("passages", [])
        if not passages:
            logger.debug("No passages found in document")
            continue

        for passage in passages:
            section_type = passage.get("infons", {}).get("section_type", "").lower()
            passage_text = passage.get("text", "")

            if section_type in ["fig", "figure", "figure legend", "figure_legend"]:
                figure_url = passage.get("infons", {}).get("url")

                if not figure_url and "annotations" in passage:
                    for annotation in passage["annotations"]:
                        possible_url = annotation.get("obj") or annotation.get("url")
                        if possible_url and isinstance(possible_url, str) and possible_url.lower().startswith("http"):
                            figure_url = possible_url
                            break

                captions.append({
                    "caption": passage_text,
                    "figure_url": figure_url
                })

            # 🧠 Fallback logic for captions even if section_type is missing
            elif any(keyword in passage_text.lower() for keyword in ["fig", "figure", "fig.", "fig:"]) and len(passage_text) > 20:
                logger.debug(f"Possible caption fallback hit: {passage_text[:80]}")
                captions.append({
                    "caption": passage_text,
                    "figure_url": None  # Fallbacks often don't include URLs
                })

    if not captions:
        logger.info("No figure captions found.")

    return captions

def save_captions_to_json(paper_id, captions, output_dir="captions_output"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{paper_id}_captions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"paper_id": paper_id, "captions": captions}, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved captions for {paper_id} to {output_path}")


def process_paper(pmc_id):
    logger.info(f"Processing paper: {pmc_id}")
    
    paper_json = fetch_paper_json(pmc_id)
    if paper_json is None:
        logger.info(f"No data fetched for {pmc_id}, skipping insert.")
        return

    captions = extract_figure_captions(paper_json)
    
    if not captions:
        with open(f"debug_{pmc_id}.json", "w", encoding="utf-8") as f:
            json.dump(paper_json, f, indent=2)
        logger.info(f"No figure captions extracted for {pmc_id}. Saved raw JSON to debug_{pmc_id}.json")
        return

    save_captions_to_json(pmc_id, captions)
    
    os.makedirs("data", exist_ok=True)
    conn = duckdb.connect("data/paper_data.duckdb")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS figure_captions (
            pmcid TEXT,
            caption TEXT,
            figure_url TEXT
        )
    """)

    for cap in captions:
        conn.execute("INSERT INTO figure_captions VALUES (?, ?, ?)", (
            pmc_id,
            cap.get("caption"),
            cap.get("figure_url")
        ))

    conn.close()
    logger.info(f"Inserted {len(captions)} figure captions for {pmc_id}")
