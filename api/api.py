from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import APIKeyHeader
from src.config_loader import load_config
import duckdb
import os
import pandas as pd

app = FastAPI()
config = load_config()
api_key = config["api_key"]
db_path = config["database_path"]
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_key(key: str = Depends(api_key_header)):
    if key != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.get("/")
async def root():
    return {"message": "Figure Caption Extractor API is running!"}

@app.get("/papers/{pmc_id}", dependencies=[Depends(verify_key)])
def get_paper(pmc_id: str):
    conn = duckdb.connect(db_path)
    # Use parameterized query to avoid SQL injection
    query = "SELECT * FROM figures WHERE pmcid = ?"
    df = conn.execute(query, (pmc_id,)).df()
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No figures found for pmcid: {pmc_id}")
    return df.to_dict(orient="records")

@app.get("/download", dependencies=[Depends(verify_key)])
def download_all(format: str = "csv"):
    conn = duckdb.connect(db_path)
    df = conn.execute("SELECT * FROM figures").df()
    if df.empty:
        raise HTTPException(status_code=404, detail="No figure data available to download")
    
    if format.lower() == "csv":
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "export.csv")
        df.to_csv(out_path, index=False)
        return FileResponse(out_path, media_type="text/csv", filename="figures.csv")
    elif format.lower() == "json":
        return JSONResponse(df.to_dict(orient="records"))
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use 'csv' or 'json'.")
