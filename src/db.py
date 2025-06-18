import duckdb
import os
import json

DB_PATH = os.environ.get("DB_PATH", "data/paper_data.duckdb")

def init_db():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS figure_data (
            pmc_id TEXT,
            caption TEXT,
            figure_url TEXT,
            entities JSON
        )
    """)
    conn.close()

def insert_captions(pmc_id, captions):
    conn = duckdb.connect(DB_PATH)
    for cap in captions:
        # Convert entities list to JSON string for proper storage
        entities_json = json.dumps(cap.get("entities", []))
        conn.execute(
            "INSERT INTO figure_data VALUES (?, ?, ?, ?)",
            (pmc_id, cap["caption"], cap.get("figure_url", "N/A"), entities_json)
        )
    conn.close()
